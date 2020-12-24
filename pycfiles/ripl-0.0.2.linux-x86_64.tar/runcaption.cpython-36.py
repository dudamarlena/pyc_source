# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/runcaption.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 621 bytes
"""  Run whatever I'm doing at the time

Stuff in here probably belongs elsewhere.
"""
import md2py, json2py, caption, show, sys, os
infile = os.path.expanduser('~/devel/blog/stories/talk.rst')
folder = '.'
if sys.argv[1:]:
    folder = sys.argv[1]
if sys.argv[2:]:
    infile = sys.argv[2]
mj = md2py
msg = open(infile)
if infile.endswith('json'):
    mj = json2py
    msg = open(infile).read()
slides = mj.interpret(msg)
print(slides[:5])
ss = caption.SlideShow()
ss.interpret(dict(slides=slides, folder=folder))