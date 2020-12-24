# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/markovmeme/main.py
# Compiled at: 2019-12-29 17:48:30
# Size of source mod 2**32: 5875 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import random
from .namer import RobotNamer
from .utils import list_corpus, list_images, get_font
from PIL import Image, ImageDraw, ImageFont
import math, random, os, sys
here = os.path.dirname(os.path.abspath(__file__))

class MemeImage:
    __doc__ = "A Meme Image includes markov (or randomly selected) text from a corpus, and\n       a matching image. The image and corpus can be customized, otherwise\n       the image is matched to the text. If the user selects a custom corpus,\n       a custom image must also be provided. If an image doesn't exist for a \n       given corpus, the user is required to specify it.\n    "

    def __init__(self, image=None, corpus=None, quiet=False):
        self.corpus = self.get_corpus(corpus)
        self.quiet = quiet
        self.imagefile = self.get_image(image, self.corpus)
        self.image = Image.open(self.imagefile).convert('RGBA')
        self.draw = ImageDraw.Draw(self.image)

    def get_corpus(self, corpus):
        """Given an input corpus, validate that it's available. If it's not
           a full path to a file, or if it doesn't exist, select one at random.
        """
        if os.path.exists(corpus):
            return corpus
        options = list_corpus()
        if corpus in options:
            return corpus
        return random.choice(corpus)

    def get_image(self, image, corpus):
        """If the image is provided, the full path must exist. Otherwise,
           we list images that come with the modula and randomly select one
           that matches the corpus.
        """
        if image is not None:
            if os.path.exists(image):
                return image
        options = [x for x in list_images() if corpus in x]
        if not options:
            sys.exit('No images exist for corpus %s. Please specify --image.' % corpus)
        choice = random.choice(options)
        return os.path.join(here, 'data', 'images', '%s.png' % choice)

    def __str__(self):
        return '[mememl][%s]' % self.corpus

    def __repr__(self):
        return self.__str__()

    def print(self, message):
        """A wrapper to print to check if quiet is True, and skip if so.
        """
        if not self.quiet:
            print(message)

    def write_text(self, text, fontsize=32, rgb=(255, 255, 255), ycoord=10, margin=30, font='Anton-Regular.ttf'):
        """Given a text string, font size, and output coordinates, write text
           onto the image. The default font provided with the package 
        """
        if text not in (None, ''):
            width, height = self.image.size
            fontfile = get_font(font)
            font = ImageFont.truetype(fontfile, fontsize)
            expect_width, expect_height = self.draw.textsize(text, font)
            lines = self.text2lines(font, text, width - margin)
            for i, line in enumerate(lines):
                w, h = self.draw.textsize(line, font)
                xcoord = width / 2 - w / 2
                ycoord = i * h
                self.draw.text((xcoord - 2, ycoord - 2), (lines[i]), (0, 0, 0), font=font)
                self.draw.text((xcoord + 2, ycoord - 2), (lines[i]), (0, 0, 0), font=font)
                self.draw.text((xcoord + 2, ycoord + 2), (lines[i]), (0, 0, 0), font=font)
                self.draw.text((xcoord - 2, ycoord + 2), (lines[i]), (0, 0, 0), font=font)
                self.draw.text((xcoord, ycoord), line, font=font, fill=rgb)

    def text2lines(self, font, text, max_width):
        """Wraps text so always fits within max_width.

        Args:
            font (ImageFont): The font being used.
            text (string): Text to wrap.
            max_width (int): Maximum number of pixels for each line's width.

        Returns:
            A list of strings, corresponding to each line.
        """
        words = text.split()
        lines = []
        current_words = []
        current_width = 0
        space_width = font.getsize(' ')[0]
        for word in words:
            word_width = font.getsize(word)[0]
            if word_width + current_width > max_width:
                lines.append(' '.join(current_words))
                current_words = [
                 word]
                current_width = word_width + space_width
            else:
                current_words.append(word)
                current_width += word_width + space_width

        lines.append(' '.join(current_words))
        return lines

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