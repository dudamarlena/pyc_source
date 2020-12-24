# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\cocos\particle_systems.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 11154 bytes
"""Pre-defined Particle Systems.

Here are some concrete implementations of Particle Systems. They 
are built by subclassing :class:`ParticleSystem` and overriding
the desired class attributes."""
from __future__ import division, print_function, unicode_literals
__all__ = [
 'Fireworks', 'Spiral', 'Meteor', 'Sun', 'Fire', 'Galaxy', 'Flower', 'Explosion', 'Smoke']
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

class Fireworks(ParticleSystem):
    total_particles = 3000
    duration = -1
    gravity = Point2(0, -90)
    angle = 90
    angle_var = 20
    radial_accel = 0
    radial_accel_var = 0
    speed = 180
    speed_var = 50
    pos_var = Point2(0, 0)
    life = 3.5
    life_var = 1
    emission_rate = total_particles / life
    start_color = Color(0.5, 0.5, 0.5, 1.0)
    start_color_var = Color(0.5, 0.5, 0.5, 1.0)
    end_color = Color(0.1, 0.1, 0.1, 0.2)
    end_color_var = Color(0.1, 0.1, 0.1, 0.2)
    size = 8.0
    size_var = 2.0
    blend_additive = False
    color_modulate = True


class Explosion(ParticleSystem):
    total_particles = 700
    duration = 0.1
    gravity = Point2(0, -90)
    angle = 90.0
    angle_var = 360.0
    radial_accel = 0
    radial_accel_var = 0
    speed = 70.0
    speed_var = 40.0
    pos_var = Point2(0, 0)
    life = 5.0
    life_var = 2.0
    emission_rate = total_particles / duration
    start_color = Color(0.7, 0.2, 0.1, 1.0)
    start_color_var = Color(0.5, 0.5, 0.5, 0.0)
    end_color = Color(0.5, 0.5, 0.5, 0.0)
    end_color_var = Color(0.5, 0.5, 0.5, 0.0)
    size = 15.0
    size_var = 10.0
    blend_additive = False
    color_modulate = True


class Fire(ParticleSystem):
    total_particles = 250
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 10.0
    radial_accel = 0
    radial_accel_var = 0
    speed = 60.0
    speed_var = 20.0
    pos_var = Point2(40, 20)
    life = 3.0
    life_var = 0.25
    emission_rate = total_particles / life
    start_color = Color(0.76, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    size = 100.0
    size_var = 10.0
    blend_additive = True
    color_modulate = True


class Flower(ParticleSystem):
    total_particles = 500
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 360.0
    speed = 80.0
    speed_var = 10.0
    radial_accel = -60
    radial_accel_var = 0
    tangential_accel = 15.0
    tangential_accel_var = 0.0
    pos_var = Point2(0, 0)
    life = 4.0
    life_var = 1.0
    emission_rate = total_particles / life
    start_color = Color(0.5, 0.5, 0.5, 1.0)
    start_color_var = Color(0.5, 0.5, 0.5, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    size = 30.0
    size_var = 0.0
    blend_additive = True
    color_modulate = True


class Sun(ParticleSystem):
    total_particles = 350
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 360.0
    speed = 20.0
    speed_var = 5.0
    radial_accel = 0
    radial_accel_var = 0
    tangential_accel = 0.0
    tangential_accel_var = 0.0
    pos_var = Point2(0, 0)
    life = 1.0
    life_var = 0.5
    emission_rate = total_particles / life
    start_color = Color(0.75, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 0.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    size = 40.0
    size_var = 0.0
    blend_additive = True
    color_modulate = True


class Spiral(ParticleSystem):
    total_particles = 500
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 0.0
    speed = 150.0
    speed_var = 0.0
    radial_accel = -380
    radial_accel_var = 0
    tangential_accel = 45.0
    tangential_accel_var = 0.0
    pos_var = Point2(0, 0)
    life = 12.0
    life_var = 0.0
    emission_rate = total_particles / life
    start_color = Color(0.5, 0.5, 0.5, 1.0)
    start_color_var = Color(0.5, 0.5, 0.5, 0.0)
    end_color = Color(0.5, 0.5, 0.5, 1.0)
    end_color_var = Color(0.5, 0.5, 0.5, 0.0)
    size = 20.0
    size_var = 10.0
    blend_additive = True
    color_modulate = True


class Meteor(ParticleSystem):
    total_particles = 150
    duration = -1
    gravity = Point2(-200, 100)
    angle = 90.0
    angle_var = 360.0
    speed = 15.0
    speed_var = 5.0
    radial_accel = 0
    radial_accel_var = 0
    tangential_accel = 0.0
    tangential_accel_var = 0.0
    pos_var = Point2(0, 0)
    life = 2.0
    life_var = 1.0
    size = 60.0
    size_var = 10.0
    emission_rate = total_particles / life
    start_color = Color(0.2, 0.7, 0.7, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.2)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    blend_additive = True
    color_modulate = True


class Galaxy(ParticleSystem):
    total_particles = 200
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 360.0
    speed = 60.0
    speed_var = 10.0
    radial_accel = -80.0
    radial_accel_var = 0
    tangential_accel = 80.0
    tangential_accel_var = 0.0
    pos_var = Point2(0, 0)
    life = 4.0
    life_var = 1.0
    size = 37.0
    size_var = 10.0
    emission_rate = total_particles / life
    start_color = Color(0.12, 0.25, 0.76, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 0.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    blend_additive = True
    color_modulate = True


class Smoke(ParticleSystem):
    total_particles = 80
    duration = -1
    gravity = Point2(0, 0)
    angle = 90.0
    angle_var = 10.0
    speed = 25.0
    speed_var = 10.0
    radial_accel = 5
    radial_accel_var = 0
    tangential_accel = 0.0
    tangential_accel_var = 0.0
    pos_var = Point2(0.1, 0)
    life = 4.0
    life_var = 1.0
    size = 40.0
    size_var = 10.0
    emission_rate = total_particles / life
    start_color = Color(0.5, 0.5, 0.5, 0.1)
    start_color_var = Color(0, 0, 0, 0.1)
    end_color = Color(0.5, 0.5, 0.5, 0.1)
    end_color_var = Color(0, 0, 0, 0.1)
    blend_additive = True
    color_modulate = False