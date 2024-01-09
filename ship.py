SHIP_RADIUS = 1


class Ship:

    def __init__(self, x_place, y_place, x_velocity, y_velocity,
                 head_direction):
        self.x_place = x_place
        self.y_place = y_place
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.head_direction = head_direction
        self.radius = SHIP_RADIUS

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

    def get_head_direction(self):
        """
        :return: the head direction of the ship
        """
        return self.head_direction

    def set_head_direction(self, head):
        self.head_direction = head

    def get_radius(self):
        return self.radius
