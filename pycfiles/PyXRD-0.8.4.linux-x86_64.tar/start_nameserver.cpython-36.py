# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/start_nameserver.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 528 bytes
if __name__ == '__main__':
    import os, sys
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from pyxrd.logs import setup_logging
    from pyxrd.server import settings
    setup_logging(basic=True, prefix='PYRO NAMESERVER:')
    import Pyro4.naming
    Pyro4.naming.startNSloop()