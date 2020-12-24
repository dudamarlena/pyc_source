# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/opstring.py
# Compiled at: 2016-07-25 14:36:49
from __future__ import print_function
from string import *

def bin(i):
    """
      Convert integer to binary string.
   """
    s = ''
    q = i
    while 1:
        (q, r) = divmod(q, 2)
        s = digits[r] + s
        if q == 0:
            break

    return s


def PadCh(S, Ch, Len):
    """ Return a string right-padded to length Len with Ch """
    if len(S) >= Len:
        return S
    else:
        return S + Ch * (Len - len(S))


def Pad(S, Len):
    """ Return a string right-padded to length len with blanks """
    return PadCh(S, ' ', Len)


def LeftPadCh(S, Ch, Len):
    """ Return a string left-padded to length len with ch """
    if len(S) >= Len:
        return S
    else:
        return Ch * (Len - len(S)) + S


def LeftPad(S, Len):
    """ Return a string left-padded to length len with blanks """
    return LeftPadCh(S, ' ', Len)


def CenterCh(S, Ch, Width):
    """ Return a string centered in a string of Ch with specified width """
    if len(S) >= Width:
        return S
    else:
        l = (Width - len(S)) // 2
        r = Width - len(S) - l
        return Ch * l + S + Ch * r


def Center(S, Width):
    """ Return a string centered in a blank string of specified width """
    return CenterCh(S, ' ', Width)


def FindStr(str, list):
    """ Find given string in the list of strings """
    for i in range(len(list)):
        if str == list[i]:
            return i

    return -1


def FindStrUC(str, list):
    """ Find string ignoring case """
    str = upper(str)
    for i in range(len(list)):
        if str == upper(list[i]):
            return i

    return -1


transl_adict = {'day': [
         b'\xc4\xc5\xce\xd8', b'\xc4\xce\xd1', b'\xc4\xce\xc5\xca'], 
   'week': [
          b'\xce\xc5\xc4\xc5\xcc\xd1', b'\xce\xc5\xc4\xc5\xcc\xc9', b'\xce\xc5\xc4\xc5\xcc\xd8'], 
   'month': [
           b'\xcd\xc5\xd3\xd1\xc3', b'\xcd\xc5\xd3\xd1\xc3\xc1', b'\xcd\xc5\xd3\xd1\xc3\xc5\xd7'], 
   'year': [
          b'\xc7\xcf\xc4', b'\xc7\xcf\xc4\xc1', b'\xcc\xc5\xd4']}
transl_adict['days'] = transl_adict['day']
transl_adict['weeks'] = transl_adict['week']
transl_adict['months'] = transl_adict['month']
transl_adict['years'] = transl_adict['year']
transl_vdict = {1: 0, 
   2: 1, 
   3: 1, 4: 1, 5: 2, 
   6: 2, 7: 2, 8: 2, 9: 2, 0: 2}

def translate_a(val, id):
    if not transl_adict.has_key(id):
        return ''
    if 5 <= val % 100 <= 20:
        val = 2
    else:
        val = transl_vdict[(val % 10)]
    return transl_adict[id][val]


def recode(s, from_encoding, to_encoding, errors='strict'):
    if isinstance(s, bytes):
        s = s.decode(from_encoding, errors)
    return s.encode(to_encoding, errors)


def win2koi(s, errors='strict'):
    return recode(s, 'cp1251', 'koi8-r', errors)


def koi2win(s, errors='strict'):
    return recode(s, 'koi8-r', 'cp1251', errors)


def test():
    print('bin(0x6) =', bin(6))
    print('bin(0xC) =', bin(12))
    print("'Test' left-padded :", LeftPad('Test', 20))
    print("'Test' right-padded:", PadCh('Test', '*', 20))
    print("'Test' centered    :", CenterCh('Test', '=', 20))
    print(b"'\xef\xcc\xc5\xc7':", koi2win(win2koi(b'\xef\xcc\xc5\xc7')))


if __name__ == '__main__':
    test()