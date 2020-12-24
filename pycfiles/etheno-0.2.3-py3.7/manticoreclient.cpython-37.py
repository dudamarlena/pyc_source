# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/manticoreclient.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 7805 bytes
import logging, time, builtins, sys
from . import manticorelogger
oldimport = builtins.__import__

def manticoreimport(name, *args, **kwargs):
    if name == 'manticore.utils.log':
        manticorelogger.__name__ = 'manticore.utils.log'
        sys.modules[name] = manticorelogger
        return manticorelogger
    return oldimport(name, *args, **kwargs)


builtins.__import__ = manticoreimport
try:
    import manticore.utils.log, manticore.utils
finally:
    builtins.__import__ = oldimport

manticore.utils.log = manticorelogger
from manticore.ethereum import ManticoreEVM
from manticore.exceptions import NoAliveStates
import manticore
from . import logger
from . import threadwrapper
from .client import EthenoClient, jsonrpc, DATA, QUANTITY
from .etheno import _CONTROLLER
from .manticoreutils import manticore_is_new_enough

def encode_hex(data):
    if data is None:
        return
    if isinstance(data, int) or isinstance(data, long):
        encoded = hex(data)
        if encoded[(-1)] == 'L':
            encoded = encoded[:-1]
        return encoded
    return '0x%s' % data.encode('hex')


class ManticoreClient(EthenoClient):

    def __init__(self, manticore=None):
        self._assigned_manticore = manticore
        self._manticore = None
        self.contracts = []
        self.short_name = 'Manticore'
        self._accounts_to_create = []

    @property
    def manticore(self):
        if self._manticore is None:
            if self._assigned_manticore is None:
                if self.log_directory is None:
                    workspace = None
                else:
                    workspace = self.log_directory
                self._assigned_manticore = ManticoreEVM(workspace_url=workspace)
            self._manticore = threadwrapper.MainThreadWrapper(self._assigned_manticore, _CONTROLLER)
            self._finalize_manticore()
        return self._manticore

    def _finalize_manticore(self):
        if not self._manticore:
            return
        for balance, address in self._accounts_to_create:
            self._manticore.create_account(balance=balance, address=address)

        self._accounts_to_create = []
        self.reassign_manticore_loggers()
        self.logger.cleanup_empty = True

    def create_account(self, balance, address):
        self._accounts_to_create.append((balance, address))
        self._finalize_manticore()

    def reassign_manticore_loggers(self):
        manticore.utils.log.ETHENO_LOGGER = self.logger
        manticore_loggers = (name for name in logging.root.manager.loggerDict if name.startswith('manticore'))
        logger_parents = {}
        for name in sorted(manticore_loggers):
            sep = name.rfind('.')
            if sep > 0:
                path = name[:sep]
                parent = logger_parents[path]
                displayname = name[len(path) + 1:]
            else:
                parent = self.logger
                displayname = name
            m_logger = logger.EthenoLogger(name, parent=parent, cleanup_empty=True, displayname=displayname)
            m_logger.propagate = False
            logger_parents[name] = m_logger

    @jsonrpc(from_addr=QUANTITY, to=QUANTITY, gas=QUANTITY, gasPrice=QUANTITY, value=QUANTITY, data=DATA, nonce=QUANTITY, RETURN=DATA)
    def eth_sendTransaction(self, from_addr, to=None, gas=90000, gasPrice=None, value=0, data=None, nonce=None, rpc_client_result=None):
        if to is None or to == 0:
            if rpc_client_result is not None:
                tx_hash = rpc_client_result['result']
                while True:
                    receipt = self.etheno.master_client.post({'id':'%s_receipt' % rpc_client_result['id'], 
                     'method':'eth_getTransactionReceipt', 
                     'params':[
                      tx_hash]})
                    if 'result' in receipt:
                        if receipt['result']:
                            address = int(receipt['result']['contractAddress'], 16)
                            break
                    time.sleep(1.0)

            else:
                address = None
            contract_address = self.manticore.create_contract(owner=from_addr, balance=value, init=data)
            self.contracts.append(contract_address)
            self.logger.info(f"Manticore contract created: {encode_hex(contract_address.address)}")
        else:
            self.manticore.transaction(address=to, data=data, caller=from_addr, value=value)
        return rpc_client_result

    @jsonrpc(TX_HASH=QUANTITY)
    def eth_getTransactionReceipt(self, tx_hash, rpc_client_result=None):
        return rpc_client_result

    def multi_tx_analysis(self, contract_address=None, tx_limit=None, tx_use_coverage=True, args=None):
        if contract_address is None:
            for contract_address in self.contracts:
                self.multi_tx_analysis(contract_address=contract_address,
                  tx_limit=tx_limit,
                  tx_use_coverage=tx_use_coverage,
                  args=args)

            return
        else:
            tx_account = self.etheno.accounts
            current_coverage = 0
            tx_no = 0
            if manticore_is_new_enough(0, 3, 0):
                shutdown_test = 'is_killed'
            else:
                shutdown_test = 'is_shutdown'
        while not current_coverage < 100:
            if not (tx_use_coverage or getattr(self.manticore, shutdown_test)()):
                try:
                    self.logger.info('Starting symbolic transaction: %d' % tx_no)
                    symbolic_data = self.manticore.make_symbolic_buffer(320)
                    symbolic_value = self.manticore.make_symbolic_value()
                    self.manticore.transaction(caller=(tx_account[min(tx_no, len(tx_account) - 1)]), address=contract_address,
                      data=symbolic_data,
                      value=symbolic_value)
                    if manticore_is_new_enough(0, 3, 0):
                        pass
                    else:
                        self.logger.info('%d alive states, %d terminated states' % (self.manticore.count_running_states(), self.manticore.count_terminated_states()))
                except NoAliveStates:
                    break

                if tx_limit is not None:
                    if tx_no + 1 >= tx_limit:
                        break
                if tx_use_coverage:
                    prev_coverage = current_coverage
                    current_coverage = self.manticore.global_coverage(contract_address)
                    found_new_coverage = prev_coverage < current_coverage
                    if not found_new_coverage:
                        break
                tx_no += 1