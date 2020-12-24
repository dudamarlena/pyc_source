# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/choropie/poly_functs.py
# Compiled at: 2017-11-20 18:49:13
# Size of source mod 2**32: 1221 bytes


def area_for_polygon(polygon):
    result = 0
    imax = len(polygon) - 1
    for i in range(0, imax):
        result += polygon[i][1] * polygon[(i + 1)][0] - polygon[(i + 1)][1] * polygon[i][0]

    result += polygon[imax][1] * polygon[0][0] - polygon[0][1] * polygon[imax][0]
    return result / 2.0


def centroid_for_polygon(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) - 1
    result_x = 0
    result_y = 0
    for i in range(0, imax):
        result_x += (polygon[i][1] + polygon[(i + 1)][1]) * (polygon[i][1] * polygon[(i + 1)][0] - polygon[(i + 1)][1] * polygon[i][0])
        result_y += (polygon[i][0] + polygon[(i + 1)][0]) * (polygon[i][1] * polygon[(i + 1)][0] - polygon[(i + 1)][1] * polygon[i][0])

    result_x += (polygon[imax][1] + polygon[0][1]) * (polygon[imax][1] * polygon[0][0] - polygon[0][1] * polygon[imax][0])
    result_y += (polygon[imax][0] + polygon[0][0]) * (polygon[imax][1] * polygon[0][0] - polygon[0][1] * polygon[imax][0])
    result_x /= area * 6.0
    result_y /= area * 6.0
    return (
     result_y, result_x)