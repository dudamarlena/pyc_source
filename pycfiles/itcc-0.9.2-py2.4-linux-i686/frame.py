# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/core/frame.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'

def parseframe(frame_str):
    if frame_str is None:
        return
    for range1 in frame_str.split(','):
        for range_ in range1.split():
            step = 1
            if '/' in range_:
                (range_, step) = tuple(range_.split('/'))
                step = int(step)
            if '-' in range_:
                (begin, end) = tuple([ int(x) - 1 for x in range_.split('-') ])
                end += 1
            else:
                begin = int(range_) - 1
                end = begin + 1
            for x in range(begin, end, step):
                yield x

    return