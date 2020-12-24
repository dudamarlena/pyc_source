# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir/__init__.py
# Compiled at: 2019-12-23 16:28:09
# Size of source mod 2**32: 33631 bytes
"""
aedir - Generic classes and functions for dealing with AE-DIR
"""
import random, time, sys, os, string, logging, logging.handlers, logging.config
from typing import Dict, Iterator, List, Optional, Set, Tuple, Union
import ldap0, ldap0.sasl, ldap0.controls, ldap0.modlist
from ldap0.functions import escape_format
from ldap0.base import encode_list, decode_list, encode_entry_dict, decode_entry_dict
import ldap0.dn as escape_dn_str
from ldap0.dn import DNObj
import ldap0.filter as escape_filter_str
from ldap0.filter import map_filter_parts, compose_filter
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.controls.readentry import PreReadControl, PostReadControl
from ldap0.controls.deref import DereferenceControl
from ldap0.controls.sss import SSSRequestControl
from ldap0.ldapurl import LDAPUrl
from ldap0.pw import random_string
from ldap0.typehints import EntryStr, StrList
from ldap0.res import LDAPResult
from aedir.__about__ import __version__, __author__, __license__
__all__ = [
 'AEDirUrl',
 'AEDirObject',
 'AEDIR_SEARCH_BASE',
 'aedir_aehost_dn',
 'aedir_aeuser_dn',
 'extract_zone',
 'init_logger',
 'members2uids']
LDAP_TIMEOUT = 4.0
LDAP_MAXRETRYCOUNT = 2
LDAP_RETRYDELAY = 2.0
AEDIR_SEARCH_BASE = 'ou=ae-dir'
AESRVGROUP_GROUPREF_ATTRS = [
 'aeDisplayNameGroups',
 'aeSetupGroups',
 'aeLogStoreGroups',
 'aeLoginGroups',
 'aeVisibleGroups',
 'aeVisibleSudoers']
AE_SUDOERS_ATTRS = [
 'cn', 'objectClass', 'description',
 'sudoCommand',
 'sudoHost',
 'sudoNotAfter', 'sudoNotBefore',
 'sudoOption', 'sudoOrder',
 'sudoRunAs', 'sudoRunAsGroup', 'sudoRunAsUser', 'sudoUser']
AUTHC_ENTITY_FILTER_TMPL = '(&(|(&(|(objectClass=aeUser)(objectClass=aeService))(uid={0}))(&(objectClass=aeHost)(host={0})))(aeStatus=0))'
PWD_LENGTH = 40
PWD_ALPHABET = string.ascii_letters + string.digits
AE_LOGGING_CONFIG = os.environ.get('AE_LOGGING_CONFIG', '/opt/ae-dir/etc/ae-logging.conf')
AE_LOGGER_QUALNAME = os.environ.get('AE_LOGGER_QUALNAME', 'aedir')

def extract_zone(ae_object_dn: str, aeroot_dn: str=AEDIR_SEARCH_BASE) -> str:
    """
    return the extracted zone name from dn
    """
    asserted_suffix = ',' + aeroot_dn.lower()
    if not ae_object_dn.lower().endswith(asserted_suffix):
        raise ValueError('%r does not end with %r' % (ae_object_dn, asserted_suffix))
    dn_with_base = DNObj.from_str(ae_object_dn[0:-len(aeroot_dn) - 1])
    assert dn_with_base[(-1)][0][0] == 'cn', ValueError('Expected zone attribute to be cn, got %r' % (dn_with_base[(-1)][0],))
    return dn_with_base[(-1)][0][1]


def aedir_aeuser_dn(uid: str, zone: Optional[str]=None, aeroot_dn: str=AEDIR_SEARCH_BASE) -> str:
    """
    Returns a bind DN of a aeUser entry
    """
    if not zone:
        try:
            uid, zone = uid.split('@', 1)
        except ValueError:
            pass

    elif zone:
        first_dn_part = ldap0.functions.escape_format(escape_dn_str, 'uid={0},cn={1}', uid, zone)
    else:
        first_dn_part = ldap0.functions.escape_format(escape_dn_str, 'uid={0}', uid)
    return ','.join((first_dn_part, aeroot_dn))


def aedir_aehost_dn(fqdn: str, srvgrp: Optional[str]=None, zone: Optional[str]=None, aeroot_dn: str=AEDIR_SEARCH_BASE) -> str:
    """
    Returns a bind DN of a aeHost entry
    """
    if zone and srvgrp:
        first_dn_part = ldap0.functions.escape_str(escape_dn_str, 'host=%s,cn=%s,cn=%s', fqdn, srvgrp, zone)
    else:
        first_dn_part = ldap0.functions.escape_str(escape_dn_str, 'host=%s', fqdn)
    return ','.join((first_dn_part, aeroot_dn))


def aedir_aegroup_dn(aegroup_cn: str, aeroot_dn: str=AEDIR_SEARCH_BASE):
    """
    Returns a bind DN of a aeHost entry
    """
    zone_cn, _ = aegroup_cn.split('-', 1)
    return 'cn={0},cn={1},{2}'.format(aegroup_cn, zone_cn, aeroot_dn)


class AEDirUrl(LDAPUrl):
    __doc__ = '\n    LDAPUrl class for AE-DIR with some more LDAP URL extensions\n    '
    attr2extype = {'who':'bindname', 
     'cred':'X-BINDPW', 
     'trace_level':'trace', 
     'pwd_filename':'x-pwdfilename', 
     'sasl_mech':'x-saslmech', 
     'sasl_authzid':'x-saslauthzid'}

    def __init__(self, ldapUrl=None, urlscheme='ldap', hostport='', dn='', attrs=None, scope=None, filterstr=None, extensions=None, who=None, cred=None, trace_level=None, sasl_mech=None, pwd_filename=None):
        LDAPUrl.__init__(self,
          ldapUrl=ldapUrl,
          urlscheme=urlscheme,
          hostport=hostport,
          dn=dn,
          attrs=attrs,
          scope=scope,
          filterstr=filterstr,
          extensions=extensions,
          who=who,
          cred=cred)
        self.trace_level = trace_level
        self.sasl_mech = sasl_mech
        self.pwd_filename = pwd_filename


class AEDirObject(ReconnectLDAPObject):
    __doc__ = '\n    AE-DIR connection class\n    '
    aeroot_filter = '(objectClass=aeRoot)'
    aeroot_filter: str

    def __init__(self, ldap_url: str, trace_level: int=0, retry_max: int=LDAP_MAXRETRYCOUNT, retry_delay: Union[(int, float)]=LDAP_RETRYDELAY, timeout: Union[(int, float)]=LDAP_TIMEOUT, who: Optional[str]=None, cred: Optional[bytes]=None, cacert_filename: Optional[str]=None, client_cert_filename: Optional[str]=None, client_key_filename: Optional[str]=None, cache_ttl: Union[(int, float)]=0.0, sasl_authz_id: str=''):
        """
        Opens connection, sets some LDAP options and binds according
        to what's provided in `uri'.

        Extensions to parameters passed to ReconnectLDAPObject():
        `ldap_url'
          Can contain the full LDAP URL with authc information and base-DN
        `who'
          Bind-DN to be used (overrules ldap_url)
        `cred'
          Bind password to be used (overrules ldap_url)
        """
        if isinstance(ldap_url, str):
            self.ldap_url_obj = AEDirUrl(ldap_url)
        else:
            if isinstance(ldap_url, AEDirUrl):
                self.ldap_url_obj = ldap_url
            else:
                if ldap_url is None:
                    self.ldap_url_obj = AEDirUrl(ldapUrl=(ldap0.functions.get_option(ldap0.OPT_URI).decode('utf-8').split(' ')[0].strip() or None),
                      dn=((ldap0.functions.get_option(ldap0.OPT_DEFBASE) or b'').decode('utf-8').strip() or None))
                else:
                    raise ValueError('Invalid value for ldap_url: %r' % ldap_url)
        ReconnectLDAPObject.__init__(self,
          (self.ldap_url_obj.connect_uri()),
          trace_level=(trace_level or int(self.ldap_url_obj.trace_level or '0')),
          cache_ttl=cache_ttl,
          retry_max=retry_max,
          retry_delay=retry_delay)
        if self.ldap_url_obj.urlscheme != 'ldapi':
            self.set_tls_options(cacert_filename=cacert_filename,
              client_cert_filename=client_cert_filename,
              client_key_filename=client_key_filename)
        self.set_option(ldap0.OPT_REFERRALS, 0)
        self.set_option(ldap0.OPT_DEREF, ldap0.DEREF_NEVER)
        self.set_option(ldap0.OPT_NETWORK_TIMEOUT, timeout)
        self.set_option(ldap0.OPT_TIMEOUT, timeout)
        if self.ldap_url_obj.urlscheme == 'ldap':
            self.start_tls_s()
        if not self.ldap_url_obj.urlscheme == 'ldapi' or who is None or self.ldap_url_obj.sasl_mech and self.ldap_url_obj.sasl_mech.upper() == 'EXTERNAL':
            sasl_authz_id = sasl_authz_id or self.ldap_url_obj.sasl_authzid or ''
            self.sasl_non_interactive_bind_s('EXTERNAL', authz_id=sasl_authz_id)
        else:
            if who is None:
                who = self.ldap_url_obj.who
            if cred is None:
                cred = self.ldap_url_obj.cred
            if who is not None:
                self.simple_bind_s(who, cred or '')
            self._search_base = self._search_base_dnobj = None

    @property
    def search_base(self):
        """
        Returns the aeRoot entry as byte-string
        """
        if self._search_base is not None:
            return self._search_base
        self._search_base = self.read_rootdse_s(attrlist=['aeRoot']).entry_s['aeRoot'][0]
        self._search_base_dnobj = None
        return self._search_base

    @property
    def search_base_dnobj(self):
        if self._search_base_dnobj is not None:
            return self._search_base_dnobj
        self._search_base_dnobj = DNObj.from_str(self.search_base)
        return self._search_base_dnobj

    def find_byname(self, name: str, name_attr: str='cn', object_class: str='aeObject', attrlist: Optional[StrList]=None) -> LDAPResult:
        """
        Returns a unique aeObject entry
        """
        return self.find_unique_entry((self.search_base),
          filterstr=escape_format(escape_filter_str,
          '(&(objectClass={oc})({at}={name}))',
          oc=object_class,
          at=name_attr,
          name=name),
          attrlist=attrlist)

    def find_uid(self, uid: str, attrlist: Optional[StrList]=None) -> LDAPResult:
        """
        Returns a unique aeUser or aeService entry found by uid
        """
        return self.find_unique_entry((self.search_base),
          filterstr='(uid={uid})'.format(uid=(escape_filter_str(uid))),
          attrlist=attrlist)

    def find_aegroup(self, common_name: str, attrlist: Optional[StrList]=None) -> LDAPResult:
        """
        Returns a unique aeGroup entry
        """
        return self.find_byname(common_name,
          name_attr='cn',
          object_class='aeGroup',
          attrlist=attrlist)

    def find_aehost(self, host_name: str, attrlist: Optional[StrList]=None) -> LDAPResult:
        """
        Returns a unique aeHost entry found by attribute 'host'
        """
        return self.find_byname(host_name,
          name_attr='host',
          object_class='aeHost',
          attrlist=attrlist)

    def get_zoneadmins(self, ae_object_dn: str, attrlist: Optional[StrList]=None, suppl_filter: str='') -> List[LDAPResult]:
        """
        Returns LDAP search results of active aeUser entries of all
        zone-admins responsible for the given `ae_object_dn'.
        """
        ae_object_dnobj = DNObj.from_str(ae_object_dn)
        zone = self.read_s((str(ae_object_dnobj.slice(-len(self.search_base_dnobj) - 1, None))),
          filterstr='(objectClass=aeZone)',
          attrlist=[
         'aeZoneAdmins'])
        return zone.entry_s and 'aeZoneAdmins' in zone.entry_s or []
        return self.search_s((self.search_base),
          (ldap0.SCOPE_SUBTREE),
          filterstr=('(&(objectClass=aeUser)(aeStatus=0)(|{0}){1})'.format(compose_filter('|', map_filter_parts('memberOf', zone.entry_s.get('aeZoneAdmins', []))), suppl_filter)),
          attrlist=attrlist)

    def get_user_groups(self, uid: str, memberof_attr: str='memberOf') -> Set[str]:
        """
        Gets a set of DNs of aeGroup entries a AE-DIR user (aeUser or
        aeService) is member of
        """
        if memberof_attr:
            attrlist = [
             memberof_attr]
        else:
            attrlist = [
             '1.1']
        aeuser = self.find_uid(uid, attrlist=attrlist)
        if memberof_attr in aeuser.entry_s:
            memberof = aeuser.entry_s[memberof_attr]
        else:
            ldap_result = self.search_s((self.search_base),
              (ldap0.SCOPE_SUBTREE),
              ldap0.functions.escape_format(escape_filter_str,
              '(&(objectClass=aeGroup)(member={user_dn}))',
              user_dn=(aeuser.dn_s)),
              attrlist=[
             '1.1'])
            memberof = [res.dn_s for res in ldap_result]
        return set(memberof)

    def search_service_groups(self, service_dn: str, filterstr='', attrlist: Optional[StrList]=None, req_ctrls: Optional[List[ldap0.controls.RequestControl]]=None):
        """
        starts searching all service group entries the aeHost/aeService defined by
        service_dn is member of
        """
        aeservice_entry = self.read_s(service_dn,
          attrlist=[
         'aeSrvGroup']).entry_s
        aesrvgroup_dn_list = [
         str(DNObj.from_str(service_dn).parent())]
        aesrvgroup_dn_list.extend(aeservice_entry.get('aeSrvGroup', []))
        srvgroup_filter = '(&{0}{1})'.format(compose_filter('|', map_filter_parts('entryDN', aesrvgroup_dn_list)), filterstr)
        msg_id = self.search((self.search_base),
          (ldap0.SCOPE_SUBTREE),
          srvgroup_filter,
          attrlist=(attrlist or ['1.1']),
          req_ctrls=req_ctrls)
        return msg_id

    def get_service_groups(self, service_dn: str, filterstr: str='', attrlist: Optional[StrList]=None) -> Iterator[LDAPResult]:
        """
        returns all service group entries the aeHost/aeService defined by
        service_dn is member of
        """
        msg_id = self.search_service_groups(service_dn,
          filterstr=filterstr,
          attrlist=attrlist)
        return self.results(msg_id)

    def get_user_srvgroup_relations--- This code section failed: ---

 L. 540         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_user_groups
                4  LOAD_FAST                'uid'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'aeuser_memberof'

 L. 541        10  LOAD_FAST                'ref_attrs'
               12  JUMP_IF_TRUE_OR_POP    16  'to 16'
               14  LOAD_GLOBAL              AESRVGROUP_GROUPREF_ATTRS
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'ref_attrs'

 L. 542        18  LOAD_FAST                'self'
               20  LOAD_ATTR                read_s

 L. 543        22  LOAD_FAST                'aesrvgroup_dn'

 L. 544        24  LOAD_STR                 '(objectClass=aeSrvGroup)'

 L. 545        26  LOAD_FAST                'ref_attrs'

 L. 542        28  LOAD_CONST               ('filterstr', 'attrlist')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  STORE_FAST               'aesrvgroup'

 L. 547        34  LOAD_FAST                'aesrvgroup'
               36  LOAD_ATTR                entry_s
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L. 548        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'Empty search result for %r'
               44  LOAD_FAST                'aesrvgroup_dn'
               46  BINARY_MODULO    
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            38  '38'

 L. 549        52  BUILD_LIST_0          0 
               54  STORE_FAST               'srvgroup_relations'

 L. 550        56  LOAD_FAST                'ref_attrs'
               58  GET_ITER         
             60_0  COME_FROM            72  '72'
               60  FOR_ITER            118  'to 118'
               62  STORE_FAST               'attr_type'

 L. 551        64  LOAD_FAST                'attr_type'
               66  LOAD_FAST                'aesrvgroup'
               68  LOAD_ATTR                entry_s
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE    60  'to 60'

 L. 552        74  LOAD_FAST                'aesrvgroup'
               76  LOAD_ATTR                entry_s
               78  LOAD_FAST                'attr_type'
               80  BINARY_SUBSCR    
               82  GET_ITER         
             84_0  COME_FROM            98  '98'
               84  FOR_ITER            116  'to 116'
               86  STORE_FAST               'attr_value'

 L. 553        88  LOAD_FAST                'attr_value'
               90  LOAD_METHOD              lower
               92  CALL_METHOD_0         0  ''
               94  LOAD_FAST                'aeuser_memberof'
               96  COMPARE_OP               in
               98  POP_JUMP_IF_FALSE    84  'to 84'

 L. 554       100  LOAD_FAST                'srvgroup_relations'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'attr_type'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 555       110  POP_TOP          
              112  CONTINUE             60  'to 60'
              114  JUMP_BACK            84  'to 84'
              116  JUMP_BACK            60  'to 60'

 L. 556       118  LOAD_FAST                'srvgroup_relations'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 112

    def get_user_service_relations(self, uid, service_dn, ref_attrs=None):
        """
        get relation(s) between aeUser specified by uid with
        aeHost/aeService specified by service_dn

        returns set of relationship attribute names
        """
        aesrvgroups = self.get_service_groups(service_dn, attrlist=None)
        aesrvgroup_dn_set = set()
        for res in aesrvgroups:
            aesrvgroup_dn_set.update([aesrvgroup.dn_s for aesrvgroup in res.rdata])
        else:
            result = set()
            for aesrvgroup_dn in aesrvgroup_dn_set:
                result.update(self.get_user_srvgroup_relations(uid,
                  aesrvgroup_dn=aesrvgroup_dn,
                  ref_attrs=ref_attrs))
            else:
                return result

    def search_users(self, service_dn: str, ae_status: int=0, filterstr: str='(|(objectClass=aeUser)(objectClass=aeService))', attrlist: Optional[StrList]=None, ref_attr: str='aeLoginGroups', req_ctrls: Optional[List[ldap0.controls.RequestControl]]=None):
        """
        starts async search for all aeUser/aeService entries having the
        appropriate relationship on given aeHost/aeService
        """
        aesrvgroups = self.get_service_groups(service_dn,
          filterstr=('({0}=*)'.format(ref_attr)),
          attrlist=[
         ref_attr])
        ref_attrs_groups = set()
        for res in aesrvgroups:
            for srvgroup in res.rdata:
                ref_attrs_groups.update([av.lower() for av in srvgroup.entry_s.get(ref_attr, [])])
            else:
                if not ref_attrs_groups:
                    return
                user_group_filter = '(&(aeStatus={0}){1}(|{2}))'.format(str(int(ae_status)), filterstr, ''.join(['(memberOf={0})'.format(escape_filter_str(dn)) for dn in ref_attrs_groups]))
                msg_id = self.search((self.search_base),
                  (ldap0.SCOPE_SUBTREE),
                  user_group_filter,
                  attrlist=attrlist,
                  req_ctrls=req_ctrls)
                return msg_id

    def get_users(self, service_dn, ae_status=0, filterstr='(|(objectClass=aeUser)(objectClass=aeService))', attrlist: Optional[StrList]=None, ref_attr='aeLoginGroups', req_ctrls: Optional[List[ldap0.controls.RequestControl]]=None):
        """
        returns all aeUser/aeService entries having the appropriate
        relationship on given aeHost/aeService  as list of 2-tuples
        """
        msg_id = self.search_users(service_dn,
          ae_status=ae_status,
          filterstr=filterstr,
          attrlist=attrlist,
          ref_attr=ref_attr,
          req_ctrls=req_ctrls)
        if msg_id is None:
            return []
        return self.results(msg_id)

    def get_next_id(self, id_pool_dn: Optional[str]=None, id_pool_attr: str='gidNumber') -> int:
        """
        consumes next ID by sending MOD_INCREMENT modify operation with
        pre-read entry control
        """
        id_pool_dn = id_pool_dn or self.search_base
        prc = PreReadControl(criticality=True, attrList=[id_pool_attr])
        res = self.modify_s(id_pool_dn,
          [
         (
          ldap0.MOD_INCREMENT, id_pool_attr.encode('ascii'), [b'1'])],
          req_ctrls=[
         prc])
        return int(res.ctrls[0].res.entry_s[id_pool_attr][0])

    def find_highest_id(self, id_pool_dn: Optional[str]=None, id_pool_attr: str='gidNumber') -> int:
        """
        search the highest value of `id_attr' by using server-side (reverse) sorting
        """
        id_pool_dn = id_pool_dn or self.search_base
        sss_control = SSSRequestControl(criticality=True,
          ordering_rules=[
         '-' + id_pool_attr])
        msg_id = self.search(id_pool_dn,
          (ldap0.SCOPE_SUBTREE),
          ('(&(!(objectClass=aePosixIdRanges))({0}=*))'.format(id_pool_attr)),
          attrlist=[
         id_pool_attr],
          sizelimit=1,
          req_ctrls=[
         sss_control])
        ldap_result = []
        try:
            for res in self.results(msg_id):
                ldap_result.extend(res.rdata)

        except ldap0.SIZELIMIT_EXCEEDED:
            pass
        else:
            highest_id_number = int(ldap_result[0].entry_s[id_pool_attr][0])
            return highest_id_number

    def add_aeuser--- This code section failed: ---

 L. 722         0  LOAD_FAST                'aeperson_attrs'
                2  JUMP_IF_TRUE_OR_POP    12  'to 12'
                4  LOAD_STR                 'mail'
                6  LOAD_STR                 'sn'
                8  LOAD_STR                 'givenName'
               10  BUILD_LIST_3          3 
             12_0  COME_FROM             2  '2'
               12  STORE_FAST               'aeperson_attrs'

 L. 724        14  SETUP_FINALLY        36  'to 36'

 L. 725        16  LOAD_DEREF               'self'
               18  LOAD_ATTR                read_s

 L. 726        20  LOAD_FAST                'ae_person_dn'

 L. 727        22  LOAD_STR                 '(aeStatus=0)'

 L. 728        24  LOAD_FAST                'aeperson_attrs'

 L. 725        26  LOAD_CONST               ('filterstr', 'attrlist')
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  STORE_FAST               'ae_person'
               32  POP_BLOCK        
               34  JUMP_FORWARD         74  'to 74'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 730        36  DUP_TOP          
               38  LOAD_GLOBAL              ldap0
               40  LOAD_ATTR                NO_SUCH_OBJECT
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    72  'to 72'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 731        52  LOAD_GLOBAL              ldap0
               54  LOAD_METHOD              NO_SUCH_OBJECT
               56  LOAD_STR                 'Could not read aePerson entry %r'
               58  LOAD_FAST                'ae_person_dn'
               60  BUILD_TUPLE_1         1 
               62  BINARY_MODULO    
               64  CALL_METHOD_1         1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            44  '44'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            34  '34'

 L. 733        74  LOAD_GLOBAL              str
               76  LOAD_DEREF               'self'
               78  LOAD_METHOD              get_next_id
               80  CALL_METHOD_0         0  ''
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'posix_id'

 L. 735        86  LOAD_GLOBAL              aedir_aeuser_dn
               88  LOAD_FAST                'uid'
               90  LOAD_FAST                'zone'
               92  LOAD_DEREF               'self'
               94  LOAD_ATTR                search_base
               96  LOAD_CONST               ('zone', 'aeroot_dn')
               98  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              100  STORE_FAST               'add_dn'

 L. 739       102  LOAD_STR                 'account'

 L. 740       104  LOAD_STR                 'person'

 L. 741       106  LOAD_STR                 'organizationalPerson'

 L. 742       108  LOAD_STR                 'inetOrgPerson'

 L. 743       110  LOAD_STR                 'aeObject'

 L. 744       112  LOAD_STR                 'aeUser'

 L. 745       114  LOAD_STR                 'posixAccount'

 L. 746       116  LOAD_STR                 'ldapPublicKey'

 L. 738       118  BUILD_LIST_8          8 

 L. 748       120  LOAD_GLOBAL              str
              122  LOAD_FAST                'ae_status'
              124  CALL_FUNCTION_1       1  ''
              126  BUILD_LIST_1          1 

 L. 749       128  LOAD_FAST                'uid'
              130  BUILD_LIST_1          1 

 L. 750       132  LOAD_FAST                'ae_person'
              134  LOAD_ATTR                dn_s
              136  BUILD_LIST_1          1 

 L. 751       138  LOAD_FAST                'posix_id'
              140  BUILD_LIST_1          1 

 L. 752       142  LOAD_FAST                'posix_id'
              144  BUILD_LIST_1          1 

 L. 754       146  LOAD_STR                 '{givenName} {sn}'
              148  LOAD_ATTR                format

 L. 755       150  LOAD_FAST                'ae_person'
              152  LOAD_ATTR                entry_s
              154  LOAD_STR                 'givenName'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    

 L. 756       162  LOAD_FAST                'ae_person'
              164  LOAD_ATTR                entry_s
              166  LOAD_STR                 'sn'
              168  BINARY_SUBSCR    
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    

 L. 754       174  LOAD_CONST               ('givenName', 'sn')
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 753       178  BUILD_LIST_1          1 

 L. 759       180  LOAD_FAST                'home_directory'
              182  LOAD_ATTR                format
              184  LOAD_FAST                'uid'
              186  LOAD_CONST               ('uid',)
              188  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              190  BUILD_LIST_1          1 

 L. 761       192  LOAD_STR                 '{givenName} {sn} ({uid}/{uidNumber})'
              194  LOAD_ATTR                format

 L. 762       196  LOAD_FAST                'ae_person'
              198  LOAD_ATTR                entry_s
              200  LOAD_STR                 'givenName'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               0
              206  BINARY_SUBSCR    

 L. 763       208  LOAD_FAST                'ae_person'
              210  LOAD_ATTR                entry_s
              212  LOAD_STR                 'sn'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    

 L. 764       220  LOAD_FAST                'uid'

 L. 765       222  LOAD_FAST                'posix_id'

 L. 761       224  LOAD_CONST               ('givenName', 'sn', 'uid', 'uidNumber')
              226  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 760       228  BUILD_LIST_1          1 

 L. 768       230  LOAD_FAST                'pwd_policy_subentry'
              232  BUILD_LIST_1          1 

 L. 737       234  LOAD_CONST               ('objectClass', 'aeStatus', 'uid', 'aePerson', 'uidNumber', 'gidNumber', 'cn', 'homeDirectory', 'displayName', 'pwdPolicySubentry')
              236  BUILD_CONST_KEY_MAP_10    10 
              238  STORE_FAST               'add_entry'

 L. 770       240  LOAD_FAST                'ae_person'
              242  LOAD_ATTR                entry_s
              244  LOAD_METHOD              items
              246  CALL_METHOD_0         0  ''
              248  GET_ITER         
              250  FOR_ITER            268  'to 268'
              252  UNPACK_SEQUENCE_2     2 
              254  STORE_FAST               'attr_type'
              256  STORE_FAST               'attr_values'

 L. 771       258  LOAD_FAST                'attr_values'
              260  LOAD_FAST                'add_entry'
              262  LOAD_FAST                'attr_type'
              264  STORE_SUBSCR     
              266  JUMP_BACK           250  'to 250'

 L. 773       268  LOAD_STR                 'aeTicketId'
              270  LOAD_FAST                'ae_ticket_id'
              272  BUILD_TUPLE_2         2 

 L. 774       274  LOAD_STR                 'description'
              276  LOAD_FAST                'description'
              278  BUILD_TUPLE_2         2 

 L. 775       280  LOAD_STR                 'loginShell'
              282  LOAD_FAST                'login_shell'
              284  BUILD_TUPLE_2         2 

 L. 772       286  BUILD_TUPLE_3         3 
              288  GET_ITER         
            290_0  COME_FROM           300  '300'
              290  FOR_ITER            318  'to 318'
              292  UNPACK_SEQUENCE_2     2 
              294  STORE_FAST               'attr_type'
              296  STORE_FAST               'attr_value'

 L. 777       298  LOAD_FAST                'attr_value'
          300_302  POP_JUMP_IF_FALSE   290  'to 290'

 L. 778       304  LOAD_FAST                'attr_value'
              306  BUILD_LIST_1          1 
              308  LOAD_FAST                'add_entry'
              310  LOAD_FAST                'attr_type'
              312  STORE_SUBSCR     
          314_316  JUMP_BACK           290  'to 290'

 L. 779       318  LOAD_DEREF               'self'
              320  LOAD_ATTR                add_s

 L. 780       322  LOAD_FAST                'add_dn'

 L. 781       324  LOAD_CLOSURE             'self'
              326  BUILD_TUPLE_1         1 
              328  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              330  LOAD_STR                 'AEDirObject.add_aeuser.<locals>.<dictcomp>'
              332  MAKE_FUNCTION_8          'closure'

 L. 783       334  LOAD_FAST                'add_entry'
              336  LOAD_METHOD              items
              338  CALL_METHOD_0         0  ''

 L. 781       340  GET_ITER         
              342  CALL_FUNCTION_1       1  ''

 L. 785       344  LOAD_GLOBAL              PostReadControl

 L. 786       346  LOAD_CONST               True

 L. 787       348  LOAD_STR                 '*'
              350  LOAD_STR                 '+'
              352  BUILD_LIST_2          2 

 L. 785       354  LOAD_CONST               ('criticality', 'attrList')
              356  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              358  BUILD_LIST_1          1 

 L. 779       360  LOAD_CONST               ('req_ctrls',)
              362  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              364  STORE_FAST               'add_res'

 L. 790       366  LOAD_FAST                'add_res'
              368  LOAD_ATTR                ctrls
              370  LOAD_CONST               0
              372  BINARY_SUBSCR    
              374  LOAD_ATTR                res
              376  LOAD_ATTR                entry_s
              378  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 328

    def get_role_groups(self, service_dn: str, role_attrs) -> Dict[(str, Set[str])]:
        srv_grps = self.get_service_groups(service_dn, attrlist=role_attrs)
        role_groups = {}
        for role_attr in role_attrs:
            role_groups[role_attr] = set()
            for res in srv_grps:
                for srv_grp in res.rdata:
                    role_groups[role_attr].update(srv_grp.entry_s.get(role_attr, []))

            else:
                return role_groups

    def get_role_groups_filter(self, service_dn: str, assertion_type: str, role_attr: str='aeVisibleGroups') -> str:
        groups = self.get_role_groups(service_dn, [role_attr])[role_attr]
        if groups:
            entry_dn_filter = ldap0.filter.compose_filter('|', ldap0.filter.map_filter_parts(assertion_type, groups))
        else:
            entry_dn_filter = ''
        return entry_dn_filter

    def get_sudoers(self, service_dn: str, attrlist: Optional[StrList]=None, req_ctrls: Optional[List[ldap0.controls.RequestControl]]=None):
        attrlist = attrlist or AE_SUDOERS_ATTRS
        req_ctrls = req_ctrls or []
        req_ctrls.append(DereferenceControl(True, {'aeVisibleSudoers': attrlist}))
        msg_id = self.search_service_groups(service_dn, attrlist=['1.1'], req_ctrls=req_ctrls)
        sudoers = []
        for ldap_res in self.results(msg_id):
            for res in ldap_res.rdata:
                if res.ctrls and res.ctrls[0].controlType == DereferenceControl.controlType:
                    sudoers.extend(res.ctrls[0].derefRes['aeVisibleSudoers'])
            else:
                return sudoers

    def add_aehost--- This code section failed: ---

 L. 850         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                find_byname

 L. 851         4  LOAD_FAST                'srvgroup_name'

 L. 852         6  LOAD_STR                 'cn'

 L. 853         8  LOAD_STR                 'aeSrvGroup'

 L. 854        10  LOAD_STR                 '1.1'
               12  BUILD_LIST_1          1 

 L. 850        14  LOAD_CONST               ('name_attr', 'object_class', 'attrlist')
               16  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               18  STORE_FAST               'srvgroup'

 L. 856        20  LOAD_STR                 ','
               22  LOAD_METHOD              join

 L. 857        24  LOAD_STR                 'host={0}'
               26  LOAD_METHOD              format
               28  LOAD_GLOBAL              escape_dn_str
               30  LOAD_FAST                'host_name'
               32  CALL_FUNCTION_1       1  ''
               34  CALL_METHOD_1         1  ''

 L. 858        36  LOAD_FAST                'srvgroup'
               38  LOAD_ATTR                dn_s

 L. 856        40  BUILD_TUPLE_2         2 
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'host_dn'

 L. 861        46  LOAD_STR                 'device'
               48  LOAD_STR                 'aeDevice'
               50  LOAD_STR                 'aeObject'
               52  LOAD_STR                 'aeHost'
               54  LOAD_STR                 'ldapPublicKey'
               56  BUILD_LIST_5          5 

 L. 862        58  LOAD_FAST                'host_name'
               60  BUILD_LIST_1          1 

 L. 863        62  LOAD_FAST                'host_name'
               64  BUILD_LIST_1          1 

 L. 864        66  LOAD_STR                 '0'
               68  BUILD_LIST_1          1 

 L. 860        70  LOAD_CONST               ('objectClass', 'cn', 'host', 'aeStatus')
               72  BUILD_CONST_KEY_MAP_4     4 
               74  STORE_FAST               'host_entry'

 L. 866        76  LOAD_FAST                'entry'
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L. 867        80  LOAD_FAST                'host_entry'
               82  LOAD_METHOD              update
               84  LOAD_FAST                'entry'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            78  '78'

 L. 868        90  LOAD_DEREF               'self'
               92  LOAD_METHOD              add_s

 L. 869        94  LOAD_FAST                'host_dn'

 L. 870        96  LOAD_CLOSURE             'self'
               98  BUILD_TUPLE_1         1 
              100  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              102  LOAD_STR                 'AEDirObject.add_aehost.<locals>.<dictcomp>'
              104  MAKE_FUNCTION_8          'closure'

 L. 872       106  LOAD_FAST                'host_entry'
              108  LOAD_METHOD              items
              110  CALL_METHOD_0         0  ''

 L. 870       112  GET_ITER         
              114  CALL_FUNCTION_1       1  ''

 L. 868       116  CALL_METHOD_2         2  ''
              118  POP_TOP          

 L. 875       120  LOAD_FAST                'password'
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L. 876       124  LOAD_DEREF               'self'
              126  LOAD_METHOD              passwd_s
              128  LOAD_FAST                'host_dn'
              130  LOAD_CONST               None
              132  LOAD_FAST                'password'
              134  CALL_METHOD_3         3  ''
              136  POP_TOP          
            138_0  COME_FROM           122  '122'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 100

    def set_password(self, name: str, password: Optional[bytes], filterstr_tmpl: str=AUTHC_ENTITY_FILTER_TMPL) -> Tuple[(str, Optional[str])]:
        """
        Set a password of an entity specified by name.
        The entity can be a aeUser, aeService or aeHost and its full DN
        is searched by unique find based on filterstr_tmpl.

        A 2-tuple with DN of the entry and password is returned as result.

        The caller has to handle exception ldap0.err.NoUniqueEntry.
        """
        res = self.find_unique_entry((self.search_base),
          scope=(ldap0.SCOPE_SUBTREE),
          filterstr=(filterstr_tmpl.format(escape_filter_str(name))),
          attrlist=[
         'pwdPolicySubentry'])
        generated_password = None
        if password is None:
            pwd_policy = self.read_s((res.entry_s['pwdPolicySubentry'][0]),
              filterstr='(objectClass=pwdPolicy)',
              attrlist=[
             'pwdMinLength'])
            pwd_min_length = int(pwd_policy.entry_s.get('pwdMinLength', ['0'])[0])
            password = generated_password = random_string(length=(max(PWD_LENGTH, pwd_min_length)))
        self.passwd_s(res.dn_s, None, password)
        return (res.dn_s, generated_password)

    def add_aezone--- This code section failed: ---

 L. 913         0  BUILD_LIST_0          0 
                2  STORE_FAST               'new_entries'

 L. 915         4  LOAD_STR                 'cn={zone_cn},{aedir_suffix}'
                6  LOAD_ATTR                format

 L. 916         8  LOAD_FAST                'zone_name'

 L. 917        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                search_base

 L. 915        14  LOAD_CONST               ('zone_cn', 'aedir_suffix')
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  STORE_FAST               'zone_dn'

 L. 920        20  LOAD_STR                 'namedObject'
               22  LOAD_STR                 'aeObject'
               24  LOAD_STR                 'aeZone'
               26  BUILD_LIST_3          3 

 L. 921        28  LOAD_STR                 '0'
               30  BUILD_LIST_1          1 

 L. 922        32  LOAD_FAST                'zone_name'
               34  BUILD_LIST_1          1 

 L. 923        36  LOAD_FAST                'ticket_id'
               38  BUILD_LIST_1          1 

 L. 924        40  LOAD_FAST                'zone_desc'
               42  BUILD_LIST_1          1 

 L. 919        44  LOAD_CONST               ('objectClass', 'aeStatus', 'cn', 'aeTicketId', 'description')
               46  BUILD_CONST_KEY_MAP_5     5 
               48  STORE_FAST               'zone_entry'

 L. 926        50  LOAD_FAST                'new_entries'
               52  LOAD_METHOD              append
               54  LOAD_FAST                'zone_dn'
               56  LOAD_FAST                'zone_entry'
               58  BUILD_TUPLE_2         2 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 928        64  LOAD_FAST                'zone_name'
               66  LOAD_STR                 '-init'
               68  BINARY_ADD       
               70  STORE_FAST               'tag_cn'

 L. 929        72  LOAD_STR                 'cn={zone_cn}-init,{zone_dn}'
               74  LOAD_ATTR                format

 L. 930        76  LOAD_FAST                'zone_name'

 L. 931        78  LOAD_FAST                'zone_dn'

 L. 929        80  LOAD_CONST               ('zone_cn', 'zone_dn')
               82  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               84  STORE_FAST               'tag_dn'

 L. 934        86  LOAD_STR                 'namedObject'
               88  LOAD_STR                 'aeTag'
               90  BUILD_LIST_2          2 

 L. 935        92  LOAD_STR                 '0'
               94  BUILD_LIST_1          1 

 L. 936        96  LOAD_FAST                'tag_cn'
               98  BUILD_LIST_1          1 

 L. 937       100  LOAD_STR                 'Initialization of "{zone_desc}"'
              102  LOAD_ATTR                format
              104  BUILD_TUPLE_0         0 
              106  LOAD_GLOBAL              vars
              108  CALL_FUNCTION_0       0  ''
              110  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              112  BUILD_LIST_1          1 

 L. 933       114  LOAD_CONST               ('objectClass', 'aeStatus', 'cn', 'description')
              116  BUILD_CONST_KEY_MAP_4     4 
              118  STORE_FAST               'tag_entry'

 L. 939       120  LOAD_FAST                'new_entries'
              122  LOAD_METHOD              append
              124  LOAD_FAST                'tag_dn'
              126  LOAD_FAST                'tag_entry'
              128  BUILD_TUPLE_2         2 
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L. 941       134  LOAD_STR                 'cn={zone_cn}-zone-admins,{zone_dn}'
              136  LOAD_ATTR                format

 L. 942       138  LOAD_FAST                'zone_name'

 L. 943       140  LOAD_FAST                'zone_dn'

 L. 941       142  LOAD_CONST               ('zone_cn', 'zone_dn')
              144  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              146  STORE_FAST               'zone_admins_dn'

 L. 946       148  LOAD_STR                 'aeObject'
              150  LOAD_STR                 'groupOfEntries'
              152  LOAD_STR                 'posixGroup'
              154  LOAD_STR                 'aeGroup'
              156  BUILD_LIST_4          4 

 L. 947       158  LOAD_STR                 '0'
              160  BUILD_LIST_1          1 

 L. 948       162  LOAD_FAST                'tag_cn'
              164  BUILD_LIST_1          1 

 L. 949       166  LOAD_FAST                'zone_name'
              168  LOAD_STR                 '-zone-admins'
              170  BINARY_ADD       
              172  BUILD_LIST_1          1 

 L. 950       174  LOAD_FAST                'ticket_id'
              176  BUILD_LIST_1          1 

 L. 952       178  LOAD_STR                 "Group members are zone admins who can manage zone '{zone_cn}'"
              180  LOAD_ATTR                format
              182  LOAD_FAST                'zone_name'
              184  LOAD_CONST               ('zone_cn',)
              186  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 951       188  BUILD_LIST_1          1 

 L. 955       190  LOAD_GLOBAL              str
              192  LOAD_DEREF               'self'
              194  LOAD_ATTR                get_next_id

 L. 956       196  LOAD_DEREF               'self'
              198  LOAD_ATTR                search_base

 L. 957       200  LOAD_STR                 'gidNumber'

 L. 955       202  LOAD_CONST               ('id_pool_dn', 'id_pool_attr')
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  CALL_FUNCTION_1       1  ''

 L. 954       208  BUILD_LIST_1          1 

 L. 945       210  LOAD_CONST               ('objectClass', 'aeStatus', 'aeTag', 'cn', 'aeTicketId', 'description', 'gidNumber')
              212  BUILD_CONST_KEY_MAP_7     7 
              214  STORE_FAST               'zone_admins_entry'

 L. 961       216  LOAD_FAST                'new_entries'
              218  LOAD_METHOD              append
              220  LOAD_FAST                'zone_admins_dn'
              222  LOAD_FAST                'zone_admins_entry'
              224  BUILD_TUPLE_2         2 
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 963       230  LOAD_STR                 'cn={zone_cn}-zone-auditors,{zone_dn}'
              232  LOAD_ATTR                format

 L. 964       234  LOAD_FAST                'zone_name'

 L. 965       236  LOAD_FAST                'zone_dn'

 L. 963       238  LOAD_CONST               ('zone_cn', 'zone_dn')
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  STORE_FAST               'zone_auditors_dn'

 L. 968       244  LOAD_STR                 'aeObject'
              246  LOAD_STR                 'groupOfEntries'
              248  LOAD_STR                 'posixGroup'
              250  LOAD_STR                 'aeGroup'
              252  BUILD_LIST_4          4 

 L. 969       254  LOAD_STR                 '0'
              256  BUILD_LIST_1          1 

 L. 970       258  LOAD_FAST                'tag_cn'
              260  BUILD_LIST_1          1 

 L. 971       262  LOAD_FAST                'zone_name'
              264  LOAD_STR                 '-zone-auditors'
              266  BINARY_ADD       
              268  BUILD_LIST_1          1 

 L. 972       270  LOAD_FAST                'ticket_id'
              272  BUILD_LIST_1          1 

 L. 973       274  LOAD_STR                 "Group members are zone auditors who can read zone '{zone_cn}'"
              276  LOAD_ATTR                format
              278  LOAD_FAST                'zone_name'
              280  LOAD_CONST               ('zone_cn',)
              282  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              284  BUILD_LIST_1          1 

 L. 975       286  LOAD_GLOBAL              str
              288  LOAD_DEREF               'self'
              290  LOAD_ATTR                get_next_id

 L. 976       292  LOAD_DEREF               'self'
              294  LOAD_ATTR                search_base

 L. 977       296  LOAD_STR                 'gidNumber'

 L. 975       298  LOAD_CONST               ('id_pool_dn', 'id_pool_attr')
              300  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              302  CALL_FUNCTION_1       1  ''

 L. 974       304  BUILD_LIST_1          1 

 L. 967       306  LOAD_CONST               ('objectClass', 'aeStatus', 'aeTag', 'cn', 'aeTicketId', 'description', 'gidNumber')
              308  BUILD_CONST_KEY_MAP_7     7 
              310  STORE_FAST               'zone_auditors_entry'

 L. 981       312  LOAD_FAST                'new_entries'
              314  LOAD_METHOD              append
              316  LOAD_FAST                'zone_auditors_dn'
              318  LOAD_FAST                'zone_auditors_entry'
              320  BUILD_TUPLE_2         2 
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L. 983       326  LOAD_FAST                'new_entries'
              328  GET_ITER         
              330  FOR_ITER            372  'to 372'
              332  UNPACK_SEQUENCE_2     2 
              334  STORE_FAST               'new_dn'
              336  STORE_FAST               'new_entry'

 L. 984       338  LOAD_DEREF               'self'
              340  LOAD_METHOD              add_s

 L. 985       342  LOAD_FAST                'new_dn'

 L. 986       344  LOAD_CLOSURE             'self'
              346  BUILD_TUPLE_1         1 
              348  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              350  LOAD_STR                 'AEDirObject.add_aezone.<locals>.<dictcomp>'
              352  MAKE_FUNCTION_8          'closure'

 L. 988       354  LOAD_FAST                'new_entry'
              356  LOAD_METHOD              items
              358  CALL_METHOD_0         0  ''

 L. 986       360  GET_ITER         
              362  CALL_FUNCTION_1       1  ''

 L. 984       364  CALL_METHOD_2         2  ''
              366  POP_TOP          
          368_370  JUMP_BACK           330  'to 330'

 L. 992       372  LOAD_DEREF               'self'
              374  LOAD_METHOD              modify_s

 L. 993       376  LOAD_FAST                'zone_dn'

 L. 995       378  LOAD_GLOBAL              ldap0
              380  LOAD_ATTR                MOD_ADD
              382  LOAD_CONST               b'aeTag'
              384  LOAD_FAST                'tag_cn'
              386  LOAD_METHOD              encode
              388  LOAD_STR                 'utf-8'
              390  CALL_METHOD_1         1  ''
              392  BUILD_LIST_1          1 
              394  BUILD_TUPLE_3         3 

 L. 996       396  LOAD_GLOBAL              ldap0
              398  LOAD_ATTR                MOD_ADD
              400  LOAD_CONST               b'aeZoneAdmins'
              402  LOAD_FAST                'zone_admins_dn'
              404  LOAD_METHOD              encode
              406  LOAD_STR                 'utf-8'
              408  CALL_METHOD_1         1  ''
              410  BUILD_LIST_1          1 
              412  BUILD_TUPLE_3         3 

 L. 997       414  LOAD_GLOBAL              ldap0
              416  LOAD_ATTR                MOD_ADD
              418  LOAD_CONST               b'aeZoneAuditors'
              420  LOAD_FAST                'zone_auditors_dn'
              422  LOAD_METHOD              encode
              424  LOAD_STR                 'utf-8'
              426  CALL_METHOD_1         1  ''
              428  BUILD_LIST_1          1 
              430  BUILD_TUPLE_3         3 

 L. 994       432  BUILD_LIST_3          3 

 L. 992       434  CALL_METHOD_2         2  ''
              436  POP_TOP          

 L.1000       438  LOAD_FAST                'zone_dn'
              440  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 348


def members2uids(members):
    """
    transforms list of group member DNs into list of uid values
    """
    return [dn[4:].split(',')[0] for dn in members]


def init_logger(log_name=None, logging_config=AE_LOGGING_CONFIG, logger_qualname=AE_LOGGER_QUALNAME):
    """
    get logger instance
    """
    logging.config.fileConfig(logging_config)
    logger = logging.getLogger(logger_qualname)
    if log_name:
        logger.name = log_name
    return logger