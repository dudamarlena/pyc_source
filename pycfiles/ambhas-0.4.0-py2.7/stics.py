# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/stics.py
# Compiled at: 2012-02-04 00:29:42
"""
Created on Fri Feb 03 18:12:26 2012

@author: K. Sreelash
@website: www.ambhas.com
@email: satkumartomer@gmail.com
"""
from __future__ import division
import numpy as np
from ambhas.xls import xlsread
infile_name = 'D:/svn/ambhas/examples/input_stics.xls'
xls_file = xlsread(infile_name)
argis = xls_file.get_cells('B2', 'soil_par')
norgs = xls_file.get_cells('C2', 'soil_par')