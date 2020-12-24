# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/beholder/shared_config.py
# Compiled at: 2019-08-01 11:57:19
# Size of source mod 2**32: 1213 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
PLUGIN_NAME = 'beholder'
TAG_NAME = 'beholder-frame'
SUMMARY_FILENAME = 'frame.summary'
CONFIG_FILENAME = 'config.pkl'
SECTION_INFO_FILENAME = 'section-info.pkl'
SUMMARY_COLLECTION_KEY_NAME = 'summaries_beholder'
DEFAULT_CONFIG = {'values':'trainable_variables', 
 'mode':'variance', 
 'scaling':'layer', 
 'window_size':15, 
 'FPS':10, 
 'is_recording':False, 
 'show_all':False, 
 'colormap':'magma'}
SECTION_HEIGHT = 128
IMAGE_WIDTH = 768
TB_WHITE = 245