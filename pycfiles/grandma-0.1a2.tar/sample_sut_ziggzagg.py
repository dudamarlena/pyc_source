# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/sample_sut_ziggzagg.py
# Compiled at: 2010-10-28 01:10:35


def sut_ziggzagg(x):
    """
    Sample SUT used to demonstrate heuristic test oracles.
    """
    if x <= 90.0:
        result = float(x) / 90.0
    elif 90.0 < x <= 270.0:
        result = 1.0 - float(x - 90.0) / 90
    elif 270.0 < x <= 360.0:
        result = -1.0 + float(x - 270.0) / 90
    else:
        result = 0.0
    return result