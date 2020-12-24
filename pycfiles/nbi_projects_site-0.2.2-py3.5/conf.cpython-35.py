# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nbi/conf.py
# Compiled at: 2019-12-19 09:45:12
# Size of source mod 2**32: 134 bytes
import os
from projects.conf import config
config.read(os.path.abspath(os.path.join('nbi-projects-site', 'res', 'config.ini')))