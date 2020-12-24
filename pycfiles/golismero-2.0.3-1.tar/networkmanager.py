# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/networkmanager.py
# Compiled at: 2013-11-08 09:23:49
"""
Manager for network connections.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'NetworkManager']
from .rpcmanager import implementor
from ..common import random
from ..messaging.codes import MessageCode
from collections import defaultdict
from threading import BoundedSemaphore, RLock

@implementor(MessageCode.MSG_RPC_REQUEST_SLOT, blocking=True)
def rpc_netdb_request_slot(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.netManager.request_slot(audit_name, *args, **kwargs)


@implementor(MessageCode.MSG_RPC_RELEASE_SLOT)
def rpc_netdb_release_slot(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.netManager.release_slot(audit_name, *args, **kwargs)


class NetworkManager(object):
    """
    Manager for network connections.
    """

    def __init__(self, config):
        """
        :param config: Global configuration object.
        :type config: OrchestratorConfig
        """
        self.__config = config
        self.__rlock = RLock()
        self.__counts = defaultdict(int)
        self.__semaphores = defaultdict(self.__create_semaphore)
        self.__tokens = defaultdict(dict)

    @property
    def max_connections(self):
        """
        :returns: Maximum allowed number of connection slots per host.
        :rtype: int
        """
        return self.__config.max_connections

    def __create_semaphore(self):
        return BoundedSemaphore(self.max_connections)

    def request_slot(self, audit_name, host, number=1):
        """
        Request the given number of connection slots for a host.
        Blocks until the requested slots become available.

        .. warning: Currently requesting more than one slot is not supported.
            There's a good reason for this, so don't try calling this method
            multiple times to work around the limitation!

        :param audit_name: Audit name.
        :type audit_name: str

        :param host: Host to connect to.
        :type host: str

        :param number: Number of connection slots to request.
        :type number: int

        :returns: Request token.
        :rtype: str
        """
        if number != 1:
            raise NotImplementedError()
        token = None
        host = host.lower()
        with self.__rlock:
            sem = self.__semaphores[host]
            self.__tokens[audit_name]
        sem.acquire()
        try:
            with self.__rlock:
                if audit_name not in self.__tokens:
                    raise RuntimeError('Audit is shutting down')
                token = '%.8X|%s' % (random.randint(0, 2147483647), host)
                self.__tokens[audit_name][token] = (host, number)
                self.__counts[host] += 1
                return token
        except:
            try:
                if token is not None:
                    with self.__rlock:
                        del self.__tokens[audit_name][token]
            finally:
                sem.release()

            raise

        return

    def release_slot(self, audit_name, token):
        """
        Release a previously requested number of connection slots for a host.

        This method doesn't raise any exceptions.

        :param audit_name: Audit name.
        :type audit_name: str

        :param token: Request token.
        :type token: str
        """
        try:
            with self.__rlock:
                host, number = self.__tokens[audit_name].pop(token)
                sem = self.__semaphores[host]
                try:
                    self.__counts[host] -= number
                    if self.__counts[host] <= 0:
                        del self.__counts[host]
                        del self.__semaphores[host]
                finally:
                    sem.release()

        except Exception:
            pass

    def release_all_slots(self, audit_name):
        """
        Release all connection slots for the given audit.

        :param audit_name: Audit name.
        :type audit_name: str
        """
        with self.__rlock:
            for host, number in self.__tokens.pop(audit_name, {}).itervalues():
                try:
                    sem = self.__semaphores[host]
                    try:
                        self.__counts[host] -= number
                        if self.__counts[host] <= 0:
                            del self.__counts[host]
                            del self.__semaphores[host]
                    finally:
                        sem.release()

                except:
                    pass