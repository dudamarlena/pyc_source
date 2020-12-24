# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/flytrax/strip_blank_xrc_lines.py
# Compiled at: 2009-04-14 12:30:53
import re, sys
m = re.compile('^\\s*$')
fname = sys.argv[1]
fd = open(fname, mode='r')
for line in fd:
    mo = m.search(line)
    if mo is None:
        print line.rstrip()