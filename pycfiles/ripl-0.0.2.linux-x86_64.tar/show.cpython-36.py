# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/show.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 1888 bytes
"""
Simple slide shower using eog.

TODO: would be nice if it did not give eog focus.
"""
import os, time, subprocess
from PIL import Image, ImageDraw

class SlideShow:

    def __init__(self):
        self.slides = []
        self.pos = 0
        self.wait = 0
        self.feh = None

    def interpret(self, msg):
        """ Create a slide show """
        self.captions = msg.get('captions', '.')
        for item in msg['slides']:
            self.add(item)

    def add(self, slide):
        self.slides.append(slide)

    def next(self):
        os.system('kill -s 10 %d' % self.feh.pid)

    def show(self):
        slides = ' '.join([x.get('image', '') for x in self.slides])
        cmd = 'feh --scale-down --caption-path %s %s' % (
         self.captions, slides)
        self.feh = subprocess.Popen(cmd.split(' '))

    def set_duration(self, duration):
        """ Calculate how long each slide should show """
        fixed = sum(int(x.get('time', 0)) for x in self.slides)
        nfixed = len([x for x in self.slides if x.get('time', 0) > 0])
        unfixed = len(self.slides) - nfixed
        self.wait = max(1, int(duration / unfixed))

    def run(self):
        """ Run the show """
        self.show()
        if not self.wait:
            return
        for image in self.slides:
            wait = image.get('time', 0)
            wait = max(self.wait, wait)
            print('waiting %d seconds %s' % (
             wait, image.get('image', '')))
            yield image
            time.sleep(wait)
            self.next()