# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/runner.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 1637 bytes
"""  Run whatever I'm doing at the time

Stuff in here probably belongs elsewhere.
"""
from . import md2slides
from . import slidelayout
from . import json2py
from . import py2json
from . import slide2png
from . import imagefind
import sys, os, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--markdown', type=(argparse.FileType('r')))
    parser.add_argument('-j', '--json', type=(argparse.FileType('r')))
    parser.add_argument('-g', '--gallery', nargs='*', default=['../gallery'])
    parser.add_argument('-o', '--output', nargs='*', default=['.'])
    parser.add_argument('--slide')
    parser.add_argument('--show')
    args = parser.parse_args()
    galleries = args.gallery
    folder = args.output
    mj = md2slides
    if args.markdown:
        msg = args.markdown
        mj = md2slides
    else:
        if args.json:
            mj = json2py
            msg = open(infile).read()
        slides = mj.interpret(msg)
        sl = slidelayout.SlideLayout()
        slides = sl.interpret(dict(slides=slides))
        s2png = slide2png.Slide2png()
        msg = dict(slides=slides, gallery=galleries)
        if args.slide:
            todo = []
            for slide in slides:
                heading = slide['heading']['text'].lower()
                if args.slide in heading:
                    print('processing:', heading)
                    todo.append(slide)

            msg['slides'] = todo
        else:
            msg['logname'] = 'slides.txt'
    s2png.interpret(msg)


if __name__ == '__main__':
    main()