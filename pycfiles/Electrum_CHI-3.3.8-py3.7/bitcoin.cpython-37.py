# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/bitcoin.py
# Compiled at: 2019-08-25 05:38:52
# Size of source mod 2**32: 19889 bytes
import hashlib
from typing import List, Tuple, TYPE_CHECKING, Optional, Union
from enum import IntEnum
from .util import bfh, bh2u, BitcoinException, assert_bytes, to_bytes, inv_dict
from . import version
from . import segwit_addr
from . import constants
from . import ecc
from .crypto import sha256d, sha256, hash_160, hmac_oneshot
if TYPE_CHECKING:
    from .network import Network
COINBASE_MATURITY = 100
COIN = 100000000
TOTAL_COIN_SUPPLY_LIMIT_IN_BTC = 555555555
TYPE_ADDRESS = 0
TYPE_PUBKEY = 1
TYPE_SCRIPT = 2

class opcodes(IntEnum):
    OP_0 = 0
    OP_FALSE = OP_0
    OP_PUSHDATA1 = 76
    OP_PUSHDATA2 = 77
    OP_PUSHDATA4 = 78
    OP_1NEGATE = 79
    OP_RESERVED = 80
    OP_1 = 81
    OP_TRUE = OP_1
    OP_2 = 82
    OP_3 = 83
    OP_4 = 84
    OP_5 = 85
    OP_6 = 86
    OP_7 = 87
    OP_8 = 88
    OP_9 = 89
    OP_10 = 90
    OP_11 = 91
    OP_12 = 92
    OP_13 = 93
    OP_14 = 94
    OP_15 = 95
    OP_16 = 96
    OP_NOP = 97
    OP_VER = 98
    OP_IF = 99
    OP_NOTIF = 100
    OP_VERIF = 101
    OP_VERNOTIF = 102
    OP_ELSE = 103
    OP_ENDIF = 104
    OP_VERIFY = 105
    OP_RETURN = 106
    OP_TOALTSTACK = 107
    OP_FROMALTSTACK = 108
    OP_2DROP = 109
    OP_2DUP = 110
    OP_3DUP = 111
    OP_2OVER = 112
    OP_2ROT = 113
    OP_2SWAP = 114
    OP_IFDUP = 115
    OP_DEPTH = 116
    OP_DROP = 117
    OP_DUP = 118
    OP_NIP = 119
    OP_OVER = 120
    OP_PICK = 121
    OP_ROLL = 122
    OP_ROT = 123
    OP_SWAP = 124
    OP_TUCK = 125
    OP_CAT = 126
    OP_SUBSTR = 127
    OP_LEFT = 128
    OP_RIGHT = 129
    OP_SIZE = 130
    OP_INVERT = 131
    OP_AND = 132
    OP_OR = 133
    OP_XOR = 134
    OP_EQUAL = 135
    OP_EQUALVERIFY = 136
    OP_RESERVED1 = 137
    OP_RESERVED2 = 138
    OP_1ADD = 139
    OP_1SUB = 140
    OP_2MUL = 141
    OP_2DIV = 142
    OP_NEGATE = 143
    OP_ABS = 144
    OP_NOT = 145
    OP_0NOTEQUAL = 146
    OP_ADD = 147
    OP_SUB = 148
    OP_MUL = 149
    OP_DIV = 150
    OP_MOD = 151
    OP_LSHIFT = 152
    OP_RSHIFT = 153
    OP_BOOLAND = 154
    OP_BOOLOR = 155
    OP_NUMEQUAL = 156
    OP_NUMEQUALVERIFY = 157
    OP_NUMNOTEQUAL = 158
    OP_LESSTHAN = 159
    OP_GREATERTHAN = 160
    OP_LESSTHANOREQUAL = 161
    OP_GREATERTHANOREQUAL = 162
    OP_MIN = 163
    OP_MAX = 164
    OP_WITHIN = 165
    OP_RIPEMD160 = 166
    OP_SHA1 = 167
    OP_SHA256 = 168
    OP_HASH160 = 169
    OP_HASH256 = 170
    OP_CODESEPARATOR = 171
    OP_CHECKSIG = 172
    OP_CHECKSIGVERIFY = 173
    OP_CHECKMULTISIG = 174
    OP_CHECKMULTISIGVERIFY = 175
    OP_NOP1 = 176
    OP_CHECKLOCKTIMEVERIFY = 177
    OP_NOP2 = OP_CHECKLOCKTIMEVERIFY
    OP_CHECKSEQUENCEVERIFY = 178
    OP_NOP3 = OP_CHECKSEQUENCEVERIFY
    OP_NOP4 = 179
    OP_NOP5 = 180
    OP_NOP6 = 181
    OP_NOP7 = 182
    OP_NOP8 = 183
    OP_NOP9 = 184
    OP_NOP10 = 185
    OP_INVALIDOPCODE = 255

    def hex(self) -> str:
        return bytes([self]).hex()


def rev_hex(s: str) -> str:
    return bh2u(bfh(s)[::-1])


def int_to_hex(i: int, length: int=1) -> str:
    """Converts int to little-endian hex string.
    `length` is the number of bytes available
    """
    if not isinstance(i, int):
        raise TypeError('{} instead of int'.format(i))
    range_size = pow(256, length)
    if i < -(range_size // 2) or i >= range_size:
        raise OverflowError('cannot convert int {} to hex ({} bytes)'.format(i, length))
    if i < 0:
        i = range_size + i
    s = hex(i)[2:].rstrip('L')
    s = '0' * (2 * length - len(s)) + s
    return rev_hex(s)


def script_num_to_hex(i: int) -> str:
    """See CScriptNum in Bitcoin Core.
    Encodes an integer as hex, to be used in script.

    ported from https://github.com/bitcoin/bitcoin/blob/8cbc5c4be4be22aca228074f087a374a7ec38be8/src/script/script.h#L326
    """
    if i == 0:
        return ''
    else:
        result = bytearray()
        neg = i < 0
        absvalue = abs(i)
        while absvalue > 0:
            result.append(absvalue & 255)
            absvalue >>= 8

        if result[(-1)] & 128:
            result.append(128 if neg else 0)
        else:
            if neg:
                result[(-1)] |= 128
    return bh2u(result)


def var_int(i: int) -> str:
    if i < 253:
        return int_to_hex(i)
    if i <= 65535:
        return 'fd' + int_to_hex(i, 2)
    if i <= 4294967295:
        return 'fe' + int_to_hex(i, 4)
    return 'ff' + int_to_hex(i, 8)


def witness_push(item: str) -> str:
    """Returns data in the form it should be present in the witness.
    hex -> hex
    """
    return var_int(len(item) // 2) + item


def _op_push(i: int) -> str:
    if i < opcodes.OP_PUSHDATA1:
        return int_to_hex(i)
    if i <= 255:
        return opcodes.OP_PUSHDATA1.hex() + int_to_hex(i, 1)
    if i <= 65535:
        return opcodes.OP_PUSHDATA2.hex() + int_to_hex(i, 2)
    return opcodes.OP_PUSHDATA4.hex() + int_to_hex(i, 4)


def push_script(data: str) -> str:
    """Returns pushed data to the script, automatically
    choosing canonical opcodes depending on the length of the data.
    hex -> hex

    ported from https://github.com/btcsuite/btcd/blob/fdc2bc867bda6b351191b5872d2da8270df00d13/txscript/scriptbuilder.go#L128
    """
    data = bfh(data)
    data_len = len(data)
    if (data_len == 0 or data_len) == 1:
        if data[0] == 0:
            return opcodes.OP_0.hex()
    if data_len == 1:
        if data[0] <= 16:
            return bh2u(bytes([opcodes.OP_1 - 1 + data[0]]))
    if data_len == 1:
        if data[0] == 129:
            return opcodes.OP_1NEGATE.hex()
    return _op_push(data_len) + bh2u(data)


def add_number_to_script(i: int) -> bytes:
    return bfh(push_script(script_num_to_hex(i)))


def relayfee(network: 'Network'=None) -> int:
    from .simple_config import FEERATE_DEFAULT_RELAY
    MAX_RELAY_FEE = 50000
    f = network.relay_fee if (network and network.relay_fee) else FEERATE_DEFAULT_RELAY
    return min(f, MAX_RELAY_FEE)


def dust_threshold(network: 'Network'=None) -> int:
    return 546 * relayfee(network) // 1000


def hash_encode(x: bytes) -> str:
    return bh2u(x[::-1])


def hash_decode(x: str) -> bytes:
    return bfh(x)[::-1]


def hash160_to_b58_address(h160: bytes, addrtype: int) -> str:
    s = bytes([addrtype]) + h160
    s = s + sha256d(s)[0:4]
    return base_encode(s, base=58)


def b58_address_to_hash160(addr: str) -> Tuple[(int, bytes)]:
    addr = to_bytes(addr, 'ascii')
    _bytes = base_decode(addr, 25, base=58)
    return (_bytes[0], _bytes[1:21])


def hash160_to_p2pkh(h160: bytes, *, net=None) -> str:
    if net is None:
        net = constants.net
    return hash160_to_b58_address(h160, net.ADDRTYPE_P2PKH)


def hash160_to_p2sh(h160: bytes, *, net=None) -> str:
    if net is None:
        net = constants.net
    return hash160_to_b58_address(h160, net.ADDRTYPE_P2SH)


def public_key_to_p2pkh(public_key: bytes, *, net=None) -> str:
    if net is None:
        net = constants.net
    return hash160_to_p2pkh((hash_160(public_key)), net=net)


def hash_to_segwit_addr(h: bytes, witver: int, *, net=None) -> str:
    if net is None:
        net = constants.net
    return segwit_addr.encode(net.SEGWIT_HRP, witver, h)


def public_key_to_p2wpkh(public_key: bytes, *, net=None) -> str:
    if net is None:
        net = constants.net
    return hash_to_segwit_addr((hash_160(public_key)), witver=0, net=net)


def script_to_p2wsh(script: str, *, net=None) -> str:
    if net is None:
        net = constants.net
    return hash_to_segwit_addr((sha256(bfh(script))), witver=0, net=net)


def p2wpkh_nested_script(pubkey: str) -> str:
    pkh = bh2u(hash_160(bfh(pubkey)))
    return '00' + push_script(pkh)


def p2wsh_nested_script(witness_script: str) -> str:
    wsh = bh2u(sha256(bfh(witness_script)))
    return '00' + push_script(wsh)


def pubkey_to_address(txin_type: str, pubkey: str, *, net=None) -> str:
    if net is None:
        net = constants.net
    if txin_type == 'p2pkh':
        return public_key_to_p2pkh((bfh(pubkey)), net=net)
    if txin_type == 'p2wpkh':
        return public_key_to_p2wpkh((bfh(pubkey)), net=net)
    if txin_type == 'p2wpkh-p2sh':
        scriptSig = p2wpkh_nested_script(pubkey)
        return hash160_to_p2sh((hash_160(bfh(scriptSig))), net=net)
    raise NotImplementedError(txin_type)


def redeem_script_to_address(txin_type: str, redeem_script: str, *, net=None) -> str:
    if net is None:
        net = constants.net
    if txin_type == 'p2sh':
        return hash160_to_p2sh((hash_160(bfh(redeem_script))), net=net)
    if txin_type == 'p2wsh':
        return script_to_p2wsh(redeem_script, net=net)
    if txin_type == 'p2wsh-p2sh':
        scriptSig = p2wsh_nested_script(redeem_script)
        return hash160_to_p2sh((hash_160(bfh(scriptSig))), net=net)
    raise NotImplementedError(txin_type)


def script_to_address(script: str, *, net=None) -> str:
    from .transaction import get_address_from_output_script
    t, addr = get_address_from_output_script((bfh(script)), net=net)
    assert t == TYPE_ADDRESS
    return addr


def address_to_script(addr: str, *, net=None) -> str:
    if net is None:
        net = constants.net
    elif not is_address(addr, net=net):
        raise BitcoinException(f"invalid address: {addr}")
    else:
        witver, witprog = segwit_addr.decode(net.SEGWIT_HRP, addr)
        if witprog is not None:
            if not 0 <= witver <= 16:
                raise BitcoinException(f"impossible witness version: {witver}")
            script = bh2u(add_number_to_script(witver))
            script += push_script(bh2u(bytes(witprog)))
            return script
            addrtype, hash_160_ = b58_address_to_hash160(addr)
            if addrtype == net.ADDRTYPE_P2PKH:
                script = pubkeyhash_to_p2pkh_script(bh2u(hash_160_))
        elif addrtype == net.ADDRTYPE_P2SH:
            script = opcodes.OP_HASH160.hex()
            script += push_script(bh2u(hash_160_))
            script += opcodes.OP_EQUAL.hex()
        else:
            raise BitcoinException(f"unknown address type: {addrtype}")
    return script


def address_to_scripthash(addr: str) -> str:
    script = address_to_script(addr)
    return script_to_scripthash(script)


def script_to_scripthash(script: str) -> str:
    h = sha256(bfh(script))[0:32]
    return bh2u(bytes(reversed(h)))


def public_key_to_p2pk_script(pubkey: str) -> str:
    return push_script(pubkey) + opcodes.OP_CHECKSIG.hex()


def pubkeyhash_to_p2pkh_script(pubkey_hash160: str) -> str:
    script = bytes([opcodes.OP_DUP, opcodes.OP_HASH160]).hex()
    script += push_script(pubkey_hash160)
    script += bytes([opcodes.OP_EQUALVERIFY, opcodes.OP_CHECKSIG]).hex()
    return script


__b58chars = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
assert len(__b58chars) == 58
__b43chars = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'
assert len(__b43chars) == 43

def base_encode(v: bytes, base: int) -> str:
    """ encode v, which is a string of bytes, to base58."""
    assert_bytes(v)
    if base not in (58, 43):
        raise ValueError('not supported base: {}'.format(base))
    chars = __b58chars
    if base == 43:
        chars = __b43chars
    long_value = 0
    for i, c in enumerate(v[::-1]):
        long_value += 256 ** i * c

    result = bytearray()
    while long_value >= base:
        div, mod = divmod(long_value, base)
        result.append(chars[mod])
        long_value = div

    result.append(chars[long_value])
    nPad = 0
    for c in v:
        if c == 0:
            nPad += 1
        else:
            break

    result.extend([chars[0]] * nPad)
    result.reverse()
    return result.decode('ascii')


def base_decode(v: Union[(bytes, str)], length: Optional[int], base: int) -> Optional[bytes]:
    """ decode v into a string of len bytes."""
    v = to_bytes(v, 'ascii')
    if base not in (58, 43):
        raise ValueError('not supported base: {}'.format(base))
    chars = __b58chars
    if base == 43:
        chars = __b43chars
    long_value = 0
    for i, c in enumerate(v[::-1]):
        digit = chars.find(bytes([c]))
        if digit == -1:
            raise ValueError('Forbidden character {} for base {}'.format(c, base))
        long_value += digit * base ** i

    result = bytearray()
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result.append(mod)
        long_value = div

    result.append(long_value)
    nPad = 0
    for c in v:
        if c == chars[0]:
            nPad += 1
        else:
            break

    result.extend(b'\x00' * nPad)
    if length is not None:
        if len(result) != length:
            return
    result.reverse()
    return bytes(result)


class InvalidChecksum(Exception):
    pass


def EncodeBase58Check(vchIn: bytes) -> str:
    hash = sha256d(vchIn)
    return base_encode((vchIn + hash[0:4]), base=58)


def DecodeBase58Check(psz: Union[(bytes, str)]) -> bytes:
    vchRet = base_decode(psz, None, base=58)
    payload = vchRet[0:-4]
    csum_found = vchRet[-4:]
    csum_calculated = sha256d(payload)[0:4]
    if csum_calculated != csum_found:
        raise InvalidChecksum(f"calculated {bh2u(csum_calculated)}, found {bh2u(csum_found)}")
    else:
        return payload


WIF_SCRIPT_TYPES = {'p2pkh':0, 
 'p2wpkh':1, 
 'p2wpkh-p2sh':2, 
 'p2sh':5, 
 'p2wsh':6, 
 'p2wsh-p2sh':7}
WIF_SCRIPT_TYPES_INV = inv_dict(WIF_SCRIPT_TYPES)

def is_segwit_script_type(txin_type: str) -> bool:
    return txin_type in ('p2wpkh', 'p2wpkh-p2sh', 'p2wsh', 'p2wsh-p2sh')


def serialize_privkey(secret: bytes, compressed: bool, txin_type: str, internal_use: bool=False) -> str:
    secret = ecc.ECPrivkey.normalize_secret_bytes(secret)
    if internal_use:
        prefix = bytes([WIF_SCRIPT_TYPES[txin_type] + constants.net.WIF_PREFIX & 255])
    else:
        prefix = bytes([constants.net.WIF_PREFIX])
    suffix = b'\x01' if compressed else b''
    vchIn = prefix + secret + suffix
    base58_wif = EncodeBase58Check(vchIn)
    if internal_use:
        return base58_wif
    return '{}:{}'.format(txin_type, base58_wif)


def deserialize_privkey(key: str) -> Tuple[(str, bytes, bool)]:
    if is_minikey(key):
        return (
         'p2pkh', minikey_to_private_key(key), False)
        txin_type = None
        if ':' in key:
            txin_type, key = key.split(sep=':', maxsplit=1)
            if txin_type not in WIF_SCRIPT_TYPES:
                raise BitcoinException('unknown script type: {}'.format(txin_type))
    else:
        try:
            vch = DecodeBase58Check(key)
        except BaseException:
            neutered_privkey = str(key)[:3] + '..' + str(key)[-2:]
            raise BitcoinException('cannot deserialize privkey {}'.format(neutered_privkey))

    if txin_type is None:
        prefix_value = vch[0] - constants.net.WIF_PREFIX
        try:
            txin_type = WIF_SCRIPT_TYPES_INV[prefix_value]
        except KeyError:
            raise BitcoinException('invalid prefix ({}) for WIF key (1)'.format(vch[0]))

    else:
        if vch[0] != constants.net.WIF_PREFIX:
            raise BitcoinException('invalid prefix ({}) for WIF key (2)'.format(vch[0]))
        else:
            if len(vch) not in (33, 34):
                raise BitcoinException('invalid vch len for WIF key: {}'.format(len(vch)))
            else:
                compressed = False
                if len(vch) == 34:
                    if vch[33] == 1:
                        compressed = True
                    else:
                        raise BitcoinException(f"invalid WIF key. length suggests compressed pubkey, but last byte is {vch[33]} != 0x01")
            if is_segwit_script_type(txin_type) and not compressed:
                raise BitcoinException('only compressed public keys can be used in segwit scripts')
        secret_bytes = vch[1:33]
        secret_bytes = ecc.ECPrivkey.normalize_secret_bytes(secret_bytes)
        return (txin_type, secret_bytes, compressed)


def is_compressed_privkey(sec: str) -> bool:
    return deserialize_privkey(sec)[2]


def address_from_private_key(sec: str) -> str:
    txin_type, privkey, compressed = deserialize_privkey(sec)
    public_key = ecc.ECPrivkey(privkey).get_public_key_hex(compressed=compressed)
    return pubkey_to_address(txin_type, public_key)


def is_segwit_address(addr: str, *, net=None) -> bool:
    if net is None:
        net = constants.net
    try:
        witver, witprog = segwit_addr.decode(net.SEGWIT_HRP, addr)
    except Exception as e:
        try:
            return False
        finally:
            e = None
            del e

    return witprog is not None


def is_b58_address(addr: str, *, net=None) -> bool:
    if net is None:
        net = constants.net
    try:
        addrtype, h = b58_address_to_hash160(addr)
    except Exception as e:
        try:
            return False
        finally:
            e = None
            del e

    if addrtype not in [net.ADDRTYPE_P2PKH, net.ADDRTYPE_P2SH]:
        return False
    return addr == hash160_to_b58_address(h, addrtype)


def is_address(addr: str, *, net=None) -> bool:
    if net is None:
        net = constants.net
    return is_segwit_address(addr, net=net) or is_b58_address(addr, net=net)


def is_private_key(key: str, *, raise_on_error=False) -> bool:
    try:
        deserialize_privkey(key)
        return True
    except BaseException as e:
        try:
            if raise_on_error:
                raise
            return False
        finally:
            e = None
            del e


def is_minikey(text: str) -> bool:
    return len(text) >= 20 and text[0] == 'S' and all((ord(c) in __b58chars for c in text)) and sha256(text + '?')[0] == 0


def minikey_to_private_key(text: str) -> bytes:
    return sha256(text)