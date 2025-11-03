import tkinter as tk
from tkcalendar import Calendar

import Moon

def on_date_selected(event):
    selected_date = cal.get_date()
    result_label.config(text=f"Showing moon phase for {selected_date}")
    canvas.delete("all") # Clears previous drawings
    moon.set_phase(selected_date)

# Create main window
root = tk.Tk()
root.title("Lunar Tracker")
root.geometry("400x600")

# Title label
title_label = tk.Label(root, text="Select a Date", font=("Arial", 16))
title_label.pack(pady=10)

# Calendar widget
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(pady=20)

# Bind date selection
cal.bind("<<CalendarSelected>>", on_date_selected)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

canvas = tk.Canvas(root, width=200, height=200, bg="gray")
canvas.pack()

# Creates a moon
moon = Moon.Moon(canvas, 50, (100,100))

# Run the application
root.mainloop()
