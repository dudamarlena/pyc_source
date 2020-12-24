# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vision/track/util.py
# Compiled at: 2010-10-24 04:45:38
from .. import boundingboxes

def calculateslidingspace(base, offset, frame):
    xstart = max(0, base.xtl - offset)
    xstop = min(frame[0] - 1, base.xbr + offset)
    ystart = max(0, base.ytl - offset)
    ystop = min(frame[1] - 1, base.ybr + offset)
    return (xstart, ystart, xstop, ystop)


def buildslidingwindows(base, space, skip):
    """
    Generate sliding windows based off the image that are displaced and resized.
    """
    nextframe = base.frame
    w = base.get_width()
    h = base.get_height()
    xstart = (space[0], ystart) = space[1]
    xstop = space[2] - w
    ystop = space[3] - h
    boxes = []
    for i in range(xstart, xstop, skip):
        for j in range(ystart, ystop, skip):
            boxes.append(TBox(i, j, i + w, j + h, nextframe))

    return boxes