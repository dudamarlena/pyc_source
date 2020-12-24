# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/stics.py
# Compiled at: 2012-02-04 00:29:42
__doc__ = '\nCreated on Fri Feb 03 18:12:26 2012\n\n@author: K. Sreelash\n@website: www.ambhas.com\n@email: satkumartomer@gmail.com\n'
from __future__ import division
import numpy as np
from ambhas.xls import xlsread
infile_name = 'D:/svn/ambhas/examples/input_stics.xls'
xls_file = xlsread(infile_name)
argis = xls_file.get_cells('B2', 'soil_par')
norgs = xls_file.get_cells('C2', 'soil_par')