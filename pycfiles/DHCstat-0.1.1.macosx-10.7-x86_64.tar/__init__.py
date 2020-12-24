# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/anaconda/lib/python2.7/site-packages/DHCstat/__init__.py
# Compiled at: 2018-05-02 05:08:10
"""
Copyright (c) 2018 Eddie Yi.Huang

"""
from ._version import __version__
from statistics import LuwakStat
from datamining import LuwakMining
LuwakStat = LuwakStat()
LuwakMining = LuwakMining()