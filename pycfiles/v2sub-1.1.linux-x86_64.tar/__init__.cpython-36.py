# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/v2sub/__init__.py
# Compiled at: 2019-11-04 00:19:40
# Size of source mod 2**32: 338 bytes
import os
__version__ = '1.1'
user = os.getenv('SUDO_USER') or os.getenv('USER')
BASE_PATH = os.path.join(os.path.expanduser('~%s' % user), '.v2sub')
SUBSCRIBE_CONFIG = os.path.join(BASE_PATH, 'subscribes.json')
SERVER_CONFIG = os.path.join(BASE_PATH, 'servers.json')
DEFAULT_SUBSCRIBE = 'default'