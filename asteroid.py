class Asteroid:

    def __init__(self, x_place, y_place, x_velocity, y_velocity, size):
        self.x_place = x_place
        self.y_place = y_place
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.size = size

    def get_place(self):
        """
        :return: the coordinates of the ship as a tuple
        """
        return self.x_place, self.y_place

    def set_place_x(self, place):
        self.x_place = place

    def set_place_y(self, place):
        self.y_place = place

    def get_velocity(self):
        """
        :return: the velocity of the ship as a tuple
        """
        return self.x_velocity, self.y_velocity

    def set_velocity_x(self, speed):
        self.x_velocity = speed

    def set_velocity_y(self, speed):
        self.y_velocity = speed

    def get_size(self):
        """
        :return: the head direction of the ship
        """
        return self.size

    def set_size(self, new_size):
        self.size = new_size

    def get_radius(self):
        rad = self.size * 10 - 5
        return rad

    def has_intersection(self, obj):
        distance1 = (obj.x_place - self.x_place) ** 2 + (
                obj.y_place - self.y_place) ** 2
        distance2 = distance1 ** 0.5
        if distance2 <= self.get_radius() + obj.get_radius():
            return True
        return False
