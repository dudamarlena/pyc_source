# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/compat.py
# Compiled at: 2019-09-16 13:23:31
# Size of source mod 2**32: 3745 bytes
from __future__ import absolute_import
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    long = long
    raw_input = raw_input
    unicode = unicode
    unichr = unichr
    basestring = basestring

    def as_bytes(s, encoding='utf-8'):
        if isinstance(s, str):
            return s
        return s.encode(encoding)


    def as_string(s, encoding='utf-8'):
        if isinstance(s, unicode):
            return s
        return s.decode(encoding)


    def is_text_stream--- This code section failed: ---

 L.  27         0  SETUP_FINALLY        28  'to 28'

 L.  28         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'stream'
                6  LOAD_GLOBAL              file
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L.  29        12  LOAD_STR                 'b'
               14  LOAD_FAST                'stream'
               16  LOAD_ATTR                mode
               18  COMPARE_OP               not-in
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'
               24  POP_BLOCK        
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM_FINALLY     0  '0'

 L.  30        28  DUP_TOP          
               30  LOAD_GLOBAL              NameError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  31        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            34  '34'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            26  '26'

 L.  33        48  SETUP_FINALLY        72  'to 72'

 L.  34        50  LOAD_CONST               0
               52  LOAD_CONST               None
               54  IMPORT_NAME              _io
               56  STORE_FAST               '_io'

 L.  35        58  LOAD_GLOBAL              isinstance
               60  LOAD_FAST                'stream'
               62  LOAD_FAST                '_io'
               64  LOAD_ATTR                _TextIOBase
               66  CALL_FUNCTION_2       2  ''
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    48  '48'

 L.  36        72  DUP_TOP          
               74  LOAD_GLOBAL              ImportError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   110  'to 110'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  37        86  LOAD_CONST               0
               88  LOAD_CONST               None
               90  IMPORT_NAME              io
               92  STORE_FAST               'io'

 L.  38        94  LOAD_GLOBAL              isinstance
               96  LOAD_FAST                'stream'
               98  LOAD_FAST                'io'
              100  LOAD_ATTR                TextIOWrapper
              102  CALL_FUNCTION_2       2  ''
              104  ROT_FOUR         
              106  POP_EXCEPT       
              108  RETURN_VALUE     
            110_0  COME_FROM            78  '78'
              110  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 82


else:
    long = int
    basestring = str
    raw_input = input
    unichr = chr

    class unicode(str):

        def __init__(self, string, encoding, errors):
            str.__init__(self, string)


    def as_bytes(s, encoding='utf8'):
        if isinstance(s, bytes):
            return s
        return s.encode(encoding)


    def as_string(s, encoding='utf8'):
        if isinstance(s, str):
            return s
        return s.decode(encoding)


    def is_text_stream(stream):
        import _io
        return isinstance(stream, _io._TextIOBase)


try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib

try:
    import urllib.parse as urlparse
    import urllib.parse as urllib
except ImportError:
    import urlparse, urllib

try:
    from hashlib import sha1
except ImportError:
    from sha import new as sha1

try:
    import syslog
except ImportError:
    syslog = None

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from sys import maxint
except ImportError:
    from sys import maxsize as maxint

try:
    import http.client as httplib
except ImportError:
    import httplib

try:
    from base64 import decodebytes as decodestring, encodebytes as encodestring
except ImportError:
    from base64 import decodestring, encodestring

try:
    from xmlrpc.client import Fault
except ImportError:
    from xmlrpclib import Fault

try:
    from string import ascii_letters as letters
except ImportError:
    from string import letters

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

try:
    import thread
except ImportError:
    import _thread as thread

try:
    from types import StringTypes
except ImportError:
    StringTypes = (
     str,)

try:
    from html import escape
except ImportError:
    from cgi import escape

try:
    import html.entities as htmlentitydefs
except ImportError:
    import htmlentitydefs

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser