# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\particle.py
# Compiled at: 2020-03-29 14:00:05
# Size of source mod 2**32: 4711 bytes
__doc__ = '\nParticle - Object produced by an Emitter.  Often used in large quantity to produce visual effects effects\n'
from arcadeplus.sprite import Sprite
from arcadeplus.draw_commands import Texture
import arcadeplus.utils
from arcadeplus.arcade_types import Point, Vector
from typing import Union
FilenameOrTexture = Union[(str, Texture)]

class Particle(Sprite):
    """Particle"""

    def __init__(self, filename_or_texture, change_xy, center_xy=(0.0, 0.0), angle=0.0, change_angle=0.0, scale=1.0, alpha=255, mutation_callback=None):
        if isinstance(filename_or_texture, Texture):
            super().__init__(None, scale=scale)
            self.append_texture(filename_or_texture)
            self.set_texture(0)
        else:
            super().__init__(filename_or_texture, scale=scale)
        self.center_x = center_xy[0]
        self.center_y = center_xy[1]
        self.change_x = change_xy[0]
        self.change_y = change_xy[1]
        self.angle = angle
        self.change_angle = change_angle
        self.alpha = alpha
        self.mutation_callback = mutation_callback

    def update(self):
        super().update()
        if self.mutation_callback:
            self.mutation_callback(self)

    def can_reap(self):
        """Determine if Particle can be deleted"""
        raise NotImplementedError('Particle.can_reap needs to be implemented')


class EternalParticle(Particle):
    """EternalParticle"""

    def __init__(self, filename_or_texture, change_xy, center_xy=(0.0, 0.0), angle=0, change_angle=0, scale=1.0, alpha=255, mutation_callback=None):
        super().__init__(filename_or_texture, change_xy, center_xy, angle, change_angle, scale, alpha, mutation_callback)

    def can_reap(self):
        """Determine if Particle can be deleted"""
        return False


class LifetimeParticle(Particle):
    """LifetimeParticle"""

    def __init__(self, filename_or_texture, change_xy, lifetime, center_xy=(0.0, 0.0), angle=0, change_angle=0, scale=1.0, alpha=255, mutation_callback=None):
        super().__init__(filename_or_texture, change_xy, center_xy, angle, change_angle, scale, alpha, mutation_callback)
        self.lifetime_original = lifetime
        self.lifetime_elapsed = 0.0

    def update(self):
        super().update()
        self.lifetime_elapsed += 0.016666666666666666

    def can_reap(self):
        """Determine if Particle can be deleted"""
        return self.lifetime_elapsed >= self.lifetime_original


def clamp(a, low, high):
    if a > high:
        return high
    if a < low:
        return low
    return a


class FadeParticle(LifetimeParticle):
    """FadeParticle"""

    def __init__(self, filename_or_texture, change_xy, lifetime, center_xy=(0.0, 0.0), angle=0, change_angle=0, scale=1.0, start_alpha=255, end_alpha=0, mutation_callback=None):
        super().__init__(filename_or_texture, change_xy, lifetime, center_xy, angle, change_angle, scale, start_alpha, mutation_callback)
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha

    def update(self):
        super().update()
        a = arcadeplus.utils.lerp(self.start_alpha, self.end_alpha, self.lifetime_elapsed / self.lifetime_original)
        self.alpha = clamp(a, 0, 255)