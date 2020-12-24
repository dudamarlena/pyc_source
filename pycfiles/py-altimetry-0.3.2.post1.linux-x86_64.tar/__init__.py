# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/__init__.py
# Compiled at: 2016-03-23 12:35:00
"""
altimetry module
@summary: Contains several functions and routines to deal with altimetry, remote sensing and in-situ data.
@author: Renaud DUSSURGET, LER/PAC IFREMER.
@change: Create in December 2012 by RD.
"""
from config import defaults as def_class
defaults = def_class()
from tools import *
from externals import *
from data import *