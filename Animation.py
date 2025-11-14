import tkinter as tk
from datetime import datetime, timedelta

class MoonAnimation:
    """Handles moon phase animation playback"""
    
    def __init__(self, canvas, moon, result_label):
        self.canvas = canvas
        self.moon = moon
        self.result_label = result_label
        self.is_playing = False
        self.current_day = 0
        self.start_date = None
        self.animation_speed = 100  # milliseconds per frame
        self.after_id = None
        
    def start_animation(self, start_date_str):
        """Start the animation from the given date"""
        if self.is_playing:
            return
        
        self.is_playing = True
        self.current_day = 0
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        self._animate_next_frame()
    
    def stop_animation(self):
        """Stop the animation"""
        self.is_playing = False
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
    
    def pause_animation(self):
        """Pause the animation"""
        self.is_playing = False
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None
    
    def resume_animation(self):
        """Resume the animation"""
        if not self.is_playing and self.start_date:
            self.is_playing = True
            self._animate_next_frame()
    
    def set_speed(self, speed):
        """Set animation speed in milliseconds per frame"""
        self.animation_speed = speed
    
    def _animate_next_frame(self):
        """Render the next frame of the animation"""
        if not self.is_playing:
            return
        
        # Current date
        current_date = self.start_date + timedelta(days=self.current_day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Update the display
        day_info = f"Day {self.current_day}/{int(self.moon.PERIOD)}"
        self.result_label.config(text=f"Animating: {date_str} ({day_info})")
        
        # Draw phase
        self.canvas.delete("all")
        self.moon.set_phase(date_str)
        
        # Increment 
        self.current_day += 0.5  # For smoother animation
        
        # Loop back 
        if self.current_day >= self.moon.PERIOD:
            self.current_day = 0
        
        # Next frame
        self.after_id = self.canvas.after(self.animation_speed, self._animate_next_frame)
    

    
    def skip_forward(self, days=1):
         """Skip forward by specified number of days"""
         if self.start_date:
             self.current_day = (self.current_day + days) % self.moon.PERIOD
             if not self.is_playing:
                 # Manually update
                 current_date = self.start_date + timedelta(days=self.current_day)
                 date_str = current_date.strftime("%Y-%m-%d")
                 self.result_label.config(text=f"Showing: {date_str} (Day {int(self.current_day)})")
                 self.canvas.delete("all")
                 self.moon.set_phase(date_str)
    
    def skip_backward(self, days=1):
         """Skip backward by specified number of days"""
         if self.start_date:
             self.current_day = (self.current_day - days) % self.moon.PERIOD
             if not self.is_playing:
                 # Manually update 
                 current_date = self.start_date + timedelta(days=self.current_day)
                 date_str = current_date.strftime("%Y-%m-%d")
                 self.result_label.config(text=f"Showing: {date_str} (Day {int(self.current_day)})")
                 self.canvas.delete("all")
                 self.moon.set_phase(date_str)

