# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/dropbox/decrypt25.py
# Compiled at: 2020-04-20 10:24:57
import types, struct
from xdis.version_info import PYTHON3
import xdis.marsh as xmarshal
from xdis.codetype import Code2Compat

def rng(a, b):
    b = (b << 13 ^ b) & 4294967295
    c = b ^ b >> 17
    c = c ^ c << 5
    return a * 69069 + c + 1712442171 & 4294967295


def get_keys(a, b):
    ka = rng(a, b)
    kb = rng(ka, a)
    kc = rng(kb, ka)
    kd = rng(kc, kb)
    ke = rng(kd, kc)
    return (kb, kc, kd, ke)


def MX(z, y, sum, key, p, e):
    return (z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (key[(p & 3 ^ e)] ^ z)


def tea_decipher(v, key):
    """
    Tiny Decryption Algorithm decription (TEA)
    See https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm
    """
    DELTA = 2654435769
    n = len(v)
    rounds = 6 + 52 // n
    sum = rounds * DELTA
    y = v[0]
    while sum != 0:
        e = sum >> 2 & 3
        for p in range(n - 1, -1, -1):
            z = v[((n + p - 1) % n)]
            v[p] = v[p] - MX(z, y, sum, key, p, e) & 4294967295
            y = v[p]

        sum -= DELTA

    return v


def load_code(self):
    """
    Returns a Python code object like xdis.unmarshal.load_code(),
    but in we decrypt the data in self.bufstr.

    That is:
      * calculate the TEA key,
      * decrypt self.bufstr
      * create and return a Python code-object
    """
    a = self.load_int()
    b = self.load_int()
    key = get_keys(a, b)
    padsize = b + 15 & -16
    intsize = padsize / 4
    data = self.bufstr[self.bufpos:self.bufpos + padsize]
    data = list(struct.unpack('<%dL' % intsize, data))
    tea_decipher(data, key)
    self.bufpos += padsize
    obj = xmarshal._FastUnmarshaller(struct.pack(('<%dL' % intsize), *data))
    code = obj.load_code()
    co_code = patch(code.co_code)
    if PYTHON3:
        return Code2Compat(code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags, co_code, code.co_consts, code.co_names, code.co_varnames, code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)
    else:
        return types.CodeType(code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags, co_code, code.co_consts, code.co_names, code.co_varnames, code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)


try:
    a = bytearray()
except:

    class bytearray(object):
        __module__ = __name__

        def __init__(self, s):
            self.l = map(ord, s)

        def __setitem__(self, idx, val):
            self.l[idx] = val

        def __getitem__(self, idx):
            return self.l[idx]

        def __str__(self):
            return ('').join(map(chr, self.l))

        def __len__(self):
            return len(self.l)


table = {0: 0, 1: 87, 2: 66, 4: 25, 6: 55, 7: 62, 9: 71, 10: 79, 12: 21, 13: 4, 14: 72, 15: 1, 16: 30, 17: 31, 18: 32, 19: 33, 22: 63, 26: 86, 29: 56, 31: 60, 33: 73, 34: 15, 35: 74, 36: 20, 38: 12, 39: 68, 40: 80, 41: 22, 42: 89, 43: 26, 50: 64, 51: 82, 52: 23, 54: 11, 55: 24, 56: 84, 59: 2, 60: 3, 61: 40, 62: 41, 63: 42, 64: 43, 65: 85, 66: 83, 67: 88, 68: 18, 69: 61, 70: 116, 71: 126, 72: 100, 73: 110, 74: 120, 75: 122, 76: 132, 77: 133, 78: 104, 79: 101, 80: 102, 81: 93, 82: 125, 83: 111, 84: 95, 85: 134, 86: 105, 88: 107, 89: 108, 90: 112, 91: 130, 92: 124, 93: 92, 94: 91, 95: 90, 97: 135, 99: 136, 100: 137, 101: 106, 102: 131, 103: 113, 104: 99, 105: 97, 106: 121, 107: 103, 111: 140, 112: 141, 113: 142}
table[37] = 81
table[28] = 19
table[87] = 96
table[21] = 65
table[96] = 119
table[8] = 57
table[32] = 28
table[44] = 50
table[45] = 51
table[46] = 52
table[47] = 53
table[23] = 78
table[24] = 77
table[3] = 59
table[11] = 75
table[58] = 76
misses = {}

def patch(code):
    code = bytearray(code)
    i = 0
    n = len(code)
    while i < n:
        op = code[i]
        if op not in table:
            print (
             'missing opcode %d. code: ' % op, repr(str(code)))
            misses[op] = misses.get(op, 0) + 1
        code[i] = table.get(op, op)
        i += 1
        if table.get(op, op) >= 90:
            i += 2

    return str(code)


try:
    from __pypy__ import builtinify
except ImportError:
    builtinify = lambda f: f

def loads(s):
    """
    xdis.marshal.load() but with its dispatch load_code() function replaced
    with our decoding version.
    """
    um = xmarshal._FastUnmarshaller(s)
    um.dispatch[xmarshal.TYPE_CODE] = load_code
    return um.load()


def fix_dropbox_pyc(fp, fixed_pyc='/tmp/test.pyc'):
    source_size = struct.unpack('I', fp.read(4))[0]
    ts = fp.read(4)
    timestamp = struct.unpack('I', ts)[0]
    b = fp.read()
    co = loads(b)
    return (2.5, timestamp, 62131, co, False, source_size, None)


def fix_dir(path):
    import os
    for (root, dirs, files) in os.walk(path):
        for name in files:
            if not name.endswith('pyc'):
                continue
            name = os.path.join(root, name)
            print ('fixing', name)
            data = open(name).read()
            try:
                c = xmarshal.loads(data[8:])
            except Exception(e):
                print (
                 'error', e, repr(e))
                continue

            open(name, 'w').write(b'\xb3\xf2\r\n' + data[4:8] + xmarshal.dumps(c))


if __name__ == '__main__':
    import os, sys
    if sys.argv != 2:
        print 'Usage: %s python-file' % os.path.basename(sys.argv[0])
        sys.exit(1)
    fix_dir(sys.argv[1])