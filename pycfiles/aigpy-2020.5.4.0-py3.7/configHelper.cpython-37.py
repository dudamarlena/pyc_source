# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\configHelper.py
# Compiled at: 2020-05-04 02:46:26
# Size of source mod 2**32: 4430 bytes
"""
@File    :   configHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Config Tool
"""
import os, configparser
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES

def Count--- This code section failed: ---

 L.  20         0  SETUP_EXCEPT        104  'to 104'

 L.  21         2  LOAD_CONST               0
                4  STORE_FAST               'ret'

 L.  22         6  LOAD_GLOBAL              configparser
                8  LOAD_METHOD              ConfigParser
               10  CALL_METHOD_0         0  '0 positional arguments'
               12  STORE_FAST               'cf'

 L.  23        14  LOAD_FAST                'cf'
               16  LOAD_METHOD              read
               18  LOAD_FAST                'fileName'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          

 L.  24        24  LOAD_FAST                'section'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    78  'to 78'

 L.  25        32  LOAD_FAST                'cf'
               34  LOAD_METHOD              sections
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  STORE_FAST               'seclist'

 L.  26        40  SETUP_LOOP          100  'to 100'
               42  LOAD_FAST                'seclist'
               44  GET_ITER         
               46  FOR_ITER             74  'to 74'
               48  STORE_FAST               'sec'

 L.  27        50  LOAD_FAST                'cf'
               52  LOAD_METHOD              options
               54  LOAD_FAST                'sec'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  STORE_FAST               'oplist'

 L.  28        60  LOAD_FAST                'ret'
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'oplist'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  BINARY_ADD       
               70  STORE_FAST               'ret'
               72  JUMP_BACK            46  'to 46'
               74  POP_BLOCK        
               76  JUMP_FORWARD        100  'to 100'
             78_0  COME_FROM            30  '30'

 L.  29        78  LOAD_FAST                'cf'
               80  LOAD_METHOD              has_section
               82  LOAD_FAST                'section'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_JUMP_IF_FALSE   100  'to 100'

 L.  30        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'cf'
               92  LOAD_FAST                'section'
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'ret'
            100_0  COME_FROM            86  '86'
            100_1  COME_FROM            76  '76'
            100_2  COME_FROM_LOOP       40  '40'

 L.  31       100  LOAD_FAST                'ret'
              102  RETURN_VALUE     
            104_0  COME_FROM_EXCEPT      0  '0'

 L.  32       104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L.  33       110  LOAD_CONST               0
              112  RETURN_VALUE     

Parse error at or near `COME_FROM_LOOP' instruction at offset 100_2


def Sections(fileName):
    """Get groups"""
    try:
        cf = configparser.ConfigParser
        cf.readfileName
        return cf.sections
    except:
        return


def GetValue(section, key, default, fileName, aesKey=None):
    try:
        cf = configparser.ConfigParser
        cf.readfileName
        if not cf.has_sectionsection:
            return default
        if key in cf[section]:
            default = cf.get(section, key)
        if aesKey is not None:
            if default is not None:
                if len(default) > 0:
                    func = AES_FUNC(aesKey)
                    default = func.decryptdefault
        return default
    except:
        return default


def SetValue(section, key, value, fileName, aesKey=None):
    try:
        if os.access(fileName, 0) is False:
            fp = open(fileName, 'w')
            fp.close
        else:
            cf = configparser.ConfigParser
            cf.readfileName
            if cf.has_sectionsection is False:
                cf[section] = {}
            real_value = value
            if aesKey is not None:
                if value is not None and len(value) > 0:
                    func = AES_FUNC(aesKey)
                    real_value = func.encryptvalue
                    real_value = str(real_value, encoding='utf-8')
        cf[section][key] = real_value
        with open(fileName, 'w') as (f):
            cf.writef
        return True
    except:
        return False


def ParseNoEqual(fileName):
    ret = {}
    try:
        fd = open(fileName, 'r')
        arr = fd.readlines
        group = None
        for item in arr:
            item = item.strip
            if len(item) <= 0:
                continue
            else:
                if item[0] == '#':
                    continue
            if item[0] == '[' and item[(len(item) - 1)] == ']':
                group = item[1:len(item) - 1]
                ret[group] = []
            elif group is None:
                continue
            else:
                ret[group].appenditem

        return ret
    except:
        return ret


class AES_FUNC:

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB
        self.AES_LENGTH = 16
        self.cryptor = AES.new(self.pad_keyself.key.encode, self.mode)

    def pad(self, text):
        while len(text) % self.AES_LENGTH != 0:
            text += ' '

        return text

    def pad_key(self, key):
        while len(key) % self.AES_LENGTH != 0:
            key += ' '

        return key

    def encrypt(self, text):
        self.ciphertext = self.cryptor.encryptself.padtext.encode
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        plain_text = self.cryptor.decrypta2b_hex(text).decode
        return plain_text.rstrip' '