# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/module_testing/eth_module.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 27830 bytes
import pytest
from eth_abi import decode_single
from eth_utils import is_boolean, is_bytes, is_checksum_address, is_dict, is_integer, is_list_like, is_same_address, is_string
from hexbytes import HexBytes
from web3.exceptions import InvalidAddress
UNKNOWN_ADDRESS = '0xdeadbeef00000000000000000000000000000000'
UNKNOWN_HASH = '0xdeadbeef00000000000000000000000000000000000000000000000000000000'

class EthModuleTest:

    def test_eth_protocolVersion(self, web3):
        protocol_version = web3.version.ethereum
        if not is_string(protocol_version):
            raise AssertionError
        elif not protocol_version.isdigit():
            raise AssertionError

    def test_eth_syncing(self, web3):
        syncing = web3.eth.syncing
        if not is_boolean(syncing):
            if not is_dict(syncing):
                raise AssertionError
        if is_boolean(syncing):
            assert syncing is False
        else:
            assert is_dict(syncing) and 'startingBlock' in syncing
        if not 'currentBlock' in syncing:
            raise AssertionError
        else:
            if not 'highestBlock' in syncing:
                raise AssertionError
            elif not is_integer(syncing['startingBlock']):
                raise AssertionError
            assert is_integer(syncing['currentBlock'])
        assert is_integer(syncing['highestBlock'])

    def test_eth_coinbase(self, web3):
        coinbase = web3.eth.coinbase
        assert is_checksum_address(coinbase)

    def test_eth_mining(self, web3):
        mining = web3.eth.mining
        assert is_boolean(mining)

    def test_eth_hashrate(self, web3):
        hashrate = web3.eth.hashrate
        if not is_integer(hashrate):
            raise AssertionError
        elif not hashrate >= 0:
            raise AssertionError

    def test_eth_gasPrice(self, web3):
        gas_price = web3.eth.gasPrice
        if not is_integer(gas_price):
            raise AssertionError
        elif not gas_price > 0:
            raise AssertionError

    def test_eth_accounts(self, web3):
        accounts = web3.eth.accounts
        if not is_list_like(accounts):
            raise AssertionError
        else:
            if not len(accounts) != 0:
                raise AssertionError
            elif not all(is_checksum_address(account) for account in accounts):
                raise AssertionError
            assert web3.eth.coinbase in accounts

    def test_eth_blockNumber(self, web3):
        block_number = web3.eth.blockNumber
        if not is_integer(block_number):
            raise AssertionError
        elif not block_number >= 0:
            raise AssertionError

    def test_eth_getBalance(self, web3):
        coinbase = web3.eth.coinbase
        with pytest.raises(InvalidAddress):
            web3.eth.getBalance(coinbase.lower())
        balance = web3.eth.getBalance(coinbase)
        if not is_integer(balance):
            raise AssertionError
        elif not balance >= 0:
            raise AssertionError

    def test_eth_getStorageAt(self, web3):
        coinbase = web3.eth.coinbase
        with pytest.raises(InvalidAddress):
            web3.eth.getStorageAt(coinbase.lower(), 0)

    def test_eth_getTransactionCount(self, web3):
        coinbase = web3.eth.coinbase
        transaction_count = web3.eth.getTransactionCount(coinbase)
        with pytest.raises(InvalidAddress):
            web3.eth.getTransactionCount(coinbase.lower())
        if not is_integer(transaction_count):
            raise AssertionError
        elif not transaction_count >= 0:
            raise AssertionError

    def test_eth_getBlockTransactionCountByHash_empty_block(self, web3, empty_block):
        transaction_count = web3.eth.getBlockTransactionCount(empty_block['hash'])
        if not is_integer(transaction_count):
            raise AssertionError
        elif not transaction_count == 0:
            raise AssertionError

    def test_eth_getBlockTransactionCountByNumber_empty_block(self, web3, empty_block):
        transaction_count = web3.eth.getBlockTransactionCount(empty_block['number'])
        if not is_integer(transaction_count):
            raise AssertionError
        elif not transaction_count == 0:
            raise AssertionError

    def test_eth_getBlockTransactionCountByHash_block_with_txn(self, web3, block_with_txn):
        transaction_count = web3.eth.getBlockTransactionCount(block_with_txn['hash'])
        if not is_integer(transaction_count):
            raise AssertionError
        elif not transaction_count >= 1:
            raise AssertionError

    def test_eth_getBlockTransactionCountByNumber_block_with_txn(self, web3, block_with_txn):
        transaction_count = web3.eth.getBlockTransactionCount(block_with_txn['number'])
        if not is_integer(transaction_count):
            raise AssertionError
        elif not transaction_count >= 1:
            raise AssertionError

    def test_eth_getUncleCountByBlockHash(self, web3, empty_block):
        uncle_count = web3.eth.getUncleCount(empty_block['hash'])
        if not is_integer(uncle_count):
            raise AssertionError
        elif not uncle_count == 0:
            raise AssertionError

    def test_eth_getUncleCountByBlockNumber(self, web3, empty_block):
        uncle_count = web3.eth.getUncleCount(empty_block['number'])
        if not is_integer(uncle_count):
            raise AssertionError
        elif not uncle_count == 0:
            raise AssertionError

    def test_eth_getCode(self, web3, math_contract):
        code = web3.eth.getCode(math_contract.address)
        with pytest.raises(InvalidAddress):
            code = web3.eth.getCode(math_contract.address.lower())
        if not is_string(code):
            raise AssertionError
        elif not len(code) > 2:
            raise AssertionError

    def test_eth_sign(self, web3, unlocked_account):
        signature = web3.eth.sign(unlocked_account, text='Message tö sign. Longer than hash!')
        if not is_bytes(signature):
            raise AssertionError
        else:
            if not len(signature) == 65:
                raise AssertionError
            else:
                hexsign = web3.eth.sign(unlocked_account,
                  hexstr='0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821')
                assert hexsign == signature
                intsign = web3.eth.sign(unlocked_account, 587325666277427769629338178602988758445823328399241807555923126839773042036851304481)
                assert intsign == signature
                bytessign = web3.eth.sign(unlocked_account, b'Message t\xc3\xb6 sign. Longer than hash!')
                assert bytessign == signature
            new_signature = web3.eth.sign(unlocked_account, text='different message is different')
            assert new_signature != signature

    def test_eth_sendTransaction_addr_checksum_required(self, web3, unlocked_account):
        non_checksum_addr = unlocked_account.lower()
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        with pytest.raises(InvalidAddress):
            invalid_params = dict(txn_params, **{'from': non_checksum_addr})
            web3.eth.sendTransaction(invalid_params)
        with pytest.raises(InvalidAddress):
            invalid_params = dict(txn_params, **{'to': non_checksum_addr})
            web3.eth.sendTransaction(invalid_params)

    def test_eth_sendTransaction(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn = web3.eth.getTransaction(txn_hash)
        if not is_same_address(txn['from'], txn_params['from']):
            raise AssertionError
        else:
            if not is_same_address(txn['to'], txn_params['to']):
                raise AssertionError
            else:
                assert txn['value'] == 1
                assert txn['gas'] == 21000
            assert txn['gasPrice'] == txn_params['gasPrice']

    def test_eth_sendTransaction_with_nonce(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice * 2, 
         'nonce':web3.eth.getTransactionCount(unlocked_account)}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn = web3.eth.getTransaction(txn_hash)
        if not is_same_address(txn['from'], txn_params['from']):
            raise AssertionError
        else:
            if not is_same_address(txn['to'], txn_params['to']):
                raise AssertionError
            else:
                if not txn['value'] == 1:
                    raise AssertionError
                elif not txn['gas'] == 21000:
                    raise AssertionError
                assert txn['gasPrice'] == txn_params['gasPrice']
            assert txn['nonce'] == txn_params['nonce']

    def test_eth_replaceTransaction(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn_params['gasPrice'] = web3.eth.gasPrice * 2
        replace_txn_hash = web3.eth.replaceTransaction(txn_hash, txn_params)
        replace_txn = web3.eth.getTransaction(replace_txn_hash)
        if not is_same_address(replace_txn['from'], txn_params['from']):
            raise AssertionError
        else:
            if not is_same_address(replace_txn['to'], txn_params['to']):
                raise AssertionError
            else:
                assert replace_txn['value'] == 1
                assert replace_txn['gas'] == 21000
            assert replace_txn['gasPrice'] == txn_params['gasPrice']

    def test_eth_replaceTransaction_non_existing_transaction(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        with pytest.raises(ValueError):
            web3.eth.replaceTransaction('0x98e8cc09b311583c5079fa600f6c2a3bea8611af168c52e4b60b5b243a441997', txn_params)

    def test_eth_replaceTransaction_already_mined(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn_params['gasPrice'] = web3.eth.gasPrice * 2
        with pytest.raises(ValueError):
            web3.eth.replaceTransaction(txn_hash, txn_params)

    def test_eth_replaceTransaction_incorrect_nonce(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn = web3.eth.getTransaction(txn_hash)
        txn_params['gasPrice'] = web3.eth.gasPrice * 2
        txn_params['nonce'] = txn['nonce'] + 1
        with pytest.raises(ValueError):
            web3.eth.replaceTransaction(txn_hash, txn_params)

    def test_eth_replaceTransaction_gas_price_too_low(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':10}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn_params['gasPrice'] = 9
        with pytest.raises(ValueError):
            web3.eth.replaceTransaction(txn_hash, txn_params)

    def test_eth_replaceTransaction_gas_price_defaulting_minimum(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':10}
        txn_hash = web3.eth.sendTransaction(txn_params)
        txn_params.pop('gasPrice')
        replace_txn_hash = web3.eth.replaceTransaction(txn_hash, txn_params)
        replace_txn = web3.eth.getTransaction(replace_txn_hash)
        assert replace_txn['gasPrice'] == 11

    def test_eth_replaceTransaction_gas_price_defaulting_strategy_higher(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':10}
        txn_hash = web3.eth.sendTransaction(txn_params)

        def higher_gas_price_strategy(web3, txn):
            return 20

        web3.eth.setGasPriceStrategy(higher_gas_price_strategy)
        txn_params.pop('gasPrice')
        replace_txn_hash = web3.eth.replaceTransaction(txn_hash, txn_params)
        replace_txn = web3.eth.getTransaction(replace_txn_hash)
        assert replace_txn['gasPrice'] == 20

    def test_eth_replaceTransaction_gas_price_defaulting_strategy_lower(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':10}
        txn_hash = web3.eth.sendTransaction(txn_params)

        def lower_gas_price_strategy(web3, txn):
            return 5

        web3.eth.setGasPriceStrategy(lower_gas_price_strategy)
        txn_params.pop('gasPrice')
        replace_txn_hash = web3.eth.replaceTransaction(txn_hash, txn_params)
        replace_txn = web3.eth.getTransaction(replace_txn_hash)
        assert replace_txn['gasPrice'] == 11

    def test_eth_modifyTransaction(self, web3, unlocked_account):
        txn_params = {'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice}
        txn_hash = web3.eth.sendTransaction(txn_params)
        modified_txn_hash = web3.eth.modifyTransaction(txn_hash,
          gasPrice=(txn_params['gasPrice'] * 2), value=2)
        modified_txn = web3.eth.getTransaction(modified_txn_hash)
        if not is_same_address(modified_txn['from'], txn_params['from']):
            raise AssertionError
        else:
            if not is_same_address(modified_txn['to'], txn_params['to']):
                raise AssertionError
            else:
                assert modified_txn['value'] == 2
                assert modified_txn['gas'] == 21000
            assert modified_txn['gasPrice'] == txn_params['gasPrice'] * 2

    @pytest.mark.parametrize('raw_transaction, expected_hash', [
     ('0xf8648085174876e8008252089439eeed73fb1d3855e90cbd42f348b3d7b340aaa601801ba0ec1295f00936acd0c2cb90ab2cdaacb8bf5e11b3d9957833595aca9ceedb7aada05dfc8937baec0e26029057abd3a1ef8c505dca2cdc07ffacb046d090d2bea06a',
 '0x1f80f8ab5f12a45be218f76404bda64d37270a6f4f86ededd0eb599f80548c13'),
     (
      HexBytes('0xf85f808082c35094d898d5e829717c72e7438bad593076686d7d164a80801ba005c2e99ecee98a12fbf28ab9577423f42e9e88f2291b3acc8228de743884c874a077d6bc77a47ad41ec85c96aac2ad27f05a039c4787fca8a1e5ee2d8c7ec1bb6a'),
      '0x98eeadb99454427f6aad7b558bac13e9d225512a6f5e5c11cf48e8d4067e51b5')])
    def test_eth_sendRawTransaction(self, web3, raw_transaction, funded_account_for_raw_txn, expected_hash):
        txn_hash = web3.eth.sendRawTransaction(raw_transaction)
        assert txn_hash == web3.toBytes(hexstr=expected_hash)

    def test_eth_call(self, web3, math_contract):
        coinbase = web3.eth.coinbase
        txn_params = math_contract._prepare_transaction(fn_name='add',
          fn_args=(7, 11),
          transaction={'from':coinbase, 
         'to':math_contract.address})
        call_result = web3.eth.call(txn_params)
        if not is_string(call_result):
            raise AssertionError
        else:
            result = decode_single('uint256', call_result)
            assert result == 18

    def test_eth_call_with_0_result(self, web3, math_contract):
        coinbase = web3.eth.coinbase
        txn_params = math_contract._prepare_transaction(fn_name='add',
          fn_args=(0, 0),
          transaction={'from':coinbase, 
         'to':math_contract.address})
        call_result = web3.eth.call(txn_params)
        if not is_string(call_result):
            raise AssertionError
        else:
            result = decode_single('uint256', call_result)
            assert result == 0

    def test_eth_estimateGas(self, web3):
        coinbase = web3.eth.coinbase
        gas_estimate = web3.eth.estimateGas({'from':coinbase, 
         'to':coinbase, 
         'value':1})
        if not is_integer(gas_estimate):
            raise AssertionError
        elif not gas_estimate > 0:
            raise AssertionError

    def test_eth_getBlockByHash(self, web3, empty_block):
        block = web3.eth.getBlock(empty_block['hash'])
        assert block['hash'] == empty_block['hash']

    def test_eth_getBlockByHash_not_found(self, web3, empty_block):
        block = web3.eth.getBlock(UNKNOWN_HASH)
        assert block is None

    def test_eth_getBlockByNumber_with_integer(self, web3, empty_block):
        block = web3.eth.getBlock(empty_block['number'])
        assert block['number'] == empty_block['number']

    def test_eth_getBlockByNumber_latest(self, web3, empty_block):
        current_block_number = web3.eth.blockNumber
        block = web3.eth.getBlock('latest')
        assert block['number'] == current_block_number

    def test_eth_getBlockByNumber_not_found(self, web3, empty_block):
        block = web3.eth.getBlock(12345)
        assert block is None

    def test_eth_getBlockByNumber_pending(self, web3, empty_block):
        current_block_number = web3.eth.blockNumber
        block = web3.eth.getBlock('pending')
        assert block['number'] == current_block_number + 1

    def test_eth_getBlockByNumber_earliest(self, web3, empty_block):
        genesis_block = web3.eth.getBlock(0)
        block = web3.eth.getBlock('earliest')
        if not block['number'] == 0:
            raise AssertionError
        elif not block['hash'] == genesis_block['hash']:
            raise AssertionError

    def test_eth_getBlockByNumber_full_transactions(self, web3, block_with_txn):
        block = web3.eth.getBlock(block_with_txn['number'], True)
        transaction = block['transactions'][0]
        assert transaction['hash'] == block_with_txn['transactions'][0]

    def test_eth_getTransactionByHash(self, web3, mined_txn_hash):
        transaction = web3.eth.getTransaction(mined_txn_hash)
        if not is_dict(transaction):
            raise AssertionError
        elif not transaction['hash'] == HexBytes(mined_txn_hash):
            raise AssertionError

    def test_eth_getTransactionByHash_contract_creation(self, web3, math_contract_deploy_txn_hash):
        transaction = web3.eth.getTransaction(math_contract_deploy_txn_hash)
        if not is_dict(transaction):
            raise AssertionError
        elif not transaction['to'] is None:
            raise AssertionError('to field is %r' % transaction['to'])

    def test_eth_getTransactionByBlockHashAndIndex(self, web3, block_with_txn, mined_txn_hash):
        transaction = web3.eth.getTransactionFromBlock(block_with_txn['hash'], 0)
        if not is_dict(transaction):
            raise AssertionError
        elif not transaction['hash'] == HexBytes(mined_txn_hash):
            raise AssertionError

    def test_eth_getTransactionByBlockNumberAndIndex(self, web3, block_with_txn, mined_txn_hash):
        transaction = web3.eth.getTransactionFromBlock(block_with_txn['number'], 0)
        if not is_dict(transaction):
            raise AssertionError
        elif not transaction['hash'] == HexBytes(mined_txn_hash):
            raise AssertionError

    def test_eth_getTransactionReceipt_mined(self, web3, block_with_txn, mined_txn_hash):
        receipt = web3.eth.getTransactionReceipt(mined_txn_hash)
        if not is_dict(receipt):
            raise AssertionError
        else:
            if not receipt['blockNumber'] == block_with_txn['number']:
                raise AssertionError
            else:
                assert receipt['blockHash'] == block_with_txn['hash']
                assert receipt['transactionIndex'] == 0
            assert receipt['transactionHash'] == HexBytes(mined_txn_hash)

    def test_eth_getTransactionReceipt_unmined(self, web3, unlocked_account):
        txn_hash = web3.eth.sendTransaction({'from':unlocked_account, 
         'to':unlocked_account, 
         'value':1, 
         'gas':21000, 
         'gasPrice':web3.eth.gasPrice})
        receipt = web3.eth.getTransactionReceipt(txn_hash)
        assert receipt is None

    def test_eth_getTransactionReceipt_with_log_entry(self, web3, block_with_txn_with_log, emitter_contract, txn_hash_with_log):
        receipt = web3.eth.getTransactionReceipt(txn_hash_with_log)
        if not is_dict(receipt):
            raise AssertionError
        else:
            if not receipt['blockNumber'] == block_with_txn_with_log['number']:
                raise AssertionError
            else:
                if not receipt['blockHash'] == block_with_txn_with_log['hash']:
                    raise AssertionError
                else:
                    if not receipt['transactionIndex'] == 0:
                        raise AssertionError
                    else:
                        if not receipt['transactionHash'] == HexBytes(txn_hash_with_log):
                            raise AssertionError
                        else:
                            if not len(receipt['logs']) == 1:
                                raise AssertionError
                            else:
                                log_entry = receipt['logs'][0]
                                assert log_entry['blockNumber'] == block_with_txn_with_log['number']
                            assert log_entry['blockHash'] == block_with_txn_with_log['hash']
                        assert log_entry['logIndex'] == 0
                    assert is_same_address(log_entry['address'], emitter_contract.address)
                assert log_entry['transactionIndex'] == 0
            assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

    def test_eth_getUncleByBlockHashAndIndex(self, web3):
        pass

    def test_eth_getUncleByBlockNumberAndIndex(self, web3):
        pass

    def test_eth_getCompilers(self, web3):
        pass

    def test_eth_compileSolidity(self, web3):
        pass

    def test_eth_compileLLL(self, web3):
        pass

    def test_eth_compileSerpent(self, web3):
        pass

    def test_eth_newFilter(self, web3):
        filter = web3.eth.filter({})
        changes = web3.eth.getFilterChanges(filter.filter_id)
        if not is_list_like(changes):
            raise AssertionError
        else:
            if not not changes:
                raise AssertionError
            else:
                logs = web3.eth.getFilterLogs(filter.filter_id)
                assert is_list_like(logs)
                assert not logs
            result = web3.eth.uninstallFilter(filter.filter_id)
            assert result is True

    def test_eth_newBlockFilter(self, web3):
        filter = web3.eth.filter('latest')
        if not is_string(filter.filter_id):
            raise AssertionError
        else:
            changes = web3.eth.getFilterChanges(filter.filter_id)
            assert is_list_like(changes)
            assert not changes
            result = web3.eth.uninstallFilter(filter.filter_id)
            assert result is True

    def test_eth_newPendingTransactionFilter(self, web3):
        filter = web3.eth.filter('pending')
        if not is_string(filter.filter_id):
            raise AssertionError
        else:
            changes = web3.eth.getFilterChanges(filter.filter_id)
            assert is_list_like(changes)
            assert not changes
            result = web3.eth.uninstallFilter(filter.filter_id)
            assert result is True

    def test_eth_getLogs_without_logs(self, web3, block_with_txn_with_log):
        filter_params = {'fromBlock':0, 
         'toBlock':block_with_txn_with_log['number'] - 1}
        result = web3.eth.getLogs(filter_params)
        if not len(result) == 0:
            raise AssertionError
        else:
            filter_params = {'fromBlock':block_with_txn_with_log['number'], 
             'toBlock':block_with_txn_with_log['number'] - 1}
            result = web3.eth.getLogs(filter_params)
            assert len(result) == 0
            filter_params = {'fromBlock':0, 
             'address':UNKNOWN_ADDRESS}
            result = web3.eth.getLogs(filter_params)
            assert len(result) == 0

    def test_eth_getLogs_with_logs(self, web3, block_with_txn_with_log, emitter_contract, txn_hash_with_log):

        def assert_contains_log(result):
            if not len(result) == 1:
                raise AssertionError
            else:
                log_entry = result[0]
                assert log_entry['blockNumber'] == block_with_txn_with_log['number']
                assert log_entry['blockHash'] == block_with_txn_with_log['hash']
                assert log_entry['logIndex'] == 0
                assert is_same_address(log_entry['address'], emitter_contract.address)
                assert log_entry['transactionIndex'] == 0
                assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

        filter_params = {'fromBlock':block_with_txn_with_log['number'], 
         'toBlock':block_with_txn_with_log['number']}
        result = web3.eth.getLogs(filter_params)
        assert_contains_log(result)
        filter_params = {'fromBlock': 0}
        result = web3.eth.getLogs(filter_params)
        assert_contains_log(result)
        filter_params = {'fromBlock':0, 
         'address':emitter_contract.address}
        result = web3.eth.getLogs(filter_params)
        assert_contains_log(result)

    def test_eth_call_old_contract_state(self, web3, math_contract, unlocked_account):
        start_block = web3.eth.getBlock('latest')
        block_num = start_block.number
        block_hash = start_block.hash
        math_contract.functions.increment().transact({'from': unlocked_account})
        block_hash_call_result = math_contract.functions.counter().call(block_identifier=block_hash)
        block_num_call_result = math_contract.functions.counter().call(block_identifier=block_num)
        latest_call_result = math_contract.functions.counter().call(block_identifier='latest')
        default_call_result = math_contract.functions.counter().call()
        pending_call_result = math_contract.functions.counter().call(block_identifier='pending')
        if not block_hash_call_result == 0:
            raise AssertionError
        else:
            if not block_num_call_result == 0:
                raise AssertionError
            elif not latest_call_result == 0:
                raise AssertionError
            assert default_call_result == 0
        if pending_call_result != 1:
            raise AssertionError('pending call result was %d instead of 1' % pending_call_result)

    def test_eth_uninstallFilter(self, web3):
        filter = web3.eth.filter({})
        if not is_string(filter.filter_id):
            raise AssertionError
        else:
            success = web3.eth.uninstallFilter(filter.filter_id)
            assert success is True
            failure = web3.eth.uninstallFilter(filter.filter_id)
            assert failure is False