# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/srv.py
# Compiled at: 2020-05-10 16:11:48
# Size of source mod 2**32: 3054 bytes
__doc__ = '\naehostd.srv - main service module\n'
import logging, os
from .__about__ import __version__
from .cfg import CFG
from .service import NSSPAMServer, init_service
from . import monitor
from . import refresh
from . import pam
from .refresh import UsersUpdater, NetworkAddrUpdater
LOG_NAME = 'aehostd.srv'
DESCRIPTION = 'NSS/PAM service for AE-DIR'

def main():
    """
    entry point for demon running as non-privileged user
    """
    script_name, ctx = init_service(LOG_NAME, DESCRIPTION)
    with ctx:
        try:
            try:
                logging.debug('Initializing %s instance listening on %r', NSSPAMServer.__name__, CFG.socketpath)
                server = NSSPAMServer(CFG.socketpath)
                logging.debug('Start refresh thread')
                refresh.USERSUPDATER_TASK = UsersUpdater(CFG.refresh_sleep)
                spawned_threads = [refresh.USERSUPDATER_TASK]
                if CFG.netaddr_refresh > 0 and CFG.netaddr_level > 0:
                    netaddr_refresh_task = NetworkAddrUpdater(CFG.netaddr_refresh)
                    spawned_threads.append(netaddr_refresh_task)
                else:
                    netaddr_refresh_task = None
                if CFG.pam_authc_cache_ttl > 0:
                    spawned_threads.append(pam.AuthcCachePurgeThread(CFG.pam_authc_cache_ttl))
                if CFG.monitor > 0:
                    spawned_threads.append(monitor.Monitor(CFG.monitor, server, refresh.USERSUPDATER_TASK, netaddr_refresh_task))
                for thr in spawned_threads:
                    logging.debug('Starting %s', thr.__class__.__name__)
                    thr.enabled = True
                    thr.start()

                logging.info('%s instance is listening on %r, start serving requests', server.__class__.__name__, server.server_address)
                server.serve_forever()
            except (KeyboardInterrupt, SystemExit) as exit_exc:
                try:
                    logging.debug('Exit exception received: %r', exit_exc)
                    for thr in spawned_threads:
                        logging.debug('Disabled %s', thr.__class__.__name__)
                        thr.enabled = False

                finally:
                    exit_exc = None
                    del exit_exc

        finally:
            logging.debug('Removing socket path %r', CFG.socketpath)
            try:
                os.remove(CFG.socketpath)
            except OSError as os_error:
                try:
                    logging.debug('Error removing socket path %r: %s', CFG.socketpath, os_error)
                finally:
                    os_error = None
                    del os_error

        logging.info('Stopped %s %s', script_name, __version__)


if __name__ == '__main__':
    main()