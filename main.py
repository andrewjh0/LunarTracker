import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, timedelta, date

import Moon
import Animation

# Create a frame to hold moon phase legend and controls
combined_frame = None
moon_phase_frame = None
controls_frame = None
animator = None

def create_moon_phase_legend():
    """Create a legend showing moon phases for the current month"""
    global combined_frame, moon_phase_frame
    
    # Only destroy and recreate the moon phase section
    if moon_phase_frame:
        moon_phase_frame.destroy()
    
    # Create combined frame if it doesn't exist
    if not combined_frame:
        combined_frame = tk.Frame(root, bg="lightgray", relief=tk.RIDGE, borderwidth=2)
        combined_frame.pack(after=cal, pady=5, padx=20, fill="x")
    
    # Moon phase legend section (left side)
    moon_phase_frame = tk.Frame(combined_frame, bg="lightgray")
    moon_phase_frame.pack(side=tk.LEFT, padx=5)
    
    legend_title = tk.Label(moon_phase_frame, text="Moon Phases:", 
                           font=("Arial", 10, "bold"), bg="lightgray")
    legend_title.pack(side=tk.LEFT, padx=5)
    
    # Get the currently displayed month and year from calendar
    month, year = cal.get_displayed_month()
    
    # Create temporary moon object for phase calculation
    temp_canvas = tk.Canvas(root, width=1, height=1)
    temp_moon = Moon.Moon(temp_canvas, 1, (0, 0))
    
    # Find key moon phases in the month
    phases_found = {}
    for day in range(1, 32):
        try:
            date_obj = date(year, month, day)
            date_str = date_obj.strftime("%Y-%m-%d")
            emoji = temp_moon.get_phase_emoji(date_str)
            
            # Store first occurrence
            if emoji not in phases_found:
                phases_found[emoji] = day
        except ValueError:
            break
    
    # Display the phases
    for emoji, day in sorted(phases_found.items(), key=lambda x: x[1]):
        phase_label = tk.Label(moon_phase_frame, text=f"{emoji} ({day})", 
                              font=("Arial", 12), bg="lightgray", padx=5)
        phase_label.pack(side=tk.LEFT)
    
    temp_canvas.destroy()

def on_month_changed(event=None):
    """Update moon phase legend when calendar month changes"""
    root.after(50, create_moon_phase_legend)

def on_date_selected(event):
    # Stop animation if running
    if animator and animator.is_playing:
        animator.stop_animation()
    
    selected_date = cal.get_date()
    result_label.config(text=f"Showing moon phase for {selected_date}")
    canvas.delete("all") # Clears previous drawings
    moon.set_phase(selected_date)

def start_animation():
    """Start the moon phase animation from current selected date"""
    selected_date = cal.get_date()
    animator.start_animation(selected_date)
    play_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.NORMAL)

def pause_animation():
    """Pause the animation"""
    animator.pause_animation()
    play_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)

def resume_animation():
    """Resume the animation"""
    animator.resume_animation()
    play_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.NORMAL)

def stop_animation():
    """Stop the animation"""
    animator.stop_animation()
    play_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.DISABLED)
    # Reset to selected date
    selected_date = cal.get_date()
    result_label.config(text=f"Showing moon phase for {selected_date}")
    canvas.delete("all")
    moon.set_phase(selected_date)

def change_speed(value):
    """Change animation speed"""
    speed = int(float(value))
    animator.set_speed(speed)

def on_window_resize(event):
    # Only respond to window resize events
    if event.widget == root:
        # Get new window dimensions
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        
        # Calculate calendar font size based on window width
        cal_font_size = max(8, min(12, window_width // 90))
                
        # Calculate available space for canvas (below other widgets)
        canvas_size = min(window_width - 40, window_height - 350)  # Leave margin and space for calendar
        canvas_size = max(canvas_size, 150)  # Minimum size
        
        # Update canvas size
        canvas.config(width=canvas_size, height=canvas_size)
        
        # Update moon size and position
        moon.radius = canvas_size // 3  # 2/3 of canvas
        moon.position = (canvas_size // 2, canvas_size // 2)  # Center of canvas
        
        # Redraw moon if a date has been selected
        if result_label.cget("text"):
            canvas.delete("all")
            selected_date = cal.get_date()
            moon.set_phase(selected_date)

# Create main window
root = tk.Tk()
root.title("Lunar Tracker")
#root.geometry("400x600")
root.geometry("1280x720")
#root.geometry("1920x1080")
root.minsize(400, 600)

#Var
padding_y = 5
padding_x = 5

# Title label
title_label = tk.Label(root, text="Select a Date", font=("Arial", 16))
title_label.pack(pady=10)


# Calendar widget
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(pady=padding_y, padx=padding_x, fill="both", expand=False)

# Bind date selection
cal.bind("<<CalendarSelected>>", on_date_selected)

# Bind month/year changes to update moon phases
cal.bind("<<CalendarMonthChanged>>", on_month_changed)

# Initial moon phase legend
root.after(200, create_moon_phase_legend)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=padding_y)

# Get initial window size
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()

# Calculate initial canvas size
canvas_size = min(window_width - 40, window_height - 350)
canvas_size = max(canvas_size, 150)  # Minimum size

canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="gray")
canvas.pack()

# Creates a moon with dynamic sizing
moon_radius = canvas_size // 3
moon_position = (canvas_size // 2, canvas_size // 2)
moon = Moon.Moon(canvas, moon_radius, moon_position)

# Create animation controller
animator = Animation.MoonAnimation(canvas, moon, result_label)

# Animation controls section (will be added to combined frame on right side)
def create_animation_controls():
    """Create animation controls in the combined frame"""
    global controls_frame, play_button, pause_button, stop_button, speed_label
    
    if not combined_frame:
        return
    
    # Controls section (right side)
    controls_frame = tk.Frame(combined_frame, bg="lightgray")
    controls_frame.pack(side=tk.RIGHT, padx=5)
    
    # Control buttons
    play_button = tk.Button(controls_frame, text="▶ Play", command=start_animation, 
                           font=("Arial", 9), padx=8, pady=3)
    play_button.pack(side=tk.LEFT, padx=3)
    
    pause_button = tk.Button(controls_frame, text="⏸ Pause", command=pause_animation, 
                            font=("Arial", 9), padx=8, pady=3, state=tk.DISABLED)
    pause_button.pack(side=tk.LEFT, padx=3)
    
    stop_button = tk.Button(controls_frame, text="⏹ Stop", command=stop_animation, 
                           font=("Arial", 9), padx=8, pady=3, state=tk.DISABLED)
    stop_button.pack(side=tk.LEFT, padx=3)
    
    # Speed control
    speed_label = tk.Label(controls_frame, text="Speed:", 
                          font=("Arial", 9), bg="lightgray", padx=5)
    speed_label.pack(side=tk.LEFT, padx=2)
    
    speed_slider = tk.Scale(controls_frame, from_=500, to=20, orient=tk.HORIZONTAL, 
                           command=change_speed, length=100, bg="lightgray", 
                           showvalue=False, width=10)
    speed_slider.set(100)
    speed_slider.pack(side=tk.LEFT, padx=2)

# Create animation controls after legend
root.after(250, create_animation_controls)

# Bind window resize event
root.bind("<Configure>", on_window_resize)

# Run the application
root.mainloop()
