# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/kill_server.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 519 bytes
import logging
logger = logging.getLogger(__name__)
from traceback import print_exc
from . import settings
import Pyro4
if __name__ == '__main__':
    try:
        server = Pyro4.Proxy('PYRONAME:%s' % settings.PYRO_NAME)
        server.shutdown()
    except:
        logging.error('Error when trying to shut down Pyro server!')
        print_exc()