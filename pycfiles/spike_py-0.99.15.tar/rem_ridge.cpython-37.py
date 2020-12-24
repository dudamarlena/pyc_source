# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/rem_ridge.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 1038 bytes
"""removes ridges in 2D

Created by Marc-André on 2011-08-15.
Copyright (c) 2011 IGBMC. All rights reserved.
"""
from __future__ import print_function
from spike import NPKError
from spike.NPKData import NPKData_plugin
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def rem_ridge(data):
    """
    This function removes a F1 ridge by evaluating a mean avalue over the last 10% data of each column of a 2D
    """
    data.check2D()
    deb = int(0.9 * data.size1)
    fin = data.size1
    r = data.row(deb)
    for i in xrange(deb + 1, fin):
        r.add(data.row(i))

    r.mult(-1.0 / (fin - deb))
    for i in xrange(data.size1):
        data.set_row(i, data.row(i).add(r))

    return data


NPKData_plugin('rem_ridge', rem_ridge)