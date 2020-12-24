# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/__init__.py
# Compiled at: 2020-03-29 18:10:29
# Size of source mod 2**32: 1979 bytes
"""
oathldap -- Python package for OATH-LDAP client tool
"""
import sys, getpass, ldap0, ldap0.base
from ldap0 import LDAPError
from ldap0.ldapobject import ReconnectLDAPObject
__all__ = [
 'cli_output',
 'ABORT_MSG',
 'ErrorExit',
 'SEP_LINE']
SEP_LINE = '--------------------------------------------------------------------------------'
ABORT_MSG = 'Aborted -> exit'

class ErrorExit(Exception):
    __doc__ = '\n    to be raised if any condition should result in program exit\n    '

    def __init__(self, msg, code=1):
        Exception.__init__(self, msg)
        self.code = code


def cli_output(text, lf_before=1, lf_after=1):
    """
    Command-line program output
    """
    sys.stdout.write(''.join((
     lf_before * '\n',
     text,
     lf_after * '\n')))


def interactive_ldapconnect--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              cli_output
                2  LOAD_STR                 'You have to login as admin.'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L.  65         8  LOAD_GLOBAL              getpass
               10  LOAD_METHOD              getpass
               12  LOAD_STR                 'Enter password for %r'
               14  LOAD_FAST                'ldap_who'
               16  BINARY_MODULO    
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'ldap_pw'

 L.  66        22  LOAD_FAST                'ldap_pw'
               24  POP_JUMP_IF_TRUE     34  'to 34'

 L.  67        26  LOAD_GLOBAL              ErrorExit
               28  LOAD_GLOBAL              ABORT_MSG
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L.  68        34  SETUP_FINALLY        60  'to 60'

 L.  69        36  LOAD_GLOBAL              ReconnectLDAPObject
               38  LOAD_FAST                'ldap_uri'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'oath_ldap'

 L.  70        44  LOAD_FAST                'oath_ldap'
               46  LOAD_METHOD              simple_bind_s
               48  LOAD_FAST                'ldap_who'
               50  LOAD_FAST                'ldap_pw'
               52  CALL_METHOD_2         2  ''
               54  POP_TOP          
               56  POP_BLOCK        
               58  BREAK_LOOP           94  'to 94'
             60_0  COME_FROM_FINALLY    34  '34'

 L.  71        60  DUP_TOP          
               62  LOAD_GLOBAL              ldap0
               64  LOAD_ATTR                INVALID_CREDENTIALS
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    88  'to 88'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L.  72        76  LOAD_GLOBAL              cli_output
               78  LOAD_STR                 'Password(s) wrong => try again'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          
               84  POP_EXCEPT       
               86  JUMP_BACK             0  'to 0'
             88_0  COME_FROM            68  '68'
               88  END_FINALLY      

 L.  74        90  BREAK_LOOP           94  'to 94'
               92  JUMP_BACK             0  'to 0'

 L.  75        94  LOAD_FAST                'oath_ldap'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 72