# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/transaction.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 51778 bytes
import struct, traceback, sys
from typing import Sequence, Union, NamedTuple, Tuple, Optional, Iterable, Callable, List, Dict
from . import ecc, bitcoin, constants, segwit_addr
from .util import profiler, to_bytes, bh2u, bfh
from .bitcoin import TYPE_ADDRESS, TYPE_PUBKEY, TYPE_SCRIPT, hash_160, hash160_to_p2sh, hash160_to_p2pkh, hash_to_segwit_addr, hash_encode, var_int, TOTAL_COIN_SUPPLY_LIMIT_IN_BTC, COIN, push_script, int_to_hex, push_script, b58_address_to_hash160, opcodes, add_number_to_script, base_decode, is_segwit_script_type
from .crypto import sha256d
from .keystore import xpubkey_to_address, xpubkey_to_pubkey
from .logging import get_logger
_logger = get_logger(__name__)
NO_SIGNATURE = 'ff'
PARTIAL_TXN_HEADER_MAGIC = b'EPTF\xff'

class SerializationError(Exception):
    __doc__ = " Thrown when there's a problem deserializing or serializing "


class UnknownTxinType(Exception):
    pass


class NotRecognizedRedeemScript(Exception):
    pass


class MalformedBitcoinScript(Exception):
    pass


class TxOutput(NamedTuple):
    type: int
    address: str
    value: Union[(int, str)]
    name_op: dict


TxOutput.__new__.__defaults__ = (None, )

class TxOutputForUI(NamedTuple):
    address: str
    value: int
    name_op: dict


TxOutputForUI.__new__.__defaults__ = (None, )

class TxOutputHwInfo(NamedTuple):
    address_index: Tuple
    sorted_xpubs: Iterable[str]
    num_sig: Optional[int]
    script_type: str


class BIP143SharedTxDigestFields(NamedTuple):
    hashPrevouts: str
    hashSequence: str
    hashOutputs: str


class BCDataStream(object):
    __doc__ = "Workalike python implementation of Bitcoin's CDataStream class."

    def __init__(self):
        self.input = None
        self.read_cursor = 0

    def clear(self):
        self.input = None
        self.read_cursor = 0

    def write(self, _bytes):
        if self.input is None:
            self.input = bytearray(_bytes)
        else:
            self.input += bytearray(_bytes)

    def read_string(self, encoding='ascii'):
        if self.input is None:
            raise SerializationError('call write(bytes) before trying to deserialize')
        length = self.read_compact_size()
        return self.read_bytes(length).decode(encoding)

    def write_string(self, string, encoding='ascii'):
        string = to_bytes(string, encoding)
        self.write_compact_size(len(string))
        self.write(string)

    def read_bytes(self, length):
        try:
            result = self.input[self.read_cursor:self.read_cursor + length]
            self.read_cursor += length
            return result
        except IndexError:
            raise SerializationError('attempt to read past end of buffer') from None

    def can_read_more(self) -> bool:
        if not self.input:
            return False
        return self.read_cursor < len(self.input)

    def read_boolean(self):
        return self.read_bytes(1)[0] != chr(0)

    def read_int16(self):
        return self._read_num('<h')

    def read_uint16(self):
        return self._read_num('<H')

    def read_int32(self):
        return self._read_num('<i')

    def read_uint32(self):
        return self._read_num('<I')

    def read_int64(self):
        return self._read_num('<q')

    def read_uint64(self):
        return self._read_num('<Q')

    def write_boolean(self, val):
        return self.write(chr(1) if val else chr(0))

    def write_int16(self, val):
        return self._write_num('<h', val)

    def write_uint16(self, val):
        return self._write_num('<H', val)

    def write_int32(self, val):
        return self._write_num('<i', val)

    def write_uint32(self, val):
        return self._write_num('<I', val)

    def write_int64(self, val):
        return self._write_num('<q', val)

    def write_uint64(self, val):
        return self._write_num('<Q', val)

    def read_compact_size(self):
        try:
            size = self.input[self.read_cursor]
            self.read_cursor += 1
            if size == 253:
                size = self._read_num('<H')
            else:
                if size == 254:
                    size = self._read_num('<I')
                else:
                    if size == 255:
                        size = self._read_num('<Q')
            return size
        except IndexError as e:
            try:
                raise SerializationError('attempt to read past end of buffer') from e
            finally:
                e = None
                del e

    def write_compact_size(self, size):
        if size < 0:
            raise SerializationError('attempt to write size < 0')
        else:
            if size < 253:
                self.write(bytes([size]))
            else:
                if size < 65536:
                    self.write(b'\xfd')
                    self._write_num('<H', size)
                else:
                    if size < 4294967296:
                        self.write(b'\xfe')
                        self._write_num('<I', size)
                    else:
                        if size < 18446744073709551616:
                            self.write(b'\xff')
                            self._write_num('<Q', size)

    def _read_num(self, format):
        try:
            i, = struct.unpack_from(format, self.input, self.read_cursor)
            self.read_cursor += struct.calcsize(format)
        except Exception as e:
            try:
                raise SerializationError(e) from e
            finally:
                e = None
                del e

        return i

    def _write_num(self, format, num):
        s = struct.pack(format, num)
        self.write(s)


def script_GetOp(_bytes: bytes):
    i = 0
    while i < len(_bytes):
        vch = None
        opcode = _bytes[i]
        i += 1
        if opcode <= opcodes.OP_PUSHDATA4:
            nSize = opcode
            if opcode == opcodes.OP_PUSHDATA1:
                try:
                    nSize = _bytes[i]
                except IndexError:
                    raise MalformedBitcoinScript()

                i += 1
            else:
                if opcode == opcodes.OP_PUSHDATA2:
                    try:
                        nSize, = struct.unpack_from('<H', _bytes, i)
                    except struct.error:
                        raise MalformedBitcoinScript()

                    i += 2
                else:
                    if opcode == opcodes.OP_PUSHDATA4:
                        try:
                            nSize, = struct.unpack_from('<I', _bytes, i)
                        except struct.error:
                            raise MalformedBitcoinScript()

                        i += 4
            vch = _bytes[i:i + nSize]
            i += nSize
        yield (opcode, vch, i)


class OPPushDataGeneric:

    def __init__(self, pushlen: Callable=None):
        if pushlen is not None:
            self.check_data_len = pushlen

    @classmethod
    def check_data_len(cls, datalen: int) -> bool:
        return opcodes.OP_PUSHDATA4 >= datalen >= 0

    @classmethod
    def is_instance(cls, item):
        return isinstance(item, cls) or isinstance(item, type) and issubclass(item, cls)


OPPushDataPubkey = OPPushDataGeneric(lambda x: x in (33, 65))

def match_decoded(decoded, to_match):
    if decoded is None:
        return False
    if len(decoded) != len(to_match):
        return False
    for i in range(len(decoded)):
        to_match_item = to_match[i]
        decoded_item = decoded[i]
        if OPPushDataGeneric.is_instance(to_match_item):
            if to_match_item.check_data_len(decoded_item[0]):
                continue
        if to_match_item != decoded_item[0]:
            return False

    return True


def parse_sig(x_sig):
    return [None if x == NO_SIGNATURE else x for x in x_sig]


def safe_parse_pubkey(x):
    try:
        return xpubkey_to_pubkey(x)
    except:
        return x


def parse_scriptSig(d, _bytes):
    try:
        decoded = [x for x in script_GetOp(_bytes)]
    except Exception as e:
        try:
            _logger.info(f"parse_scriptSig: cannot find address in input script (coinbase?) {bh2u(_bytes)}")
            return
        finally:
            e = None
            del e

    match = [
     OPPushDataGeneric]
    if match_decoded(decoded, match):
        item = decoded[0][1]
        if item[0] == 0:
            d['address'] = bitcoin.hash160_to_p2sh(hash_160(item))
            if len(item) == 22:
                d['type'] = 'p2wpkh-p2sh'
        elif len(item) == 34:
            d['type'] = 'p2wsh-p2sh'
        else:
            _logger.info(f"unrecognized txin type {bh2u(item)}")
    else:
        if opcodes.OP_1 <= item[0] <= opcodes.OP_16:
            pass
        else:
            d['type'] = 'p2pk'
            d['address'] = '(pubkey)'
            d['signatures'] = [bh2u(item)]
            d['num_sig'] = 1
            d['x_pubkeys'] = ['(pubkey)']
            d['pubkeys'] = ['(pubkey)']
        return
        match = [
         OPPushDataGeneric, OPPushDataGeneric]
        if match_decoded(decoded, match):
            sig = bh2u(decoded[0][1])
            x_pubkey = bh2u(decoded[1][1])
            try:
                signatures = parse_sig([sig])
                pubkey, address = xpubkey_to_address(x_pubkey)
            except:
                _logger.info(f"parse_scriptSig: cannot find address in input script (p2pkh?) {bh2u(_bytes)}")
                return
                d['type'] = 'p2pkh'
                d['signatures'] = signatures
                d['x_pubkeys'] = [x_pubkey]
                d['num_sig'] = 1
                d['pubkeys'] = [pubkey]
                d['address'] = address
                return

        match = [opcodes.OP_0] + [OPPushDataGeneric] * (len(decoded) - 1)
        if match_decoded(decoded, match):
            x_sig = [bh2u(x[1]) for x in decoded[1:-1]]
            redeem_script_unsanitized = decoded[(-1)][1]
            try:
                m, n, x_pubkeys, pubkeys, redeem_script = parse_redeemScript_multisig(redeem_script_unsanitized)
            except NotRecognizedRedeemScript:
                _logger.info(f"parse_scriptSig: cannot find address in input script (p2sh?) {bh2u(_bytes)}")
                return
            else:
                d['type'] = 'p2sh'
                d['num_sig'] = m
                d['signatures'] = parse_sig(x_sig)
                d['x_pubkeys'] = x_pubkeys
                d['pubkeys'] = pubkeys
                d['redeem_script'] = redeem_script
                d['address'] = hash160_to_p2sh(hash_160(bfh(redeem_script)))
                return
        match = [opcodes.OP_INVALIDOPCODE, opcodes.OP_0, OPPushDataGeneric]
        if match_decoded(decoded, match):
            x_pubkey = bh2u(decoded[2][1])
            pubkey, address = xpubkey_to_address(x_pubkey)
            d['type'] = 'address'
            d['address'] = address
            d['num_sig'] = 1
            d['x_pubkeys'] = [x_pubkey]
            d['pubkeys'] = None
            d['signatures'] = [None]
            return
        _logger.info(f"parse_scriptSig: cannot find address in input script (unknown) {bh2u(_bytes)}")


def parse_redeemScript_multisig(redeem_script: bytes):
    try:
        dec2 = [x for x in script_GetOp(redeem_script)]
    except MalformedBitcoinScript:
        raise NotRecognizedRedeemScript()

    try:
        m = dec2[0][0] - opcodes.OP_1 + 1
        n = dec2[(-2)][0] - opcodes.OP_1 + 1
    except IndexError:
        raise NotRecognizedRedeemScript()

    op_m = opcodes.OP_1 + m - 1
    op_n = opcodes.OP_1 + n - 1
    match_multisig = [op_m] + [OPPushDataGeneric] * n + [op_n, opcodes.OP_CHECKMULTISIG]
    if not match_decoded(dec2, match_multisig):
        raise NotRecognizedRedeemScript()
    x_pubkeys = [bh2u(x[1]) for x in dec2[1:-2]]
    pubkeys = [safe_parse_pubkey(x) for x in x_pubkeys]
    redeem_script2 = bfh(multisig_script(x_pubkeys, m))
    if redeem_script2 != redeem_script:
        raise NotRecognizedRedeemScript()
    redeem_script_sanitized = multisig_script(pubkeys, m)
    return (m, n, x_pubkeys, pubkeys, redeem_script_sanitized)


def get_address_from_output_script(_bytes: bytes, *, net=None) -> Tuple[(int, str)]:
    try:
        decoded = [x for x in script_GetOp(_bytes)]
    except MalformedBitcoinScript:
        decoded = None

    decoded = split_name_script(decoded)['address_scriptPubKey']
    match = [
     OPPushDataPubkey, opcodes.OP_CHECKSIG]
    if match_decoded(decoded, match):
        if ecc.ECPubkey.is_pubkey_bytes(decoded[0][1]):
            return (
             TYPE_PUBKEY, bh2u(decoded[0][1]))
    match = [opcodes.OP_DUP, opcodes.OP_HASH160, OPPushDataGeneric(lambda x: x == 20), opcodes.OP_EQUALVERIFY, opcodes.OP_CHECKSIG]
    if match_decoded(decoded, match):
        return (
         TYPE_ADDRESS, hash160_to_p2pkh((decoded[2][1]), net=net))
    match = [
     opcodes.OP_HASH160, OPPushDataGeneric(lambda x: x == 20), opcodes.OP_EQUAL]
    if match_decoded(decoded, match):
        return (
         TYPE_ADDRESS, hash160_to_p2sh((decoded[1][1]), net=net))
    match = [
     opcodes.OP_0, OPPushDataGeneric(lambda x: x in (20, 32))]
    if match_decoded(decoded, match):
        return (
         TYPE_ADDRESS, hash_to_segwit_addr((decoded[1][1]), witver=0, net=net))
    future_witness_versions = list(range(opcodes.OP_1, opcodes.OP_16 + 1))
    for witver, opcode in enumerate(future_witness_versions, start=1):
        match = [
         opcode, OPPushDataGeneric(lambda x: 2 <= x <= 40)]
        if match_decoded(decoded, match):
            return (
             TYPE_ADDRESS, hash_to_segwit_addr((decoded[1][1]), witver=witver, net=net))

    return (
     TYPE_SCRIPT, bh2u(_bytes))


def parse_input(vds, full_parse: bool):
    d = {}
    prevout_hash = hash_encode(vds.read_bytes(32))
    prevout_n = vds.read_uint32()
    scriptSig = vds.read_bytes(vds.read_compact_size())
    sequence = vds.read_uint32()
    d['prevout_hash'] = prevout_hash
    d['prevout_n'] = prevout_n
    d['scriptSig'] = bh2u(scriptSig)
    d['sequence'] = sequence
    d['type'] = 'unknown' if prevout_hash != '0000000000000000000000000000000000000000000000000000000000000000' else 'coinbase'
    d['address'] = None
    d['num_sig'] = 0
    if not full_parse:
        return d
    d['x_pubkeys'] = []
    d['pubkeys'] = []
    d['signatures'] = {}
    if d['type'] != 'coinbase':
        if scriptSig:
            try:
                parse_scriptSig(d, scriptSig)
            except BaseException:
                _logger.exception(f"failed to parse scriptSig {bh2u(scriptSig)}")

    return d


def construct_witness(items: Sequence[Union[(str, int, bytes)]]) -> str:
    """Constructs a witness from the given stack items."""
    witness = var_int(len(items))
    for item in items:
        if type(item) is int:
            item = bitcoin.script_num_to_hex(item)
        else:
            if type(item) is bytes:
                item = bh2u(item)
        witness += bitcoin.witness_push(item)

    return witness


def parse_witness(vds, txin, full_parse: bool):
    n = vds.read_compact_size()
    if n == 0:
        txin['witness'] = '00'
        return
    else:
        if n == 4294967295:
            txin['value'] = vds.read_uint64()
            txin['witness_version'] = vds.read_uint16()
            n = vds.read_compact_size()
        w = list((bh2u(vds.read_bytes(vds.read_compact_size())) for i in range(n)))
        txin['witness'] = construct_witness(w)
        return full_parse or None
    try:
        if txin.get('witness_version', 0) != 0:
            raise UnknownTxinType()
        elif txin['type'] == 'coinbase':
            pass
        elif txin['type'] == 'address':
            pass
        elif txin['type'] == 'p2wsh-p2sh' or n > 2:
            witness_script_unsanitized = w[(-1)]
            try:
                m, n, x_pubkeys, pubkeys, witness_script = parse_redeemScript_multisig(bfh(witness_script_unsanitized))
            except NotRecognizedRedeemScript:
                raise UnknownTxinType()

            txin['signatures'] = parse_sig(w[1:-1])
            txin['num_sig'] = m
            txin['x_pubkeys'] = x_pubkeys
            txin['pubkeys'] = pubkeys
            txin['witness_script'] = witness_script
            txin['type'] = txin.get('scriptSig') or 'p2wsh'
            txin['address'] = bitcoin.script_to_p2wsh(witness_script)
        else:
            if txin['type'] == 'p2wpkh-p2sh' or n == 2:
                txin['num_sig'] = 1
                txin['x_pubkeys'] = [w[1]]
                txin['pubkeys'] = [safe_parse_pubkey(w[1])]
                txin['signatures'] = parse_sig([w[0]])
                txin['type'] = txin.get('scriptSig') or 'p2wpkh'
                txin['address'] = bitcoin.public_key_to_p2wpkh(bfh(txin['pubkeys'][0]))
            else:
                raise UnknownTxinType()
    except UnknownTxinType:
        txin['type'] = 'unknown'
    except BaseException:
        txin['type'] = 'unknown'
        _logger.exception(f"failed to parse witness {txin.get('witness')}")


def parse_output(vds, i):
    d = {}
    d['value'] = vds.read_int64()
    if d['value'] > TOTAL_COIN_SUPPLY_LIMIT_IN_BTC * COIN:
        raise SerializationError('invalid output amount (too large)')
    if d['value'] < 0:
        raise SerializationError('invalid output amount (negative)')
    scriptPubKey = vds.read_bytes(vds.read_compact_size())
    d['type'], d['address'] = get_address_from_output_script(scriptPubKey)
    d['name_op'] = get_name_op_from_output_script(scriptPubKey)
    if d['name_op'] is not None:
        d['value'] = d['value'] - COIN // 100
        if d['value'] < 0:
            raise SerializationError('invalid output amount (insufficient for name output)')
    d['scriptPubKey'] = bh2u(scriptPubKey)
    d['prevout_n'] = i
    return d


def deserialize(raw: str, force_full_parse=False, expect_trailing_data=False, raw_bytes=None, expect_trailing_bytes=False, copy_input=True, start_position=0) -> dict:
    if raw_bytes is None:
        raw_bytes = bfh(raw)
    else:
        d = {}
        if raw_bytes[:5] == PARTIAL_TXN_HEADER_MAGIC:
            d['partial'] = is_partial = True
            partial_format_version = raw_bytes[5]
            if partial_format_version != 0:
                raise SerializationError('unknown tx partial serialization format version: {}'.format(partial_format_version))
            raw_bytes = raw_bytes[6:]
        else:
            d['partial'] = is_partial = False
        full_parse = force_full_parse or is_partial
        vds = BCDataStream()
        if copy_input:
            vds.write(raw_bytes)
        else:
            vds.input = raw_bytes
        vds.read_cursor = start_position
        d['version'] = vds.read_int32()
        n_vin = vds.read_compact_size()
        is_segwit = n_vin == 0
        if is_segwit:
            marker = vds.read_bytes(1)
            if marker != b'\x01':
                raise ValueError('invalid txn marker byte: {}'.format(marker))
            n_vin = vds.read_compact_size()
        d['segwit_ser'] = is_segwit
        d['inputs'] = [parse_input(vds, full_parse=full_parse) for i in range(n_vin)]
        n_vout = vds.read_compact_size()
        d['outputs'] = [parse_output(vds, i) for i in range(n_vout)]
        if is_segwit:
            for i in range(n_vin):
                txin = d['inputs'][i]
                parse_witness(vds, txin, full_parse=full_parse)

        d['lockTime'] = vds.read_uint32()
        if vds.can_read_more() and not expect_trailing_data:
            raise SerializationError('extra junk at the end')
        return expect_trailing_data or d
    if expect_trailing_bytes:
        return (
         d, vds.read_cursor)
    raise Exception('Unimplemented: starting position for trailing data in hex format')


def multisig_script--- This code section failed: ---

 L. 610         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'public_keys'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'n'

 L. 611         8  LOAD_CONST               1
               10  LOAD_FAST                'm'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               <=
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  LOAD_FAST                'n'
               22  DUP_TOP          
               24  ROT_THREE        
               26  COMPARE_OP               <=
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_CONST               15
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_TRUE     60  'to 60'
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            18  '18'
               38  POP_TOP          
             40_0  COME_FROM            36  '36'
               40  LOAD_GLOBAL              AssertionError
               42  LOAD_STR                 'm '
               44  LOAD_FAST                'm'
               46  FORMAT_VALUE          0  ''
               48  LOAD_STR                 ', n '
               50  LOAD_FAST                'n'
               52  FORMAT_VALUE          0  ''
               54  BUILD_STRING_4        4 
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            34  '34'

 L. 612        60  LOAD_GLOBAL              bh2u
               62  LOAD_GLOBAL              add_number_to_script
               64  LOAD_FAST                'm'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  STORE_FAST               'op_m'

 L. 613        72  LOAD_GLOBAL              bh2u
               74  LOAD_GLOBAL              add_number_to_script
               76  LOAD_FAST                'n'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  STORE_FAST               'op_n'

 L. 614        84  LOAD_LISTCOMP            '<code_object <listcomp>>'
               86  LOAD_STR                 'multisig_script.<locals>.<listcomp>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_FAST                'public_keys'
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  STORE_FAST               'keylist'

 L. 615        98  LOAD_FAST                'op_m'
              100  LOAD_STR                 ''
              102  LOAD_METHOD              join
              104  LOAD_FAST                'keylist'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  BINARY_ADD       
              110  LOAD_FAST                'op_n'
              112  BINARY_ADD       
              114  LOAD_GLOBAL              opcodes
              116  LOAD_ATTR                OP_CHECKMULTISIG
              118  LOAD_METHOD              hex
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  BINARY_ADD       
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 38


class Transaction:

    def __str__(self):
        if self.raw is None:
            self.raw = self.serialize()
        return self.raw

    def __init__(self, raw, expect_trailing_data=False, raw_bytes=None, expect_trailing_bytes=False, copy_input=True, start_position=0):
        if raw is None:
            self.raw = None
            self.raw_bytes = raw_bytes
        else:
            if isinstance(raw, str):
                self.raw = raw.strip() if raw else None
                self.raw_bytes = raw_bytes
            else:
                if isinstance(raw, dict):
                    self.raw = raw['hex']
                    self.raw_bytes = raw_bytes
                else:
                    raise Exception('cannot initialize transaction', raw)
        self._inputs = None
        self._outputs = None
        self.locktime = 0
        self.version = 2
        self.is_partial_originally = True
        self._segwit_ser = None
        self.output_info = None
        self.expect_trailing_data = expect_trailing_data
        self.expect_trailing_bytes = expect_trailing_bytes
        self.copy_input = copy_input
        self.start_position = start_position

    def update(self, raw):
        self.raw = raw
        self._inputs = None
        self.deserialize()

    def inputs(self):
        if self._inputs is None:
            self.deserialize()
        return self._inputs

    def outputs(self) -> List[TxOutput]:
        if self._outputs is None:
            self.deserialize()
        return self._outputs

    @classmethod
    def get_sorted_pubkeys(self, txin):
        if txin['type'] == 'coinbase':
            return ([], [])
        x_pubkeys = txin['x_pubkeys']
        pubkeys = txin.get('pubkeys')
        if pubkeys is None:
            pubkeys = [xpubkey_to_pubkey(x) for x in x_pubkeys]
            pubkeys, x_pubkeys = zip(*sorted(zip(pubkeys, x_pubkeys)))
            txin['pubkeys'] = pubkeys = list(pubkeys)
            txin['x_pubkeys'] = x_pubkeys = list(x_pubkeys)
        return (
         pubkeys, x_pubkeys)

    def update_signatures(self, signatures: Sequence[str]):
        """Add new signatures to a transaction

        `signatures` is expected to be a list of sigs with signatures[i]
        intended for self._inputs[i].
        This is used by the Trezor, KeepKey an Safe-T plugins.
        """
        if self.is_complete():
            return
        if len(self.inputs()) != len(signatures):
            raise Exception('expected {} signatures; got {}'.format(len(self.inputs()), len(signatures)))
        for i, txin in enumerate(self.inputs()):
            pubkeys, x_pubkeys = self.get_sorted_pubkeys(txin)
            sig = signatures[i]
            if sig in txin.get('signatures'):
                continue
            pre_hash = sha256d(bfh(self.serialize_preimage(i)))
            sig_string = ecc.sig_string_from_der_sig(bfh(sig[:-2]))
            for recid in range(4):
                try:
                    public_key = ecc.ECPubkey.from_sig_string(sig_string, recid, pre_hash)
                except ecc.InvalidECPointException:
                    continue

                pubkey_hex = public_key.get_public_key_hex(compressed=True)
                if pubkey_hex in pubkeys:
                    try:
                        public_key.verify_message_hash(sig_string, pre_hash)
                    except Exception:
                        _logger.exception('')
                        continue

                    j = pubkeys.index(pubkey_hex)
                    _logger.info(f"adding sig {i} {j} {pubkey_hex} {sig}")
                    self.add_signature_to_txin(i, j, sig)
                    break

        self.raw = self.serialize()

    def add_signature_to_txin(self, i, signingPos, sig):
        txin = self._inputs[i]
        txin['signatures'][signingPos] = sig
        txin['scriptSig'] = None
        txin['witness'] = None
        self.raw = None

    def add_inputs_info(self, wallet):
        if self.is_complete():
            return
        for txin in self.inputs():
            wallet.add_input_info(txin)

    def remove_signatures(self):
        for txin in self.inputs():
            txin['signatures'] = [
             None] * len(txin['signatures'])
            txin['scriptSig'] = None
            txin['witness'] = None

        assert not self.is_complete()
        self.raw = None

    def deserialize(self, force_full_parse=False):
        if self.raw is None:
            if self.raw_bytes is None:
                return
        else:
            if self._inputs is not None:
                return
                if self.expect_trailing_data:
                    d, start_position = deserialize((self.raw), force_full_parse, expect_trailing_data=(self.expect_trailing_data), raw_bytes=(self.raw_bytes), expect_trailing_bytes=(self.expect_trailing_bytes), copy_input=(self.copy_input), start_position=(self.start_position))
                else:
                    d = deserialize((self.raw), force_full_parse, raw_bytes=(self.raw_bytes), start_position=(self.start_position))
                self._inputs = d['inputs']
                self._outputs = [TxOutput(x['type'], x['address'], x['value'], x['name_op']) for x in d['outputs']]
                self.locktime = d['lockTime']
                self.version = d['version']
                self.is_partial_originally = d['partial']
                self._segwit_ser = d['segwit_ser']
                if self.expect_trailing_data:
                    if self.expect_trailing_bytes:
                        if self.raw is not None:
                            self.raw = self.raw[2 * self.start_position:2 * start_position]
                        if self.raw_bytes is not None:
                            self.raw_bytes = self.raw_bytes[self.start_position:start_position]
            elif self.raw is not None:
                self.raw = self.raw[self.start_position:start_position]
            if self.raw_bytes is not None:
                self.raw_bytes = self.raw_bytes[self.start_position // 2:start_position // 2]
            self.expect_trailing_data = False
            self.start_position = 0
            return (d, start_position)
        return d

    @classmethod
    def from_io(klass, inputs, outputs, locktime=0, version=None):
        self = klass(None)
        self._inputs = inputs
        self._outputs = outputs
        self.locktime = locktime
        if version is not None:
            self.version = version
        self.BIP69_sort()
        return self

    @classmethod
    def pay_script(self, output_type, addr: str, name_op=None) -> str:
        """Returns scriptPubKey in hex form."""
        name_prefix = name_op_to_script(name_op)
        if output_type == TYPE_SCRIPT:
            return name_prefix + addr
        if output_type == TYPE_ADDRESS:
            return name_prefix + bitcoin.address_to_script(addr)
        if output_type == TYPE_PUBKEY:
            return name_prefix + bitcoin.public_key_to_p2pk_script(addr)
        raise TypeError('Unknown output type')

    @classmethod
    def estimate_pubkey_size_from_x_pubkey(cls, x_pubkey):
        try:
            if x_pubkey[0:2] in ('02', '03'):
                return 33
            if x_pubkey[0:2] == '04':
                return 65
            if x_pubkey[0:2] == 'ff':
                return 33
            if x_pubkey[0:2] == 'fe':
                return 65
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e

        return 33

    @classmethod
    def estimate_pubkey_size_for_txin(cls, txin):
        pubkeys = txin.get('pubkeys', [])
        x_pubkeys = txin.get('x_pubkeys', [])
        if pubkeys:
            if len(pubkeys) > 0:
                return cls.estimate_pubkey_size_from_x_pubkey(pubkeys[0])
        if x_pubkeys:
            if len(x_pubkeys) > 0:
                return cls.estimate_pubkey_size_from_x_pubkey(x_pubkeys[0])
        return 33

    @classmethod
    def get_siglist(self, txin, estimate_size=False):
        if txin['type'] == 'coinbase':
            return ([], [])
        num_sig = txin.get('num_sig', 1)
        if estimate_size:
            pubkey_size = self.estimate_pubkey_size_for_txin(txin)
            pk_list = ['00' * pubkey_size] * len(txin.get('x_pubkeys', [None]))
            sig_list = [
             '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'] * num_sig
        else:
            pubkeys, x_pubkeys = self.get_sorted_pubkeys(txin)
            x_signatures = txin['signatures']
            signatures = list(filter(None, x_signatures))
            is_complete = len(signatures) == num_sig
            if is_complete:
                pk_list = pubkeys
                sig_list = signatures
            else:
                pk_list = x_pubkeys
                sig_list = [sig if sig else NO_SIGNATURE for sig in x_signatures]
        return (
         pk_list, sig_list)

    @classmethod
    def serialize_witness(self, txin, estimate_size=False):
        _type = txin['type']
        if not self.is_segwit_input(txin):
            if not txin['type'] == 'address':
                return '00'
        else:
            if _type == 'coinbase':
                return txin['witness']
            witness = txin.get('witness', None)
            if witness is None or estimate_size:
                if _type == 'address':
                    if estimate_size:
                        _type = self.guess_txintype_from_address(txin['address'])
                else:
                    pubkeys, sig_list = self.get_siglist(txin, estimate_size)
                    if _type in ('p2wpkh', 'p2wpkh-p2sh'):
                        witness = construct_witness([sig_list[0], pubkeys[0]])
                    else:
                        if _type in ('p2wsh', 'p2wsh-p2sh'):
                            witness_script = multisig_script(pubkeys, txin['num_sig'])
                            witness = construct_witness([0] + sig_list + [witness_script])
                        else:
                            witness = txin.get('witness', '00')
        if self.is_txin_complete(txin) or estimate_size:
            partial_format_witness_prefix = ''
        else:
            input_value = int_to_hex(txin['value'], 8)
            witness_version = int_to_hex(txin.get('witness_version', 0), 2)
            partial_format_witness_prefix = var_int(4294967295) + input_value + witness_version
        return partial_format_witness_prefix + witness

    @classmethod
    def is_segwit_input(cls, txin, guess_for_address=False):
        _type = txin['type']
        if _type == 'address':
            if guess_for_address:
                _type = cls.guess_txintype_from_address(txin['address'])
        has_nonzero_witness = txin.get('witness', '00') not in ('00', None)
        return is_segwit_script_type(_type) or has_nonzero_witness

    @classmethod
    def guess_txintype_from_address(cls, addr):
        witver, witprog = segwit_addr.decode(constants.net.SEGWIT_HRP, addr)
        if witprog is not None:
            return 'p2wpkh'
        addrtype, hash_160_ = b58_address_to_hash160(addr)
        if addrtype == constants.net.ADDRTYPE_P2PKH:
            return 'p2pkh'
        if addrtype == constants.net.ADDRTYPE_P2SH:
            return 'p2wpkh-p2sh'

    @classmethod
    def input_script(self, txin, estimate_size=False):
        _type = txin['type']
        if _type == 'coinbase':
            return txin['scriptSig']
        script_sig = txin.get('scriptSig', None)
        if script_sig is not None:
            if self.is_txin_complete(txin):
                return script_sig
        pubkeys, sig_list = self.get_siglist(txin, estimate_size)
        script = ''.join((push_script(x) for x in sig_list))
        if _type == 'address':
            if estimate_size:
                _type = self.guess_txintype_from_address(txin['address'])
        if _type == 'p2pk':
            pass
        elif _type == 'p2sh':
            script = '00' + script
            redeem_script = multisig_script(pubkeys, txin['num_sig'])
            script += push_script(redeem_script)
        else:
            if _type == 'p2pkh':
                script += push_script(pubkeys[0])
            else:
                if _type in ('p2wpkh', 'p2wsh'):
                    return ''
                else:
                    if _type == 'p2wpkh-p2sh':
                        pubkey = safe_parse_pubkey(pubkeys[0])
                        scriptSig = bitcoin.p2wpkh_nested_script(pubkey)
                        return push_script(scriptSig)
                        if _type == 'p2wsh-p2sh':
                            if estimate_size:
                                witness_script = ''
                    else:
                        witness_script = self.get_preimage_script(txin)
                    scriptSig = bitcoin.p2wsh_nested_script(witness_script)
                    return push_script(scriptSig)
                if _type == 'address':
                    return bytes([opcodes.OP_INVALIDOPCODE, opcodes.OP_0]).hex() + push_script(pubkeys[0])
                if _type == 'unknown':
                    return txin['scriptSig']
                return script

    @classmethod
    def is_txin_complete(cls, txin):
        if txin['type'] == 'coinbase':
            return True
        num_sig = txin.get('num_sig', 1)
        if num_sig == 0:
            return True
        x_signatures = txin['signatures']
        signatures = list(filter(None, x_signatures))
        return len(signatures) == num_sig

    @classmethod
    def get_preimage_script(self, txin):
        preimage_script = txin.get('preimage_script', None)
        if preimage_script is not None:
            return preimage_script
        else:
            pubkeys, x_pubkeys = self.get_sorted_pubkeys(txin)
            if txin['type'] in ('p2sh', 'p2wsh', 'p2wsh-p2sh'):
                result = multisig_script(pubkeys, txin['num_sig'])
            else:
                if txin['type'] in ('p2pkh', 'p2wpkh', 'p2wpkh-p2sh'):
                    pubkey = pubkeys[0]
                    pkh = bh2u(hash_160(bfh(pubkey)))
                    result = bitcoin.pubkeyhash_to_p2pkh_script(pkh)
                else:
                    if txin['type'] == 'p2pk':
                        pubkey = pubkeys[0]
                        result = bitcoin.public_key_to_p2pk_script(pubkey)
                    else:
                        raise TypeError('Unknown txin type', txin['type'])
        if txin['type'] in ('p2pkh', 'p2pk'):
            if 'name_op' in txin:
                if txin['name_op'] is not None:
                    result = name_op_to_script(txin['name_op']) + result
        return result

    @classmethod
    def serialize_outpoint(self, txin):
        return bh2u(bfh(txin['prevout_hash'])[::-1]) + int_to_hex(txin['prevout_n'], 4)

    @classmethod
    def get_outpoint_from_txin(cls, txin):
        if txin['type'] == 'coinbase':
            return
        prevout_hash = txin['prevout_hash']
        prevout_n = txin['prevout_n']
        return prevout_hash + ':%d' % prevout_n

    @classmethod
    def serialize_input(self, txin, script):
        s = self.serialize_outpoint(txin)
        s += var_int(len(script) // 2)
        s += script
        s += int_to_hex(txin.get('sequence', 4294967294), 4)
        return s

    def set_rbf(self, rbf):
        nSequence = 4294967295 - (2 if rbf else 1)
        for txin in self.inputs():
            txin['sequence'] = nSequence

    def BIP69_sort(self, inputs=True, outputs=True):
        if inputs:
            self._inputs.sort(key=(lambda i: (i['prevout_hash'], i['prevout_n'])))
        if outputs:
            self._outputs.sort(key=(lambda o: (o.value, self.pay_script(o.type, o.address, o.name_op))))

    @classmethod
    def serialize_output(cls, output: TxOutput) -> str:
        amount = output.value
        if output.name_op is not None:
            amount = amount + COIN // 100
        s = int_to_hex(amount, 8)
        script = cls.pay_script(output.type, output.address, output.name_op)
        s += var_int(len(script) // 2)
        s += script
        return s

    def _calc_bip143_shared_txdigest_fields(self) -> BIP143SharedTxDigestFields:
        inputs = self.inputs()
        outputs = self.outputs()
        hashPrevouts = bh2u(sha256d(bfh(''.join((self.serialize_outpoint(txin) for txin in inputs)))))
        hashSequence = bh2u(sha256d(bfh(''.join((int_to_hex(txin.get('sequence', 4294967294), 4) for txin in inputs)))))
        hashOutputs = bh2u(sha256d(bfh(''.join((self.serialize_output(o) for o in outputs)))))
        return BIP143SharedTxDigestFields(hashPrevouts=hashPrevouts, hashSequence=hashSequence,
          hashOutputs=hashOutputs)

    def serialize_preimage(self, txin_index: int, *, bip143_shared_txdigest_fields: BIP143SharedTxDigestFields=None) -> str:
        nVersion = int_to_hex(self.version, 4)
        nHashType = int_to_hex(1, 4)
        nLocktime = int_to_hex(self.locktime, 4)
        inputs = self.inputs()
        outputs = self.outputs()
        txin = inputs[txin_index]
        if self.is_segwit_input(txin):
            if bip143_shared_txdigest_fields is None:
                bip143_shared_txdigest_fields = self._calc_bip143_shared_txdigest_fields()
            hashPrevouts = bip143_shared_txdigest_fields.hashPrevouts
            hashSequence = bip143_shared_txdigest_fields.hashSequence
            hashOutputs = bip143_shared_txdigest_fields.hashOutputs
            outpoint = self.serialize_outpoint(txin)
            preimage_script = self.get_preimage_script(txin)
            scriptCode = var_int(len(preimage_script) // 2) + preimage_script
            txin_value = txin['value']
            if 'name_op' in txin:
                if txin['name_op'] is not None:
                    txin_value += COIN // 100
            amount = int_to_hex(txin_value, 8)
            nSequence = int_to_hex(txin.get('sequence', 4294967294), 4)
            preimage = nVersion + hashPrevouts + hashSequence + outpoint + scriptCode + amount + nSequence + hashOutputs + nLocktime + nHashType
        else:
            txins = var_int(len(inputs)) + ''.join((self.serialize_input(txin, self.get_preimage_script(txin) if txin_index == k else '') for k, txin in enumerate(inputs)))
            txouts = var_int(len(outputs)) + ''.join((self.serialize_output(o) for o in outputs))
            preimage = nVersion + txins + txouts + nLocktime + nHashType
        return preimage

    def is_segwit(self, guess_for_address=False):
        if not self.is_partial_originally:
            return self._segwit_ser
        return any((self.is_segwit_input(x, guess_for_address=guess_for_address) for x in self.inputs()))

    def serialize(self, estimate_size=False, witness=True):
        network_ser = self.serialize_to_network(estimate_size, witness)
        if estimate_size:
            return network_ser
        if self.is_partial_originally:
            if not self.is_complete():
                partial_format_version = '00'
                return bh2u(PARTIAL_TXN_HEADER_MAGIC) + partial_format_version + network_ser
        return network_ser

    def serialize_to_network(self, estimate_size=False, witness=True):
        self.deserialize()
        nVersion = int_to_hex(self.version, 4)
        nLocktime = int_to_hex(self.locktime, 4)
        inputs = self.inputs()
        outputs = self.outputs()
        txins = var_int(len(inputs)) + ''.join((self.serialize_input(txin, self.input_script(txin, estimate_size)) for txin in inputs))
        txouts = var_int(len(outputs)) + ''.join((self.serialize_output(o) for o in outputs))
        use_segwit_ser_for_estimate_size = estimate_size and self.is_segwit(guess_for_address=True)
        use_segwit_ser_for_actual_use = not estimate_size and (self.is_segwit() or any((txin['type'] == 'address' for txin in inputs)))
        use_segwit_ser = use_segwit_ser_for_estimate_size or use_segwit_ser_for_actual_use
        if witness:
            if use_segwit_ser:
                marker = '00'
                flag = '01'
                witness = ''.join((self.serialize_witness(x, estimate_size) for x in inputs))
                return nVersion + marker + flag + txins + txouts + witness + nLocktime
        return nVersion + txins + txouts + nLocktime

    def txid(self):
        self.deserialize()
        all_segwit = all((self.is_segwit_input(x) for x in self.inputs()))
        if not all_segwit:
            if not self.is_complete():
                return
        ser = self.serialize_to_network(witness=False)
        return bh2u(sha256d(bfh(ser))[::-1])

    def wtxid(self):
        self.deserialize()
        if not self.is_complete():
            return
        ser = self.serialize_to_network(witness=True)
        return bh2u(sha256d(bfh(ser))[::-1])

    def add_inputs(self, inputs):
        self._inputs.extend(inputs)
        self.raw = None
        self.BIP69_sort(outputs=False)

    def add_outputs(self, outputs):
        self._outputs.extend(outputs)
        self.raw = None
        self.BIP69_sort(inputs=False)

    def input_value(self) -> int:
        return sum((x['value'] for x in self.inputs()))

    def output_value(self) -> int:
        newly_locked_amount = 0
        for o in self.outputs():
            if o.name_op is None:
                continue
            if o.name_op['op'] == OP_NAME_REGISTER:
                newly_locked_amount += COIN // 100

        return newly_locked_amount + sum((o.value for o in self.outputs()))

    def get_fee(self) -> int:
        return self.input_value() - self.output_value()

    def is_final(self):
        return not any([x.get('sequence', 4294967294) < 4294967294 for x in self.inputs()])

    def estimated_size(self):
        """Return an estimated virtual tx size in vbytes.
        BIP-0141 defines 'Virtual transaction size' to be weight/4 rounded up.
        This definition is only for humans, and has little meaning otherwise.
        If we wanted sub-byte precision, fee calculation should use transaction
        weights, but for simplicity we approximate that with (virtual_size)x4
        """
        weight = self.estimated_weight()
        return self.virtual_size_from_weight(weight)

    @classmethod
    def estimated_input_weight(cls, txin, is_segwit_tx):
        """Return an estimate of serialized input weight in weight units."""
        script = cls.input_script(txin, True)
        input_size = len(cls.serialize_input(txin, script)) // 2
        if cls.is_segwit_input(txin, guess_for_address=True):
            witness_size = len(cls.serialize_witness(txin, True)) // 2
        else:
            witness_size = 1 if is_segwit_tx else 0
        return 4 * input_size + witness_size

    @classmethod
    def estimated_output_size(cls, address):
        """Return an estimate of serialized output size in bytes."""
        script = bitcoin.address_to_script(address)
        return 9 + len(script) // 2

    @classmethod
    def virtual_size_from_weight(cls, weight):
        return weight // 4 + (weight % 4 > 0)

    def estimated_total_size(self):
        """Return an estimated total transaction size in bytes."""
        if not self.is_complete() or self.raw is None:
            return len(self.serialize(True)) // 2
        return len(self.raw) // 2

    def estimated_witness_size(self):
        """Return an estimate of witness size in bytes."""
        estimate = not self.is_complete()
        if not self.is_segwit(guess_for_address=estimate):
            return 0
        inputs = self.inputs()
        witness = ''.join((self.serialize_witness(x, estimate) for x in inputs))
        witness_size = len(witness) // 2 + 2
        return witness_size

    def estimated_base_size(self):
        """Return an estimated base transaction size in bytes."""
        return self.estimated_total_size() - self.estimated_witness_size()

    def estimated_weight(self):
        """Return an estimate of transaction weight."""
        total_tx_size = self.estimated_total_size()
        base_tx_size = self.estimated_base_size()
        return 3 * base_tx_size + total_tx_size

    def signature_count(self):
        r = 0
        s = 0
        for txin in self.inputs():
            if txin['type'] == 'coinbase':
                continue
            signatures = list(filter(None, txin.get('signatures', [])))
            s += len(signatures)
            r += txin.get('num_sig', -1)

        return (
         s, r)

    def is_complete(self):
        s, r = self.signature_count()
        return r == s

    def sign(self, keypairs) -> None:
        bip143_shared_txdigest_fields = self._calc_bip143_shared_txdigest_fields()
        for i, txin in enumerate(self.inputs()):
            pubkeys, x_pubkeys = self.get_sorted_pubkeys(txin)
            for j, (pubkey, x_pubkey) in enumerate(zip(pubkeys, x_pubkeys)):
                if self.is_txin_complete(txin):
                    break
                if pubkey in keypairs:
                    _pubkey = pubkey
                else:
                    if x_pubkey in keypairs:
                        _pubkey = x_pubkey
                    else:
                        continue
                    _logger.info(f"adding signature for {_pubkey}")
                    sec, compressed = keypairs.get(_pubkey)
                    sig = self.sign_txin(i, sec, bip143_shared_txdigest_fields=bip143_shared_txdigest_fields)
                    self.add_signature_to_txin(i, j, sig)

        _logger.info(f"is_complete {self.is_complete()}")
        self.raw = self.serialize()

    def sign_txin(self, txin_index, privkey_bytes, *, bip143_shared_txdigest_fields=None) -> str:
        pre_hash = sha256d(bfh(self.serialize_preimage(txin_index, bip143_shared_txdigest_fields=bip143_shared_txdigest_fields)))
        privkey = ecc.ECPrivkey(privkey_bytes)
        sig = privkey.sign_transaction(pre_hash)
        sig = bh2u(sig) + '01'
        return sig

    def get_outputs_for_UI(self) -> Sequence[TxOutputForUI]:
        outputs = []
        for o in self.outputs():
            if o.type == TYPE_ADDRESS:
                addr = o.address
            else:
                if o.type == TYPE_PUBKEY:
                    addr = 'PUBKEY ' + o.address
                else:
                    addr = 'SCRIPT ' + o.address
            outputs.append(TxOutputForUI(addr, o.value, o.name_op))

        return outputs

    def has_address(self, addr: str) -> bool:
        return addr in (o.address for o in self.outputs()) or addr in (txin.get('address') for txin in self.inputs())

    def as_dict(self):
        if self.raw is None:
            self.raw = self.serialize()
        self.deserialize()
        out = {'hex':self.raw, 
         'complete':self.is_complete(), 
         'final':self.is_final()}
        return out


def tx_from_str(txt: str) -> str:
    """Sanitizes tx-describing input (json or raw hex or base43) into
    raw hex transaction."""
    if not isinstance(txt, str):
        raise AssertionError(f"txt must be str, not {type(txt)}")
    else:
        txt = txt.strip()
        if not txt:
            raise ValueError('empty string')
        try:
            bfh(txt)
            return txt
        except:
            pass

    try:
        return base_decode(txt, length=None, base=43).hex()
    except:
        pass

    import json
    tx_dict = json.loads(str(txt))
    assert 'hex' in tx_dict.keys()
    return tx_dict['hex']


from .names import get_name_op_from_output_script, name_op_to_script, OP_NAME_REGISTER, split_name_script