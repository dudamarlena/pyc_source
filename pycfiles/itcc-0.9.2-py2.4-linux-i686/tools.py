# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/torsionfit/tools.py
# Compiled at: 2008-04-20 13:19:45
"""Common parts for parmeval and parmfit"""
__revision__ = '$Rev$'

def readdat(datfname):
    fnames = []
    enes = []
    weights = []
    for line in file(datfname):
        words = line.split()
        assert len(words) in [2, 3]
        fnames.append(words[0])
        enes.append(float(words[1]))
        if len(words) == 2:
            weights.append(1.0)
        else:
            weights.append(float(words[2]))

    return (
     fnames, enes, weights)