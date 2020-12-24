# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\math.py
# Compiled at: 2020-04-12 12:08:25
# Size of source mod 2**32: 209 bytes
"""Math"""

def calculate_distance(p1, p2):
    """Calculate Distance between two points p1=[x1,y1],p2=[x2,y2]"""
    x1, y1 = p1
    x2, y2 = p2
    distance = ((y1 - y2) ** 2 + (x1 - x2) ** 2) ** 0.5
    return distance