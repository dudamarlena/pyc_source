# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/groups.py
# Compiled at: 2020-02-05 10:32:00
# Size of source mod 2**32: 16387 bytes
__doc__ = "\naedir_pproc.groups - Performs two tasks:\n1. Removes inactive members from static group entries referenced by 'memberOf'.\n2. Updates all static aeGroup entries which contain attribute 'memberURL'\n"
import ldap0, ldap0.base, ldap0.filter
from ldap0.filter import compose_filter, map_filter_parts
from ldap0.controls.deref import DereferenceControl
import ldap0.ldapurl, aedir, aedir.process
from .__about__ import __version__, __author__, __license__
MEMBER_ATTR = 'member'
MEMBEROF_ATTR = 'memberOf'
MEMBERURL_ATTR = 'memberURL'
MEMBER_ATTRS_MAP = {'aeGroup':('memberUid', 'uid'), 
 'aeMailGroup':('rfc822MailMember', 'mail')}
MEMBER_ATTRS = [attr[0] for attr in MEMBER_ATTRS_MAP.values()]
USER_ATTRS = [attr[1] for attr in MEMBER_ATTRS_MAP.values()]

class AEGroupUpdater(aedir.process.AEProcess):
    """AEGroupUpdater"""
    script_version = __version__
    deref_person_attrs = ('aeDept', 'aeLocation')

    @staticmethod
    def _member_zones_filter(aegroup_entry):
        """
        construct a filter from attribute 'aeMemberZone' if present in aegroup_entry
        """
        try:
            member_zones = aegroup_entry['aeMemberZone']
        except KeyError:
            res = ''
        else:
            res = compose_filter('|', map_filter_parts('entryDN:dnSubordinateMatch:', member_zones))
        return res

    def _update_members(self, group_dn, member_map_attr, old_members, new_members, old_member_attr_values, new_member_attr_values):
        """
        update attribute 'member' and additional membership attribute
        """
        mod_list = []
        add_members = new_members - old_members
        if add_members:
            mod_list.append((
             ldap0.MOD_ADD, MEMBER_ATTR, list(add_members)))
        else:
            remove_members = old_members - new_members
            if remove_members:
                mod_list.append((
                 ldap0.MOD_DELETE, MEMBER_ATTR, list(remove_members)))
            remove_member_attr_values = old_member_attr_values - new_member_attr_values
            if remove_member_attr_values:
                mod_list.append((
                 ldap0.MOD_DELETE, member_map_attr, list(remove_member_attr_values)))
            add_member_attr_values = new_member_attr_values - old_member_attr_values
            if add_member_attr_values:
                mod_list.append((
                 ldap0.MOD_ADD, member_map_attr, list(add_member_attr_values)))
            if mod_list:
                try:
                    self.ldap_conn.modify_s(group_dn, [(
                     mod, at.encode('ascii'), ldap0.base.encode_list(avl)) for mod, at, avl in mod_list])
                except ldap0.LDAPError as ldap_error:
                    try:
                        self.logger.error('LDAPError modifying %r: %s mod_list = %r', group_dn, ldap_error, mod_list)
                    finally:
                        ldap_error = None
                        del ldap_error

                else:
                    self.logger.debug('Updated %r: mod_list = %r', group_dn, mod_list)
                    self.logger.info('Updated member values of group entry %r: add_members=%d add_member_attr_values=%d remove_members=%d remove_member_attr_values=%d', group_dn, len(add_members), len(add_member_attr_values), len(remove_members), len(remove_member_attr_values))
            else:
                self.logger.debug('Nothing to be done with %r', group_dn)

    def fix_static_groups(self):
        """
        1. Removes obsolete 'member' and other member values and
        2. adds missing other member values
        in all active static aeGroup entries
        """
        for group_object_class, member_attrs in MEMBER_ATTRS_MAP.items():
            member_map_attr, member_user_attr = member_attrs
            msg_id = self.ldap_conn.search((self.ldap_conn.search_base),
              (ldap0.SCOPE_SUBTREE),
              ('(&(objectClass={0})(!({1}=*))(aeStatus=0))'.format(group_object_class, MEMBERURL_ATTR)),
              attrlist=[
             MEMBER_ATTR,
             member_map_attr],
              req_ctrls=[
             DereferenceControl(True, {MEMBER_ATTR: [
                            'aeStatus',
                            MEMBEROF_ATTR,
                            member_user_attr]})])
            for ldap_results in self.ldap_conn.results(msg_id):
                for ldap_group in ldap_results.rdata:
                    if not ldap_group.ctrls:
                        pass
                    else:
                        member_deref_result = ldap_group.ctrls[0].derefRes[MEMBER_ATTR]
                        old_members = set(ldap_group.entry_s.get(MEMBER_ATTR, []))
                        old_member_attr_values = set(ldap_group.entry_s.get(member_map_attr, []))
                        new_members = set()
                        new_member_attr_values = set()
                        for deref_res in member_deref_result:
                            if int(deref_res.entry_s['aeStatus'][0]) <= 0:
                                new_members.add(deref_res.dn_s)
                                try:
                                    new_member_attr_values.add(deref_res.entry_s[member_user_attr][0])
                                except KeyError:
                                    self.logger.error('Attribute %r not found in entry %r: %r', member_user_attr, deref_res.dn_s, deref_res.entry_s)

                            self._update_members(ldap_group.dn_s, member_map_attr, old_members, new_members, old_member_attr_values, new_member_attr_values)

    def _constrained_persons(self, aegroup_entry):
        """
        return list of DNs of valid aePerson entries
        """
        deref_attrs = []
        person_filter_parts = [
         '(objectClass=aePerson)(aeStatus=0)']
        for deref_attr_type in self.deref_person_attrs:
            try:
                deref_attr_values = aegroup_entry[deref_attr_type]
            except KeyError:
                pass
            else:
                deref_attrs.append(deref_attr_type)
                person_filter_parts.append(compose_filter('|', map_filter_parts(deref_attr_type, deref_attr_values)))

        if not deref_attrs:
            return
        ldap_result = self.ldap_conn.search_s((self.ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          ('(&{0})'.format(''.join(person_filter_parts))),
          attrlist=[
         '1.1']) or 
        res = set([res.dn_s.lower() for res in ldap_result])
        return res

    def empty_archived_groups(self):
        """
        2. remove all members from archived groups
        """
        non_empty_archived_groups = self.ldap_conn.search_s((self.ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          ('(&(objectClass=aeGroup)(aeStatus=2)({0}=*))'.format(MEMBER_ATTR)),
          attrlist=([
         'structuralObjectClass',
         MEMBER_ATTR] + MEMBER_ATTRS),
          attrsonly=True)
        for group_dn, group_entry in non_empty_archived_groups:
            mod_list = [(ldap0.MOD_DELETE, attr, None) for attr in [MEMBER_ATTR] + MEMBER_ATTRS if attr in group_entry]
            try:
                self.ldap_conn.modify_s(group_dn, mod_list)
            except ldap0.LDAPError as ldap_error:
                try:
                    self.logger.error('LDAPError modifying %r: %s mod_list = %r', group_dn, ldap_error, mod_list)
                finally:
                    ldap_error = None
                    del ldap_error

            else:
                self.logger.info('Removed all member attributes from %r: mod_list = %r', group_dn, mod_list)

    def update_memberurl_groups--- This code section failed: ---

 L. 288         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ldap_conn
                4  LOAD_ATTR                search_s

 L. 289         6  LOAD_FAST                'self'
                8  LOAD_ATTR                ldap_conn
               10  LOAD_ATTR                search_base

 L. 290        12  LOAD_GLOBAL              ldap0
               14  LOAD_ATTR                SCOPE_SUBTREE

 L. 291        16  LOAD_STR                 '(&({0}=*)(aeStatus=0))'
               18  LOAD_METHOD              format
               20  LOAD_GLOBAL              MEMBERURL_ATTR
               22  CALL_METHOD_1         1  ''

 L. 293        24  LOAD_STR                 'aeDept'

 L. 294        26  LOAD_STR                 'aeLocation'

 L. 295        28  LOAD_STR                 'aeMemberZone'

 L. 296        30  LOAD_STR                 'structuralObjectClass'

 L. 297        32  LOAD_GLOBAL              MEMBER_ATTR

 L. 298        34  LOAD_GLOBAL              MEMBERURL_ATTR

 L. 292        36  BUILD_LIST_6          6 

 L. 299        38  LOAD_GLOBAL              MEMBER_ATTRS

 L. 292        40  BINARY_ADD       

 L. 288        42  LOAD_CONST               ('attrlist',)
               44  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               46  STORE_FAST               'dynamic_groups'

 L. 301        48  LOAD_FAST                'dynamic_groups'
               50  GET_ITER         
            52_54  FOR_ITER            796  'to 796'
               56  STORE_FAST               'dyn_group'

 L. 303        58  LOAD_FAST                'self'
               60  LOAD_ATTR                logger
               62  LOAD_METHOD              debug
               64  LOAD_STR                 'Processing group entry %r ...'
               66  LOAD_FAST                'dyn_group'
               68  LOAD_ATTR                dn_s
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          

 L. 305        74  LOAD_FAST                'dyn_group'
               76  LOAD_ATTR                entry_s
               78  LOAD_STR                 'structuralObjectClass'
               80  BINARY_SUBSCR    
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  STORE_FAST               'group_object_class'

 L. 306        88  LOAD_GLOBAL              MEMBER_ATTRS_MAP
               90  LOAD_FAST                'group_object_class'
               92  BINARY_SUBSCR    
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'member_map_attr'
               98  STORE_FAST               'member_user_attr'

 L. 307       100  LOAD_FAST                'self'
              102  LOAD_ATTR                logger
              104  LOAD_METHOD              debug

 L. 308       106  LOAD_STR                 'group_object_class=%r member_map_attr=%r member_user_attr=%r'

 L. 309       108  LOAD_FAST                'group_object_class'

 L. 309       110  LOAD_FAST                'member_map_attr'

 L. 309       112  LOAD_FAST                'member_user_attr'

 L. 307       114  CALL_METHOD_4         4  ''
              116  POP_TOP          

 L. 312       118  LOAD_GLOBAL              set
              120  LOAD_FAST                'dyn_group'
              122  LOAD_ATTR                entry_s
              124  LOAD_METHOD              get
              126  LOAD_GLOBAL              MEMBER_ATTR
              128  BUILD_LIST_0          0 
              130  CALL_METHOD_2         2  ''
              132  CALL_FUNCTION_1       1  ''
              134  STORE_FAST               'old_members'

 L. 313       136  LOAD_GLOBAL              set
              138  LOAD_FAST                'dyn_group'
              140  LOAD_ATTR                entry_s
              142  LOAD_METHOD              get
              144  LOAD_FAST                'member_map_attr'
              146  BUILD_LIST_0          0 
              148  CALL_METHOD_2         2  ''
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'old_member_attr_values'

 L. 314       154  LOAD_GLOBAL              set
              156  CALL_FUNCTION_0       0  ''
              158  STORE_FAST               'new_members'

 L. 315       160  LOAD_GLOBAL              set
              162  CALL_FUNCTION_0       0  ''
              164  STORE_FAST               'new_member_attr_values'

 L. 317       166  LOAD_FAST                'self'
              168  LOAD_METHOD              _constrained_persons
              170  LOAD_FAST                'dyn_group'
              172  LOAD_ATTR                entry_s
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'person_dn_set'

 L. 318       178  LOAD_FAST                'self'
              180  LOAD_ATTR                logger
              182  LOAD_METHOD              debug
              184  LOAD_STR                 'person_dn_set = %r'
              186  LOAD_FAST                'person_dn_set'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 319       192  LOAD_FAST                'person_dn_set'
              194  LOAD_CONST               None
              196  COMPARE_OP               is
              198  POP_JUMP_IF_FALSE   206  'to 206'

 L. 320       200  LOAD_STR                 ''
              202  STORE_FAST               'person_filter_part'
              204  JUMP_FORWARD        210  'to 210'
            206_0  COME_FROM           198  '198'

 L. 322       206  LOAD_STR                 '(&(objectClass=aeUser)(aePerson=*))'
              208  STORE_FAST               'person_filter_part'
            210_0  COME_FROM           204  '204'

 L. 323       210  LOAD_FAST                'self'
              212  LOAD_ATTR                logger
              214  LOAD_METHOD              debug
              216  LOAD_STR                 'person_filter_part = %r'
              218  LOAD_FAST                'person_filter_part'
              220  CALL_METHOD_2         2  ''
              222  POP_TOP          

 L. 325       224  LOAD_FAST                'dyn_group'
              226  LOAD_ATTR                entry_s
              228  LOAD_GLOBAL              MEMBERURL_ATTR
              230  BINARY_SUBSCR    
              232  GET_ITER         
          234_236  FOR_ITER            772  'to 772'
              238  STORE_FAST               'member_url'

 L. 327       240  LOAD_FAST                'self'
              242  LOAD_ATTR                logger
              244  LOAD_METHOD              debug
              246  LOAD_STR                 'member_url = %r'
              248  LOAD_FAST                'member_url'
              250  CALL_METHOD_2         2  ''
              252  POP_TOP          

 L. 328       254  LOAD_GLOBAL              ldap0
              256  LOAD_ATTR                ldapurl
              258  LOAD_METHOD              LDAPUrl
              260  LOAD_FAST                'member_url'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'member_url_obj'

 L. 329       266  LOAD_STR                 '(&{0}(!(entryDN={1})){2}{3})'
              268  LOAD_METHOD              format

 L. 330       270  LOAD_FAST                'member_url_obj'
              272  LOAD_ATTR                filterstr

 L. 331       274  LOAD_FAST                'dyn_group'
              276  LOAD_ATTR                dn_s

 L. 332       278  LOAD_FAST                'self'
              280  LOAD_METHOD              _member_zones_filter
              282  LOAD_FAST                'dyn_group'
              284  LOAD_ATTR                entry_s
              286  CALL_METHOD_1         1  ''

 L. 333       288  LOAD_FAST                'person_filter_part'

 L. 329       290  CALL_METHOD_4         4  ''
              292  STORE_FAST               'dyn_group_filter'

 L. 335       294  LOAD_FAST                'self'
              296  LOAD_ATTR                logger
              298  LOAD_METHOD              debug
              300  LOAD_STR                 'dyn_group_filter = %r'
              302  LOAD_FAST                'dyn_group_filter'
              304  CALL_METHOD_2         2  ''
              306  POP_TOP          

 L. 337       308  LOAD_FAST                'member_url_obj'
              310  LOAD_ATTR                attrs
          312_314  POP_JUMP_IF_FALSE   346  'to 346'

 L. 338       316  LOAD_GLOBAL              DereferenceControl

 L. 339       318  LOAD_CONST               True

 L. 341       320  LOAD_FAST                'member_url_obj'
              322  LOAD_ATTR                attrs
              324  LOAD_CONST               0
              326  BINARY_SUBSCR    

 L. 342       328  LOAD_STR                 'aeStatus'

 L. 343       330  LOAD_STR                 'aePerson'

 L. 344       332  LOAD_FAST                'member_user_attr'

 L. 341       334  BUILD_LIST_3          3 

 L. 340       336  BUILD_MAP_1           1 

 L. 338       338  CALL_FUNCTION_2       2  ''
              340  BUILD_LIST_1          1 
              342  STORE_FAST               'server_ctrls'
              344  JUMP_FORWARD        350  'to 350'
            346_0  COME_FROM           312  '312'

 L. 349       346  LOAD_CONST               None
              348  STORE_FAST               'server_ctrls'
            350_0  COME_FROM           344  '344'

 L. 351   350_352  SETUP_FINALLY       702  'to 702'

 L. 352       354  LOAD_FAST                'self'
              356  LOAD_ATTR                ldap_conn
              358  LOAD_ATTR                search

 L. 353       360  LOAD_FAST                'member_url_obj'
              362  LOAD_ATTR                dn

 L. 354       364  LOAD_FAST                'member_url_obj'
              366  LOAD_ATTR                scope
          368_370  JUMP_IF_TRUE_OR_POP   376  'to 376'
              372  LOAD_GLOBAL              ldap0
              374  LOAD_ATTR                SCOPE_SUBTREE
            376_0  COME_FROM           368  '368'

 L. 355       376  LOAD_FAST                'dyn_group_filter'

 L. 357       378  LOAD_STR                 'cn'

 L. 358       380  LOAD_STR                 'aeStatus'

 L. 359       382  LOAD_STR                 'aePerson'

 L. 356       384  BUILD_LIST_3          3 

 L. 360       386  LOAD_FAST                'member_url_obj'
              388  LOAD_ATTR                attrs
          390_392  JUMP_IF_TRUE_OR_POP   396  'to 396'
              394  BUILD_LIST_0          0 
            396_0  COME_FROM           390  '390'

 L. 356       396  BINARY_ADD       

 L. 360       398  LOAD_GLOBAL              USER_ATTRS

 L. 356       400  BINARY_ADD       

 L. 361       402  LOAD_FAST                'server_ctrls'

 L. 352       404  LOAD_CONST               ('attrlist', 'req_ctrls')
              406  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              408  STORE_FAST               'msg_id'

 L. 363       410  LOAD_FAST                'self'
              412  LOAD_ATTR                ldap_conn
              414  LOAD_METHOD              results
              416  LOAD_FAST                'msg_id'
              418  CALL_METHOD_1         1  ''
              420  GET_ITER         
          422_424  FOR_ITER            698  'to 698'
              426  STORE_FAST               'ldap_results'

 L. 364       428  LOAD_FAST                'ldap_results'
              430  LOAD_ATTR                rdata
              432  GET_ITER         
          434_436  FOR_ITER            694  'to 694'
              438  STORE_FAST               'group'

 L. 366       440  LOAD_FAST                'person_dn_set'
              442  LOAD_CONST               None
              444  COMPARE_OP               is-not

 L. 365   446_448  POP_JUMP_IF_FALSE   478  'to 478'

 L. 367       450  LOAD_FAST                'group'
              452  LOAD_ATTR                entry_s
              454  LOAD_STR                 'aePerson'
              456  BINARY_SUBSCR    
              458  LOAD_CONST               0
              460  BINARY_SUBSCR    
              462  LOAD_METHOD              lower
              464  CALL_METHOD_0         0  ''
              466  LOAD_FAST                'person_dn_set'
              468  COMPARE_OP               not-in

 L. 365   470_472  POP_JUMP_IF_FALSE   478  'to 478'

 L. 369   474_476  JUMP_BACK           434  'to 434'
            478_0  COME_FROM           470  '470'
            478_1  COME_FROM           446  '446'

 L. 370       478  LOAD_FAST                'member_url_obj'
              480  LOAD_ATTR                attrs
          482_484  POP_JUMP_IF_FALSE   506  'to 506'

 L. 371       486  LOAD_FAST                'member_url_obj'
              488  LOAD_ATTR                attrs
              490  LOAD_CONST               0
              492  BINARY_SUBSCR    
              494  LOAD_METHOD              lower
              496  CALL_METHOD_0         0  ''
              498  LOAD_STR                 'entrydn'
              500  COMPARE_OP               ==

 L. 370   502_504  POP_JUMP_IF_FALSE   514  'to 514'
            506_0  COME_FROM           482  '482'

 L. 372       506  LOAD_FAST                'group'
              508  BUILD_LIST_1          1 
              510  STORE_FAST               'member_deref_results'
              512  JUMP_FORWARD        572  'to 572'
            514_0  COME_FROM           502  '502'

 L. 373       514  LOAD_FAST                'member_url_obj'
              516  LOAD_ATTR                attrs
          518_520  POP_JUMP_IF_FALSE   556  'to 556'
              522  LOAD_FAST                'group'
              524  LOAD_ATTR                ctrls
          526_528  POP_JUMP_IF_TRUE    556  'to 556'

 L. 374       530  LOAD_FAST                'self'
              532  LOAD_ATTR                logger
              534  LOAD_METHOD              debug

 L. 375       536  LOAD_STR                 'ignoring empty %r: %r'

 L. 376       538  LOAD_FAST                'group'
              540  LOAD_ATTR                dn_s

 L. 377       542  LOAD_FAST                'group'
              544  LOAD_ATTR                entry_s

 L. 374       546  CALL_METHOD_3         3  ''
              548  POP_TOP          

 L. 379   550_552  JUMP_BACK           434  'to 434'
              554  JUMP_FORWARD        572  'to 572'
            556_0  COME_FROM           526  '526'
            556_1  COME_FROM           518  '518'

 L. 381       556  LOAD_FAST                'group'
              558  LOAD_ATTR                ctrls
              560  LOAD_CONST               0
              562  BINARY_SUBSCR    
              564  LOAD_ATTR                derefRes
              566  LOAD_GLOBAL              MEMBER_ATTR
              568  BINARY_SUBSCR    
              570  STORE_FAST               'member_deref_results'
            572_0  COME_FROM           554  '554'
            572_1  COME_FROM           512  '512'

 L. 382       572  LOAD_FAST                'member_deref_results'
              574  GET_ITER         
            576_0  COME_FROM           600  '600'
              576  FOR_ITER            690  'to 690'
              578  STORE_FAST               'deref_res'

 L. 383       580  LOAD_GLOBAL              int
              582  LOAD_FAST                'deref_res'
              584  LOAD_ATTR                entry_s
              586  LOAD_STR                 'aeStatus'
              588  BINARY_SUBSCR    
              590  LOAD_CONST               0
              592  BINARY_SUBSCR    
              594  CALL_FUNCTION_1       1  ''
              596  LOAD_CONST               0
              598  COMPARE_OP               <=
          600_602  POP_JUMP_IF_FALSE   576  'to 576'

 L. 384       604  LOAD_FAST                'new_members'
              606  LOAD_METHOD              add
              608  LOAD_FAST                'deref_res'
              610  LOAD_ATTR                dn_s
              612  CALL_METHOD_1         1  ''
              614  POP_TOP          

 L. 385       616  SETUP_FINALLY       642  'to 642'

 L. 386       618  LOAD_FAST                'new_member_attr_values'
              620  LOAD_METHOD              add
              622  LOAD_FAST                'deref_res'
              624  LOAD_ATTR                entry_s
              626  LOAD_FAST                'member_user_attr'
              628  BINARY_SUBSCR    
              630  LOAD_CONST               0
              632  BINARY_SUBSCR    
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          
              638  POP_BLOCK        
              640  JUMP_BACK           576  'to 576'
            642_0  COME_FROM_FINALLY   616  '616'

 L. 387       642  DUP_TOP          
              644  LOAD_GLOBAL              KeyError
              646  COMPARE_OP               exception-match
          648_650  POP_JUMP_IF_FALSE   684  'to 684'
              652  POP_TOP          
              654  POP_TOP          
              656  POP_TOP          

 L. 388       658  LOAD_FAST                'self'
              660  LOAD_ATTR                logger
              662  LOAD_METHOD              error

 L. 389       664  LOAD_STR                 'Attribute %r not found in entry %r: %r'

 L. 390       666  LOAD_FAST                'member_user_attr'

 L. 391       668  LOAD_FAST                'deref_res'
              670  LOAD_ATTR                dn_s

 L. 392       672  LOAD_FAST                'deref_res'
              674  LOAD_ATTR                entry_s

 L. 388       676  CALL_METHOD_4         4  ''
              678  POP_TOP          
              680  POP_EXCEPT       
              682  JUMP_BACK           576  'to 576'
            684_0  COME_FROM           648  '648'
              684  END_FINALLY      
          686_688  JUMP_BACK           576  'to 576'
          690_692  JUMP_BACK           434  'to 434'
          694_696  JUMP_BACK           422  'to 422'
              698  POP_BLOCK        
              700  JUMP_BACK           234  'to 234'
            702_0  COME_FROM_FINALLY   350  '350'

 L. 395       702  DUP_TOP          
              704  LOAD_GLOBAL              ldap0
              706  LOAD_ATTR                LDAPError
              708  COMPARE_OP               exception-match
          710_712  POP_JUMP_IF_FALSE   768  'to 768'
              714  POP_TOP          
              716  STORE_FAST               'ldap_error'
              718  POP_TOP          
              720  SETUP_FINALLY       756  'to 756'

 L. 396       722  LOAD_FAST                'self'
              724  LOAD_ATTR                logger
              726  LOAD_METHOD              error

 L. 397       728  LOAD_STR                 'LDAPError searching members for %r with %r and %r: %s'

 L. 398       730  LOAD_FAST                'dyn_group'
              732  LOAD_ATTR                dn_s

 L. 399       734  LOAD_FAST                'member_url'

 L. 400       736  LOAD_FAST                'dyn_group_filter'

 L. 401       738  LOAD_FAST                'ldap_error'

 L. 396       740  CALL_METHOD_5         5  ''
              742  POP_TOP          

 L. 403       744  POP_BLOCK        
              746  POP_EXCEPT       
              748  CALL_FINALLY        756  'to 756'
              750  JUMP_BACK           234  'to 234'
              752  POP_BLOCK        
              754  BEGIN_FINALLY    
            756_0  COME_FROM           748  '748'
            756_1  COME_FROM_FINALLY   720  '720'
              756  LOAD_CONST               None
              758  STORE_FAST               'ldap_error'
              760  DELETE_FAST              'ldap_error'
              762  END_FINALLY      
              764  POP_EXCEPT       
              766  JUMP_BACK           234  'to 234'
            768_0  COME_FROM           710  '710'
              768  END_FINALLY      
              770  JUMP_BACK           234  'to 234'

 L. 405       772  LOAD_FAST                'self'
              774  LOAD_METHOD              _update_members

 L. 406       776  LOAD_FAST                'dyn_group'
              778  LOAD_ATTR                dn_s

 L. 407       780  LOAD_FAST                'member_map_attr'

 L. 408       782  LOAD_FAST                'old_members'

 L. 409       784  LOAD_FAST                'new_members'

 L. 410       786  LOAD_FAST                'old_member_attr_values'

 L. 411       788  LOAD_FAST                'new_member_attr_values'

 L. 405       790  CALL_METHOD_6         6  ''
              792  POP_TOP          
              794  JUMP_BACK            52  'to 52'

Parse error at or near `JUMP_FORWARD' instruction at offset 554

    def run_worker(self, state):
        """
        the main program
        """
        self.logger.debug('invoke empty_archived_groups()')
        self.empty_archived_groups()
        self.logger.debug('invoke update_memberurl_groups()')
        self.update_memberurl_groups()
        self.logger.debug('invoke fix_static_groups()')
        self.fix_static_groups()


def main--- This code section failed: ---

 L. 432         0  LOAD_GLOBAL              AEGroupUpdater
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           24  'to 24'
                6  STORE_FAST               'ae_process'

 L. 433         8  LOAD_FAST                'ae_process'
               10  LOAD_ATTR                run
               12  LOAD_CONST               1
               14  LOAD_CONST               ('max_runs',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  POP_TOP          
               20  POP_BLOCK        
               22  BEGIN_FINALLY    
             24_0  COME_FROM_WITH        4  '4'
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 22


if __name__ == '__main__':
    main()