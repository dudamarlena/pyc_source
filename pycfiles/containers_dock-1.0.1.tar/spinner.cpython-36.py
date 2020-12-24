# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/share/containershare-python/containershare/logger/spinner.py
# Compiled at: 2018-07-30 07:20:36
# Size of source mod 2**32: 2822 bytes
__doc__ = '\n\nlogger/spinner.py: Simple spinner for logger\n\nCopyright (c) 2017 Vanessa Sochat\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
import os, sys, sys, time, threading
from random import choice

class Spinner:
    spinning = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    @staticmethod
    def balloons_cursor():
        while True:
            for cursor in '. o O @ *':
                yield cursor

    @staticmethod
    def changing_arrows():
        while True:
            for cursor in '<^>v':
                yield cursor

    def select_generator(self, generator):
        if generator == None:
            generator = choice(['cursor',
             'arrow',
             'balloons'])
        return generator

    def __init__(self, delay=None, generator=None):
        generator = self.select_generator(generator)
        if generator == 'cursor':
            self.spinner_generator = self.spinning_cursor()
        else:
            if generator == 'arrow':
                self.spinner_generator = self.changing_arrows()
            else:
                if generator == 'balloons':
                    self.spinner_generator = self.balloons_cursor()
                    if delay is None:
                        delay = 0.2
                else:
                    self.spinner_generator = self.spinning_cursor()
        if delay:
            if float(delay):
                self.delay = delay

    def run(self):
        while self.spinning:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\x08')
            sys.stdout.flush()

    def start(self):
        self.spinning = True
        threading.Thread(target=(self.run)).start()

    def stop(self):
        self.spinning = False
        time.sleep(self.delay)