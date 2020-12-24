# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/run.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 1509 bytes
"""  Run whatever I'm doing at the time

Stuff in here probably belongs elsewhere.
"""
import sys, time
from . import md2py
from . import json2py
from . import show
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', default=0,
      type=int,
      help='time for slideshow in minutes')
    parser.add_argument('-f', '--folder', default='.',
      help='folder of slides')
    parser.add_argument('-s', '--slides', default='slides.txt',
      help='list of slides to show')
    parser.add_argument('-w', '--wait', default=0,
      type=int,
      help='time to wait for slideshow')
    args = parser.parse_args()
    folder = args.folder
    infile = args.slides
    wait = args.wait
    msg = open(infile)
    mj = md2py
    if infile.endswith('json'):
        mj = json2py
        msg = open(infile).read()
    slides = mj.interpret(msg)
    print('Number of slides:', len(slides))
    print()
    print(slides[0]['image'])
    print()
    ss = show.SlideShow()
    ss.interpret(dict(slides=slides, captions=folder))
    if args.time:
        ss.set_duration(args.time * 60)
    time.sleep(wait)
    for item in ss.run():
        pass


if __name__ == '__main__':
    main()