# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/aedir.py
# Compiled at: 2020-04-11 08:17:41
# Size of source mod 2**32: 71551 bytes
"""
web2ldap plugin classes for

Æ-DIR -- Yet another LDAP user and systems management
"""
import re, time, socket
from typing import List
import ldap0, ldap0.filter
from ldap0.pw import random_string
from ldap0.controls.readentry import PreReadControl
from ldap0.controls.deref import DereferenceControl
from ldap0.filter import compose_filter, map_filter_parts
from ldap0.dn import DNObj
from ldap0.res import SearchResultEntry
from ldap0.base import decode_list
import web2ldapcnf
from web2ldap.web.forms import HiddenInput
import web2ldap.ldaputil, web2ldap.app.searchform, web2ldap.app.plugins.inetorgperson, web2ldap.app.plugins.sudoers, web2ldap.app.plugins.ppolicy
from web2ldap.app.plugins.nis import UidNumber, GidNumber, MemberUID, Shell
from web2ldap.app.plugins.inetorgperson import DisplayNameInetOrgPerson
from web2ldap.app.plugins.groups import GroupEntryDN
from web2ldap.app.plugins.oath import OathHOTPToken
from web2ldap.app.plugins.opensshlpk import SshPublicKey
from web2ldap.app.plugins.posixautogen import HomeDirectory
from web2ldap.app.schema.syntaxes import ComposedAttribute, DirectoryString, DistinguishedName, DNSDomain, DerefDynamicDNSelectList, DynamicValueSelectList, IA5String, Integer, NotAfter, NotBefore, RFC822Address, SelectList, syntax_registry
AE_OID_PREFIX = '1.3.6.1.4.1.5427.1.389.100'
AE_USER_OID = AE_OID_PREFIX + '.6.2'
AE_GROUP_OID = AE_OID_PREFIX + '.6.1'
AE_MAILGROUP_OID = AE_OID_PREFIX + '.6.27'
AE_SRVGROUP_OID = AE_OID_PREFIX + '.6.13'
AE_SUDORULE_OID = AE_OID_PREFIX + '.6.7'
AE_HOST_OID = AE_OID_PREFIX + '.6.6.1'
AE_SERVICE_OID = AE_OID_PREFIX + '.6.4'
AE_ZONE_OID = AE_OID_PREFIX + '.6.20'
AE_PERSON_OID = AE_OID_PREFIX + '.6.8'
AE_TAG_OID = AE_OID_PREFIX + '.6.24'
AE_POLICY_OID = AE_OID_PREFIX + '.6.26'
AE_AUTHCTOKEN_OID = AE_OID_PREFIX + '.6.25'
AE_DEPT_OID = AE_OID_PREFIX + '.6.29'
AE_CONTACT_OID = AE_OID_PREFIX + '.6.5'
AE_LOCATION_OID = AE_OID_PREFIX + '.6.35'
AE_NWDEVICE_OID = AE_OID_PREFIX + '.6.6.2'
syntax_registry.reg_at(DNSDomain.oid, [
 AE_OID_PREFIX + '.4.10'])

def ae_validity_filter(secs=None):
    if secs is None:
        secs = time.time()
    return '(&(|(!(aeNotBefore=*))(aeNotBefore<={0}))(|(!(aeNotAfter=*))(aeNotAfter>={0})))'.format(time.strftime('%Y%m%d%H%M%SZ', time.gmtime(secs)))


class AEObjectMixIn:
    __doc__ = '\n    utility mix-in class\n    '

    @property
    def ae_status(self):
        try:
            ae_status = int(self._entry['aeStatus'][0])
        except (KeyError, ValueError, IndexError):
            ae_status = None
        else:
            return ae_status

    def _zone_entry(self, attrlist=None):
        zone_dn = 'cn={0},{1}'.format(self._get_zone_name(), self._app.naming_context)
        try:
            zone = self._app.ls.l.read_s(zone_dn,
              attrlist=attrlist,
              filterstr='(objectClass=aeZone)')
        except ldap0.LDAPError:
            res = {}
        else:
            if zone is None:
                res = {}
            else:
                res = zone.entry_s

    def _get_zone_dn(self) -> str:
        return str(self.dn.slice(None, -len(DNObj.from_str(self._app.naming_context)) - 1))

    def _get_zone_name(self) -> str:
        return self.dn[(-len(DNObj.from_str(self._app.naming_context)) - 1)][0][1]


class AEHomeDirectory(HomeDirectory):
    oid = 'AEHomeDirectory-oid'
    oid: str
    homeDirectoryPrefixes = ('/home', )
    homeDirectoryHidden = b'-/-'

    def _validate(self, attrValue: bytes) -> bool:
        av_u = self._app.ls.uc_decode(attrValue)[0]
        if attrValue == self.homeDirectoryHidden:
            return True
        for prefix in self.homeDirectoryPrefixes:
            if av_u.startswith(prefix):
                uid = self._app.ls.uc_decode(self._entry.get('uid', [b''])[0])[0]
                return av_u.endswith(uid)
            return False

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if attrValues == [self.homeDirectoryHidden]:
            return attrValues
        else:
            if 'uid' in self._entry:
                uid = self._app.ls.uc_decode(self._entry['uid'][0])[0]
            else:
                uid = ''
            if attrValues:
                av_u = self._app.ls.uc_decode(attrValues[0])[0]
                for prefix in self.homeDirectoryPrefixes:
                    if av_u.startswith(prefix):
                        break
                    prefix = self.homeDirectoryPrefixes[0]

            else:
                prefix = self.homeDirectoryPrefixes[0]
        return [
         self._app.ls.uc_encode('/'.join((prefix, uid)))[0]]

    def formField(self) -> str:
        input_field = HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues),
          None,
          default=(self.formValue()))
        input_field.charset = self._app.form.accept_charset
        return input_field


syntax_registry.reg_at((AEHomeDirectory.oid),
  [
 '1.3.6.1.1.1.1.3'],
  structural_oc_oids=[
 AE_USER_OID, AE_SERVICE_OID])

class AEUIDNumber(UidNumber):
    oid = 'AEUIDNumber-oid'
    oid: str
    desc = 'numeric Unix-UID'
    desc: str

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        return self._entry.get('gidNumber', [b''])

    def formField(self) -> str:
        input_field = HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None, default=(self.formValue()))
        input_field.charset = self._app.form.accept_charset
        return input_field


syntax_registry.reg_at((AEUIDNumber.oid),
  [
 '1.3.6.1.1.1.1.0'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_SERVICE_OID])

class AEGIDNumber(GidNumber):
    oid = 'AEGIDNumber-oid'
    oid: str
    desc = 'numeric Unix-GID'
    desc: str
    minNewValue = 30000
    maxNewValue = 49999
    id_pool_dn = None

    def _get_id_pool_dn(self) -> str:
        """
        determine which ID pool entry to use
        """
        return self.id_pool_dn or str(self._app.naming_context)

    def _get_next_gid(self) -> int:
        """
        consumes next ID by sending MOD_INCREMENT modify operation with
        pre-read entry control
        """
        prc = PreReadControl(criticality=True, attrList=[self._at])
        ldap_result = self._app.ls.l.modify_s((self._get_id_pool_dn()),
          [
         (
          ldap0.MOD_INCREMENT, self.at_b, [b'1'])],
          req_ctrls=[
         prc])
        return int(ldap_result.ctrls[0].res.entry_s[self._at][0])

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if attrValues:
            if attrValues[0]:
                return attrValues
        try:
            ldap_result = self._app.ls.l.read_s((self._dn),
              attrlist=[
             self._at],
              filterstr=('({0}=*)'.format(self._at)))
        except (
         ldap0.NO_SUCH_OBJECT,
         ldap0.INSUFFICIENT_ACCESS):
            pass
        else:
            if ldap_result:
                return ldap_result.entry_as[self._at]

    def formValue(self) -> str:
        return Integer.formValue(self)

    def formField(self) -> str:
        return Integer.formField(self)


syntax_registry.reg_at((AEGIDNumber.oid),
  [
 '1.3.6.1.1.1.1.1'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_GROUP_OID,
 AE_SERVICE_OID])

class AEUid(IA5String):
    oid = 'AEUid-oid'
    oid: str
    simpleSanitizers = (bytes.strip,
     bytes.lower)


class AEUserUid(AEUid):
    __doc__ = '\n    Class for auto-generating values for aeUser -> uid\n    '
    oid = 'AEUserUid-oid'
    oid: str
    desc = 'AE-DIR: User name'
    desc: str
    maxValues = 1
    minLen = 4
    minLen: int
    maxLen = 4
    maxLen: int
    maxCollisionChecks = 15
    maxCollisionChecks: int
    UID_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
    reobj = re.compile('^%s$' % UID_LETTERS)
    genLen = 4
    simpleSanitizers = (
     bytes.strip,
     bytes.lower)

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attrValue, entry=entry)

    def _gen_uid(self):
        gen_collisions = 0
        while gen_collisions < self.maxCollisionChecks:
            uid_candidate = random_string(alphabet=(self.UID_LETTERS), length=(self.genLen))
            uid_result = self._app.ls.l.search_s((str(self._app.naming_context)),
              (ldap0.SCOPE_SUBTREE),
              ('(uid=%s)' % ldap0.filter.escape_str(uid_candidate)),
              attrlist=[
             '1.1'])
            if not uid_result:
                return uid_candidate
                gen_collisions += 1

        raise web2ldap.app.core.ErrorExit('Gave up generating new unique <em>uid</em> after %d attempts.' % gen_collisions)

    def formValue(self) -> str:
        form_value = IA5String.formValue(self)
        if not self._av:
            form_value = self._gen_uid()
        return form_value

    def formField(self) -> str:
        return HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None, default=(self.formValue()))

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue.strip().lower()


syntax_registry.reg_at((AEUserUid.oid),
  [
 '0.9.2342.19200300.100.1.1'],
  structural_oc_oids=[
 AE_USER_OID])

class AEServiceUid(AEUid):
    oid = 'AEServiceUid-oid'
    oid: str


syntax_registry.reg_at((AEServiceUid.oid),
  [
 '0.9.2342.19200300.100.1.1'],
  structural_oc_oids=[
 AE_SERVICE_OID])

class AETicketId(IA5String):
    oid = 'AETicketId-oid'
    oid: str
    desc = 'AE-DIR: Ticket no. related to last change of entry'
    desc: str
    simpleSanitizers = (bytes.upper,
     bytes.strip)


syntax_registry.reg_at(AETicketId.oid, [
 AE_OID_PREFIX + '.4.3'])

class AEZoneDN(DerefDynamicDNSelectList):
    oid = 'AEZoneDN-oid'
    oid: str
    desc = 'AE-DIR: Zone'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeZone)(aeStatus=0))'
    ref_attrs = ((None, 'Same zone', None, 'Search all groups constrained to same zone'), )


syntax_registry.reg_at(AEZoneDN.oid, [
 AE_OID_PREFIX + '.4.36'])

class AEHost(DerefDynamicDNSelectList):
    oid = 'AEHost-oid'
    oid: str
    desc = 'AE-DIR: Host'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?host?sub?(&(objectClass=aeHost)(aeStatus=0))'
    ref_attrs = ((None, 'Same host', None, 'Search all services running on same host'), )


syntax_registry.reg_at(AEHost.oid, [
 AE_OID_PREFIX + '.4.28'])

class AENwDevice(DerefDynamicDNSelectList):
    oid = 'AENwDevice-oid'
    oid: str
    desc = 'AE-DIR: network interface'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///..?cn?sub?(&(objectClass=aeNwDevice)(aeStatus=0))'
    ref_attrs = ((None, 'Siblings', None, 'Search sibling network devices'), )

    def _search_root(self) -> str:
        if self._dn.startswith('host='):
            return self._dn
        return DerefDynamicDNSelectList._search_root(self)

    def _filterstr(self):
        orig_filter = DerefDynamicDNSelectList._filterstr(self)
        try:
            dev_name = self._app.ls.uc_decode(self._entry['cn'][0])[0]
        except (KeyError, IndexError):
            result_filter = orig_filter
        else:
            result_filter = '(&{0}(!(cn={1})))'.format(orig_filter, dev_name)
        return result_filter


syntax_registry.reg_at(AENwDevice.oid, [
 AE_OID_PREFIX + '.4.34'])

class AEGroupMember(DerefDynamicDNSelectList, AEObjectMixIn):
    oid = 'AEGroupMember-oid'
    oid: str
    desc = 'AE-DIR: Member of a group'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?displayName?sub?(&(|(objectClass=aeUser)(objectClass=aeService))(aeStatus=0))'
    deref_person_attrs = ('aeDept', 'aeLocation')

    def _zone_filter(self):
        member_zones = [self._app.ls.uc_decode(mezo)[0] for mezo in self._entry.get('aeMemberZone', []) if mezo]
        if member_zones:
            member_zone_filter = compose_filter('|', map_filter_parts('entryDN:dnSubordinateMatch:', member_zones))
        else:
            member_zone_filter = ''
        return member_zone_filter

    def _deref_person_attrset(self):
        result = {}
        for attr_type in self.deref_person_attrs:
            if attr_type in self._entry and list(filter(None, self._entry[attr_type])):
                result[attr_type] = set(self._entry[attr_type])
            return result

    def _filterstr(self):
        return '(&{0}{1})'.format(DerefDynamicDNSelectList._filterstr(self), self._zone_filter())

    def _get_attr_value_dict--- This code section failed: ---

 L. 500         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _deref_person_attrset
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'deref_person_attrset'

 L. 501         8  LOAD_FAST                'deref_person_attrset'
               10  POP_JUMP_IF_TRUE     22  'to 22'

 L. 502        12  LOAD_GLOBAL              DerefDynamicDNSelectList
               14  LOAD_METHOD              _get_attr_value_dict
               16  LOAD_FAST                'self'
               18  CALL_METHOD_1         1  ''
               20  RETURN_VALUE     
             22_0  COME_FROM            10  '10'

 L. 503        22  LOAD_FAST                'deref_person_attrset'
               24  POP_JUMP_IF_FALSE    48  'to 48'

 L. 504        26  LOAD_GLOBAL              DereferenceControl
               28  LOAD_CONST               True
               30  LOAD_STR                 'aePerson'
               32  LOAD_FAST                'deref_person_attrset'
               34  LOAD_METHOD              keys
               36  CALL_METHOD_0         0  ''
               38  BUILD_MAP_1           1 
               40  CALL_FUNCTION_2       2  ''
               42  BUILD_LIST_1          1 
               44  STORE_FAST               'srv_ctrls'
               46  JUMP_FORWARD         52  'to 52'
             48_0  COME_FROM            24  '24'

 L. 506        48  LOAD_CONST               None
               50  STORE_FAST               'srv_ctrls'
             52_0  COME_FROM            46  '46'

 L. 508        52  LOAD_GLOBAL              SelectList
               54  LOAD_METHOD              _get_attr_value_dict
               56  LOAD_FAST                'self'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'attr_value_dict'

 L. 509     62_64  SETUP_FINALLY       384  'to 384'

 L. 510        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _app
               70  LOAD_ATTR                ls
               72  LOAD_ATTR                l
               74  LOAD_ATTR                search_s

 L. 511        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _search_root
               80  CALL_METHOD_0         0  ''

 L. 512        82  LOAD_FAST                'self'
               84  LOAD_ATTR                lu_obj
               86  LOAD_ATTR                scope
               88  JUMP_IF_TRUE_OR_POP    94  'to 94'
               90  LOAD_GLOBAL              ldap0
               92  LOAD_ATTR                SCOPE_SUBTREE
             94_0  COME_FROM            88  '88'

 L. 513        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _filterstr
               98  CALL_METHOD_0         0  ''

 L. 514       100  LOAD_FAST                'self'
              102  LOAD_ATTR                lu_obj
              104  LOAD_ATTR                attrs
              106  LOAD_STR                 'description'
              108  BUILD_LIST_1          1 
              110  BINARY_ADD       

 L. 515       112  LOAD_FAST                'srv_ctrls'

 L. 510       114  LOAD_CONST               ('filterstr', 'attrlist', 'req_ctrls')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  STORE_FAST               'ldap_result'

 L. 517       120  LOAD_FAST                'ldap_result'
              122  GET_ITER         
            124_0  COME_FROM           266  '266'
          124_126  FOR_ITER            380  'to 380'
              128  STORE_FAST               'ldap_res'

 L. 518       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'ldap_res'
              134  LOAD_GLOBAL              SearchResultEntry
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_TRUE    142  'to 142'

 L. 520       140  JUMP_BACK           124  'to 124'
            142_0  COME_FROM           138  '138'

 L. 522       142  LOAD_FAST                'ldap_res'
              144  LOAD_ATTR                ctrls
              146  POP_JUMP_IF_FALSE   206  'to 206'

 L. 523       148  LOAD_FAST                'ldap_res'
              150  LOAD_ATTR                ctrls
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  STORE_FAST               'deref_control'

 L. 524       158  LOAD_GLOBAL              print
              160  LOAD_STR                 'deref_control.derefRes ='
              162  LOAD_GLOBAL              repr
              164  LOAD_FAST                'deref_control'
              166  LOAD_ATTR                derefRes
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_2       2  ''
              172  POP_TOP          

 L. 525       174  LOAD_FAST                'deref_control'
              176  LOAD_ATTR                derefRes
              178  LOAD_STR                 'aePerson'
              180  BINARY_SUBSCR    
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_ATTR                entry_s
              188  STORE_FAST               'deref_entry'

 L. 526       190  LOAD_GLOBAL              print
              192  LOAD_STR                 'deref_entry ='
              194  LOAD_GLOBAL              repr
              196  LOAD_FAST                'deref_entry'
              198  CALL_FUNCTION_1       1  ''
              200  CALL_FUNCTION_2       2  ''
              202  POP_TOP          
              204  JUMP_FORWARD        212  'to 212'
            206_0  COME_FROM           146  '146'

 L. 527       206  LOAD_FAST                'deref_person_attrset'
              208  POP_JUMP_IF_FALSE   212  'to 212'

 L. 530       210  JUMP_BACK           124  'to 124'
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           204  '204'

 L. 532       212  LOAD_CONST               True
              214  STORE_FAST               'valid'

 L. 533       216  LOAD_FAST                'deref_person_attrset'
              218  LOAD_METHOD              items
              220  CALL_METHOD_0         0  ''
              222  GET_ITER         
            224_0  COME_FROM           256  '256'
              224  FOR_ITER            264  'to 264'
              226  UNPACK_SEQUENCE_2     2 
              228  STORE_FAST               'attr_type'
              230  STORE_FAST               'attr_values'

 L. 534       232  LOAD_FAST                'attr_type'
              234  LOAD_FAST                'deref_entry'
              236  COMPARE_OP               not-in
          238_240  POP_JUMP_IF_TRUE    258  'to 258'

 L. 535       242  LOAD_FAST                'deref_entry'
              244  LOAD_FAST                'attr_type'
              246  BINARY_SUBSCR    
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_FAST                'attr_values'
              254  COMPARE_OP               not-in

 L. 534       256  POP_JUMP_IF_FALSE   224  'to 224'
            258_0  COME_FROM           238  '238'

 L. 536       258  LOAD_CONST               False
              260  STORE_FAST               'valid'
              262  JUMP_BACK           224  'to 224'

 L. 537       264  LOAD_FAST                'valid'
              266  POP_JUMP_IF_FALSE   124  'to 124'

 L. 538       268  LOAD_FAST                'ldap_res'
              270  LOAD_ATTR                dn_s
              272  STORE_FAST               'option_value'

 L. 539       274  SETUP_FINALLY       294  'to 294'

 L. 540       276  LOAD_FAST                'ldap_res'
              278  LOAD_ATTR                entry_s
              280  LOAD_STR                 'displayName'
              282  BINARY_SUBSCR    
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  STORE_FAST               'option_text'
              290  POP_BLOCK        
              292  JUMP_FORWARD        320  'to 320'
            294_0  COME_FROM_FINALLY   274  '274'

 L. 541       294  DUP_TOP          
              296  LOAD_GLOBAL              KeyError
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   318  'to 318'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 542       310  LOAD_FAST                'option_value'
              312  STORE_FAST               'option_text'
              314  POP_EXCEPT       
              316  JUMP_FORWARD        320  'to 320'
            318_0  COME_FROM           300  '300'
              318  END_FINALLY      
            320_0  COME_FROM           316  '316'
            320_1  COME_FROM           292  '292'

 L. 543       320  SETUP_FINALLY       340  'to 340'

 L. 544       322  LOAD_FAST                'ldap_res'
              324  LOAD_ATTR                entry_s
              326  LOAD_STR                 'description'
              328  BINARY_SUBSCR    
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
              334  STORE_FAST               'option_title'
              336  POP_BLOCK        
              338  JUMP_FORWARD        366  'to 366'
            340_0  COME_FROM_FINALLY   320  '320'

 L. 545       340  DUP_TOP          
              342  LOAD_GLOBAL              KeyError
              344  COMPARE_OP               exception-match
          346_348  POP_JUMP_IF_FALSE   364  'to 364'
              350  POP_TOP          
              352  POP_TOP          
              354  POP_TOP          

 L. 546       356  LOAD_FAST                'option_value'
              358  STORE_FAST               'option_title'
              360  POP_EXCEPT       
              362  JUMP_FORWARD        366  'to 366'
            364_0  COME_FROM           346  '346'
              364  END_FINALLY      
            366_0  COME_FROM           362  '362'
            366_1  COME_FROM           338  '338'

 L. 547       366  LOAD_FAST                'option_text'
              368  LOAD_FAST                'option_title'
              370  BUILD_TUPLE_2         2 
              372  LOAD_FAST                'attr_value_dict'
              374  LOAD_FAST                'option_value'
              376  STORE_SUBSCR     
              378  JUMP_BACK           124  'to 124'
              380  POP_BLOCK        
              382  JUMP_FORWARD        434  'to 434'
            384_0  COME_FROM_FINALLY    62  '62'

 L. 548       384  DUP_TOP          

 L. 549       386  LOAD_GLOBAL              ldap0
              388  LOAD_ATTR                NO_SUCH_OBJECT

 L. 550       390  LOAD_GLOBAL              ldap0
              392  LOAD_ATTR                SIZELIMIT_EXCEEDED

 L. 551       394  LOAD_GLOBAL              ldap0
              396  LOAD_ATTR                TIMELIMIT_EXCEEDED

 L. 552       398  LOAD_GLOBAL              ldap0
              400  LOAD_ATTR                PARTIAL_RESULTS

 L. 553       402  LOAD_GLOBAL              ldap0
              404  LOAD_ATTR                INSUFFICIENT_ACCESS

 L. 554       406  LOAD_GLOBAL              ldap0
              408  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 555       410  LOAD_GLOBAL              ldap0
              412  LOAD_ATTR                REFERRAL

 L. 548       414  BUILD_TUPLE_7         7 
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   432  'to 432'
              422  POP_TOP          
              424  POP_TOP          
              426  POP_TOP          

 L. 557       428  POP_EXCEPT       
              430  JUMP_FORWARD        434  'to 434'
            432_0  COME_FROM           418  '418'
              432  END_FINALLY      
            434_0  COME_FROM           430  '430'
            434_1  COME_FROM           382  '382'

 L. 558       434  LOAD_FAST                'attr_value_dict'
              436  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 384

    def _validate(self, attrValue: bytes) -> bool:
        if 'memberURL' in self._entry:
            return DistinguishedName._validate(self, attrValue)
        return SelectList._validate(self, attrValue)

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if self.ae_status == 2:
            return []
        return DerefDynamicDNSelectList.transmute(self, attrValues)


syntax_registry.reg_at((AEGroupMember.oid),
  [
 '2.5.4.31'],
  structural_oc_oids=[
 AE_GROUP_OID])

class AEMailGroupMember(AEGroupMember):
    oid = 'AEMailGroupMember-oid'
    oid: str
    desc = 'AE-DIR: Member of a mail group'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?displayName?sub?(&(|(objectClass=inetLocalMailRecipient)(objectClass=aeContact))(mail=*)(aeStatus=0))'


syntax_registry.reg_at((AEMailGroupMember.oid),
  [
 '2.5.4.31'],
  structural_oc_oids=[
 AE_MAILGROUP_OID])

class AEMemberUid(MemberUID, AEObjectMixIn):
    oid = 'AEMemberUid-oid'
    oid: str
    desc = 'AE-DIR: username (uid) of member of a group'
    desc: str
    ldap_url = None
    showValueButton = False
    reobj = AEUserUid.reobj

    def _member_uids_from_member(self):
        return [dn[4:].split(b',')[0] for dn in self._entry.get('member', [])]

    def _validate(self, attrValue: bytes) -> bool:
        """
        Because AEMemberUid.transmute() always resets all attribute values it's
        ok to not validate values thoroughly
        """
        return IA5String._validate(self, attrValue)

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if 'member' not in self._entry:
            return []
        if self.ae_status == 2:
            return []
        return list(filter(None, self._member_uids_from_member()))

    def formValue(self) -> str:
        return ''

    def formField(self) -> str:
        input_field = HiddenInput(self._at, ': '.join([self._at, self.desc]), self.maxLen, self.maxValues, None)
        input_field.charset = self._app.form.accept_charset
        input_field.set_default(self.formValue())
        return input_field


syntax_registry.reg_at((AEMemberUid.oid),
  [
 '1.3.6.1.1.1.1.12'],
  structural_oc_oids=[
 AE_GROUP_OID])

class AEGroupDN(DerefDynamicDNSelectList):
    oid = 'AEGroupDN-oid'
    oid: str
    desc = 'AE-DIR: DN of user group entry'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_??sub?(&(|(objectClass=aeGroup)(objectClass=aeMailGroup))(aeStatus=0))'
    ref_attrs = (('memberOf', 'Members', None, 'Search all member entries of this user group'), )

    def display(self, valueindex=0, commandbutton=False) -> str:
        group_dn = DNObj.from_str(self.av_u)
        group_cn = group_dn[0][0][1]
        r = [
         'cn=<strong>{0}</strong>,{1}'.format(self._app.form.utf2display(group_cn), self._app.form.utf2display(str(group_dn.parent())))]
        if commandbutton:
            r.extend(self._additional_links())
        return web2ldapcnf.command_link_separator.join(r)


syntax_registry.reg_at((AEGroupDN.oid),
  [
 '1.2.840.113556.1.2.102'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_SERVICE_OID,
 AE_CONTACT_OID])

class AEZoneAdminGroupDN(AEGroupDN):
    oid = 'AEZoneAdminGroupDN-oid'
    oid: str
    desc = 'AE-DIR: DN of zone admin group entry'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(objectClass=aeGroup)(aeStatus=0)(cn=*-zone-admins)(!(|(cn:dn:=pub)(cn:dn:=ae))))'


syntax_registry.reg_at(AEZoneAdminGroupDN.oid, [
 AE_OID_PREFIX + '.4.31',
 AE_OID_PREFIX + '.4.33'])

class AEZoneAuditorGroupDN(AEGroupDN):
    oid = 'AEZoneAuditorGroupDN-oid'
    oid: str
    desc = 'AE-DIR: DN of zone auditor group entry'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(objectClass=aeGroup)(aeStatus=0)(|(cn=*-zone-admins)(cn=*-zone-auditors))(!(|(cn:dn:=pub)(cn:dn:=ae))))'


syntax_registry.reg_at(AEZoneAuditorGroupDN.oid, [
 AE_OID_PREFIX + '.4.32'])

class AESrvGroupRightsGroupDN(AEGroupDN):
    oid = 'AESrvGroupRightsGroupDN-oid'
    oid: str
    desc = 'AE-DIR: DN of user group entry'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(objectClass=aeGroup)(aeStatus=0)(!(|(cn:dn:=pub)(cn=*-zone-admins)(cn=*-zone-auditors))))'


syntax_registry.reg_at(AESrvGroupRightsGroupDN.oid, [
 AE_OID_PREFIX + '.4.4',
 AE_OID_PREFIX + '.4.6',
 AE_OID_PREFIX + '.4.7',
 AE_OID_PREFIX + '.4.37'])

class AEDisplayNameGroups(AESrvGroupRightsGroupDN):
    oid = 'AEDisplayNameGroups-oid'
    oid: str
    desc = 'AE-DIR: DN of visible user group entry'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(|(objectClass=aeGroup)(objectClass=aeMailGroup))(aeStatus=0)(!(|(cn:dn:=pub)(cn=*-zone-admins)(cn=*-zone-auditors))))'


syntax_registry.reg_at(AEDisplayNameGroups.oid, [
 AE_OID_PREFIX + '.4.30'])

class AEVisibleGroups(AEDisplayNameGroups):
    oid = 'AEVisibleGroups-oid'
    oid: str
    desc = 'AE-DIR: DN of visible user group entry'
    desc: str
    always_add_groups = ('aeLoginGroups', 'aeDisplayNameGroups')

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        attrValues = set(attrValues)
        for attr_type in self.always_add_groups:
            attrValues.update(self._entry.get(attr_type, []))
        else:
            return list(attrValues)


syntax_registry.reg_at(AEVisibleGroups.oid, [
 AE_OID_PREFIX + '.4.20'])

class AESameZoneObject(DerefDynamicDNSelectList, AEObjectMixIn):
    oid = 'AESameZoneObject-oid'
    oid: str
    desc = 'AE-DIR: DN of referenced aeSrvGroup entry this is proxy for'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeObject)(aeStatus=0))'

    def _search_root(self):
        return self._get_zone_dn()


class AESrvGroup(AESameZoneObject):
    oid = 'AESrvGroup-oid'
    oid: str
    desc = 'AE-DIR: DN of referenced aeSrvGroup entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeSrvGroup)(aeStatus=0)(!(aeProxyFor=*)))'

    def _filterstr(self):
        filter_str = self.lu_obj.filterstr or '(objectClass=*)'
        return '(&%s(!(entryDN=%s)))' % (
         filter_str,
         ldap0.filter.escape_str(str(self.dn.parent())))


syntax_registry.reg_at(AESrvGroup.oid, [
 AE_OID_PREFIX + '.4.27'])

class AERequires(DerefDynamicDNSelectList):
    oid = 'AERequires-oid'
    oid: str
    desc = 'AE-DIR: DN of required aeSrvGroup'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeSrvGroup)(aeStatus=0))'
    ref_attrs = (('aeRequires', 'Same require', None, 'aeSrvGroup', 'Search all service groups depending on this service group.'), )


syntax_registry.reg_at(AERequires.oid, [
 AE_OID_PREFIX + '.4.48'])

class AEProxyFor(AESameZoneObject, AEObjectMixIn):
    oid = 'AEProxyFor-oid'
    oid: str
    desc = 'AE-DIR: DN of referenced aeSrvGroup entry this is proxy for'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeSrvGroup)(aeStatus=0)(!(aeProxyFor=*)))'

    def _filterstr(self):
        filter_str = self.lu_obj.filterstr or '(objectClass=*)'
        return '(&%s(!(entryDN=%s)))' % (
         filter_str,
         self._dn)


syntax_registry.reg_at(AEProxyFor.oid, [
 AE_OID_PREFIX + '.4.25'])

class AETag(DynamicValueSelectList):
    oid = 'AETag-oid'
    oid: str
    desc = 'AE-DIR: cn of referenced aeTag entry'
    desc: str
    ldap_url = 'ldap:///_?cn,cn?sub?(&(objectClass=aeTag)(aeStatus=0))'


syntax_registry.reg_at(AETag.oid, [
 AE_OID_PREFIX + '.4.24'])

class AEEntryDNAEPerson(DistinguishedName):
    oid = 'AEEntryDNAEPerson-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aePerson entry'
    desc: str
    ref_attrs = (('manager', 'Manages', None, 'Search all entries managed by this person'),
                 ('aePerson', 'Users', None, 'aeUser', 'Search all personal AE-DIR user accounts (aeUser entries) of this person.'),
                 ('aeOwner', 'Devices', None, 'aeDevice', 'Search all devices (aeDevice entries) assigned to this person.'))


syntax_registry.reg_at((AEEntryDNAEPerson.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_PERSON_OID])

class AEEntryDNAEUser(DistinguishedName):
    oid = 'AEEntryDNAEUser-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeUser entry'
    desc: str

    def _additional_links(self):
        r = DistinguishedName._additional_links(self)
        if self._app.audit_context:
            r.append(self._app.anchor('search',
              'Activity', (
             (
              'dn', self._app.audit_context),
             ('searchform_mode', 'adv'),
             ('search_attr', 'objectClass'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             ('search_string', 'auditObject'),
             ('search_attr', 'reqAuthzID'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             (
              'search_string', self.av_u)),
              title=('Search modifications made by %s in accesslog DB' % self.av_u)))
        return r


syntax_registry.reg_at((AEEntryDNAEUser.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_USER_OID])

class AEEntryDNAEHost(DistinguishedName):
    oid = 'AEEntryDNAEHost-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeUser entry'
    desc: str
    ref_attrs = (('aeHost', 'Services', None, 'Search all services running on this host'), )

    def _additional_links(self):
        aesrvgroup_filter = ''.join(['(aeSrvGroup=%s)' % av.decode(self._app.ls.charset) for av in self._entry.get('aeSrvGroup', [])])
        r = DistinguishedName._additional_links(self)
        r.extend([
         self._app.anchor('search',
           'Siblings', (
          (
           'dn', self._dn),
          (
           'search_root', str(self._app.naming_context)),
          ('searchform_mode', 'exp'),
          (
           'filterstr',
           '(&(|(objectClass=aeHost)(objectClass=aeService))(|(entryDN:dnSubordinateMatch:=%s)%s))' % (
            ldap0.filter.escape_str(str(self.dn.parent())),
            aesrvgroup_filter))),
           title='Search all host entries which are member in at least one common server group(s) with this host')])
        return r


syntax_registry.reg_at((AEEntryDNAEHost.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_HOST_OID])

class AEEntryDNAEZone(DistinguishedName):
    oid = 'AEEntryDNAEZone-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeZone entry'
    desc: str

    def _additional_links(self):
        r = DistinguishedName._additional_links(self)
        if self._app.audit_context:
            r.append(self._app.anchor('search',
              'Audit all', (
             (
              'dn', self._app.audit_context),
             ('searchform_mode', 'adv'),
             ('search_attr', 'objectClass'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             ('search_string', 'auditObject'),
             ('search_attr', 'reqDN'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_DN_SUBTREE),
             (
              'search_string', self.av_u)),
              title=('Search all audit log entries for sub-tree %s' % self.av_u)))
            r.append(self._app.anchor('search',
              'Audit writes', (
             (
              'dn', self._app.audit_context),
             ('searchform_mode', 'adv'),
             ('search_attr', 'objectClass'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             ('search_string', 'auditObject'),
             ('search_attr', 'reqDN'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_DN_SUBTREE),
             (
              'search_string', self.av_u)),
              title=('Search audit log entries for write operation within sub-tree %s' % self.av_u)))
        return r


syntax_registry.reg_at((AEEntryDNAEZone.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_ZONE_OID])

class AEEntryDNAEMailGroup(GroupEntryDN):
    oid = 'AEEntryDNAEMailGroup-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeGroup entry'
    desc: str
    ref_attrs = (('memberOf', 'Members', None, 'Search all member entries of this mail group'),
                 ('aeVisibleGroups', 'Visible', None, 'Search all server/service groups (aeSrvGroup)\non which this mail group is visible'))


syntax_registry.reg_at((AEEntryDNAEMailGroup.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_MAILGROUP_OID])

class AEEntryDNAEGroup(GroupEntryDN):
    oid = 'AEEntryDNAEGroup-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeGroup entry'
    desc: str
    ref_attrs = (('memberOf', 'Members', None, 'Search all member entries of this user group'),
                 ('aeLoginGroups', 'Login', None, 'Search all server/service groups (aeSrvGroup)\non which this user group has login right'),
                 ('aeLogStoreGroups', 'View Logs', None, 'Search all server/service groups (aeSrvGroup)\non which this user group has log view right'),
                 ('aeSetupGroups', 'Setup', None, 'Search all server/service groups (aeSrvGroup)\non which this user group has setup/installation rights'),
                 ('aeVisibleGroups', 'Visible', None, 'Search all server/service groups (aeSrvGroup)\non which this user group is at least visible'))

    def _additional_links(self):
        aegroup_cn = self._entry['cn'][0].decode(self._app.ls.charset)
        ref_attrs = list(AEEntryDNAEGroup.ref_attrs)
        if aegroup_cn.endswith('zone-admins'):
            ref_attrs.extend([
             ('aeZoneAdmins', 'Zone Admins', None, 'Search all zones (aeZone)\nfor which members of this user group act as zone admins'),
             ('aePasswordAdmins', 'Password Admins', None, 'Search all zones (aeZone)\nfor which members of this user group act as password admins')])
        if aegroup_cn.endswith('zone-auditors') or aegroup_cn.endswith('zone-admins'):
            ref_attrs.append(('aeZoneAuditors', 'Zone Auditors', None, 'Search all zones (aeZone)\nfor which members of this user group act as zone auditors'))
        self.ref_attrs = tuple(ref_attrs)
        r = DistinguishedName._additional_links(self)
        r.append(self._app.anchor('search',
          'SUDO rules', (
         (
          'dn', self._dn),
         (
          'search_root', str(self._app.naming_context)),
         ('searchform_mode', 'adv'),
         ('search_attr', 'sudoUser'),
         (
          'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
         (
          'search_string', '%' + self._entry['cn'][0].decode(self._app.ls.charset))),
          title='Search for SUDO rules\napplicable with this user group'))
        return r


syntax_registry.reg_at((AEEntryDNAEGroup.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_GROUP_OID])

class AEEntryDNAESrvGroup(DistinguishedName):
    oid = 'AEEntryDNAESrvGroup-oid'
    oid: str
    desc = 'AE-DIR: entryDN'
    desc: str
    ref_attrs = (('aeProxyFor', 'Proxy', None, 'Search access gateway/proxy group for this server group'),
                 ('aeRequires', 'Required by', None, 'aeSrvGroup', 'Search all service groups depending on this service group.'))

    def _additional_links(self):
        r = DistinguishedName._additional_links(self)
        r.append(self._app.anchor('search',
          'All members', (
         (
          'dn', self._dn),
         (
          'search_root', str(self._app.naming_context)),
         ('searchform_mode', 'exp'),
         (
          'filterstr',
          '(&(|(objectClass=aeHost)(objectClass=aeService))(|(entryDN:dnSubordinateMatch:={0})(aeSrvGroup={0})))'.format(self.av_u))),
          title=('Search all service and host entries which are member in this service/host group {0}'.format(self.av_u))))
        return r


syntax_registry.reg_at((AEEntryDNAESrvGroup.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_SRVGROUP_OID])

class AEEntryDNSudoRule(DistinguishedName):
    oid = 'AEEntryDNSudoRule-oid'
    oid: str
    desc = 'AE-DIR: entryDN'
    desc: str
    ref_attrs = (('aeVisibleSudoers', 'Used on', None, 'Search all server groups (aeSrvGroup entries) referencing this SUDO rule'), )


syntax_registry.reg_at((AEEntryDNSudoRule.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_SUDORULE_OID])

class AEEntryDNAELocation(DistinguishedName):
    oid = 'AEEntryDNAELocation-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeLocation entry'
    desc: str
    ref_attrs = (('aeLocation', 'Persons', None, 'aePerson', 'Search all persons assigned to this location.'),
                 ('aeLocation', 'Zones', None, 'aeZone', 'Search all location-based zones associated with this location.'),
                 ('aeLocation', 'Groups', None, 'groupOfEntries', 'Search all location-based zones associated with this location.'))


syntax_registry.reg_at((AEEntryDNAELocation.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_LOCATION_OID])

class AELocation(DerefDynamicDNSelectList):
    oid = 'AELocation-oid'
    oid: str
    desc = 'AE-DIR: DN of location entry'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?displayName?sub?(&(objectClass=aeLocation)(aeStatus=0))'
    ref_attrs = AEEntryDNAELocation.ref_attrs


syntax_registry.reg_at(AELocation.oid, [
 AE_OID_PREFIX + '.4.35'])

class AEEntryDNAEDept(DistinguishedName):
    oid = 'AEEntryDNAEDept-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aePerson entry'
    desc: str
    ref_attrs = (('aeDept', 'Persons', None, 'aePerson', 'Search all persons assigned to this department.'),
                 ('aeDept', 'Zones', None, 'aeZone', 'Search all team-related zones associated with this department.'),
                 ('aeDept', 'Groups', None, 'groupOfEntries', 'Search all team-related groups associated with this department.'))


syntax_registry.reg_at((AEEntryDNAEDept.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_DEPT_OID])

class AEDept(DerefDynamicDNSelectList):
    oid = 'AEDept-oid'
    oid: str
    desc = 'AE-DIR: DN of department entry'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?displayName?sub?(&(objectClass=aeDept)(aeStatus=0))'
    ref_attrs = AEEntryDNAEDept.ref_attrs


syntax_registry.reg_at(AEDept.oid, [
 AE_OID_PREFIX + '.4.29'])

class AEOwner(DerefDynamicDNSelectList):
    oid = 'AEOwner-oid'
    oid: str
    desc = 'AE-DIR: DN of owner entry'
    desc: str
    ldap_url = 'ldap:///_?displayName?sub?(&(objectClass=aePerson)(aeStatus=0))'
    ref_attrs = (('aeOwner', 'Devices', None, 'aeDevice', 'Search all devices (aeDevice entries) assigned to same owner.'), )


syntax_registry.reg_at(AEOwner.oid, [
 AE_OID_PREFIX + '.4.2'])

class AEPerson(DerefDynamicDNSelectList, AEObjectMixIn):
    oid = 'AEPerson-oid'
    oid: str
    desc = 'AE-DIR: DN of person entry'
    desc: str
    ldap_url = 'ldap:///_?displayName?sub?(objectClass=aePerson)'
    ref_attrs = (('aePerson', 'Users', None, 'aeUser', 'Search all personal AE-DIR user accounts (aeUser entries) of this person.'), )
    ae_status_map = {-1:(-1, 0), 
     0:(0, ), 
     1:(0, 1, 2), 
     2:(0, 1, 2)}
    deref_attrs = ('aeDept', 'aeLocation')

    def _status_filter(self):
        ae_status = self.ae_status or 0
        return compose_filter('|', map_filter_parts('aeStatus', map(str, self.ae_status_map.get(ae_status, []))))

    def _filterstr(self):
        filter_components = [
         DerefDynamicDNSelectList._filterstr(self),
         self._status_filter()]
        zone_entry = self._zone_entry(attrlist=(self.deref_attrs))
        for deref_attr_type in self.deref_attrs:
            deref_attr_values = [z for z in zone_entry.get(deref_attr_type, []) if z]
            if deref_attr_values:
                filter_components.append(compose_filter('|', map_filter_parts(deref_attr_type, deref_attr_values)))
            ocs = self._entry.object_class_oid_set()
            if 'inetLocalMailRecipient' not in ocs:
                filter_components.append('(mail=*)')
            filter_str = '(&{})'.format(''.join(filter_components))
            return filter_str

    def _validate(self, attrValue: bytes) -> bool:
        if self.ae_status == 2:
            return True
        return DerefDynamicDNSelectList._validate(self, attrValue)


syntax_registry.reg_at(AEPerson.oid, [
 AE_OID_PREFIX + '.4.16'])

class AEManager(DerefDynamicDNSelectList):
    oid = 'AEManager-oid'
    oid: str
    desc = 'AE-DIR: Manager responsible for a person/department'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?displayName?sub?(&(objectClass=aePerson)(aeStatus=0))'


syntax_registry.reg_at((AEManager.oid),
  [
 '0.9.2342.19200300.100.1.10'],
  structural_oc_oids=[
 AE_PERSON_OID,
 AE_DEPT_OID])

class AEDerefAttribute(DirectoryString):
    oid = 'AEDerefAttribute-oid'
    oid: str
    maxValues = 1
    deref_object_class = None
    deref_attribute_type = None
    deref_filter_tmpl = '(&(objectClass={deref_object_class})(aeStatus<=0)({attribute_type}=*))'

    def _read_person_attr(self):
        try:
            sre = self._app.ls.l.read_s((self._entry[self.deref_attribute_type][0].decode(self._app.ls.charset)),
              attrlist=[
             self._at],
              filterstr=self.deref_filter_tmpl.format(deref_object_class=(self.deref_object_class),
              attribute_type=(self._at)))
        except ldap0.LDAPError:
            return
        else:
            if sre is None:
                return
            return sre.entry_s[self._at][0]

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if self.deref_attribute_type in self._entry:
            ae_person_attribute = self._read_person_attr()
            if ae_person_attribute is not None:
                result = [
                 ae_person_attribute.encode(self._app.ls.charset)]
            else:
                result = []
        else:
            result = attrValues
        return result

    def formValue(self) -> str:
        return ''

    def formField(self) -> str:
        input_field = HiddenInput(self._at, ': '.join([self._at, self.desc]), self.maxLen, self.maxValues, None)
        input_field.charset = self._app.form.accept_charset
        input_field.set_default(self.formValue())
        return input_field


class AEPersonAttribute(AEDerefAttribute):
    oid = 'AEPersonAttribute-oid'
    oid: str
    maxValues = 1
    deref_object_class = 'aePerson'
    deref_attribute_type = 'aePerson'


class AEUserNames(AEPersonAttribute, DirectoryString):
    oid = 'AEUserNames-oid'
    oid: str


syntax_registry.reg_at((AEUserNames.oid),
  [
 '2.5.4.4',
 '2.5.4.42'],
  structural_oc_oids=[
 AE_USER_OID])

class AEMailLocalAddress(RFC822Address):
    oid = 'AEMailLocalAddress-oid'
    oid: str
    simpleSanitizers = (bytes.strip,
     bytes.lower)


syntax_registry.reg_at((AEMailLocalAddress.oid),
  [
 '2.16.840.1.113730.3.1.13'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_SERVICE_OID])

class AEUserMailaddress(AEPersonAttribute, SelectList):
    oid = 'AEUserMailaddress-oid'
    oid: str
    html_tmpl = RFC822Address.html_tmpl
    maxValues = 1
    input_fallback = False
    simpleSanitizers = AEMailLocalAddress.simpleSanitizers

    def _get_attr_value_dict(self):
        attr_value_dict = {'': '-/-'}
        attr_value_dict.update([(
         addr.decode(self._app.ls.charset), addr.decode(self._app.ls.charset)) for addr in self._entry.get('mailLocalAddress', [])])
        return attr_value_dict

    def _is_mail_account(self):
        return b'inetLocalMailRecipient' in self._entry['objectClass']

    def _validate(self, attrValue: bytes) -> bool:
        if self._is_mail_account():
            return SelectList._validate(self, attrValue)
        return AEPersonAttribute._validate(self, attrValue)

    def formValue(self) -> str:
        if self._is_mail_account():
            return SelectList.formValue(self)
        return AEPersonAttribute.formValue(self)

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if self._is_mail_account() and not list(filter(None, map(bytes.strip, attrValues))):
            try:
                attrValues = [
                 self._entry['mailLocalAddress'][0]]
            except KeyError:
                attrValues = []

        else:
            attrValues = AEPersonAttribute.transmute(self, attrValues)
        return attrValues

    def formField(self) -> str:
        if self._is_mail_account():
            return SelectList.formField(self)
        return AEPersonAttribute.formField(self)


syntax_registry.reg_at((AEUserMailaddress.oid),
  [
 '0.9.2342.19200300.100.1.3'],
  structural_oc_oids=[
 AE_USER_OID])

class AEPersonMailaddress(DynamicValueSelectList, RFC822Address):
    oid = 'AEPersonMailaddress-oid'
    oid: str
    maxValues = 1
    ldap_url = 'ldap:///_?mail,mail?sub?'
    input_fallback = True
    html_tmpl = RFC822Address.html_tmpl

    def _validate--- This code section failed: ---

 L.1502         0  LOAD_GLOBAL              RFC822Address
                2  LOAD_METHOD              _validate
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'attrValue'
                8  CALL_METHOD_2         2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.1503        12  LOAD_CONST               False
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.1504        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _get_attr_value_dict
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'attr_value_dict'

 L.1506        24  LOAD_FAST                'attr_value_dict'

 L.1505        26  POP_JUMP_IF_FALSE    56  'to 56'

 L.1508        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'attr_value_dict'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  COMPARE_OP               ==

 L.1505        38  POP_JUMP_IF_FALSE    60  'to 60'

 L.1509        40  LOAD_GLOBAL              tuple
               42  LOAD_FAST                'attr_value_dict'
               44  LOAD_METHOD              keys
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               ('',)
               52  COMPARE_OP               ==

 L.1505        54  POP_JUMP_IF_FALSE    60  'to 60'
             56_0  COME_FROM            26  '26'

 L.1512        56  LOAD_CONST               True
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'
             60_1  COME_FROM            38  '38'

 L.1513        60  LOAD_GLOBAL              DynamicValueSelectList
               62  LOAD_METHOD              _validate
               64  LOAD_FAST                'self'
               66  LOAD_FAST                'attrValue'
               68  CALL_METHOD_2         2  ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 70

    def _filterstr(self):
        return '(&(objectClass=aeUser)(objectClass=inetLocalMailRecipient)(aeStatus=0)(aePerson=%s)(mailLocalAddress=*))' % ldap0.filter.escape_str(self._dn)


syntax_registry.reg_at((AEPersonMailaddress.oid),
  [
 '0.9.2342.19200300.100.1.3'],
  structural_oc_oids=[
 AE_PERSON_OID])

class AEDeptAttribute(AEDerefAttribute, DirectoryString):
    oid = 'AEDeptAttribute-oid'
    oid: str
    maxValues = 1
    deref_object_class = 'aeDept'
    deref_attribute_type = 'aeDept'


syntax_registry.reg_at((AEDeptAttribute.oid),
  [
 '2.16.840.1.113730.3.1.2',
 '2.5.4.11'],
  structural_oc_oids=[
 AE_PERSON_OID])

class AEHostname(DNSDomain):
    oid = 'AEHostname-oid'
    oid: str
    desc = 'Canonical hostname / FQDN'
    desc: str
    host_lookup = 0

    def _validate(self, attrValue: bytes) -> bool:
        if not DNSDomain._validate(self, attrValue):
            return False
        if self.host_lookup:
            try:
                ip_addr = socket.gethostbyname(attrValue)
            except (socket.gaierror, socket.herror):
                return False

            if self.host_lookup >= 2:
                try:
                    reverse_hostname = socket.gethostbyaddr(ip_addr)[0]
                except (socket.gaierror, socket.herror):
                    return False
                else:
                    return reverse_hostname == attrValue
        return True

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        result = []
        for attr_value in attrValues:
            attr_value.lower().strip()
            if self.host_lookup:
                try:
                    ip_addr = socket.gethostbyname(attr_value)
                    reverse_hostname = socket.gethostbyaddr(ip_addr)[0]
                except (socket.gaierror, socket.herror):
                    pass
                else:
                    attr_value = reverse_hostname.encode(self._app.ls.charset)
            result.append(attr_value)
        else:
            return attrValues


syntax_registry.reg_at((AEHostname.oid),
  [
 '0.9.2342.19200300.100.1.9'],
  structural_oc_oids=[
 AE_HOST_OID])

class AEDisplayNameUser(ComposedAttribute, DirectoryString):
    oid = 'AEDisplayNameUser-oid'
    oid: str
    desc = 'Attribute displayName in object class aeUser'
    desc: str
    compose_templates = ('{givenName} {sn} ({uid}/{uidNumber})', '{givenName} {sn} ({uid})')


syntax_registry.reg_at((AEDisplayNameUser.oid),
  [
 '2.16.840.1.113730.3.1.241'],
  structural_oc_oids=[
 AE_USER_OID])

class AEDisplayNameContact(ComposedAttribute, DirectoryString):
    oid = 'AEDisplayNameContact-oid'
    oid: str
    desc = 'Attribute displayName in object class aeContact'
    desc: str
    compose_templates = ('{cn} <{mail}>', '{cn}')


syntax_registry.reg_at((AEDisplayNameContact.oid),
  [
 '2.16.840.1.113730.3.1.241'],
  structural_oc_oids=[
 AE_CONTACT_OID])

class AEDisplayNameDept(ComposedAttribute, DirectoryString):
    oid = 'AEDisplayNameDept-oid'
    oid: str
    desc = 'Attribute displayName in object class aeDept'
    desc: str
    compose_templates = ('{ou} ({departmentNumber})', '{ou}', '#{departmentNumber}')


syntax_registry.reg_at((AEDisplayNameDept.oid),
  [
 '2.16.840.1.113730.3.1.241'],
  structural_oc_oids=[
 AE_DEPT_OID])

class AEDisplayNameLocation(ComposedAttribute, DirectoryString):
    oid = 'AEDisplayNameLocation-oid'
    oid: str
    desc = 'Attribute displayName in object class aeLocation'
    desc: str
    compose_templates = ('{cn}: {l}, {street}', '{cn}: {l}', '{cn}: {street}', '{cn}: {st}',
                         '{cn}')


syntax_registry.reg_at((AEDisplayNameLocation.oid),
  [
 '2.16.840.1.113730.3.1.241'],
  structural_oc_oids=[
 AE_LOCATION_OID])

class AEDisplayNamePerson(DisplayNameInetOrgPerson):
    oid = 'AEDisplayNamePerson-oid'
    oid: str
    desc = 'Attribute displayName in object class aePerson'
    desc: str
    compose_templates = ('{givenName} {sn} / {ou}', '{givenName} {sn} / #{departmentNumber}',
                         '{givenName} {sn} ({uniqueIdentifier})', '{givenName} {sn}')


syntax_registry.reg_at((AEDisplayNamePerson.oid),
  [
 '2.16.840.1.113730.3.1.241'],
  structural_oc_oids=[
 AE_PERSON_OID])

class AEUniqueIdentifier(DirectoryString):
    oid = 'AEUniqueIdentifier-oid'
    oid: str
    maxValues = 1
    gen_template = 'web2ldap-{timestamp}'

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        return attrValues and attrValues[0].strip() or [
         self.gen_template.format(timestamp=(time.time())).encode(self._app.ls.charset)]
        return attrValues

    def formField(self) -> str:
        input_field = HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None, default=(self.formValue()))
        input_field.charset = self._app.form.accept_charset
        return input_field


syntax_registry.reg_at((AEUniqueIdentifier.oid),
  [
 '0.9.2342.19200300.100.1.44'],
  structural_oc_oids=[
 AE_PERSON_OID])

class AEDepartmentNumber(DirectoryString):
    oid = 'AEDepartmentNumber-oid'
    oid: str
    maxValues = 1


syntax_registry.reg_at((AEDepartmentNumber.oid),
  [
 '2.16.840.1.113730.3.1.2'],
  structural_oc_oids=[
 AE_DEPT_OID])

class AECommonName(DirectoryString):
    oid = 'AECommonName-oid'
    oid: str
    desc = 'AE-DIR: common name of aeObject'
    desc: str
    maxValues = 1
    simpleSanitizers = (
     bytes.strip,)


class AECommonNameAEZone(AECommonName):
    oid = 'AECommonNameAEZone-oid'
    oid: str
    desc = 'AE-DIR: common name of aeZone'
    desc: str
    simpleSanitizers = (bytes.strip,
     bytes.lower)


syntax_registry.reg_at((AECommonNameAEZone.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_ZONE_OID])

class AECommonNameAELocation(AECommonName):
    oid = 'AECommonNameAELocation-oid'
    oid: str
    desc = 'AE-DIR: common name of aeLocation'
    desc: str


syntax_registry.reg_at((AECommonNameAELocation.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_LOCATION_OID])

class AECommonNameAEHost(AECommonName):
    oid = 'AECommonNameAEHost-oid'
    oid: str
    desc = 'Canonical hostname'
    desc: str
    derive_from_host = True
    host_begin_item = 0
    host_end_item = None

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if self.derive_from_host:
            return list(set([(b'.').join(av.strip().lower().split(b'.')[self.host_begin_item:self.host_end_item]) for av in self._entry['host']]))
        return attrValues


syntax_registry.reg_at((AECommonNameAEHost.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_HOST_OID])

class AEZonePrefixCommonName(AECommonName, AEObjectMixIn):
    oid = 'AEZonePrefixCommonName-oid'
    oid: str
    desc = 'AE-DIR: Attribute values have to be prefixed with zone name'
    desc: str
    reObj = re.compile('^[a-z0-9]+-[a-z0-9-]+$')
    special_names = {
     'zone-admins',
     'zone-auditors'}

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue.strip()

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        attrValues = [attrValues[0].lower()]
        return attrValues

    def _validate(self, attrValue: bytes) -> bool:
        result = DirectoryString._validate(self, attrValue)
        if result:
            if attrValue:
                zone_cn = self._get_zone_name()
                result = zone_cn and (zone_cn == 'pub' or attrValue.decode(self._app.ls.charset).startswith(zone_cn + '-'))
        return result

    def formValue(self) -> str:
        result = DirectoryString.formValue(self)
        zone_cn = self._get_zone_name()
        if zone_cn:
            if not self._av:
                result = zone_cn + '-'
            else:
                if self._av_u in self.special_names:
                    result = '-'.join((zone_cn, self.av_u))
        return result


class AECommonNameAEGroup(AEZonePrefixCommonName):
    oid = 'AECommonNameAEGroup-oid'
    oid: str


syntax_registry.reg_at((AECommonNameAEGroup.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_GROUP_OID,
 AE_MAILGROUP_OID])

class AECommonNameAESrvGroup(AEZonePrefixCommonName):
    oid = 'AECommonNameAESrvGroup-oid'
    oid: str


syntax_registry.reg_at((AECommonNameAESrvGroup.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_SRVGROUP_OID])

class AECommonNameAETag(AEZonePrefixCommonName):
    oid = 'AECommonNameAETag-oid'
    oid: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        display_value = AEZonePrefixCommonName.display(self, valueindex, commandbutton)
        if commandbutton:
            search_anchor = self._app.anchor('searchform',
              '&raquo;', (
             (
              'dn', self._dn),
             (
              'search_root', str(self._app.naming_context)),
             ('searchform_mode', 'adv'),
             ('search_attr', 'aeTag'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             (
              'search_string', self.av_u)),
              title='Search all entries tagged with this tag')
        else:
            search_anchor = ''
        return ''.join((display_value, search_anchor))


syntax_registry.reg_at((AECommonNameAETag.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_TAG_OID])

class AECommonNameAESudoRule(AEZonePrefixCommonName):
    oid = 'AECommonNameAESudoRule-oid'
    oid: str


syntax_registry.reg_at((AECommonNameAESudoRule.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_SUDORULE_OID])
syntax_registry.reg_at((web2ldap.app.plugins.inetorgperson.CNInetOrgPerson.oid),
  [
 '2.5.4.3'],
  structural_oc_oids=[
 AE_PERSON_OID,
 AE_USER_OID])

class AESudoRuleDN(DerefDynamicDNSelectList):
    oid = 'AESudoRuleDN-oid'
    oid: str
    desc = 'AE-DIR: DN(s) of visible SUDO rules'
    desc: str
    input_fallback = False
    ldap_url = 'ldap:///_?cn?sub?(&(objectClass=aeSudoRule)(aeStatus=0))'


syntax_registry.reg_at(AESudoRuleDN.oid, [
 AE_OID_PREFIX + '.4.21'])

class AENotBefore(NotBefore):
    oid = 'AENotBefore-oid'
    oid: str
    desc = 'AE-DIR: begin of validity period'
    desc: str


syntax_registry.reg_at(AENotBefore.oid, [
 AE_OID_PREFIX + '.4.22'])

class AENotAfter(NotAfter):
    oid = 'AENotAfter-oid'
    oid: str
    desc = 'AE-DIR: begin of validity period'
    desc: str

    def _validate(self, attrValue: bytes) -> bool:
        result = NotAfter._validate(self, attrValue)
        if result:
            ae_not_after = time.strptime(attrValue.decode('ascii'), '%Y%m%d%H%M%SZ')
            if not 'aeNotBefore' not in self._entry:
                if not (self._entry['aeNotBefore'] and self._entry['aeNotBefore'][0]):
                    return True
                    try:
                        ae_not_before = time.strptime(self._entry['aeNotBefore'][0].decode('ascii'), '%Y%m%d%H%M%SZ')
                    except KeyError:
                        result = True
                    except (UnicodeDecodeError, ValueError):
                        result = False
                    else:
                        result = ae_not_before <= ae_not_after
        return result


syntax_registry.reg_at(AENotAfter.oid, [
 AE_OID_PREFIX + '.4.23'])

class AEStatus(SelectList, Integer):
    oid = 'AEStatus-oid'
    oid: str
    desc = 'AE-DIR: Status of object'
    desc: str
    attr_value_dict = {'-1':'requested',  '0':'active', 
     '1':'deactivated', 
     '2':'archived'}

    def _validate(self, attrValue: bytes) -> bool:
        result = SelectList._validate(self, attrValue)
        return result and attrValue or result
        ae_status = int(attrValue)
        current_time = time.gmtime(time.time())
        try:
            ae_not_before = time.strptime(self._entry['aeNotBefore'][0].decode('ascii'), '%Y%m%d%H%M%SZ')
        except (KeyError, IndexError, ValueError, UnicodeDecodeError):
            ae_not_before = time.strptime('19700101000000Z', '%Y%m%d%H%M%SZ')
        else:
            try:
                ae_not_after = time.strptime(self._entry['aeNotAfter'][0].decode('ascii'), '%Y%m%d%H%M%SZ')
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                ae_not_after = current_time
            else:
                if current_time > ae_not_after:
                    result = ae_status >= 1
                else:
                    if current_time < ae_not_before:
                        result = ae_status == -1
                    else:
                        result = ae_not_before <= current_time <= ae_not_after
                return result

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        return attrValues and attrValues[0] or attrValues
        ae_status = int(attrValues[0].decode('ascii'))
        current_time = time.gmtime(time.time())
        try:
            ae_not_before = time.strptime(self._entry['aeNotBefore'][0].decode('ascii'), '%Y%m%d%H%M%SZ')
        except (KeyError, IndexError, ValueError):
            ae_not_before = None
        else:
            if ae_status == 0:
                if current_time < ae_not_before:
                    ae_status = -1
        try:
            ae_not_after = time.strptime(self._entry['aeNotAfter'][0].decode('ascii'), '%Y%m%d%H%M%SZ')
        except (KeyError, IndexError, ValueError):
            ae_not_after = None
        else:
            if current_time > ae_not_after:
                try:
                    ae_expiry_status = int(self._entry.get('aeExpiryStatus', ['1'])[0].decode('ascii'))
                except (KeyError, IndexError, ValueError):
                    pass

                if ae_status <= ae_expiry_status:
                    ae_status = ae_expiry_status
            return [
             str(ae_status).encode('ascii')]

    def display(self, valueindex=0, commandbutton=False) -> str:
        if not commandbutton:
            return Integer.display(self, valueindex)
        return SelectList.display(self, valueindex, commandbutton)


syntax_registry.reg_at(AEStatus.oid, [
 AE_OID_PREFIX + '.4.5'])

class AEExpiryStatus(SelectList):
    oid = 'AEExpiryStatus-oid'
    oid: str
    desc = 'AE-DIR: Expiry status of object'
    desc: str
    attr_value_dict = {'-/-':'',  '1':'deactivated', 
     '2':'archived'}


syntax_registry.reg_at(AEStatus.oid, [
 AE_OID_PREFIX + '.4.46'])

class AESudoUser(web2ldap.app.plugins.sudoers.SudoUserGroup):
    oid = 'AESudoUser-oid'
    oid: str
    desc = 'AE-DIR: sudoUser'
    desc: str
    ldap_url = 'ldap:///_?cn,cn?sub?(&(objectClass=aeGroup)(aeStatus=0)(!(|(cn=ae-admins)(cn=ae-auditors)(cn=ae-providers)(cn=ae-replicas)(cn=ae-login-proxies)(cn=*-zone-admins)(cn=*-zone-auditors))))'


syntax_registry.reg_at((AESudoUser.oid),
  [
 '1.3.6.1.4.1.15953.9.1.1'],
  structural_oc_oids=[
 AE_SUDORULE_OID])

class AEServiceSshPublicKey(SshPublicKey):
    oid = 'AEServiceSshPublicKey-oid'
    oid: str
    desc = 'AE-DIR: aeService:sshPublicKey'
    desc: str


syntax_registry.reg_at((AEServiceSshPublicKey.oid),
  [
 '1.3.6.1.4.1.24552.500.1.1.1.13'],
  structural_oc_oids=[
 AE_SERVICE_OID])

class AEEntryDNAEAuthcToken(DistinguishedName):
    oid = 'AEEntryDNAEAuthcToken-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aeAuthcToken entry'
    desc: str
    ref_attrs = (('oathToken', 'Users', None, 'aeUser', 'Search all personal user accounts using this OATH token.'), )


syntax_registry.reg_at((AEEntryDNAEAuthcToken.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_AUTHCTOKEN_OID])

class AEEntryDNAEPolicy(DistinguishedName):
    oid = 'AEEntryDNAEPolicy-oid'
    oid: str
    desc = 'AE-DIR: entryDN of aePolicy entry'
    desc: str
    ref_attrs = (('pwdPolicySubentry', 'Users', None, 'aeUser', 'Search all personal user accounts restricted by this password policy.'),
                 ('pwdPolicySubentry', 'Services', None, 'aeService', 'Search all service accounts restricted by this password policy.'),
                 ('pwdPolicySubentry', 'Tokens', None, 'aeAuthcToken', 'Search all authentication tokens restricted by this password policy.'),
                 ('oathHOTPParams', 'HOTP Tokens', None, 'oathHOTPToken', 'Search all HOTP tokens affected by this HOTP parameters.'),
                 ('oathTOTPParams', 'TOTP Tokens', None, 'oathTOTPToken', 'Search all TOTP tokens affected by this TOTP parameters.'))


syntax_registry.reg_at((AEEntryDNAEPolicy.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 AE_POLICY_OID])

class AEUserSshPublicKey(SshPublicKey):
    oid = 'AEUserSshPublicKey-oid'
    oid: str
    desc = 'AE-DIR: aeUser:sshPublicKey'
    desc: str


syntax_registry.reg_at((AEUserSshPublicKey.oid),
  [
 '1.3.6.1.4.1.24552.500.1.1.1.13'],
  structural_oc_oids=[
 AE_USER_OID])

class AERFC822MailMember(DynamicValueSelectList, AEObjectMixIn):
    oid = 'AERFC822MailMember-oid'
    oid: str
    desc = 'AE-DIR: rfc822MailMember'
    desc: str
    ldap_url = 'ldap:///_?mail,displayName?sub?(&(|(objectClass=inetLocalMailRecipient)(objectClass=aeContact))(mail=*)(aeStatus=0))'
    html_tmpl = RFC822Address.html_tmpl
    showValueButton = False

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        if 'member' not in self._entry:
            return []
        if self.ae_status == 2:
            return []
        entrydn_filter = compose_filter('|', map_filter_parts('entryDN', decode_list((self._entry['member']), encoding=(self._app.ls.charset))))
        ldap_result = self._app.ls.l.search_s((self._search_root()),
          (ldap0.SCOPE_SUBTREE),
          entrydn_filter,
          attrlist=[
         'mail'])
        mail_addresses = []
        for res in ldap_result or []:
            mail_addresses.extend(res.entry_as['mail'])
        else:
            return sorted(mail_addresses)

    def formField(self) -> str:
        input_field = HiddenInput(self._at, ': '.join([self._at, self.desc]), self.maxLen, self.maxValues, None)
        input_field.charset = self._app.form.accept_charset
        input_field.set_default(self.formValue())
        return input_field


syntax_registry.reg_at((AERFC822MailMember.oid),
  [
 '1.3.6.1.4.1.42.2.27.2.1.15'],
  structural_oc_oids=[
 AE_MAILGROUP_OID])

class AEPwdPolicy(web2ldap.app.plugins.ppolicy.PwdPolicySubentry):
    oid = 'AEPwdPolicy-oid'
    oid: str
    desc = 'AE-DIR: pwdPolicySubentry'
    desc: str
    ldap_url = 'ldap:///_??sub?(&(objectClass=aePolicy)(objectClass=pwdPolicy)(aeStatus=0))'


syntax_registry.reg_at((AEPwdPolicy.oid),
  [
 '1.3.6.1.4.1.42.2.27.8.1.23'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_SERVICE_OID,
 AE_HOST_OID])

class AESudoHost(IA5String):
    oid = 'AESudoHost-oid'
    oid: str
    desc = 'AE-DIR: sudoHost'
    desc: str
    maxValues = 1
    reobj = re.compile('^ALL$')

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        return [b'ALL']

    def formField(self) -> str:
        input_field = HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None, default=(self.formValue()))
        input_field.charset = self._app.form.accept_charset
        return input_field


syntax_registry.reg_at((AESudoHost.oid),
  [
 '1.3.6.1.4.1.15953.9.1.2'],
  structural_oc_oids=[
 AE_SUDORULE_OID])

class AELoginShell(Shell):
    oid = 'AELoginShell-oid'
    oid: str
    desc = 'AE-DIR: Login shell for POSIX users'
    desc: str
    attr_value_dict = {'/bin/bash':'/bin/bash',  '/bin/true':'/bin/true', 
     '/bin/false':'/bin/false'}


syntax_registry.reg_at((AELoginShell.oid),
  [
 '1.3.6.1.1.1.1.4'],
  structural_oc_oids=[
 AE_USER_OID,
 AE_SERVICE_OID])

class AEOathHOTPToken(OathHOTPToken):
    oid = 'AEOathHOTPToken-oid'
    oid: str
    desc = 'DN of the associated oathHOTPToken entry in aeUser entry'
    desc: str
    ref_attrs = ((None, 'Users', None, None), )
    input_fallback = False

    def _filterstr(self):
        if 'aePerson' in self._entry:
            return '(&{0}(aeOwner={1}))'.format(OathHOTPToken._filterstr(self), ldap0.filter.escape_str(self._entry['aePerson'][0].decode(self._app.form.accept_charset)))
        return OathHOTPToken._filterstr(self)


syntax_registry.reg_at((AEOathHOTPToken.oid),
  [
 '1.3.6.1.4.1.5427.1.389.4226.4.9.1'],
  structural_oc_oids=[
 AE_USER_OID])

class AESSHPermissions(SelectList):
    oid = 'AESSHPermissions-oid'
    oid: str
    desc = 'AE-DIR: Status of object'
    desc: str
    attr_value_dict = {'pty':'PTY allocation',  'X11-forwarding':'X11 forwarding', 
     'agent-forwarding':'Key agent forwarding', 
     'port-forwarding':'Port forwarding', 
     'user-rc':'Execute ~/.ssh/rc'}


syntax_registry.reg_at(AESSHPermissions.oid, [
 AE_OID_PREFIX + '.4.47'])

class AERemoteHostAEHost(DynamicValueSelectList):
    oid = 'AERemoteHostAEHost-oid'
    oid: str
    desc = 'AE-DIR: aeRemoteHost in aeHost entry'
    desc: str
    ldap_url = 'ldap:///.?ipHostNumber,aeFqdn?one?(&(objectClass=aeNwDevice)(aeStatus=0))'
    input_fallback = True


syntax_registry.reg_at((AERemoteHostAEHost.oid),
  [
 AE_OID_PREFIX + '.4.8'],
  structural_oc_oids=[
 AE_HOST_OID])

class AEDescriptionAENwDevice(ComposedAttribute):
    oid = 'AEDescriptionAENwDevice-oid'
    oid: str
    desc = 'Attribute description in object class  aeNwDevice'
    desc: str
    compose_templates = ('{cn}: {aeFqdn} / {ipHostNumber}', '{cn}: {ipHostNumber}')


syntax_registry.reg_at((AEDescriptionAENwDevice.oid),
  [
 '2.5.4.13'],
  structural_oc_oids=[
 AE_NWDEVICE_OID])

class AEChildClasses(SelectList):
    oid = 'AEChildClasses-oid'
    desc = 'AE-DIR: Structural object classes allowed to be added in child entries'
    attr_value_dict = {'-/-':'', 
     'aeAuthcToken':'Authentication Token (aeAuthcToken)', 
     'aeContact':'Contact (aeContact)', 
     'aeDept':'Department (aeDept)', 
     'aeLocation':'Location (aeLocation)', 
     'aeMailGroup':'Mail Group (aeMailGroup)', 
     'aePerson':'Person (aePerson)', 
     'aePolicy':'Policy (aePolicy)', 
     'aeService':'Service/tool Account (aeService)', 
     'aeSrvGroup':'Service Group (aeSrvGroup)', 
     'aeSudoRule':'Sudoers Rule (sudoRole)', 
     'aeUser':'User account (aeUser)', 
     'aeGroup':'User group (aeGroup)', 
     'aeTag':'Tag (aeTag)'}


syntax_registry.reg_at(AEChildClasses.oid, [
 AE_OID_PREFIX + '.4.49'])
syntax_registry.reg_syntaxes(__name__)