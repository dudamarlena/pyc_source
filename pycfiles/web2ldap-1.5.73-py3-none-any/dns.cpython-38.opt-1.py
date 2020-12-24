# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/ldaputil/dns.py
# Compiled at: 2020-05-04 08:36:41
# Size of source mod 2**32: 2123 bytes
"""
ldaputil.dns - basic functions for dealing dc-style DNs and SRV RRs

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import socket
from ldap0.dn import DNObj
from dns import resolver
from web2ldap.log import logger

def srv_lookup(dns_name, srv_prefix: str='_ldap._tcp'):
    """
    Look up SRV RR with name _ldap._tcp.dns_name and return
    list of tuples of results.

    dns_name
          Domain name
    dns_resolver
          Address/port tuple of name server to use.
    """
    if not dns_name:
        return []
    else:
        query_name = '%s.%s' % (srv_prefix, dns_name)
        logger.debug('Query DNS for SRV RR %r', query_name)
        srv_result = resolver.query(query_name, 'SRV')
        return srv_result or []
    srv_result_answers = [(
     res.priority,
     res.weight,
     res.port,
     res.target.to_text().rstrip('.')) for res in srv_result]
    srv_result_answers.sort()
    logger.debug('DNS result for SRV RR %r: %r', query_name, srv_result_answers)
    return srv_result_answers


def dc_dn_lookup--- This code section failed: ---

 L.  60         0  LOAD_FAST                'dn'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.  61         4  BUILD_LIST_0          0 
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  62         8  LOAD_GLOBAL              DNObj
               10  LOAD_METHOD              from_str
               12  LOAD_FAST                'dn'
               14  CALL_METHOD_1         1  ''
               16  LOAD_ATTR                domain
               18  LOAD_CONST               False
               20  LOAD_CONST               ('only_dc',)
               22  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               24  STORE_FAST               'dns_domain'

 L.  63        26  SETUP_FINALLY        40  'to 40'

 L.  64        28  LOAD_GLOBAL              srv_lookup
               30  LOAD_FAST                'dns_domain'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'dns_result'
               36  POP_BLOCK        
               38  JUMP_FORWARD        120  'to 120'
             40_0  COME_FROM_FINALLY    26  '26'

 L.  65        40  DUP_TOP          

 L.  66        42  LOAD_GLOBAL              resolver
               44  LOAD_ATTR                NoAnswer

 L.  67        46  LOAD_GLOBAL              resolver
               48  LOAD_ATTR                NoNameservers

 L.  68        50  LOAD_GLOBAL              resolver
               52  LOAD_ATTR                NotAbsolute

 L.  69        54  LOAD_GLOBAL              resolver
               56  LOAD_ATTR                NoRootSOA

 L.  70        58  LOAD_GLOBAL              resolver
               60  LOAD_ATTR                NXDOMAIN

 L.  71        62  LOAD_GLOBAL              socket
               64  LOAD_ATTR                error

 L.  65        66  BUILD_TUPLE_6         6 
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE   118  'to 118'
               72  POP_TOP          
               74  STORE_FAST               'dns_err'
               76  POP_TOP          
               78  SETUP_FINALLY       106  'to 106'

 L.  73        80  LOAD_GLOBAL              logger
               82  LOAD_METHOD              warning
               84  LOAD_STR                 'Error looking up SRV RR for %s: %s'
               86  LOAD_FAST                'dns_domain'
               88  LOAD_FAST                'dns_err'
               90  CALL_METHOD_3         3  ''
               92  POP_TOP          

 L.  74        94  BUILD_LIST_0          0 
               96  ROT_FOUR         
               98  POP_BLOCK        
              100  POP_EXCEPT       
              102  CALL_FINALLY        106  'to 106'
              104  RETURN_VALUE     
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM_FINALLY    78  '78'
              106  LOAD_CONST               None
              108  STORE_FAST               'dns_err'
              110  DELETE_FAST              'dns_err'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            70  '70'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            38  '38'

 L.  75       120  LOAD_GLOBAL              logger
              122  LOAD_METHOD              debug
              124  LOAD_STR                 'dns_result = %r'
              126  LOAD_FAST                'dns_result'
              128  CALL_METHOD_2         2  ''
              130  POP_TOP          

 L.  76       132  LOAD_LISTCOMP            '<code_object <listcomp>>'
              134  LOAD_STR                 'dc_dn_lookup.<locals>.<listcomp>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  78       138  LOAD_FAST                'dns_result'

 L.  76       140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 98