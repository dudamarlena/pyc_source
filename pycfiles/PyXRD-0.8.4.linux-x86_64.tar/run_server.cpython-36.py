# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/run_server.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1411 bytes
if __name__ == '__main__':
    import logging
    logger = logging.getLogger(__name__)
    import os, sys
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from pyxrd.data.appdirs import user_log_dir
    from pyxrd.server import settings
    from pyxrd.server.pyxrd_server import PyXRDServer
    from pyxrd.server.utils import start_script
    from pyxrd.logs import setup_logging
    setup_logging(basic=True, prefix='PYRO SERVER:')
    import Pyro4
    try:
        from Pyro4.naming import NamingError
    except (AttributeError, ImportError):
        from Pyro4.errors import NamingError

    server = PyXRDServer()
    daemon = Pyro4.Daemon()
    try:
        ns = Pyro4.locateNS()
    except NamingError:
        logger.info('NamingError encountered when trying to locate the nameserver')
        log_file = os.path.join(user_log_dir('PyXRD'), 'nameserver.log')
        start_script('start_nameserver.py', auto_kill=(not settings.KEEP_SERVER_ALIVE), log_file=log_file)
        ns = Pyro4.locateNS()

    server_uri = daemon.register(server)
    ns.register(settings.PYRO_NAME, server_uri)
    try:
        daemon.requestLoop(server.loopCondition)
    finally:
        daemon.shutdown()