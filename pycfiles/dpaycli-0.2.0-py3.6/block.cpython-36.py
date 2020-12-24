# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpaycli/block.py
# Compiled at: 2018-10-15 03:13:49
# Size of source mod 2**32: 14067 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime, timedelta, date
import json
from .exceptions import BlockDoesNotExistsException
from .utils import parse_time, formatTimeString
from .blockchainobject import BlockchainObject
from dpaycliapi.exceptions import ApiNotSupported
from dpaycligraphenebase.py23 import bytes_types, integer_types, string_types, text_type

class Block(BlockchainObject):
    __doc__ = ' Read a single block from the chain\n\n        :param int block: block number\n        :param dpaycli.dpay.DPay dpay_instance: DPay\n            instance\n        :param bool lazy: Use lazy loading\n        :param bool only_ops: Includes only operations, when set to True (default: False)\n        :param bool only_virtual_ops: Includes only virtual operations (default: False)\n\n        Instances of this class are dictionaries that come with additional\n        methods (see below) that allow dealing with a block and its\n        corresponding functions.\n\n        When only_virtual_ops is set to True, only_ops is always set to True.\n\n        In addition to the block data, the block number is stored as self["id"] or self.identifier.\n\n        .. code-block:: python\n\n            >>> from dpaycli.block import Block\n            >>> block = Block(1)\n            >>> print(block)\n            <Block 1>\n\n        .. note:: This class comes with its own caching function to reduce the\n                  load on the API server. Instances of this class can be\n                  refreshed with ``Account.refresh()``.\n\n    '

    def __init__(self, block, only_ops=False, only_virtual_ops=False, full=True, lazy=False, dpay_instance=None):
        """ Initilize a block

            :param int block: block number
            :param dpaycli.dpay.DPay dpay_instance: DPay
                instance
            :param bool lazy: Use lazy loading
            :param bool only_ops: Includes only operations, when set to True (default: False)
            :param bool only_virtual_ops: Includes only virtual operations (default: False)

        """
        self.full = full
        self.lazy = lazy
        self.only_ops = only_ops
        self.only_virtual_ops = only_virtual_ops
        if isinstance(block, float):
            block = int(block)
        else:
            if isinstance(block, dict):
                block = self._parse_json_data(block)
        super(Block, self).__init__(block,
          lazy=lazy,
          full=full,
          dpay_instance=dpay_instance)

    def _parse_json_data(self, block):
        parse_times = [
         'timestamp']
        for p in parse_times:
            if p in block and isinstance(block.get(p), string_types):
                block[p] = formatTimeString(block.get(p, '1970-01-01T00:00:00'))

        if 'transactions' in block:
            for i in range(len(block['transactions'])):
                if 'expiration' in block['transactions'][i] and isinstance(block['transactions'][i]['expiration'], string_types):
                    block['transactions'][i]['expiration'] = formatTimeString(block['transactions'][i]['expiration'])

        else:
            if 'operations' in block:
                for i in range(len(block['operations'])):
                    if 'timestamp' in block['operations'][i] and isinstance(block['operations'][i]['timestamp'], string_types):
                        block['operations'][i]['timestamp'] = formatTimeString(block['operations'][i]['timestamp'])

        return block

    def json(self):
        output = self.copy()
        parse_times = [
         'timestamp']
        for p in parse_times:
            if p in output:
                p_date = output.get(p, datetime(1970, 1, 1, 0, 0))
                if isinstance(p_date, (datetime, date)):
                    output[p] = formatTimeString(p_date)
                else:
                    output[p] = p_date

        if 'transactions' in output:
            for i in range(len(output['transactions'])):
                if 'expiration' in output['transactions'][i] and isinstance(output['transactions'][i]['expiration'], (datetime, date)):
                    output['transactions'][i]['expiration'] = formatTimeString(output['transactions'][i]['expiration'])

        else:
            if 'operations' in output:
                for i in range(len(output['operations'])):
                    if 'timestamp' in output['operations'][i] and isinstance(output['operations'][i]['timestamp'], (datetime, date)):
                        output['operations'][i]['timestamp'] = formatTimeString(output['operations'][i]['timestamp'])

        ret = json.loads(str(json.dumps(output)))
        output = self._parse_json_data(output)
        return ret

    def refresh(self):
        if self.identifier is None:
            return
        if not self.dpay.is_connected():
            return
        self.dpay.rpc.set_next_node_on_empty_reply(False)
        if self.only_ops or self.only_virtual_ops:
            if self.dpay.rpc.get_use_appbase():
                try:
                    ops = self.dpay.rpc.get_ops_in_block({'block_num':self.identifier,  'only_virtual':self.only_virtual_ops}, api='account_history')['ops']
                except ApiNotSupported:
                    ops = self.dpay.rpc.get_ops_in_block((self.identifier), (self.only_virtual_ops), api='condenser')

            else:
                ops = self.dpay.rpc.get_ops_in_block(self.identifier, self.only_virtual_ops)
            if bool(ops):
                block = {'block':ops[0]['block'], 
                 'timestamp':ops[0]['timestamp'], 
                 'operations':ops}
            else:
                block = {}
        else:
            if self.dpay.rpc.get_use_appbase():
                try:
                    block = self.dpay.rpc.get_block({'block_num': self.identifier}, api='block')
                    if block:
                        if 'block' in block:
                            block = block['block']
                except ApiNotSupported:
                    block = self.dpay.rpc.get_block((self.identifier), api='condenser')

            else:
                block = self.dpay.rpc.get_block(self.identifier)
            if not block:
                raise BlockDoesNotExistsException('output: %s of identifier %s' % (str(block), str(self.identifier)))
            block = self._parse_json_data(block)
            super(Block, self).__init__(block, lazy=(self.lazy), full=(self.full), dpay_instance=(self.dpay))

    @property
    def block_num(self):
        """Returns the block number"""
        if 'block_id' in self:
            return int((self['block_id'][:8]), base=16)
        else:
            return

    def time(self):
        """Return a datetime instance for the timestamp of this block"""
        return self['timestamp']

    @property
    def transactions(self):
        """ Returns all transactions as list"""
        if self.only_ops or self.only_virtual_ops:
            return list()
        else:
            trxs = []
            if 'transactions' not in self:
                return []
            trx_id = 0
            for trx in self['transactions']:
                trx_new = {'transaction_id': self['transaction_ids'][trx_id]}
                trx_new.update(trx.copy())
                trx_new.update({'block_num':self.block_num,  'transaction_num':trx_id})
                trxs.append(trx_new)
                trx_id += 1

            return trxs

    @property
    def operations(self):
        """Returns all block operations as list"""
        if self.only_ops or self.only_virtual_ops:
            return self['operations']
        else:
            ops = []
            trxs = []
            if 'transactions' in self:
                trxs = self['transactions']
            for tx in trxs:
                if 'operations' not in tx:
                    pass
                else:
                    for op in tx['operations']:
                        if isinstance(op, list):
                            ops.append(list(op))
                        else:
                            ops.append(op.copy())

            return ops

    @property
    def json_transactions(self):
        """ Returns all transactions as list, all dates are strings."""
        if self.only_ops or self.only_virtual_ops:
            return list()
        else:
            trxs = []
            if 'transactions' not in self:
                return []
            trx_id = 0
            for trx in self['transactions']:
                trx_new = {'transaction_id': self['transaction_ids'][trx_id]}
                trx_new.update(trx.copy())
                trx_new.update({'block_num':self.block_num,  'transaction_num':trx_id})
                if 'expiration' in trx:
                    p_date = trx.get('expiration', datetime(1970, 1, 1, 0, 0))
                    if isinstance(p_date, (datetime, date)):
                        trx_new.update({'expiration': formatTimeString(p_date)})
                trxs.append(trx_new)
                trx_id += 1

            return trxs

    @property
    def json_operations(self):
        """Returns all block operations as list, all dates are strings."""
        if self.only_ops or self.only_virtual_ops:
            return self['operations']
        else:
            ops = []
            for tx in self['transactions']:
                for op in tx['operations']:
                    if 'operations' not in tx:
                        pass
                    else:
                        if isinstance(op, list):
                            op_new = list(op)
                        else:
                            op_new = op.copy()
                        if 'timestamp' in op:
                            p_date = op.get('timestamp', datetime(1970, 1, 1, 0, 0))
                            if isinstance(p_date, (datetime, date)):
                                op_new.update({'timestamp': formatTimeString(p_date)})
                        ops.append(op_new)

            return ops

    def ops_statistics(self, add_to_ops_stat=None):
        """Returns a statistic with the occurrence of the different operation types"""
        if add_to_ops_stat is None:
            import dpayclibase.operationids
            ops_stat = dpayclibase.operationids.operations.copy()
            for key in ops_stat:
                ops_stat[key] = 0

        else:
            ops_stat = add_to_ops_stat.copy()
        for op in self.operations:
            if 'op' in op:
                op = op['op']
            if isinstance(op, dict) and 'type' in op:
                op_type = op['type']
                if len(op_type) > 10:
                    if op_type[len(op_type) - 10:] == '_operation':
                        op_type = op_type[:-10]
            else:
                op_type = op[0]
            ops_stat[op_type] += 1

        return ops_stat


class BlockHeader(BlockchainObject):
    __doc__ = ' Read a single block header from the chain\n\n        :param int block: block number\n        :param dpaycli.dpay.DPay dpay_instance: DPay\n            instance\n        :param bool lazy: Use lazy loading\n\n        In addition to the block data, the block number is stored as self["id"] or self.identifier.\n\n        .. code-block:: python\n\n            >>> from dpaycli.block import BlockHeader\n            >>> block = BlockHeader(1)\n            >>> print(block)\n            <BlockHeader 1>\n\n    '

    def __init__(self, block, full=True, lazy=False, dpay_instance=None):
        """ Initilize a block

            :param int block: block number
            :param dpaycli.dpay.DPay dpay_instance: DPay
                instance
            :param bool lazy: Use lazy loading

        """
        self.full = full
        self.lazy = lazy
        if isinstance(block, float):
            block = int(block)
        super(BlockHeader, self).__init__(block,
          lazy=lazy,
          full=full,
          dpay_instance=dpay_instance)

    def refresh(self):
        if not self.dpay.is_connected():
            return
        else:
            self.dpay.rpc.set_next_node_on_empty_reply(False)
            if self.dpay.rpc.get_use_appbase():
                block = self.dpay.rpc.get_block_header({'block_num': self.identifier}, api='block')
                if 'header' in block:
                    block = block['header']
            else:
                block = self.dpay.rpc.get_block_header(self.identifier)
            raise block or BlockDoesNotExistsException(str(self.identifier))
        block = self._parse_json_data(block)
        super(BlockHeader, self).__init__(block,
          lazy=(self.lazy), full=(self.full), dpay_instance=(self.dpay))

    def time(self):
        """ Return a datetime instance for the timestamp of this block
        """
        return self['timestamp']

    @property
    def block_num(self):
        """Returns the block number"""
        return self.identifier

    def _parse_json_data(self, block):
        parse_times = [
         'timestamp']
        for p in parse_times:
            if p in block and isinstance(block.get(p), string_types):
                block[p] = formatTimeString(block.get(p, '1970-01-01T00:00:00'))

        return block

    def json(self):
        output = self.copy()
        parse_times = [
         'timestamp']
        for p in parse_times:
            if p in output:
                p_date = output.get(p, datetime(1970, 1, 1, 0, 0))
                if isinstance(p_date, (datetime, date)):
                    output[p] = formatTimeString(p_date)
                else:
                    output[p] = p_date

        return json.loads(str(json.dumps(output)))