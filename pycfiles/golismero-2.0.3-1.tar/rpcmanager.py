# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/rpcmanager.py
# Compiled at: 2013-11-08 09:23:49
"""
Manager of RPC calls from plugins.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'RPCManager']
from ..common import pickle
from ..messaging.codes import MessageCode, MSG_RPC_CODES
from functools import partial
from threading import Thread
import sys, traceback
rpcMap = {}

def implementor(rpc_code, blocking=False):
    """
    RPC implementation function.
    """
    return partial(_add_implementor, rpc_code, blocking)


def _add_implementor(rpc_code, blocking, fn):
    if type(rpc_code) is not int:
        raise TypeError('Expected int, got %r instead' % type(rpc_code))
    if type(blocking) is not bool:
        raise TypeError('Expected bool, got %r instead' % type(blocking))
    if not callable(fn):
        raise TypeError('Expected callable, got %r instead' % type(fn))
    if rpc_code in rpcMap:
        try:
            msg = 'Duplicated RPC implementors for code %d: %s and %s'
            msg %= (rpc_code, rpcMap[rpc_code][0].__name__, fn.__name__)
        except Exception:
            msg = 'Duplicated RPC implementors for code: %d' % rpc_code

        raise SyntaxError(msg)
    rpcMap[rpc_code] = (
     fn, blocking)
    return fn


@implementor(MessageCode.MSG_RPC_BULK)
def rpc_bulk(orchestrator, audit_name, rpc_code, *arguments):
    try:
        method, blocking = rpcMap[rpc_code]
    except KeyError:
        raise NotImplementedError('RPC code not implemented: %r' % rpc_code)

    if blocking:
        raise NotImplementedError('Cannot run blocking RPC calls in bulk. Code: %r' % rpc_code)
    caller = partial(method, orchestrator, audit_name)
    return map(caller, *arguments)


class RPCManager(object):
    """
    Executes remote procedure calls from plugins.
    """

    def __init__(self, orchestrator):
        """
        :param orchestrator: Orchestrator instance.
        :type orchestrator: Orchestrator
        """
        self.__orchestrator = orchestrator
        self.__rpcMap = rpcMap
        missing = MSG_RPC_CODES.difference(self.__rpcMap.keys())
        if missing:
            msg = 'Missing RPC implementors for codes: %s'
            msg %= (', ').join(str(x) for x in sorted(missing))
            raise SyntaxError(msg)

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    def execute_rpc(self, audit_name, rpc_code, response_queue, args, kwargs):
        """
        Honor a remote procedure call request from a plugin.

        :param audit_name: Name of the audit requesting the call.
        :type audit_name: str

        :param rpc_code: RPC code.
        :type rpc_code: int

        :param response_queue: Response queue.
        :type response_queue: Queue

        :param args: Positional arguments to the call.
        :type args: tuple

        :param kwargs: Keyword arguments to the call.
        :type kwargs: dict
        """
        try:
            try:
                target, blocking = self.__rpcMap[rpc_code]
            except KeyError:
                raise NotImplementedError('RPC code not implemented: %r' % rpc_code)

            if blocking:
                thread = Thread(target=self.execute_rpc_implementor, args=(
                 audit_name, target, response_queue, args, kwargs))
                thread.daemon = True
                thread.start()
            else:
                self.execute_rpc_implementor(audit_name, target, response_queue, args, kwargs)
        except Exception:
            if response_queue:
                error = self.prepare_exception(*sys.exc_info())
                try:
                    response_queue.put_nowait((False, error))
                except IOError:
                    pass

    def execute_rpc_implementor(self, audit_name, target, response_queue, args, kwargs):
        """
        Honor a remote procedure call request from a plugin.

        :param audit_name: Name of the audit requesting the call.
        :type audit_name: str

        :param target: RPC implementor function.
        :type target: callable

        :param response_queue: Response queue.
        :type response_queue: Queue

        :param args: Positional arguments to the call.
        :type args: tuple

        :param kwargs: Keyword arguments to the call.
        :type kwargs: dict
        """
        success = True
        try:
            response = target(self.orchestrator, audit_name, *args, **kwargs)
        except Exception:
            if response_queue:
                success = False
                response = self.prepare_exception(*sys.exc_info())

        if response_queue:
            response_queue.put_nowait((success, response))

    @staticmethod
    def prepare_exception(exc_type, exc_value, exc_traceback):
        """
        Prepare an exception for sending back to the plugins.

        :param exc_type: Exception type.
        :type exc_type: class

        :param exc_value: Exception value.
        :type exc_value:

        :returns: Exception type, exception value
            and formatted traceback. The exception value may be formatted too
            and the exception type replaced by Exception if it's not possible
            to serialize it for sending.
        :rtype: tuple(class, object, str)
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        try:
            pickle.dumps(exc_value, -1)
        except Exception:
            exc_value = traceback.format_exception_only(exc_type, exc_value)

        try:
            pickle.dumps(exc_type, -1)
        except Exception:
            exc_type = Exception

        exc_traceback = traceback.extract_tb(exc_traceback)
        return (exc_type, exc_value, exc_traceback)