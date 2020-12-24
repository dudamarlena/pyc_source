# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/toy_wholecell/settings.py
# Compiled at: 2017-06-09 13:36:44
"""
Settings for toy model.
"""
from __future__ import print_function, division
import os
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
model_id = 'toy_wholecell'
fba_file = ('{}_fba.xml').format(model_id)
bounds_file = ('{}_bounds.xml').format(model_id)
update_file = ('{}_update.xml').format(model_id)
top_file = ('{}_top.xml').format(model_id)
flattened_file = ('{}_flattened.xml').format(model_id)
annotations_file = 'annotations.xlsx'