# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/case/case6_x_x.py
# Compiled at: 2018-12-17 11:51:20
import binascii
from case import Case
from autobahn.websocket.utf8validator import Utf8Validator

def createUtf8TestSequences():
    """
   Create test sequences for UTF-8 decoder tests from
   http://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
   """
    UTF8_TEST_SEQUENCES = []
    vss = 'κόσμε'
    vs = ['Some valid UTF-8 sequences', []]
    vs[1].append((True, 'hello$world'))
    vs[1].append((True, 'hello¢world'))
    vs[1].append((True, 'hello€world'))
    vs[1].append((True, 'hello𤭢world'))
    vs[1].append((True, vss))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'All prefixes of a valid UTF-8 string that contains multi-byte code points', []]
    v = Utf8Validator()
    for i in xrange(1, len(vss) + 1):
        v.reset()
        res = v.validate(vss[:i])
        vs[1].append((res[0] and res[1], vss[:i]))

    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'First possible sequence of a certain length', []]
    vs[1].append((True, '\x00'))
    vs[1].append((True, '\x80'))
    vs[1].append((True, 'ࠀ'))
    vs[1].append((True, '𐀀'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'First possible sequence length 5/6 (invalid codepoints)', []]
    vs[1].append((False, b'\xf8\x88\x80\x80\x80'))
    vs[1].append((False, b'\xfc\x84\x80\x80\x80\x80'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Last possible sequence of a certain length', []]
    vs[1].append((True, '\x7f'))
    vs[1].append((True, '\u07ff'))
    vs[1].append((True, '\uffff'))
    vs[1].append((True, '\U0010ffff'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Last possible sequence length 4/5/6 (invalid codepoints)', []]
    vs[1].append((False, b'\xf7\xbf\xbf\xbf'))
    vs[1].append((False, b'\xfb\xbf\xbf\xbf\xbf'))
    vs[1].append((False, b'\xfd\xbf\xbf\xbf\xbf\xbf'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Other boundary conditions', []]
    vs[1].append((True, '\ud7ff'))
    vs[1].append((True, '\ue000'))
    vs[1].append((True, '�'))
    vs[1].append((True, '\U0010ffff'))
    vs[1].append((False, b'\xf4\x90\x80\x80'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Unexpected continuation bytes', []]
    vs[1].append((False, b'\x80'))
    vs[1].append((False, b'\xbf'))
    vs[1].append((False, b'\x80\xbf'))
    vs[1].append((False, b'\x80\xbf\x80'))
    vs[1].append((False, b'\x80\xbf\x80\xbf'))
    vs[1].append((False, b'\x80\xbf\x80\xbf\x80'))
    vs[1].append((False, b'\x80\xbf\x80\xbf\x80\xbf'))
    s = ''
    for i in xrange(128, 191):
        s += chr(i)

    vs[1].append((False, s))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Lonely start characters', []]
    m = [(192, 223), (224, 239), (240, 247), (248, 251), (252, 253)]
    for mm in m:
        s = ''
        for i in xrange(mm[0], mm[1]):
            s += chr(i)
            s += chr(32)

        vs[1].append((False, s))

    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Sequences with last continuation byte missing', []]
    k = [b'\xc0', b'\xe0\x80', b'\xf0\x80\x80', b'\xf8\x80\x80\x80', b'\xfc\x80\x80\x80\x80',
     b'\xdf', b'\xef\xbf', b'\xf7\xbf\xbf', b'\xfb\xbf\xbf\xbf', b'\xfd\xbf\xbf\xbf\xbf']
    for kk in k:
        vs[1].append((False, kk))

    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Concatenation of incomplete sequences', []]
    vs[1].append((False, ('').join(k)))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Impossible bytes', []]
    vs[1].append((False, b'\xfe'))
    vs[1].append((False, b'\xff'))
    vs[1].append((False, b'\xfe\xfe\xff\xff'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Examples of an overlong ASCII character', []]
    vs[1].append((False, b'\xc0\xaf'))
    vs[1].append((False, b'\xe0\x80\xaf'))
    vs[1].append((False, b'\xf0\x80\x80\xaf'))
    vs[1].append((False, b'\xf8\x80\x80\x80\xaf'))
    vs[1].append((False, b'\xfc\x80\x80\x80\x80\xaf'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Maximum overlong sequences', []]
    vs[1].append((False, b'\xc1\xbf'))
    vs[1].append((False, b'\xe0\x9f\xbf'))
    vs[1].append((False, b'\xf0\x8f\xbf\xbf'))
    vs[1].append((False, b'\xf8\x87\xbf\xbf\xbf'))
    vs[1].append((False, b'\xfc\x83\xbf\xbf\xbf\xbf'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Overlong representation of the NUL character', []]
    vs[1].append((False, b'\xc0\x80'))
    vs[1].append((False, b'\xe0\x80\x80'))
    vs[1].append((False, b'\xf0\x80\x80\x80'))
    vs[1].append((False, b'\xf8\x80\x80\x80\x80'))
    vs[1].append((False, b'\xfc\x80\x80\x80\x80\x80'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Single UTF-16 surrogates', []]
    vs[1].append((False, b'\xed\xa0\x80'))
    vs[1].append((False, b'\xed\xad\xbf'))
    vs[1].append((False, b'\xed\xae\x80'))
    vs[1].append((False, b'\xed\xaf\xbf'))
    vs[1].append((False, b'\xed\xb0\x80'))
    vs[1].append((False, b'\xed\xbe\x80'))
    vs[1].append((False, b'\xed\xbf\xbf'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Paired UTF-16 surrogates', []]
    vs[1].append((False, b'\xed\xa0\x80\xed\xb0\x80'))
    vs[1].append((False, b'\xed\xa0\x80\xed\xbf\xbf'))
    vs[1].append((False, b'\xed\xad\xbf\xed\xb0\x80'))
    vs[1].append((False, b'\xed\xad\xbf\xed\xbf\xbf'))
    vs[1].append((False, b'\xed\xae\x80\xed\xb0\x80'))
    vs[1].append((False, b'\xed\xae\x80\xed\xbf\xbf'))
    vs[1].append((False, b'\xed\xaf\xbf\xed\xb0\x80'))
    vs[1].append((False, b'\xed\xaf\xbf\xed\xbf\xbf'))
    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Non-character code points (valid UTF-8)', []]
    vs[1].append((True, '\ufffe'))
    vs[1].append((True, '\uffff'))
    for z1 in [b'\xf0', b'\xf1', b'\xf2', b'\xf3', b'\xf4']:
        for z2 in [b'\x8f', b'\x9f', b'\xaf', b'\xbf']:
            if not (z1 == b'\xf4' and z2 != b'\x8f'):
                for z3 in [b'\xbe', b'\xbf']:
                    zz = z1 + z2 + b'\xbf' + z3
                    if zz not in (b'\xf0\x8f\xbf\xbe', b'\xf0\x8f\xbf\xbf'):
                        vs[1].append((True, zz))

    UTF8_TEST_SEQUENCES.append(vs)
    vs = [
     'Unicode specials (i.e. replacement char)', []]
    vs[1].append((True, '\ufff9'))
    vs[1].append((True, '\ufffa'))
    vs[1].append((True, '\ufffb'))
    vs[1].append((True, '￼'))
    vs[1].append((True, '�'))
    vs[1].append((True, '\ufffe'))
    vs[1].append((True, '\uffff'))
    UTF8_TEST_SEQUENCES.append(vs)
    return UTF8_TEST_SEQUENCES


def createValidUtf8TestSequences():
    """
   Generate some exotic, but valid UTF8 test strings.
   """
    VALID_UTF8_TEST_SEQUENCES = []
    for test in createUtf8TestSequences():
        valids = [ x[1] for x in test[1] if x[0] ]
        if len(valids) > 0:
            VALID_UTF8_TEST_SEQUENCES.append([test[0], valids])

    return VALID_UTF8_TEST_SEQUENCES


def test_utf8(validator):
    """
   These tests verify the UTF-8 decoder/validator on the various test cases from
   http://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
   """
    vs = []
    for k in createUtf8TestSequences():
        vs.extend(k[1])

    for i in xrange(0, 65535):
        if i < 55296 or i > 57343:
            vs.append((True, unichr(i).encode('utf-8')))

    for i in xrange(55296, 56319):
        ss = unichr(i).encode('utf-8')
        vs.append((False, ss))

    for i in xrange(56320, 57343):
        ss = unichr(i).encode('utf-8')
        vs.append((False, ss))

    for i in xrange(55296, 56319):
        for j in xrange(56320, 57343):
            ss1 = unichr(i).encode('utf-8')
            ss2 = unichr(j).encode('utf-8')
            vs.append((False, ss1 + ss2))
            vs.append((False, ss2 + ss1))

    print 'testing validator %s on %d UTF8 sequences' % (validator, len(vs))
    for s in vs:
        validator.reset()
        r = validator.validate(s[1])
        res = r[0] and r[1]
        assert res == s[0]

    print 'ok, validator works!'
    print


def test_utf8_incremental(validator, withPositions=True):
    """
   These tests verify that the UTF-8 decoder/validator can operate incrementally.
   """
    if withPositions:
        k = 4
        print 'testing validator %s on incremental detection with positions' % validator
    else:
        k = 2
        print 'testing validator %s on incremental detection without positions' % validator
    validator.reset()
    assert (True, True, 15, 15)[:k] == validator.validate('µ@ßöäüàá')[:k]
    validator.reset()
    assert (False, False, 0, 0)[:k] == validator.validate(b'\xf5')[:k]
    validator.reset()
    assert (True, True, 6, 6)[:k] == validator.validate('edited')[:k]
    assert (False, False, 1, 7)[:k] == validator.validate(b'\xed\xa0\x80')[:k]
    validator.reset()
    assert (True, True, 4, 4)[:k] == validator.validate('edit')[:k]
    assert (False, False, 3, 7)[:k] == validator.validate(b'ed\xed\xa0\x80')[:k]
    validator.reset()
    assert (True, False, 7, 7)[:k] == validator.validate(b'edited\xed')[:k]
    assert (False, False, 0, 7)[:k] == validator.validate(b'\xa0\x80')[:k]
    print 'ok, validator works!'
    print


Case6_X_X = []
Case6_X_X_CaseSubCategories = {}

def __init__(self, protocol):
    Case.__init__(self, protocol)


def onOpen(self):
    if self.isValid:
        self.expected[Case.OK] = [
         (
          'message', self.PAYLOAD, False)]
        self.expectedClose = {'closedByMe': True, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_NORMAL], 
           'requireClean': True}
    else:
        self.expected[Case.OK] = []
        self.expectedClose = {'closedByMe': False, 'closeCode': [
                       self.p.CLOSE_STATUS_CODE_INVALID_PAYLOAD], 
           'requireClean': False, 
           'closedByWrongEndpointIsFatal': True}
    self.p.sendMessage(self.PAYLOAD, False)
    self.p.killAfter(0.5)


i = 5
for t in createUtf8TestSequences():
    j = 1
    Case6_X_X_CaseSubCategories['6.%d' % i] = t[0]
    for p in t[1]:
        if p[0]:
            desc = 'Send a text message with payload which is valid UTF-8 in one fragment.'
            exp = "The message is echo'ed back to us."
        else:
            desc = 'Send a text message with payload which is not valid UTF-8 in one fragment.'
            exp = 'The connection is failed immediately, since the payload is not valid UTF-8.'
        C = type('Case6_%d_%d' % (i, j), (
         object, Case), {'PAYLOAD': p[1], 'isValid': p[0], 
           'DESCRIPTION': '%s<br><br>Payload: 0x%s' % (desc, binascii.b2a_hex(p[1])), 
           'EXPECTATION': '%s' % exp, 
           '__init__': __init__, 
           'onOpen': onOpen})
        Case6_X_X.append(C)
        j += 1

    i += 1

import binascii, array

def encode(c):
    """
   Encode Unicode code point into UTF-8 byte string.
   """
    if c <= 127:
        b1 = c >> 0 & 127 | 0
        return array.array('B', [b1]).tostring()
    if c <= 2047:
        b1 = c >> 6 & 31 | 192
        b2 = c >> 0 & 63 | 128
        return array.array('B', [b1, b2]).tostring()
    if c <= 65535:
        b1 = c >> 12 & 15 | 224
        b2 = c >> 6 & 63 | 128
        b3 = c >> 0 & 63 | 128
        return array.array('B', [b1, b2, b3]).tostring()
    if c <= 2097151:
        b1 = c >> 18 & 7 | 240
        b2 = c >> 12 & 63 | 128
        b3 = c >> 6 & 63 | 128
        b4 = c >> 0 & 63 | 128
        return array.array('B', [b1, b2, b3, b4]).tostring()
    if c <= 67108863:
        b1 = c >> 24 & 3 | 248
        b2 = c >> 18 & 63 | 128
        b3 = c >> 12 & 63 | 128
        b4 = c >> 6 & 63 | 128
        b5 = c >> 0 & 63 | 128
        return array.array('B', [b1, b2, b3, b4, b5]).tostring()
    if c <= 2147483647:
        b1 = c >> 30 & 1 | 252
        b2 = c >> 24 & 63 | 128
        b3 = c >> 18 & 63 | 128
        b4 = c >> 12 & 63 | 128
        b5 = c >> 6 & 63 | 128
        b6 = c >> 0 & 63 | 128
        return array.array('B', [b1, b2, b3, b4, b5, b6]).tostring()
    raise Exception('invalid unicode codepoint')


def test_encode(testpoints):
    """
   Compare Python UTF-8 encoding with adhoc implementation.
   """
    for tp in testpoints:
        if tp[0]:
            print binascii.b2a_hex(encode(tp[0]))
        else:
            print tp[0]
        if tp[1]:
            print binascii.b2a_hex(tp[1].encode('utf8'))
        else:
            print tp[1]


if __name__ == '__main__':
    validator = Utf8Validator()
    test_utf8(validator)
    test_utf8_incremental(validator, withPositions=True)