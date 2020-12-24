# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\braces\__init__.py
# Compiled at: 2020-04-27 05:44:32
# Size of source mod 2**32: 1712 bytes
"""Library that implements braces for Python Programming Language."""
__title__ = 'braces'
__author__ = 'NeKitDS'
__copyright__ = 'Copyright 2020 NeKitDS'
__license__ = 'MIT'
__version__ = '0.1.2'
from collections import namedtuple
import re, token
from typing import cast
from .const import EXCEPT, TOKEN
from .register_codec import decode
from .token_transform import SmallToken, test_compile, transform
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
_normal_re = '^\\s*(?:(?P<major>\\d+)(?P<split>[\\.-])?(?P<minor>\\d+)?(?P=split)?(?P<micro>\\d+)?(?P<releaselevel>a|b|rc|f|dev)?(?P<serial>\\d+)?)\\s*$'
_compiled_re = re.compile(_normal_re, re.MULTILINE)

def make_version_details--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              _compiled_re
                2  LOAD_METHOD              match
                4  LOAD_FAST                'ver'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'match'

 L.  38        10  LOAD_FAST                'match'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    34  'to 34'

 L.  39        18  LOAD_GLOBAL              VersionInfo
               20  LOAD_CONST               0
               22  LOAD_CONST               0
               24  LOAD_CONST               0
               26  LOAD_STR                 'final'
               28  LOAD_CONST               0
               30  CALL_FUNCTION_5       5  ''
               32  RETURN_VALUE     
             34_0  COME_FROM            16  '16'

 L.  41        34  BUILD_MAP_0           0 
               36  STORE_FAST               'args'

 L.  43        38  LOAD_FAST                'match'
               40  LOAD_METHOD              groupdict
               42  CALL_METHOD_0         0  ''
               44  LOAD_METHOD              items
               46  CALL_METHOD_0         0  ''
               48  GET_ITER         
               50  FOR_ITER            156  'to 156'
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'key'
               56  STORE_FAST               'value'

 L.  44        58  LOAD_FAST                'key'
               60  LOAD_STR                 'split'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L.  45        66  JUMP_BACK            50  'to 50'
               68  JUMP_FORWARD        146  'to 146'
             70_0  COME_FROM            64  '64'

 L.  47        70  LOAD_FAST                'key'
               72  LOAD_STR                 'releaselevel'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   116  'to 116'

 L.  48        78  LOAD_FAST                'value'
               80  LOAD_CONST               None
               82  COMPARE_OP               is
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L.  49        86  LOAD_STR                 'f'
               88  STORE_FAST               'value'
             90_0  COME_FROM            84  '84'

 L.  52        90  LOAD_STR                 'alpha'

 L.  53        92  LOAD_STR                 'beta'

 L.  54        94  LOAD_STR                 'candidate'

 L.  55        96  LOAD_STR                 'final'

 L.  56        98  LOAD_STR                 'developer'

 L.  51       100  LOAD_CONST               ('a', 'b', 'rc', 'f', 'dev')
              102  BUILD_CONST_KEY_MAP_5     5 
              104  LOAD_METHOD              get

 L.  57       106  LOAD_FAST                'value'

 L.  57       108  LOAD_STR                 'final'

 L.  51       110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'value'
              114  JUMP_FORWARD        146  'to 146'
            116_0  COME_FROM            76  '76'

 L.  59       116  LOAD_FAST                'value'
              118  LOAD_CONST               None
              120  COMPARE_OP               is
              122  POP_JUMP_IF_TRUE    132  'to 132'
              124  LOAD_FAST                'value'
              126  LOAD_METHOD              isdigit
              128  CALL_METHOD_0         0  ''
              130  POP_JUMP_IF_TRUE    138  'to 138'
            132_0  COME_FROM           122  '122'

 L.  60       132  LOAD_CONST               0
              134  STORE_FAST               'value'
              136  JUMP_FORWARD        146  'to 146'
            138_0  COME_FROM           130  '130'

 L.  63       138  LOAD_GLOBAL              int
              140  LOAD_FAST                'value'
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'value'
            146_0  COME_FROM           136  '136'
            146_1  COME_FROM           114  '114'
            146_2  COME_FROM            68  '68'

 L.  65       146  LOAD_FAST                'value'
              148  LOAD_FAST                'args'
              150  LOAD_FAST                'key'
              152  STORE_SUBSCR     
              154  JUMP_BACK            50  'to 50'

 L.  67       156  LOAD_GLOBAL              VersionInfo
              158  BUILD_TUPLE_0         0 
              160  LOAD_FAST                'args'
              162  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 68


version_info = make_version_details(__version__)
del namedtuple
del re