# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_all_collisions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 9582 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'f 10 0.033, s, f 20 0.033, s, f 30 0.033, s, f 30 0.033, s, q'
tags = 'collision'
import cocos
import cocos.director as director
import cocos.actions as ac
import cocos.collision_model as cm
import cocos.euclid as eu
import random
half_street_width = 15
streets_per_side = 5
street_to_square_width_multiplier = 4
street_color = (170, 170, 0, 255)
square_color = (120, 32, 120, 255)
pool_car_size = 4
time_to_next_crossing = 1.0
squares_per_side = streets_per_side - 1
street_width = 2 * half_street_width
square_width = street_to_square_width_multiplier * street_width
crossing_point_separation = square_width + 2 * half_street_width
view_width = 1.0 * square_width + square_width * (squares_per_side - 2) + street_width * (streets_per_side - 2)
view_width = square_width * (squares_per_side - 1) + street_width * (streets_per_side - 2)
view_height = view_width
offset = 0.5 * street_width + 0.5 * square_width
offset = half_street_width + street_to_square_width_multiplier * half_street_width
offset = half_street_width * (street_to_square_width_multiplier + 1)

class Actor(cocos.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        rx = kwargs.pop('rx', None)
        ry = kwargs.pop('ry', None)
        desired_width = kwargs.pop('desired_width', None)
        (super(Actor, self).__init__)(*args, **kwargs)
        if desired_width is None:
            desired_width = self.image.width
        desired_width = float(desired_width)
        self.scale = desired_width / self.width
        if rx is None:
            rx = 0.8 * desired_width / 2.0
        if ry is None:
            ry = 0.8 * self.image.height / self.image.width * desired_width / 2.0
        self.cshape = cm.CircleShape(eu.Vector2(0.0, 0.0), rx)

    def update_position(self, new_position):
        assert isinstance(new_position, eu.Vector2)
        self.position = new_position
        self.cshape.center = new_position


class RobotCar(Actor):
    __doc__ = '\n    '

    def __init__(self):
        super(RobotCar, self).__init__('circle6.png', desired_width=32)
        self.e_free()

    def e_free(self):
        self.state = 'free'
        self.color = (20, 120, 70)

    def e_burn(self):
        self.state = 'burning'
        self.color = (180, 0, 0)
        template_action = ac.Delay(2.0) + ac.CallFunc(self.e_free)
        self.do(template_action)

    def e_travel(self):
        self.state = 'traveling'

    def do_travel(self, initial_crossing, final_crossing):
        self.e_travel()
        self.color = (20, 120, 70)
        self.next_crossing = initial_crossing
        self.final_crossing = final_crossing
        self.update_when_crossing_reached()

    def update_when_crossing_reached(self):
        ix, iy = self.next_crossing
        self.update_position(eu.Vector2(ix * crossing_point_separation, iy * crossing_point_separation))
        dx = self.final_crossing[0] - self.next_crossing[0]
        ok = False
        if dx != 0:
            dy = 0
            if dx < 0:
                dx = -1
            else:
                dx = 1
            ix += dx
            ok = 0 < ix < streets_per_side - 1 and 0 < iy < streets_per_side - 1 or (
             ix, iy) == self.final_crossing
            if not ok:
                ix -= dx
        if not ok:
            dx = 0
            dy = self.final_crossing[1] - self.next_crossing[1]
            if dy != 0:
                if dy < 0:
                    dy = -1
                else:
                    dy = 1
                iy += dy
        else:
            self.next_crossing = (
             ix, iy)
            self.elapsed = 0.0
            self.arrival = time_to_next_crossing
            self.move_in_x = dx != 0
            fastness = crossing_point_separation / time_to_next_crossing
            if self.move_in_x:
                self.scalar_vel = dx * fastness
            else:
                self.scalar_vel = dy * fastness

    def is_travel_completed(self):
        return self.elapsed > self.arrival and self.next_crossing == self.final_crossing

    def update(self, dt):
        """
        dont call this when self.state != 'traveling'
        """
        self.elapsed += dt
        if self.elapsed > self.arrival:
            if self.next_crossing == self.final_crossing:
                self.e_free()
            else:
                self.update_when_crossing_reached()
        else:
            x, y = self.cshape.center
            if self.move_in_x:
                x += self.scalar_vel * dt
            else:
                y += self.scalar_vel * dt
            self.update_position(eu.Vector2(x, y))


class City(cocos.layer.Layer):

    def __init__(self):
        super(City, self).__init__()
        bg = (cocos.layer.ColorLayer)(*street_color, width=view_width, height=view_width)
        self.add(bg)
        self.add_squares()
        self.position = (-offset, -offset)
        bg.position = (offset, offset)
        self.cars = set()
        while len(self.cars) < pool_car_size:
            car = RobotCar()
            self.cars.add(car)
            self.add(car)

        self.collman = cm.CollisionManagerGrid(-square_width, view_width + square_width, -square_width, view_height + square_width, 40.0, 40.0)
        self.schedule(self.update)

    def add_squares(self):
        for iy in range(squares_per_side):
            y = half_street_width + iy * crossing_point_separation
            for ix in range(squares_per_side):
                square = (cocos.layer.ColorLayer)(*square_color, width=square_width, height=square_width)
                x = half_street_width + ix * crossing_point_separation
                square.position = (x, y)
                self.add(square, z=2)

    def generate_travel(self):
        if random.random() > 0.5:
            ix = 0
            if random.random() > 0.5:
                ix = streets_per_side - 1
            iy = random.randint(1, streets_per_side - 2)
        else:
            iy = 0
            if random.random() > 0.5:
                iy = streets_per_side - 1
            ix = random.randint(1, streets_per_side - 2)
        jx = streets_per_side - 1 - ix
        jy = streets_per_side - 1 - iy
        initial_crossing = (ix, iy)
        final_crossing = (jx, jy)
        return (initial_crossing, final_crossing)

    def update(self, dt):
        for car in self.cars:
            if car.state == 'free':
                initial_crossing, final_crossing = self.generate_travel()
                car.do_travel(initial_crossing, final_crossing)
            if car.state == 'traveling':
                car.update(dt)
        else:
            self.collman.clear()

        for car in self.cars:
            self.collman.add(car)
        else:
            for car, other in self.collman.iter_all_collisions():
                if car.state != 'burning':
                    car.e_burn()
                if other.state != 'burning':
                    other.e_burn()


description = '\nExample for the collision module.\nIt should be seen like a top view of city streets with green circles\ntraveling the streets. When a circle colides with other, it should turn red.\n'

def main():
    print(description)
    director.init(width=view_width, height=view_height)
    scene = cocos.scene.Scene()
    city = City()
    scene.add(city)
    director.run(scene)


if __name__ == '__main__':
    main()