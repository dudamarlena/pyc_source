# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mkoenig/git/sbmlutils/sbmlutils/dfba/toy_wholecell/settings.py
# Compiled at: 2019-10-27 06:58:29
# Size of source mod 2**32: 621 bytes
"""
Definition of constants.
"""
import os
MODEL_ID = 'toy_wholecell'
VERSION = 15
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
FBA_LOCATION = '{}_fba.xml'.format(MODEL_ID)
BOUNDS_LOCATION = '{}_bounds.xml'.format(MODEL_ID)
UPDATE_LOCATION = '{}_update.xml'.format(MODEL_ID)
TOP_LOCATION = '{}_top.xml'.format(MODEL_ID)
FLATTENED_LOCATION = '{}_flattened.xml'.format(MODEL_ID)
SEDML_LOCATION = 'dfba_simulation.xml'.format(MODEL_ID)
OMEX_LOCATION = '{}_v{}.omex'.format(MODEL_ID, VERSION)
ANNOTATIONS_LOCATION = 'annotations.xlsx'