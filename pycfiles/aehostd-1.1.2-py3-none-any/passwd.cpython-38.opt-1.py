# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/passwd.py
# Compiled at: 2020-04-11 17:06:57
# Size of source mod 2**32: 2353 bytes
"""
aehostd.passwd - lookup functions for user account information (passwd map)
"""
import logging
from .cfg import CFG
from . import req
PASSWD_MAP = {}
PASSWD_NAME_MAP = {}
NSS_REQ_PASSWD_BYNAME = 524289
NSS_REQ_PASSWD_BYUID = 524290
NSS_REQ_PASSWD_ALL = 524296

class PasswdReq(req.Request):
    __doc__ = '\n    base class for handling requests to query passwd map\n    '

    def write(self, result):
        name, passwd, uid, gid, gecos, home, shell = result
        self.tios.write_string(name)
        self.tios.write_string(passwd)
        self.tios.write_int32(uid)
        self.tios.write_int32(gid)
        self.tios.write_string(gecos)
        self.tios.write_string(home)
        self.tios.write_string(shell)


class PasswdByNameReq(PasswdReq):
    __doc__ = '\n    handle passwd map query for a certain user name\n    '
    rtype = NSS_REQ_PASSWD_BYNAME

    def _read_params(self) -> dict:
        name = self.tios.read_string()
        return dict(uid=name)

    def get_results--- This code section failed: ---

 L.  47         0  LOAD_FAST                'params'
                2  LOAD_STR                 'uid'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'username'

 L.  48         8  LOAD_FAST                'username'
               10  LOAD_GLOBAL              CFG
               12  LOAD_ATTR                nss_ignore_users
               14  COMPARE_OP               in
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L.  49        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _log
               22  LOAD_GLOBAL              logging
               24  LOAD_ATTR                DEBUG
               26  LOAD_STR                 'ignore requested user %r'
               28  LOAD_FAST                'username'
               30  CALL_METHOD_3         3  ''
               32  POP_TOP          

 L.  50        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            16  '16'

 L.  51        38  SETUP_FINALLY        56  'to 56'

 L.  52        40  LOAD_GLOBAL              PASSWD_MAP
               42  LOAD_GLOBAL              PASSWD_NAME_MAP
               44  LOAD_FAST                'username'
               46  BINARY_SUBSCR    
               48  BINARY_SUBSCR    
               50  STORE_FAST               'res'
               52  POP_BLOCK        
               54  JUMP_FORWARD         94  'to 94'
             56_0  COME_FROM_FINALLY    38  '38'

 L.  53        56  DUP_TOP          
               58  LOAD_GLOBAL              KeyError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    92  'to 92'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  54        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _log
               74  LOAD_GLOBAL              logging
               76  LOAD_ATTR                DEBUG
               78  LOAD_STR                 'not found %r'
               80  LOAD_FAST                'params'
               82  CALL_METHOD_3         3  ''
               84  POP_TOP          

 L.  55        86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            62  '62'
               92  END_FINALLY      
             94_0  COME_FROM            54  '54'

 L.  56        94  LOAD_FAST                'res'
               96  YIELD_VALUE      
               98  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 88


class PasswdByUidReq(PasswdReq):
    __doc__ = '\n    handle passwd map query for a certain UID\n    '
    rtype = NSS_REQ_PASSWD_BYUID

    def _read_params(self) -> dict:
        return dict(uidNumber=(self.tios.read_int32()))

    def get_results--- This code section failed: ---

 L.  70         0  LOAD_FAST                'params'
                2  LOAD_STR                 'uidNumber'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'userid'

 L.  71         8  LOAD_FAST                'userid'
               10  LOAD_GLOBAL              CFG
               12  LOAD_ATTR                nss_min_uid
               14  COMPARE_OP               <
               16  POP_JUMP_IF_TRUE     38  'to 38'

 L.  72        18  LOAD_FAST                'userid'
               20  LOAD_GLOBAL              CFG
               22  LOAD_ATTR                nss_max_uid
               24  COMPARE_OP               >

 L.  71        26  POP_JUMP_IF_TRUE     38  'to 38'

 L.  73        28  LOAD_FAST                'userid'
               30  LOAD_GLOBAL              CFG
               32  LOAD_ATTR                nss_ignore_uids
               34  COMPARE_OP               in

 L.  71        36  POP_JUMP_IF_FALSE    58  'to 58'
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            16  '16'

 L.  74        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _log
               42  LOAD_GLOBAL              logging
               44  LOAD_ATTR                DEBUG
               46  LOAD_STR                 'ignore requested UID %d'
               48  LOAD_FAST                'userid'
               50  CALL_METHOD_3         3  ''
               52  POP_TOP          

 L.  75        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            36  '36'

 L.  76        58  SETUP_FINALLY        72  'to 72'

 L.  77        60  LOAD_GLOBAL              PASSWD_MAP
               62  LOAD_FAST                'userid'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'res'
               68  POP_BLOCK        
               70  JUMP_FORWARD        130  'to 130'
             72_0  COME_FROM_FINALLY    58  '58'

 L.  78        72  DUP_TOP          
               74  LOAD_GLOBAL              KeyError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   128  'to 128'
               80  POP_TOP          
               82  STORE_FAST               'err'
               84  POP_TOP          
               86  SETUP_FINALLY       116  'to 116'

 L.  79        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _log
               92  LOAD_GLOBAL              logging
               94  LOAD_ATTR                DEBUG
               96  LOAD_STR                 '%r not found: %s'
               98  LOAD_FAST                'params'
              100  LOAD_FAST                'err'
              102  CALL_METHOD_4         4  ''
              104  POP_TOP          

 L.  80       106  POP_BLOCK        
              108  POP_EXCEPT       
              110  CALL_FINALLY        116  'to 116'
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM           110  '110'
            116_1  COME_FROM_FINALLY    86  '86'
              116  LOAD_CONST               None
              118  STORE_FAST               'err'
              120  DELETE_FAST              'err'
              122  END_FINALLY      
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            78  '78'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM            70  '70'

 L.  81       130  LOAD_FAST                'res'
              132  YIELD_VALUE      
              134  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 110


class PasswdAllReq(PasswdReq):
    __doc__ = '\n    handle passwd map query for a listing all users\n    '
    rtype = NSS_REQ_PASSWD_ALL

    def get_results(self, params):
        for _, passwd_entry in PASSWD_MAP.items():
            (yield passwd_entry)