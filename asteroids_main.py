from screen import Screen
import sys
from random import *
from ship import *
from asteroid import *
from torpedo import *
import math

STARTING_SCORE = 0
DEFAULT_ASTEROIDS_NUM = 5
BIG_ASTEROID_SIZE = 3
MEDIUM_ASTEROID_SIZE = 2
SMALL_ASTEROID_SIZE = 1
LIVES = 3
GAME_END = "End Of Game"
LOST_GAME = "You have lost the game!"
ALERT = 'ALERT!'
ALERT_MESSAGE = 'Stay away from asteroids!'
WIN_MESSAGE = "You Won The Game"
WIN_MESSAGE_CONTENT = "GG"
BIG_ASTEROID_SCORE = 20
MEDIUM_ASTEROID_SCORE = 50
SMALL_ASTEROID_SCORE = 100
MAXIMUM_TORPEDOES = 10
TORPEDO_LIFE_SPAN = 200


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__score = STARTING_SCORE
        ship_x = random_generator("axis")
        ship_y = random_generator("axis")
        self.counter = 0
        self.__ship = Ship(ship_x, ship_y, 0, 0, math.degrees(0.0))
        self.__screen.draw_ship(ship_x, ship_y, math.degrees(0.0))
        ################################################
        self.asteroids_lst = list()
        for asteroid in range(asteroids_amount):
            asteroid_x = random_generator("axis")
            asteroid_y = random_generator("axis")
            if asteroid_x == ship_x or ship_y == asteroid_y:
                continue
            asteroid_speed_x = random_generator("velocity")
            asteroid_speed_y = random_generator("velocity")

            new_asteroid = Asteroid(asteroid_x, asteroid_y, asteroid_speed_x,
                                    asteroid_speed_y, BIG_ASTEROID_SIZE)
            self.add_object(new_asteroid)
            self.__screen.draw_asteroid(new_asteroid, asteroid_x, asteroid_y)
            ############################################################
        self.torpedo_lst = list()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        if len(self.asteroids_lst)==0:
            self.end_current_game(WIN_MESSAGE, WIN_MESSAGE_CONTENT)
        if self.__screen.should_end():
            self.end_current_game(GAME_END,LOST_GAME)
        if self.__screen.is_up_pressed():
            self.update_velocity()
        if self.__screen.is_space_pressed() and len(
                self.torpedo_lst) != MAXIMUM_TORPEDOES:
            self.new_torpedo()
        if self.__screen.is_right_pressed():
            self.__ship.head_direction -= 7
        if self.__screen.is_left_pressed():
            self.__ship.head_direction += 7
        self.update_place(self.__ship)
        self.__screen.draw_ship(self.__ship.x_place, self.__ship.y_place,
                                self.__ship.head_direction)
        #######################################################
        for asteroid in self.asteroids_lst:
            if asteroid.has_intersection(self.__ship):
                self.ship_crash(asteroid)
                continue
            self.update_place(asteroid)
            self.__screen.draw_asteroid(asteroid, asteroid.x_place,
                                        asteroid.y_place)
        ########################################################

        for torpedo in self.torpedo_lst:
            flag = False

            for asteroid in self.asteroids_lst:
                if asteroid.has_intersection(torpedo):
                    self.destroy_asteroid(torpedo, asteroid)
                    flag = True
                    break
            if flag:
                continue
            torpedo.counter += 1
            if torpedo.counter == TORPEDO_LIFE_SPAN:
                self.remove_object(torpedo)
                continue
            self.update_place(torpedo)
            self.__screen.draw_torpedo(torpedo, torpedo.x_place,
                                       torpedo.y_place,
                                       torpedo.head_direction)

    def end_current_game(self, title, content):
        self.__screen.show_message(title, content)
        self.__screen.end_game()
        sys.exit()

    def remove_object(self, old_obj):
        if type(old_obj) == Torpedo:
            self.__screen.unregister_torpedo(old_obj)
            self.torpedo_lst.remove(old_obj)
        if type(old_obj) == Asteroid:
            self.__screen.unregister_asteroid(old_obj)
            self.asteroids_lst.remove(old_obj)

    def add_object(self, obj_to_add):
        if type(obj_to_add) == Torpedo:
            self.torpedo_lst.append(obj_to_add)
            self.__screen.register_torpedo(obj_to_add)
        if type(obj_to_add) == Asteroid:
            self.__screen.register_asteroid(obj_to_add, obj_to_add.size)
            self.asteroids_lst.append(obj_to_add)

    def ship_crash(self, asteroid):
        self.counter += 1
        self.__screen.remove_life()
        self.remove_object(asteroid)
        if self.counter == LIVES:
            self.end_current_game(GAME_END,LOST_GAME)
        else:
            self.__screen.show_message(ALERT, ALERT_MESSAGE)

    def new_torpedo(self):
        speed_x = self.__ship.x_velocity + 2 * math.cos(
            math.radians(self.__ship.head_direction))
        speed_y = self.__ship.y_velocity + 2 * math.sin(
            math.radians(self.__ship.head_direction))
        new_torpedo = Torpedo(self.__ship.x_place, self.__ship.y_place,
                              speed_x, speed_y, self.__ship.head_direction)
        self.add_object(new_torpedo)

    def destroy_asteroid(self, torpedo, asteroid):

        asteroid_size = asteroid.size - 1
        if asteroid_size != 0:
            self.create_new_asteroids(asteroid, asteroid_size, torpedo)
        self.add_score(asteroid.size)
        self.remove_object(torpedo)
        self.remove_object(asteroid)

    def create_new_asteroids(self, asteroid, size, torpedo):
        formula_one_x = (torpedo.x_velocity + asteroid.x_velocity)
        formula_one_y = (torpedo.y_velocity + asteroid.y_velocity)

        formula_two = math.sqrt(
            asteroid.x_velocity ** 2 + asteroid.y_velocity ** 2)

        new_astroid_speed_x = formula_one_x / formula_two
        new_astroid_speed_y = formula_one_y / formula_two
        first_asteroid = Asteroid(asteroid.x_place, asteroid.y_place,
                                  new_astroid_speed_x, new_astroid_speed_y,
                                  asteroid.size - 1)
        second_asteroid = Asteroid(asteroid.x_place, asteroid.y_place,
                                   (-1 * new_astroid_speed_x),
                                   (-1 * new_astroid_speed_y),
                                   asteroid.size - 1)
        self.add_object(first_asteroid)
        self.add_object(second_asteroid)

    def add_score(self, size):
        if size == BIG_ASTEROID_SIZE:
            self.__score += BIG_ASTEROID_SCORE
        elif size == MEDIUM_ASTEROID_SIZE:
            self.__score += MEDIUM_ASTEROID_SCORE
        else:
            self.__score += SMALL_ASTEROID_SCORE
        self.__screen.set_score(self.__score)

    def update_place(self, old_obj):
        screen_min_x = self.__screen_min_x
        screen_min_y = self.__screen_min_y
        delta_x = self.__screen_max_x - screen_min_x
        delta_y = self.__screen_max_y - screen_min_y
        new_spot_x = screen_min_x + (
                old_obj.x_place + old_obj.x_velocity - screen_min_x) % delta_x
        new_spot_y = screen_min_y + (
                old_obj.y_place + old_obj.y_velocity - screen_min_y) % delta_y
        old_obj.set_place_x(new_spot_x)
        old_obj.set_place_y(new_spot_y)

    def update_velocity(self):
        ship1 = self.__ship
        ship1.x_velocity = ship1.x_velocity + math.cos(
            math.radians(ship1.head_direction))
        ship1.y_velocity = ship1.y_velocity + math.sin(
            math.radians(ship1.head_direction))


def main(amount):
    runner = GameRunner(amount)
    runner.run()


def random_generator(n):
    rand = 0
    if n == "axis":
        rand = randint(1, 500) * choice([-1, 1])
    elif n == "velocity":
        rand = randint(1, 4) * choice([-1, 1])
    return rand


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(1)
