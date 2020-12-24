# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/group.py
# Compiled at: 2020-04-11 17:07:15
# Size of source mod 2**32: 2867 bytes
__doc__ = '\naehostd.group - group entry lookup routines (group map)\n'
import logging
from .cfg import CFG
from . import req
GROUP_MAP = {}
GROUP_NAME_MAP = {}
GROUP_MEMBER_MAP = {CFG.aehost_vaccount_t[0]: []}
NSS_REQ_GROUP_BYNAME = 262145
NSS_REQ_GROUP_BYGID = 262146
NSS_REQ_GROUP_BYMEMBER = 262150
NSS_REQ_GROUP_ALL = 262152

class GroupReq(req.Request):
    """GroupReq"""

    def write(self, result):
        name, passwd, gid, members = result
        self.tios.write_string(name)
        self.tios.write_string(passwd)
        self.tios.write_int32(gid)
        self.tios.write_stringlist(members)


class GroupByNameReq(GroupReq):
    """GroupByNameReq"""
    rtype = NSS_REQ_GROUP_BYNAME

    def _read_params(self) -> dict:
        name = self.tios.read_string()
        return dict(cn=name)

    def get_results--- This code section failed: ---

 L.  46         0  LOAD_FAST                'params'
                2  LOAD_STR                 'cn'
                4  BINARY_SUBSCR    
                6  LOAD_GLOBAL              CFG
                8  LOAD_ATTR                nss_ignore_groups
               10  COMPARE_OP               in
               12  POP_JUMP_IF_FALSE    38  'to 38'

 L.  47        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _log
               18  LOAD_GLOBAL              logging
               20  LOAD_ATTR                DEBUG
               22  LOAD_STR                 'ignore requested group %r'
               24  LOAD_FAST                'params'
               26  LOAD_STR                 'cn'
               28  BINARY_SUBSCR    
               30  CALL_METHOD_3         3  ''
               32  POP_TOP          

 L.  48        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            12  '12'

 L.  49        38  SETUP_FINALLY        60  'to 60'

 L.  50        40  LOAD_GLOBAL              GROUP_MAP
               42  LOAD_GLOBAL              GROUP_NAME_MAP
               44  LOAD_FAST                'params'
               46  LOAD_STR                 'cn'
               48  BINARY_SUBSCR    
               50  BINARY_SUBSCR    
               52  BINARY_SUBSCR    
               54  STORE_FAST               'res'
               56  POP_BLOCK        
               58  JUMP_FORWARD         98  'to 98'
             60_0  COME_FROM_FINALLY    38  '38'

 L.  51        60  DUP_TOP          
               62  LOAD_GLOBAL              KeyError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    96  'to 96'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  52        74  LOAD_FAST                'self'
               76  LOAD_METHOD              _log
               78  LOAD_GLOBAL              logging
               80  LOAD_ATTR                DEBUG
               82  LOAD_STR                 'not found %r'
               84  LOAD_FAST                'params'
               86  CALL_METHOD_3         3  ''
               88  POP_TOP          

 L.  53        90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            66  '66'
               96  END_FINALLY      
             98_0  COME_FROM            58  '58'

 L.  54        98  LOAD_FAST                'res'
              100  YIELD_VALUE      
              102  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 92


class GroupByGidReq(GroupReq):
    """GroupByGidReq"""
    rtype = NSS_REQ_GROUP_BYGID

    def _read_params(self) -> dict:
        return dict(gidNumber=(self.tios.read_int32()))

    def get_results--- This code section failed: ---

 L.  68         0  LOAD_FAST                'params'
                2  LOAD_STR                 'gidNumber'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'gid'

 L.  69         8  LOAD_FAST                'gid'
               10  LOAD_GLOBAL              CFG
               12  LOAD_ATTR                nss_min_gid
               14  COMPARE_OP               <
               16  POP_JUMP_IF_TRUE     38  'to 38'

 L.  70        18  LOAD_FAST                'gid'
               20  LOAD_GLOBAL              CFG
               22  LOAD_ATTR                nss_max_gid
               24  COMPARE_OP               >

 L.  69        26  POP_JUMP_IF_TRUE     38  'to 38'

 L.  71        28  LOAD_FAST                'gid'
               30  LOAD_GLOBAL              CFG
               32  LOAD_ATTR                nss_ignore_gids
               34  COMPARE_OP               in

 L.  69        36  POP_JUMP_IF_FALSE    58  'to 58'
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            16  '16'

 L.  72        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _log
               42  LOAD_GLOBAL              logging
               44  LOAD_ATTR                DEBUG
               46  LOAD_STR                 'ignore requested GID %d'
               48  LOAD_FAST                'gid'
               50  CALL_METHOD_3         3  ''
               52  POP_TOP          

 L.  73        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            36  '36'

 L.  74        58  SETUP_FINALLY        72  'to 72'

 L.  75        60  LOAD_GLOBAL              GROUP_MAP
               62  LOAD_FAST                'gid'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'res'
               68  POP_BLOCK        
               70  JUMP_FORWARD        110  'to 110'
             72_0  COME_FROM_FINALLY    58  '58'

 L.  76        72  DUP_TOP          
               74  LOAD_GLOBAL              KeyError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   108  'to 108'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  77        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _log
               90  LOAD_GLOBAL              logging
               92  LOAD_ATTR                DEBUG
               94  LOAD_STR                 'not found %r'
               96  LOAD_FAST                'params'
               98  CALL_METHOD_3         3  ''
              100  POP_TOP          

 L.  78       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            78  '78'
              108  END_FINALLY      
            110_0  COME_FROM            70  '70'

 L.  79       110  LOAD_FAST                'res'
              112  YIELD_VALUE      
              114  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 104


class GroupByMemberReq(GroupReq):
    """GroupByMemberReq"""
    rtype = NSS_REQ_GROUP_BYMEMBER

    def _read_params(self) -> dict:
        memberuid = self.tios.read_string()
        return dict(memberUid=memberuid)

    def get_results(self, params):
        member_uid = params['memberUid']
        if member_uid in CFG.nss_ignore_users:
            self._loglogging.DEBUG'ignore requested memberUid %r'member_uid
            return
        for gid in GROUP_MEMBER_MAP.get(member_uid, []):
            name, passwd, gid, _ = GROUP_MAP[gid]
            yield (name, passwd, gid, [member_uid])


class GroupAllReq(GroupReq):
    """GroupAllReq"""
    rtype = NSS_REQ_GROUP_ALL

    def get_results(self, params):
        for _, group_entry in GROUP_MAP.items():
            yield group_entry