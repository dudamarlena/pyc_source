# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/settings.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 556 bytes
import Pyro4
Pyro4.config.SERIALIZERS_ACCEPTED = ['json', 'marshal', 'serpent', 'pickle']
Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.PICKLE_PROTOCOL_VERSION = 3
Pyro4.config.COMPRESSION = True
Pyro4.config.SERVERTYPE = 'multiplex'
Pyro4.config.COMMTIMEOUT = 3.5
Pyro4.config.REQUIRE_EXPOSE = False
Pyro4.config.SOCK_REUSE = True
import platform
if platform.system() == 'Windows':
    if float(platform.release()) >= 6:
        USE_MSG_WAITALL = True
PYRO_NAME = 'pyxrd.server'
KEEP_SERVER_ALIVE = False