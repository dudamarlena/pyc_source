# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/juliart/main.py
# Compiled at: 2019-12-28 17:00:40
# Size of source mod 2**32: 14357 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""
from .colors import get_theme_colors
from .namer import RobotNamer
from .utils import check_restricted, get_font
from PIL import Image, ImageDraw, ImageFont
from random import randint, uniform, choice
from math import sqrt
import os, shutil, sys, tempfile

class JuliaSetAnimation:
    __doc__ = 'A JuliaSetAnimation instantiates (and controls) a set of JuliaSet\n       instances to generate multiple images, and then assemble them into\n       an animation. We take a user requested number of frames, and then\n       sample along that range from a randomly chosen value (-1, 1) to 1.\n       Since the random values are points along a circle, the user is allowed\n       to randomize a single or both dimensions.\n    '

    def __init__(self, resolution=1000, color='random', iterations=200, theme='random', rgb=None, ca=None, cb=None, cleanup=True, zoom_max=3, zoom_min=0):
        self.ca = ca or uniform(-1, 1)
        self.cb = cb or uniform(-1, 1)
        self.check_cparams()
        self.zoom_max = max(3, zoom_max)
        self.zoom_min = max(0, zoom_min)
        self.zoom = uniform(self.zoom_min, self.zoom_max)
        self.cleanup = cleanup
        self.resolution = resolution
        self.color = color
        self.theme = theme
        self.iterations = iterations
        self.rgb = rgb

    def __str__(self):
        return '[juliaset-animation][resolution:%s][color:%s][iterations:%s]' % (
         self.resolution,
         self.color,
         self.iterations)

    def __repr__(self):
        return self.__str__()

    def check_cparams(self, min_range=-1.0, max_range=1.0):
        """Ensure that we have floats that are between -1 and 1.
        """
        for value in [self.ca, self.cb]:
            check_restricted(value, min_range, max_range)

    def calculate_range(self, value, frames, left_bound=-1, right_bound=1):
        """Given a starting value (value) calculate a range of values
           from that value to either a right or left bound. We choose the bound
           that presents the larger distance to generate greater variation. For
           the c arguments, this means between -1 and 1.
        """
        distance_left = abs(left_bound - value)
        distance_right = abs(right_bound - value)
        if distance_right > distance_left:
            increment = (right_bound - value) / frames
        else:
            increment = (left_bound - value) / frames
        rangex = [value + x * increment for x in range(frames)]
        if increment < 0:
            if choice([1, 2]) == 1:
                rangex.reverse()
        return rangex

    def generate_animation(self, iterations=None, zoom=1.8, outfile=None, frames=30, randomize_a=True, randomize_b=True, randomize_zoom=False, text=None, fontsize=16, fontalpha=100, font='OpenSans-Regular.ttf', xcoord=10, ycoord=10):
        """Generate the image. If iterations is not provided, we use the default

           Parameters
           ==========
           iterations: iterations per pixel.
        """
        if not iterations:
            iterations = self.iterations
        else:
            try:
                import imageio
            except:
                sys.exit('imageio is required to animate. pip install juliart[animate]')

            rangea = [
             self.ca] * frames
            rangeb = [self.cb] * frames
            zooms = [zoom] * frames
            if randomize_a:
                rangea = self.calculate_range(self.ca, frames)
            if randomize_b:
                rangeb = self.calculate_range(self.cb, frames)
            if randomize_zoom:
                zooms = self.calculate_range((self.zoom),
                  frames, left_bound=(self.zoom_min), right_bound=(self.zoom_max))
            juliaset = JuliaSet(resolution=(self.resolution),
              color=(self.color),
              iterations=(self.iterations),
              theme=(self.theme),
              rgb=(self.rgb))
            colorbias = juliaset.colorbias
            glow = juliaset.glow
            prefix = juliaset.generate_name()
            tmpdir = tempfile.mkdtemp()
            if not outfile:
                outfile = '%s.gif' % prefix
            if not outfile.endswith('.gif'):
                outfile = '%s.gif' % os.path.splitext(outfile)[0]
            print('Generating Julia Set Animation...')
            images = []
            with imageio.get_writer(outfile, mode='I') as (writer):
                for i in range(frames):
                    juliaset = JuliaSet(resolution=(self.resolution),
                      iterations=(self.iterations),
                      quiet=True,
                      ca=(rangea[i]),
                      cb=(rangeb[i]))
                    juliaset.colorbias = colorbias
                    juliaset.glow = glow
                    juliaset.generate_image(zoom=(zooms[i]))
                    juliaset.write_text(text,
                      fontsize=fontsize,
                      xcoord=xcoord,
                      ycoord=ycoord,
                      font=font,
                      rgb=(
                     255, 255, 255, fontalpha))
                    pngfile = os.path.join(tmpdir, '%s-%s.png' % (prefix, i))
                    images.append(pngfile)
                    juliaset.save_image(pngfile)
                    writer.append_data(imageio.imread(pngfile))

                while images:
                    pngfile = images.pop()
                    writer.append_data(imageio.imread(pngfile))

            if self.cleanup:
                print('Cleaning up %s' % tmpdir)
                shutil.rmtree(tmpdir)
            else:
                print('Intermediate .png files are in: %s' % tmpdir)
        print('Animation saved to %s' % outfile)


class JuliaSet:
    __doc__ = "A Julia Set is a function named after a famous mathemetician, I think\n       it's considered a kind of fractal art. See details at\n       https://en.m.wikipedia.org/wiki/Julia_set. This class is derived\n       from https://github.com/Visual-mov/Colorful-Julia\n    "

    def __init__(self, resolution=1000, color='random', iterations=200, theme='random', rgb=None, quiet=False, ca=None, cb=None):
        self.ca = ca or uniform(-1, 1)
        self.cb = cb or uniform(-1, 1)
        self.check_cparams()
        self.quiet = quiet
        self.res = (resolution, resolution)
        self.color = color
        self.theme = theme
        self.iterations = iterations
        self.image = Image.new('RGBA', self.res)
        self.draw = ImageDraw.Draw(self.image)
        self.generate_colors(rgb)

    def check_cparams(self, min_range=-1.0, max_range=1.0):
        """Ensure that we have floats that are between -1 and 1.
        """
        for value in [self.ca, self.cb]:
            check_restricted(value, min_range, max_range)

    def __str__(self):
        return '[juliaset][resolution:%s][color:%s][iterations:%s]' % (
         self.res,
         self.color,
         self.iterations)

    def __repr__(self):
        return self.__str__()

    def generate_colors(self, rgb):
        """Re-generate colorbias and glow.
        """
        if self.theme == 'random':
            if rgb is not None:
                try:
                    self.colorbias = tuple([int(x.strip()) for x in rgb.split(',')])
                except:
                    sys.exit('Error parsing %s, ensure is comma separated numbers.')

            else:
                self.colorbias = (
                 self.rnd(20, 200),
                 self.rnd(20, 200),
                 self.rnd(20, 200))
        else:
            self.colorbias = get_theme_colors(self.theme)
        self.glow = (
         self.rnd(0, 10), self.rnd(0, 10), self.rnd(0, 10))

    def print(self, message):
        """A wrapper to print to check if quiet is True, and skip if so.
        """
        if not self.quiet:
            print(message)

    def generate_image(self, iterations=None, zoom=1.8, radius=4):
        """Generate the image. If iterations is not provided, we use the default

           Parameters
           ==========
           iterations: iterations per pixel.
        """
        if not iterations:
            iterations = self.iterations
        self.print('Generating Julia Set...')
        for x in range(self.res[0]):
            for y in range(self.res[1]):
                za = self.translate(x, 0, self.res[0], -zoom, zoom)
                zb = self.translate(y, 0, self.res[1], -zoom, zoom)
                i = 0
                while i < iterations:
                    tmp = 2 * za * zb
                    za = za * za - zb * zb + self.ca
                    zb = tmp + self.cb
                    if sqrt(za * za + zb * zb) > radius:
                        break
                    i += 1

                self.draw.point((
                 x, y), self.colorize(i, iterations) if i != iterations else (0, 0,
                                                                              0))

    def write_text(self, text, fontsize=16, rgb=(255, 255, 255), xcoord=10, ycoord=10, font='OpenSans-Regular.ttf'):
        """Given a text string, font size, and output coordinates, write text
           onto the image. The default font provided with the package 
        """
        if text not in (None, ''):
            import textwrap
            width, height = self.res
            fontfile = get_font(font)
            font = ImageFont.truetype(fontfile, fontsize)
            lines = textwrap.wrap(text)
            draw = self.draw
            image = self.image
            if len(rgb) > 3:
                text = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(text)
            total_height = ycoord
            for line in lines:
                w, h = font.getsize(line)
                xstart = (width - w) / 2
                if width - xcoord > w:
                    xstart = xcoord
                if total_height >= height:
                    break
                draw.text((xstart, total_height), line, font=font, fill=rgb)
                total_height += h

            if len(rgb) > 3:
                self.image = Image.alpha_composite(self.image, text)
            else:
                self.image = image
                self.draw = draw

    def save_image(self, outfile=None):
        """Save the image to an output file, if provided. Optionally add some
           text to it.
        """
        if not outfile:
            outfile = '%s.png' % self.generate_name()
        print('Saving image to %s' % outfile)
        self.image.save(outfile, 'PNG')

    def generate_name(self):
        """Generate a random filename from the Robot Namer
        """
        return RobotNamer().generate()

    def colorize(self, i, iterations=None):
        """Based on the user selection, save with a pattern, random, or glowing color
        """
        if not iterations:
            iterations = self.iterations
        if self.color == 'random':
            c = int(self.translate(i, 0, iterations, 0, 255) * (i / 4))
            return (c + self.colorbias[0], c + self.colorbias[1], c + self.colorbias[2])
        if self.color == 'pattern':
            if i % 2 == 0:
                return self.colorbias
            return (0, 0, 0)
        if self.color == 'glow':
            return (
             i * self.glow[0], i * self.glow[1], i * self.glow[2])
        print('Color choice %s is not valid.' % self.color)
        sys.exit(1)

    def rnd(self, a, b):
        return randint(a, b)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        return rightMin + float(value - leftMin) / float(leftMax - leftMin) * (rightMax - rightMin)