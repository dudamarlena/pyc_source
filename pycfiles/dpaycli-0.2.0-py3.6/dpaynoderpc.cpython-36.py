# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycliapi/dpaynoderpc.py
# Compiled at: 2018-10-15 03:13:49
# Size of source mod 2**32: 8726 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes, int, str
import re, sys
from .graphenerpc import GrapheneRPC
from . import exceptions
import logging
log = logging.getLogger(__name__)

class DPayNodeRPC(GrapheneRPC):
    __doc__ = ' This class allows to call API methods exposed by the witness node via\n        websockets / rpc-json.\n\n        :param str urls: Either a single Websocket/Http URL, or a list of URLs\n        :param str user: Username for Authentication\n        :param str password: Password for Authentication\n        :param int num_retries: Try x times to num_retries to a node on disconnect, -1 for indefinitely\n        :param int num_retries_call: Repeat num_retries_call times a rpc call on node error (default is 5)\n        :param int timeout: Timeout setting for https nodes (default is 60)\n        :param bool use_condenser: Use the old condenser_api rpc protocol on nodes with version\n            0.19.4 or higher. The settings has no effect on nodes with version of 0.19.3 or lower.\n\n    '

    def __init__(self, *args, **kwargs):
        (super(DPayNodeRPC, self).__init__)(*args, **kwargs)
        self.next_node_on_empty_reply = False

    def set_next_node_on_empty_reply(self, next_node_on_empty_reply=True):
        """Switch to next node on empty reply for the next rpc call"""
        self.next_node_on_empty_reply = next_node_on_empty_reply

    def rpcexec(self, payload):
        if self.url is None:
            raise exceptions.RPCConnection('RPC is not connected!')
        doRetry = True
        maxRetryCountReached = False
        while doRetry and not maxRetryCountReached:
            doRetry = False
            try:
                reply = super(DPayNodeRPC, self).rpcexec(payload)
                if self.next_node_on_empty_reply:
                    if not bool(reply):
                        if self.nodes.working_nodes_count > 1:
                            self._retry_on_next_node('Empty Reply')
                            doRetry = True
                            self.next_node_on_empty_reply = True
                else:
                    self.next_node_on_empty_reply = False
                    return reply
            except exceptions.RPCErrorDoRetry as e:
                msg = exceptions.decodeRPCErrorMsg(e).strip()
                try:
                    self.nodes.sleep_and_check_retries((str(msg)), call_retry=True)
                    doRetry = True
                except exceptions.CallRetriesReached:
                    if self.nodes.working_nodes_count > 1:
                        self._retry_on_next_node(msg)
                        doRetry = True
                    else:
                        self.next_node_on_empty_reply = False
                        raise exceptions.CallRetriesReached

            except exceptions.RPCError as e:
                try:
                    doRetry = self._check_error_message(e, self.error_cnt_call)
                except exceptions.CallRetriesReached:
                    msg = exceptions.decodeRPCErrorMsg(e).strip()
                    if self.nodes.working_nodes_count > 1:
                        self._retry_on_next_node(msg)
                        doRetry = True
                    else:
                        self.next_node_on_empty_reply = False
                        raise exceptions.CallRetriesReached

            except Exception as e:
                self.next_node_on_empty_reply = False
                raise e

            maxRetryCountReached = self.nodes.num_retries_call_reached

        self.next_node_on_empty_reply = False

    def _retry_on_next_node(self, error_msg):
        self.nodes.increase_error_cnt()
        self.nodes.sleep_and_check_retries(error_msg, sleep=False, call_retry=False)
        self.next()

    def _check_error_message(self, e, cnt):
        """Check error message and decide what to do"""
        doRetry = False
        msg = exceptions.decodeRPCErrorMsg(e).strip()
        if re.search('missing required active authority', msg):
            raise exceptions.MissingRequiredActiveAuthority
        else:
            if re.search('missing required active authority', msg):
                raise exceptions.MissingRequiredActiveAuthority
            else:
                if re.match('^no method with name.*', msg):
                    raise exceptions.NoMethodWithName(msg)
                else:
                    if re.search('Could not find method', msg):
                        raise exceptions.NoMethodWithName(msg)
                    else:
                        if re.search('Could not find API', msg):
                            if self._check_api_name(msg):
                                raise exceptions.ApiNotSupported(msg)
                            else:
                                raise exceptions.NoApiWithName(msg)
                        else:
                            if re.search('irrelevant signature included', msg):
                                raise exceptions.UnnecessarySignatureDetected(msg)
                            else:
                                if re.search('WinError', msg):
                                    raise exceptions.RPCError(msg)
                                else:
                                    if re.search('Unable to acquire database lock', msg):
                                        self.nodes.sleep_and_check_retries((str(msg)), call_retry=True)
                                        doRetry = True
                                    else:
                                        if re.search('Request Timeout', msg):
                                            self.nodes.sleep_and_check_retries((str(msg)), call_retry=True)
                                            doRetry = True
                                        else:
                                            if re.search('Bad or missing upstream response', msg):
                                                self.nodes.sleep_and_check_retries((str(msg)), call_retry=True)
                                                doRetry = True
                                            else:
                                                if re.search('Internal Error', msg) or re.search('Unknown exception', msg):
                                                    self.nodes.sleep_and_check_retries((str(msg)), call_retry=True)
                                                    doRetry = True
                                                else:
                                                    if re.search('!check_max_block_age', str(e)):
                                                        self._switch_to_next_node(str(e))
                                                        doRetry = True
                                                    else:
                                                        if re.search('out_of_rangeEEEE: unknown key', msg) or re.search('unknown key:unknown key', msg):
                                                            raise exceptions.UnkownKey(msg)
                                                        else:
                                                            if re.search('Assert Exception:v.is_object(): Input data have to treated as object', msg):
                                                                raise exceptions.UnhandledRPCError('Use Operation(op, appbase=True) to prevent error: ' + msg)
                                                            else:
                                                                if msg:
                                                                    raise exceptions.UnhandledRPCError(msg)
                                                                else:
                                                                    raise e
        return doRetry

    def _switch_to_next_node(self, msg, error_type='UnhandledRPCError'):
        if self.nodes.working_nodes_count == 1:
            if error_type == 'UnhandledRPCError':
                raise exceptions.UnhandledRPCError(msg)
            elif error_type == 'ApiNotSupported':
                raise exceptions.ApiNotSupported(msg)
        self.nodes.increase_error_cnt()
        self.nodes.sleep_and_check_retries((str(msg)), sleep=False)
        self.next()

    def _check_api_name(self, msg):
        error_start = 'Could not find API'
        known_apis = ['account_history_api', 'tags_api',
         'database_api', 'market_history_api',
         'block_api', 'account_by_key_api', 'chain_api',
         'follow_api', 'condenser_api', 'debug_node_api',
         'witness_api', 'test_api',
         'network_broadcast_api']
        for api in known_apis:
            if re.search(error_start + ' ' + api, msg):
                return True

        if msg[-18:] == error_start:
            return True
        else:
            return False

    def get_account(self, name, **kwargs):
        """ Get full account details from account name

            :param str name: Account name
        """
        if isinstance(name, str):
            return (self.get_accounts)([name], **kwargs)