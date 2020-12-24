# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/utils.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 1646 bytes
import os, math, logging
logger = logging.getLogger('Utils')

def get_next_filename(sdir, prefix, ext):
    for cnt in range(0, 99999):
        fname = os.path.join(sdir, '{0}_{1}{2}'.format(prefix, str(cnt).zfill(5), ext))
        if os.path.isfile(fname):
            continue
        else:
            return fname

    return 'Kazam_recording{0}'.format(ext)


def in_circle(center_x, center_y, radius, x, y):
    dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
    return dist <= radius


def get_by_idx(lst, index):
    return filter(lambda s: s[0] == index, lst)