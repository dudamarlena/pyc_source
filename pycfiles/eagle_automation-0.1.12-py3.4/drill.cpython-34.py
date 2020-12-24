# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/eagle_automation/drill.py
# Compiled at: 2015-08-19 03:57:14
# Size of source mod 2**32: 581 bytes
import re, sys, logging
log = logging.getLogger('pea').getChild(__name__)

def drill():
    lines = 0
    for line in sys.stdin:
        g = re.match(' (T[0-9][0-9]) *([0-9.]+)(\\w+) *', line)
        if g:
            drill, size, unit = g.groups()
            size = float(size)
            if unit == 'inch':
                size = size * 25.4
            else:
                if unit == 'mils':
                    size = size * 0.0254
                elif unit != 'mm':
                    raise Exception('Unknown unit: ' + unit)
            sys.stdout.write('%s  %.2fmm\n' % (drill, size))
            lines += 1
            continue

    if not lines:
        log.error('no drills found!\n')
        sys.exit(1)