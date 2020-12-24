# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tjy/repos/dotez/dotez/config.py
# Compiled at: 2020-03-13 23:15:39
# Size of source mod 2**32: 502 bytes
import os, logging, sys
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_LOCS = [os.path.join('~', '.config', 'dotez.conf'),
 os.path.join('~', '.dotez.conf'),
 os.path.join(PACKAGE_DIR, 'example.conf')]
DEFAULT_CONFIG = {'includes':[
  '.bashrc',
  '.profile'], 
 'ignores':[
  '*.tmp'], 
 'dotez_data_dir':'~/dotez/'}
logging.basicConfig(stream=(sys.stdout), level=(logging.INFO))
logger = logging.getLogger('dotez')