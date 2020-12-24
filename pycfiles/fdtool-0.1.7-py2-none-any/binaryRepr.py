# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\binaryRepr.py
# Compiled at: 2018-06-19 13:38:40


def toBin(Candidate, U):
    Gen = [ '1' if k in {U.index(element) for element in Candidate} else '0' for k in range(len(U)) ]
    return ('').join(Gen)