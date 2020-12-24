# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/hosts.py
# Compiled at: 2020-03-29 09:54:38
# Size of source mod 2**32: 2122 bytes
"""
aehostd.host - lookup functions for host names and addresses (hosts map)
"""
from __future__ import absolute_import
import logging
from . import req
HOSTS_MAP = {}
HOSTS_NAME_MAP = {}
HOSTS_ADDR_MAP = {}
NSS_REQ_HOST_BYNAME = 327681
NSS_REQ_HOST_BYADDR = 327682
NSS_REQ_HOST_ALL = 327688

def hosts_convert(entry):
    """
    convert an LDAP entry dict to a hosts map tuple
    """
    hostnames = entry['aeFqdn']
    return (hostnames[0], hostnames[1:], entry['ipHostNumber'])


class HostReq(req.Request):
    __doc__ = '\n    base class for handling requests to query hosts map\n    '

    def write(self, result):
        hostname, aliases, addresses = result
        self.tios.write_string(hostname)
        self.tios.write_stringlist(aliases)
        self.tios.write_int32(len(addresses))
        for address in addresses:
            self.tios.write_address(address)


class HostByNameReq(HostReq):
    __doc__ = '\n    handle hosts map query for a certain host name\n    '
    rtype = NSS_REQ_HOST_BYNAME

    def _read_params(self) -> dict:
        return dict(aeFqdn=(self.tios.read_string()))

    def get_results--- This code section failed: ---

 L.  55         0  SETUP_FINALLY        26  'to 26'

 L.  56         2  LOAD_GLOBAL              hosts_convert
                4  LOAD_GLOBAL              HOSTS_MAP
                6  LOAD_GLOBAL              HOSTS_NAME_MAP
                8  LOAD_FAST                'params'
               10  LOAD_STR                 'aeFqdn'
               12  BINARY_SUBSCR    
               14  BINARY_SUBSCR    
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'res'
               22  POP_BLOCK        
               24  JUMP_FORWARD         64  'to 64'
             26_0  COME_FROM_FINALLY     0  '0'

 L.  57        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    62  'to 62'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  58        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _log
               44  LOAD_GLOBAL              logging
               46  LOAD_ATTR                DEBUG
               48  LOAD_STR                 'not found %r'
               50  LOAD_FAST                'params'
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L.  59        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            32  '32'
               62  END_FINALLY      
             64_0  COME_FROM            24  '24'

 L.  60        64  LOAD_FAST                'res'
               66  YIELD_VALUE      
               68  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 58


class HostByAddressReq(HostReq):
    __doc__ = '\n    handle hosts map query for a certain address\n    '
    rtype = NSS_REQ_HOST_BYADDR

    def _read_params(self) -> dict:
        return dict(ipHostNumber=(self.tios.read_address()))

    def get_results--- This code section failed: ---

 L.  74         0  SETUP_FINALLY        26  'to 26'

 L.  75         2  LOAD_GLOBAL              hosts_convert
                4  LOAD_GLOBAL              HOSTS_MAP
                6  LOAD_GLOBAL              HOSTS_ADDR_MAP
                8  LOAD_FAST                'params'
               10  LOAD_STR                 'ipHostNumber'
               12  BINARY_SUBSCR    
               14  BINARY_SUBSCR    
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'res'
               22  POP_BLOCK        
               24  JUMP_FORWARD         64  'to 64'
             26_0  COME_FROM_FINALLY     0  '0'

 L.  76        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    62  'to 62'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  77        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _log
               44  LOAD_GLOBAL              logging
               46  LOAD_ATTR                DEBUG
               48  LOAD_STR                 'not found %r'
               50  LOAD_FAST                'params'
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L.  78        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            32  '32'
               62  END_FINALLY      
             64_0  COME_FROM            24  '24'

 L.  79        64  LOAD_FAST                'res'
               66  YIELD_VALUE      
               68  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 58


class HostAllReq(HostReq):
    __doc__ = '\n    handle hosts map query for a listing all hosts\n    '
    rtype = NSS_REQ_HOST_ALL

    def get_results(self, params):
        for _, host_entry in HOSTS_MAP.items():
            (yield hosts_convert(host_entry))