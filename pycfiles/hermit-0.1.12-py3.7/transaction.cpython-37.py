# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitcointools/transaction.py
# Compiled at: 2018-12-04 13:59:45
# Size of source mod 2**32: 17150 bytes
import binascii, re, json, copy, sys
from pybitcointools.main import *
from _functools import reduce

def json_is_base(obj, base):
    if not is_python2:
        if isinstance(obj, bytes):
            return False
    alpha = get_code_string(base)
    if isinstance(obj, string_types):
        for i in range(len(obj)):
            if alpha.find(obj[i]) == -1:
                return False

        return True
    if isinstance(obj, int_types) or obj is None:
        return True
    if isinstance(obj, list):
        for i in range(len(obj)):
            if not json_is_base(obj[i], base):
                return False

        return True
    for x in obj:
        if not json_is_base(obj[x], base):
            return False

    return True


def json_changebase(obj, changer):
    if isinstance(obj, string_or_bytes_types):
        return changer(obj)
    if isinstance(obj, int_types) or obj is None:
        return obj
    if isinstance(obj, list):
        return [json_changebase(x, changer) for x in obj]
    return dict(((x, json_changebase(obj[x], changer)) for x in obj))


def deserialize(tx):
    if isinstance(tx, str):
        if re.match('^[0-9a-fA-F]*$', tx):
            return json_changebase(deserialize(binascii.unhexlify(tx)), lambda x: safe_hexlify(x))
    pos = [
     0]

    def read_as_int(bytez):
        pos[0] += bytez
        return decode(tx[pos[0] - bytez:pos[0]][::-1], 256)

    def read_var_int():
        pos[0] += 1
        val = from_byte_to_int(tx[(pos[0] - 1)])
        if val < 253:
            return val
        return read_as_int(pow(2, val - 252))

    def read_bytes(bytez):
        pos[0] += bytez
        return tx[pos[0] - bytez:pos[0]]

    def read_var_string():
        size = read_var_int()
        return read_bytes(size)

    obj = {'ins':[],  'outs':[]}
    obj['version'] = read_as_int(4)
    ins = read_var_int()
    for i in range(ins):
        obj['ins'].append({'outpoint':{'hash':read_bytes(32)[::-1], 
          'index':read_as_int(4)}, 
         'script':read_var_string(), 
         'sequence':read_as_int(4)})

    outs = read_var_int()
    for i in range(outs):
        obj['outs'].append({'value':read_as_int(8), 
         'script':read_var_string()})

    obj['locktime'] = read_as_int(4)
    return obj


def serialize(txobj):
    o = []
    if json_is_base(txobj, 16):
        json_changedbase = json_changebase(txobj, lambda x: binascii.unhexlify(x))
        hexlified = safe_hexlify(serialize(json_changedbase))
        return hexlified
    o.append(encode(txobj['version'], 256, 4)[::-1])
    o.append(num_to_var_int(len(txobj['ins'])))
    for inp in txobj['ins']:
        o.append(inp['outpoint']['hash'][::-1])
        o.append(encode(inp['outpoint']['index'], 256, 4)[::-1])
        o.append(num_to_var_int(len(inp['script'])) + inp['script'] if (inp['script'] or is_python2) else (bytes()))
        o.append(encode(inp['sequence'], 256, 4)[::-1])

    o.append(num_to_var_int(len(txobj['outs'])))
    for out in txobj['outs']:
        o.append(encode(out['value'], 256, 8)[::-1])
        o.append(num_to_var_int(len(out['script'])) + out['script'])

    o.append(encode(txobj['locktime'], 256, 4)[::-1])
    if is_python2:
        return ''.join(o)
    return reduce(lambda x, y: x + y, o, bytes())


SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 129

def signature_form(tx, i, script, hashcode=SIGHASH_ALL):
    i, hashcode = int(i), int(hashcode)
    if isinstance(tx, string_or_bytes_types):
        return serialize(signature_form(deserialize(tx), i, script, hashcode))
    newtx = copy.deepcopy(tx)
    for inp in newtx['ins']:
        inp['script'] = ''

    newtx['ins'][i]['script'] = script
    if hashcode == SIGHASH_NONE:
        newtx['outs'] = []
    else:
        if hashcode == SIGHASH_SINGLE:
            newtx['outs'] = newtx['outs'][:len(newtx['ins'])]
            for out in newtx['outs'][:len(newtx['ins']) - 1]:
                out['value'] = 18446744073709551615
                out['script'] = ''

        else:
            if hashcode == SIGHASH_ANYONECANPAY:
                newtx['ins'] = [
                 newtx['ins'][i]]
            else:
                return newtx


def der_encode_sig(v, r, s):
    b1, b2 = safe_hexlify(encode(r, 256)), safe_hexlify(encode(s, 256))
    if len(b1):
        if b1[0] in '89abcdef':
            b1 = '00' + b1
    if len(b2):
        if b2[0] in '89abcdef':
            b2 = '00' + b2
    left = '02' + encode(len(b1) // 2, 16, 2) + b1
    right = '02' + encode(len(b2) // 2, 16, 2) + b2
    return '30' + encode(len(left + right) // 2, 16, 2) + left + right


def der_decode_sig(sig):
    leftlen = decode(sig[6:8], 16) * 2
    left = sig[8:8 + leftlen]
    rightlen = decode(sig[10 + leftlen:12 + leftlen], 16) * 2
    right = sig[12 + leftlen:12 + leftlen + rightlen]
    return (None, decode(left, 16), decode(right, 16))


def is_bip66(sig):
    """Checks hex DER sig for BIP66 consistency"""
    sig = bytearray.fromhex(sig) if re.match('^[0-9a-fA-F]*$', sig) else bytearray(sig)
    if sig[0] == 48:
        if sig[1] == len(sig) - 2:
            sig.extend(b'\x01')
    if len(sig) < 9 or len(sig) > 73:
        return False
    if sig[0] != 48:
        return False
    if sig[1] != len(sig) - 3:
        return False
    rlen = sig[3]
    if 5 + rlen >= len(sig):
        return False
    slen = sig[(5 + rlen)]
    if rlen + slen + 7 != len(sig):
        return False
    if sig[2] != 2:
        return False
    if rlen == 0:
        return False
    if sig[4] & 128:
        return False
    if rlen > 1:
        if sig[4] == 0:
            if not sig[5] & 128:
                return False
    if sig[(4 + rlen)] != 2:
        return False
    if slen == 0:
        return False
    if sig[(rlen + 6)] & 128:
        return False
    if slen > 1:
        if sig[(6 + rlen)] == 0:
            if not sig[(7 + rlen)] & 128:
                return False
    return True


def txhash(tx, hashcode=None):
    if isinstance(tx, str):
        if re.match('^[0-9a-fA-F]*$', tx):
            tx = changebase(tx, 16, 256)
    if hashcode:
        return dbl_sha256(from_string_to_bytes(tx) + encode(int(hashcode), 256, 4)[::-1])
    return safe_hexlify(bin_dbl_sha256(tx)[::-1])


def bin_txhash(tx, hashcode=None):
    return binascii.unhexlify(txhash(tx, hashcode))


def ecdsa_tx_sign(tx, priv, hashcode=SIGHASH_ALL):
    rawsig = ecdsa_raw_sign(bin_txhash(tx, hashcode), priv)
    return der_encode_sig(*rawsig) + encode(hashcode, 16, 2)


def ecdsa_tx_verify(tx, sig, pub, hashcode=SIGHASH_ALL):
    return ecdsa_raw_verify(bin_txhash(tx, hashcode), der_decode_sig(sig), pub)


def ecdsa_tx_recover(tx, sig, hashcode=SIGHASH_ALL):
    z = bin_txhash(tx, hashcode)
    _, r, s = der_decode_sig(sig)
    left = ecdsa_raw_recover(z, (0, r, s))
    right = ecdsa_raw_recover(z, (1, r, s))
    return (encode_pubkey(left, 'hex'), encode_pubkey(right, 'hex'))


def mk_pubkey_script(addr):
    return '76a914' + b58check_to_hex(addr) + '88ac'


def mk_scripthash_script(addr):
    return 'a914' + b58check_to_hex(addr) + '87'


def address_to_script(addr):
    if addr[0] == '3' or addr[0] == '2':
        return mk_scripthash_script(addr)
    return mk_pubkey_script(addr)


def script_to_address(script, vbyte=0):
    if re.match('^[0-9a-fA-F]*$', script):
        script = binascii.unhexlify(script)
    elif script[:3] == b'v\xa9\x14':
        if script[-2:] == b'\x88\xac':
            if len(script) == 25:
                return bin_to_b58check(script[3:-2], vbyte)
    elif vbyte in (111, 196):
        scripthash_byte = 196
    else:
        if vbyte == 0:
            scripthash_byte = 5
        else:
            scripthash_byte = vbyte
    return bin_to_b58check(script[2:-1], scripthash_byte)


def p2sh_scriptaddr(script, magicbyte=5):
    if re.match('^[0-9a-fA-F]*$', script):
        script = binascii.unhexlify(script)
    return hex_to_b58check(hash160(script), magicbyte)


scriptaddr = p2sh_scriptaddr

def deserialize_script(script):
    if isinstance(script, str):
        if re.match('^[0-9a-fA-F]*$', script):
            return json_changebase(deserialize_script(binascii.unhexlify(script)), lambda x: safe_hexlify(x))
    out, pos = [], 0
    while pos < len(script):
        code = from_byte_to_int(script[pos])
        if code == 0:
            out.append(None)
            pos += 1
        elif code <= 75:
            out.append(script[pos + 1:pos + 1 + code])
            pos += 1 + code
        elif code <= 78:
            szsz = pow(2, code - 76)
            sz = decode(script[pos + szsz:pos:-1], 256)
            out.append(script[pos + 1 + szsz:pos + 1 + szsz + sz])
            pos += 1 + szsz + sz
        elif code <= 96:
            out.append(code - 80)
            pos += 1
        else:
            out.append(code)
            pos += 1

    return out


def serialize_script_unit(unit):
    if isinstance(unit, int):
        if unit < 16:
            return from_int_to_byte(unit + 80)
        return from_int_to_byte(unit)
    else:
        if unit is None:
            return b'\x00'
        if len(unit) <= 75:
            return from_int_to_byte(len(unit)) + unit
        if len(unit) < 256:
            return from_int_to_byte(76) + from_int_to_byte(len(unit)) + unit
        if len(unit) < 65536:
            return from_int_to_byte(77) + encode(len(unit), 256, 2)[::-1] + unit
        return from_int_to_byte(78) + encode(len(unit), 256, 4)[::-1] + unit


if is_python2:

    def serialize_script(script):
        if json_is_base(script, 16):
            return binascii.hexlify(serialize_script(json_changebase(script, lambda x: binascii.unhexlify(x))))
        return ''.join(map(serialize_script_unit, script))


else:

    def serialize_script(script):
        if json_is_base(script, 16):
            return safe_hexlify(serialize_script(json_changebase(script, lambda x: binascii.unhexlify(x))))
        result = bytes()
        for b in map(serialize_script_unit, script):
            result += b if isinstance(b, bytes) else bytes(b, 'utf-8')

        return result


def mk_multisig_script(*args):
    if isinstance(args[0], list):
        pubs, k = args[0], int(args[1])
    else:
        pubs = list(filter(lambda x: len(str(x)) >= 32, args))
        k = int(args[len(pubs)])
    return serialize_script([k] + pubs + [len(pubs)] + [174])


def verify_tx_input(tx, i, script, sig, pub):
    if re.match('^[0-9a-fA-F]*$', tx):
        tx = binascii.unhexlify(tx)
    else:
        if re.match('^[0-9a-fA-F]*$', script):
            script = binascii.unhexlify(script)
        sig = re.match('^[0-9a-fA-F]*$', sig) or safe_hexlify(sig)
    hashcode = decode(sig[-2:], 16)
    modtx = signature_form(tx, int(i), script, hashcode)
    return ecdsa_tx_verify(modtx, sig, pub, hashcode)


def sign(tx, i, priv, hashcode=SIGHASH_ALL):
    i = int(i)
    return is_python2 or isinstance(re, bytes) or re.match('^[0-9a-fA-F]*$', tx) or binascii.unhexlify(sign(safe_hexlify(tx), i, priv))
    if len(priv) <= 33:
        priv = safe_hexlify(priv)
    pub = privkey_to_pubkey(priv)
    address = pubkey_to_address(pub)
    signing_tx = signature_form(tx, i, mk_pubkey_script(address), hashcode)
    sig = ecdsa_tx_sign(signing_tx, priv, hashcode)
    txobj = deserialize(tx)
    txobj['ins'][i]['script'] = serialize_script([sig, pub])
    return serialize(txobj)


def signall(tx, priv):
    if isinstance(priv, dict):
        for e, i in enumerate(deserialize(tx)['ins']):
            k = priv[('%s:%d' % (i['outpoint']['hash'], i['outpoint']['index']))]
            tx = sign(tx, e, k)

    else:
        for i in range(len(deserialize(tx)['ins'])):
            tx = sign(tx, i, priv)

    return tx


def multisign(tx, i, script, pk, hashcode=SIGHASH_ALL):
    if re.match('^[0-9a-fA-F]*$', tx):
        tx = binascii.unhexlify(tx)
    if re.match('^[0-9a-fA-F]*$', script):
        script = binascii.unhexlify(script)
    modtx = signature_form(tx, i, script, hashcode)
    return ecdsa_tx_sign(modtx, pk, hashcode)


def apply_multisignatures(*args):
    tx, i, script = args[0], int(args[1]), args[2]
    sigs = args[3] if isinstance(args[3], list) else list(args[3:])
    if isinstance(script, str):
        if re.match('^[0-9a-fA-F]*$', script):
            script = binascii.unhexlify(script)
    sigs = [binascii.unhexlify(x) if x[:2] == '30' else x for x in sigs]
    if isinstance(tx, str):
        if re.match('^[0-9a-fA-F]*$', tx):
            return safe_hexlify(apply_multisignatures(binascii.unhexlify(tx), i, script, sigs))
    script_blob = [] if script.__len__() == 0 else [script]
    txobj = deserialize(tx)
    txobj['ins'][i]['script'] = serialize_script([None] + sigs + script_blob)
    return serialize(txobj)


def is_inp(arg):
    return len(arg) > 64 or 'output' in arg or 'outpoint' in arg


def mktx(*args):
    ins, outs = [], []
    for arg in args:
        if isinstance(arg, list):
            for a in arg:
                (ins if is_inp(a) else outs).append(a)

        else:
            (ins if is_inp(arg) else outs).append(arg)

    txobj = {'locktime':0, 
     'version':1,  'ins':[],  'outs':[]}
    for i in ins:
        if isinstance(i, dict) and 'outpoint' in i:
            txobj['ins'].append(i)
        else:
            if isinstance(i, dict):
                if 'output' in i:
                    i = i['output']
            txobj['ins'].append({'outpoint':{'hash':i[:64], 
              'index':int(i[65:])}, 
             'script':'', 
             'sequence':4294967295})

    for o in outs:
        if isinstance(o, string_or_bytes_types):
            addr = o[:o.find(':')]
            val = int(o[o.find(':') + 1:])
            o = {}
            if re.match('^[0-9a-fA-F]*$', addr):
                o['script'] = addr
            else:
                o['address'] = addr
            o['value'] = val
        else:
            outobj = {}
            if 'address' in o:
                outobj['script'] = address_to_script(o['address'])
            else:
                if 'script' in o:
                    outobj['script'] = o['script']
                else:
                    raise Exception("Could not find 'address' or 'script' in output.")
        outobj['value'] = o['value']
        txobj['outs'].append(outobj)

    return serialize(txobj)


def select(unspent, value):
    value = int(value)
    high = [u for u in unspent if u['value'] >= value]
    high.sort(key=(lambda u: u['value']))
    low = [u for u in unspent if u['value'] < value]
    low.sort(key=(lambda u: -u['value']))
    if len(high):
        return [
         high[0]]
    i, tv = (0, 0)
    while tv < value and i < len(low):
        tv += low[i]['value']
        i += 1

    if tv < value:
        raise Exception('Not enough funds')
    return low[:i]


def mksend(*args):
    argz, change, fee = args[:-2], args[(-2)], int(args[(-1)])
    ins, outs = [], []
    for arg in argz:
        if isinstance(arg, list):
            for a in arg:
                (ins if is_inp(a) else outs).append(a)

        else:
            (ins if is_inp(arg) else outs).append(arg)

    isum = sum([i['value'] for i in ins])
    osum, outputs2 = 0, []
    for o in outs:
        if isinstance(o, string_types):
            o2 = {'address':o[:o.find(':')],  'value':int(o[o.find(':') + 1:])}
        else:
            o2 = o
        outputs2.append(o2)
        osum += o2['value']

    if isum < osum + fee:
        raise Exception('Not enough money')
    else:
        if isum > osum + fee + 5430:
            outputs2 += [{'address':change,  'value':isum - osum - fee}]
        return mktx(ins, outputs2)