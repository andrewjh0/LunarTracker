import math
from datetime import date

class Moon:
    # Geometric properties of display
    radius = 0
    position = (0,0)

    # Moon's properties
    waxing = True
    standard_date = date(2025, 10, 21) # (accurate, but arbitrary) Date of a new moon phase occurrence
    PERIOD = 29.5 # Period of the lunar cycle

    def __init__(self, canvas, radius, position):
        self.canvas = canvas
        self.radius = radius
        self.position = position


    def set_phase(self, day):
        inner_radius = self.get_inner_radius(day) # distance of radius from center

        points = self.get_arc_points(self.position[0] + self.radius) # Outer arc
        points.reverse() # Reverses so the next addition is continuous
        points += self.get_arc_points((self.position[0] + inner_radius)) # Inner arc

        if self.waxing:
            self.canvas.create_oval(self.position[0] - self.radius,
                                    self.position[1] - self.radius,
                                    self.position[0] + self.radius,
                                    self.position[1] + self.radius,
                                    fill="black", outline="")
            if not inner_radius == self.radius: # Prevents sliver from showing up on full/new moon
                self.canvas.create_polygon(points, fill="white", outline="white")

        else:
            self.canvas.create_oval(self.position[0] - self.radius,
                                    self.position[1] - self.radius,
                                    self.position[0] + self.radius,
                                    self.position[1] + self.radius,
                                    fill="white", outline="")
            if not inner_radius == self.radius: # Prevents sliver from showing up on full/new moon
                self.canvas.create_polygon(points, fill="black", outline="black")

    def get_arc_points(self, end_x):
        point_list = []
        x_radius = end_x - self.position[0]

        for angle in range(-90, 90):
            point_list.append((
                self.position[0] + x_radius * math.cos(math.radians(angle)),
                self.position[1] + self.radius * math.sin(math.radians(angle))
            ))
        return point_list

    def get_inner_radius(self, day):
        delta = self.parse_date(day) - self.standard_date
        days = delta.days # extracts the days from the difference

        while days < 0:
            days = self.PERIOD + days

        days = days % self.PERIOD

        # Waxing
        if days < self.PERIOD / 2:
            self.waxing = True
        # Waning
        else:
            self.waxing = False

        # Calculates the progress per day
        # The inner arc goes from +radius to -radius in half a period
        change = (2 * self.radius) / (self.PERIOD / 2)

        days %= self.PERIOD / 2
        return self.radius - change * days

    def parse_date(self, d):
        year, month, day = map(int, d.split("-"))
        return date(year, month, day)
    
    def get_phase_emoji(self, day):
        """Returns a moon phase emoji for the given date"""
        delta = self.parse_date(day) - self.standard_date
        days = delta.days
        
        while days < 0:
            days = self.PERIOD + days
        
        days = days % self.PERIOD
        
        # Determine phase based on day in cycle
        if days < 1:
            return "🌑"  # New Moon
        elif days < 7:
            return "🌒"  # Waxing Crescent
        elif days < 8:
            return "🌓"  # First Quarter
        elif days < 14:
            return "🌔"  # Waxing Gibbous
        elif days < 15:
            return "🌕"  # Full Moon
        elif days < 21:
            return "🌖"  # Waning Gibbous
        elif days < 22:
            return "🌗"  # Last Quarter
        elif days < 29:
            return "🌘"  # Waning Crescent
        else:
            return "🌑"  # New Moon