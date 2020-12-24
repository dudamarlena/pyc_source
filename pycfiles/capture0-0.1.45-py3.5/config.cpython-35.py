# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/capture0/config.py
# Compiled at: 2016-09-23 17:28:44
# Size of source mod 2**32: 257 bytes
import os, pkg_resources
THIS_DIR, _ = os.path.split(os.path.abspath(os.path.expanduser(__file__)))
CONFIG = {'STATIC': pkg_resources.resource_filename('capture0', 'static'), 
 'SAVE_DIR': os.path.join(os.path.expanduser('~'), 'capture0')}