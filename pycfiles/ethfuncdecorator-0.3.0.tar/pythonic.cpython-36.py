# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/middleware/pythonic.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 11496 bytes
import codecs, operator
from eth_utils.curried import combine_argument_formatters, is_address, is_bytes, is_integer, is_null, is_string, remove_0x_prefix, text_if_str, to_checksum_address
from hexbytes import HexBytes
from web3.utils.encoding import hexstr_if_str, to_hex
from web3.utils.formatters import apply_formatter_at_index, apply_formatter_if, apply_formatter_to_array, apply_formatters_to_dict, apply_one_of_formatters, hex_to_integer, integer_to_hex, is_array_of_dicts, is_array_of_strings, remove_key_if
from web3.utils.toolz import complement, compose, curry, partial
from web3.utils.toolz.curried import keymap, valmap
from .formatting import construct_formatting_middleware

def bytes_to_ascii(value):
    return codecs.decode(value, 'ascii')


to_ascii_if_bytes = apply_formatter_if(is_bytes, bytes_to_ascii)
to_integer_if_hex = apply_formatter_if(is_string, hex_to_integer)
block_number_formatter = apply_formatter_if(is_integer, integer_to_hex)
is_false = partial(operator.is_, False)
is_not_false = complement(is_false)
is_not_null = complement(is_null)

@curry
def to_hexbytes(num_bytes, val, variable_length=False):
    if isinstance(val, (str, int, bytes)):
        result = HexBytes(val)
    else:
        raise TypeError('Cannot convert %r to HexBytes' % val)
    extra_bytes = len(result) - num_bytes
    if extra_bytes == 0 or variable_length and extra_bytes < 0:
        return result
    if all(byte == 0 for byte in result[:extra_bytes]):
        return HexBytes(result[extra_bytes:])
    raise ValueError('The value %r is %d bytes, but should be %d' % (
     result, len(result), num_bytes))


TRANSACTION_FORMATTERS = {'blockHash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'blockNumber':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'transactionIndex':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'nonce':to_integer_if_hex, 
 'gas':to_integer_if_hex, 
 'gasPrice':to_integer_if_hex, 
 'value':to_integer_if_hex, 
 'from':to_checksum_address, 
 'publicKey':to_hexbytes(64), 
 'r':to_hexbytes(32, variable_length=True), 
 'raw':HexBytes, 
 's':to_hexbytes(32, variable_length=True), 
 'to':apply_formatter_if(is_address, to_checksum_address), 
 'hash':to_hexbytes(32), 
 'v':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'standardV':apply_formatter_if(is_not_null, to_integer_if_hex)}
transaction_formatter = apply_formatters_to_dict(TRANSACTION_FORMATTERS)
WHISPER_LOG_FORMATTERS = {'sig':to_hexbytes(130), 
 'topic':to_hexbytes(8), 
 'payload':HexBytes, 
 'padding':apply_formatter_if(is_not_null, HexBytes), 
 'hash':to_hexbytes(64), 
 'recipientPublicKey':apply_formatter_if(is_not_null, to_hexbytes(130))}
whisper_log_formatter = apply_formatters_to_dict(WHISPER_LOG_FORMATTERS)
LOG_ENTRY_FORMATTERS = {'blockHash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'blockNumber':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'transactionIndex':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'transactionHash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'logIndex':to_integer_if_hex, 
 'address':to_checksum_address, 
 'topics':apply_formatter_to_array(to_hexbytes(32)), 
 'data':to_ascii_if_bytes}
log_entry_formatter = apply_formatters_to_dict(LOG_ENTRY_FORMATTERS)
RECEIPT_FORMATTERS = {'blockHash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'blockNumber':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'transactionIndex':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'transactionHash':to_hexbytes(32), 
 'cumulativeGasUsed':to_integer_if_hex, 
 'status':to_integer_if_hex, 
 'gasUsed':to_integer_if_hex, 
 'contractAddress':apply_formatter_if(is_not_null, to_checksum_address), 
 'logs':apply_formatter_to_array(log_entry_formatter), 
 'logsBloom':to_hexbytes(256)}
receipt_formatter = apply_formatters_to_dict(RECEIPT_FORMATTERS)
BLOCK_FORMATTERS = {'extraData':to_hexbytes(32, variable_length=True), 
 'gasLimit':to_integer_if_hex, 
 'gasUsed':to_integer_if_hex, 
 'size':to_integer_if_hex, 
 'timestamp':to_integer_if_hex, 
 'hash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'logsBloom':to_hexbytes(256), 
 'miner':apply_formatter_if(is_not_null, to_checksum_address), 
 'mixHash':to_hexbytes(32), 
 'nonce':apply_formatter_if(is_not_null, to_hexbytes(8, variable_length=True)), 
 'number':apply_formatter_if(is_not_null, to_integer_if_hex), 
 'parentHash':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'sha3Uncles':apply_formatter_if(is_not_null, to_hexbytes(32)), 
 'uncles':apply_formatter_to_array(to_hexbytes(32)), 
 'difficulty':to_integer_if_hex, 
 'receiptsRoot':to_hexbytes(32), 
 'stateRoot':to_hexbytes(32), 
 'totalDifficulty':to_integer_if_hex, 
 'transactions':apply_one_of_formatters((
  (
   apply_formatter_to_array(transaction_formatter), is_array_of_dicts),
  (
   apply_formatter_to_array(to_hexbytes(32)), is_array_of_strings))), 
 'transactionsRoot':to_hexbytes(32)}
block_formatter = apply_formatters_to_dict(BLOCK_FORMATTERS)
SYNCING_FORMATTERS = {'startingBlock':to_integer_if_hex, 
 'currentBlock':to_integer_if_hex, 
 'highestBlock':to_integer_if_hex, 
 'knownStates':to_integer_if_hex, 
 'pulledStates':to_integer_if_hex}
syncing_formatter = apply_formatters_to_dict(SYNCING_FORMATTERS)
TRANSACTION_POOL_CONTENT_FORMATTERS = {'pending':compose(keymap(to_ascii_if_bytes), valmap(transaction_formatter)), 
 'queued':compose(keymap(to_ascii_if_bytes), valmap(transaction_formatter))}
transaction_pool_content_formatter = apply_formatters_to_dict(TRANSACTION_POOL_CONTENT_FORMATTERS)
TRANSACTION_POOL_INSPECT_FORMATTERS = {'pending':keymap(to_ascii_if_bytes), 
 'queued':keymap(to_ascii_if_bytes)}
transaction_pool_inspect_formatter = apply_formatters_to_dict(TRANSACTION_POOL_INSPECT_FORMATTERS)
FILTER_PARAMS_FORMATTERS = {'fromBlock':apply_formatter_if(is_integer, integer_to_hex), 
 'toBlock':apply_formatter_if(is_integer, integer_to_hex)}
filter_params_formatter = apply_formatters_to_dict(FILTER_PARAMS_FORMATTERS)
filter_result_formatter = apply_one_of_formatters((
 (
  apply_formatter_to_array(log_entry_formatter), is_array_of_dicts),
 (
  apply_formatter_to_array(to_hexbytes(32)), is_array_of_strings)))
TRANSACTION_PARAM_FORMATTERS = {'chainId': apply_formatter_if(is_integer, str)}
transaction_param_formatter = compose(remove_key_if('to', lambda txn: txn['to'] in frozenset({'', b'', None})), apply_formatters_to_dict(TRANSACTION_PARAM_FORMATTERS))
pythonic_middleware = construct_formatting_middleware(request_formatters={'eth_getBalance':apply_formatter_at_index(block_number_formatter, 1), 
 'eth_getBlockByNumber':apply_formatter_at_index(block_number_formatter, 0), 
 'eth_getBlockTransactionCountByNumber':apply_formatter_at_index(block_number_formatter, 0), 
 'eth_getCode':apply_formatter_at_index(block_number_formatter, 1), 
 'eth_getStorageAt':apply_formatter_at_index(block_number_formatter, 2), 
 'eth_getTransactionByBlockNumberAndIndex':compose(apply_formatter_at_index(block_number_formatter, 0), apply_formatter_at_index(integer_to_hex, 1)), 
 'eth_getTransactionCount':apply_formatter_at_index(block_number_formatter, 1), 
 'eth_getUncleCountByBlockNumber':apply_formatter_at_index(block_number_formatter, 0), 
 'eth_newFilter':apply_formatter_at_index(filter_params_formatter, 0), 
 'eth_getLogs':apply_formatter_at_index(filter_params_formatter, 0), 
 'eth_call':combine_argument_formatters(transaction_param_formatter, block_number_formatter), 
 'eth_estimateGas':apply_formatter_at_index(transaction_param_formatter, 0), 
 'eth_sendTransaction':apply_formatter_at_index(transaction_param_formatter, 0), 
 'personal_importRawKey':apply_formatter_at_index(compose(remove_0x_prefix, hexstr_if_str(to_hex)), 0), 
 'personal_sign':apply_formatter_at_index(text_if_str(to_hex), 0), 
 'personal_ecRecover':apply_formatter_at_index(text_if_str(to_hex), 0), 
 'personal_sendTransaction':apply_formatter_at_index(transaction_param_formatter, 0), 
 'evm_revert':apply_formatter_at_index(integer_to_hex, 0)},
  result_formatters={'eth_accounts':apply_formatter_to_array(to_checksum_address), 
 'eth_blockNumber':to_integer_if_hex, 
 'eth_coinbase':to_checksum_address, 
 'eth_estimateGas':to_integer_if_hex, 
 'eth_gasPrice':to_integer_if_hex, 
 'eth_getBalance':to_integer_if_hex, 
 'eth_getBlockByHash':apply_formatter_if(is_not_null, block_formatter), 
 'eth_getBlockByNumber':apply_formatter_if(is_not_null, block_formatter), 
 'eth_getBlockTransactionCountByHash':to_integer_if_hex, 
 'eth_getBlockTransactionCountByNumber':to_integer_if_hex, 
 'eth_getCode':HexBytes, 
 'eth_getFilterChanges':filter_result_formatter, 
 'eth_getFilterLogs':filter_result_formatter, 
 'eth_getLogs':filter_result_formatter, 
 'eth_getStorageAt':HexBytes, 
 'eth_getTransactionByBlockHashAndIndex':apply_formatter_if(is_not_null, transaction_formatter), 
 'eth_getTransactionByBlockNumberAndIndex':apply_formatter_if(is_not_null, transaction_formatter), 
 'eth_getTransactionByHash':apply_formatter_if(is_not_null, transaction_formatter), 
 'eth_getTransactionCount':to_integer_if_hex, 
 'eth_getTransactionReceipt':apply_formatter_if(is_not_null, receipt_formatter), 
 'eth_getUncleCountByBlockHash':to_integer_if_hex, 
 'eth_getUncleCountByBlockNumber':to_integer_if_hex, 
 'eth_hashrate':to_integer_if_hex, 
 'eth_protocolVersion':compose(apply_formatter_if(is_integer, str), to_integer_if_hex), 
 'eth_sendRawTransaction':to_hexbytes(32), 
 'eth_sendTransaction':to_hexbytes(32), 
 'eth_sign':HexBytes, 
 'eth_syncing':apply_formatter_if(is_not_false, syncing_formatter), 
 'personal_importRawKey':to_checksum_address, 
 'personal_listAccounts':apply_formatter_to_array(to_checksum_address), 
 'personal_newAccount':to_checksum_address, 
 'personal_sendTransaction':to_hexbytes(32), 
 'shh_getFilterMessages':apply_formatter_to_array(whisper_log_formatter), 
 'txpool_content':transaction_pool_content_formatter, 
 'txpool_inspect':transaction_pool_inspect_formatter, 
 'evm_snapshot':hex_to_integer, 
 'net_peerCount':to_integer_if_hex})