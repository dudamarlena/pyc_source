# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/groupadm.py
# Compiled at: 2020-05-05 11:25:58
# Size of source mod 2**32: 16572 bytes
"""
web2ldap.app.groupadm: add/delete user entry to/from group entries

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0, ldap0.cidict
from ldap0.dn import DNObj
from ldap0.res import SearchResultEntry
import web2ldap.app.core, web2ldap.app.gui
ACTION2MODTYPE = {'add':ldap0.MOD_ADD, 
 'remove':ldap0.MOD_DELETE}
REQUESTED_GROUP_ATTRS = [
 'objectClass', 'cn', 'description']

def group_select_field(app, groups_dict, field_name, field_title, group_search_root, dn_list, optgroup_bounds):
    optgroup_min_level, optgroup_max_level = optgroup_bounds
    if optgroup_min_level is not None or optgroup_max_level is not None:
        optgroup_dict = {None: []}
        for dn in dn_list:
            try:
                colgroup_dn = str(DNObj.from_str(dn).slice(optgroup_min_level, optgroup_max_level))
            except (IndexError, ValueError):
                colgroup_dn = None
            else:
                if colgroup_dn:
                    try:
                        optgroup_dict[colgroup_dn].append(dn)
                    except KeyError:
                        optgroup_dict[colgroup_dn] = [
                         dn]

        else:
            optgroup_list = []
            try:
                colgroup_memberdn = str(app.dn_obj.slice(optgroup_min_level, optgroup_max_level))
            except (IndexError, ValueError):
                colgroup_memberdn = None
            else:
                if colgroup_memberdn in optgroup_dict:
                    optgroup_list.append(colgroup_memberdn)
                else:
                    colgroup_authzdn = None
                    if app.ls.who is not None:
                        try:
                            colgroup_authzdn = str(DNObj.from_str(app.ls.who).slice(optgroup_min_level, optgroup_max_level))
                        except (IndexError, ValueError, ldap0.DECODING_ERROR):
                            pass

                        if colgroup_authzdn in optgroup_dict:
                            if colgroup_authzdn != colgroup_memberdn:
                                optgroup_list.append(colgroup_authzdn)
                optgroup_list.extend(sorted([dn for dn in optgroup_dict if dn is not None if dn != colgroup_memberdn if dn != colgroup_authzdn],
                  key=(str.lower)))
                optgroup_list.append(None)

    else:
        optgroup_dict = {None: dn_list}
        optgroup_list = [None]
    option_list = []
    for optgroup_dn in optgroup_list:
        if optgroup_dn:
            option_list.append('<optgroup label="%s">' % app.form.utf2display(optgroup_dn))

    for dn in sorted((optgroup_dict[optgroup_dn]), key=(str.lower)):
        option_text = app.form.utf2display(groups_dict[dn].get('cn', [
         dn[:-len(group_search_root) or len(dn)]])[0])
        option_title = app.form.utf2display(groups_dict[dn].get('description', [
         dn[:-len(group_search_root)]])[0])
        option_list.append('<option value="%s" title="%s">%s</option>' % (
         app.form.utf2display(dn),
         option_title,
         option_text))
    else:
        if optgroup_dn:
            option_list.append('</optgroup>')
        return '<select size="15" multiple id="%s" name="%s" title="%s">\n%s\n</select>\n' % (
         field_name,
         field_name,
         field_title,
         '\n'.join(option_list))


def w2l_groupadm--- This code section failed: ---

 L. 123         0  LOAD_GLOBAL              ldap0
                2  LOAD_ATTR                cidict
                4  LOAD_METHOD              CIDict
                6  LOAD_DEREF               'app'
                8  LOAD_METHOD              cfg_param
               10  LOAD_STR                 'groupadm_defs'
               12  BUILD_MAP_0           0 
               14  CALL_METHOD_2         2  ''
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'groupadm_defs'

 L. 124        20  LOAD_FAST                'groupadm_defs'
               22  POP_JUMP_IF_TRUE     38  'to 38'

 L. 125        24  LOAD_GLOBAL              web2ldap
               26  LOAD_ATTR                app
               28  LOAD_ATTR                core
               30  LOAD_METHOD              ErrorExit
               32  LOAD_STR                 'Group admin options empty or not set.'
               34  CALL_METHOD_1         1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            22  '22'

 L. 126        38  LOAD_FAST                'groupadm_defs'
               40  LOAD_METHOD              keys
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'groupadm_defs_keys'

 L. 128        46  LOAD_LISTCOMP            '<code_object <listcomp>>'
               48  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
               50  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 130        52  LOAD_FAST                'groupadm_defs'
               54  LOAD_METHOD              values
               56  CALL_METHOD_0         0  ''

 L. 128        58  GET_ITER         
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'all_membership_attrs'

 L. 134        64  LOAD_DEREF               'app'
               66  LOAD_ATTR                ls
               68  LOAD_ATTR                l
               70  LOAD_ATTR                read_s
               72  LOAD_DEREF               'app'
               74  LOAD_ATTR                dn
               76  LOAD_FAST                'all_membership_attrs'
               78  LOAD_CONST               ('attrlist',)
               80  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               82  STORE_FAST               'search_result'

 L. 135        84  LOAD_FAST                'search_result'
               86  POP_JUMP_IF_TRUE    102  'to 102'

 L. 136        88  LOAD_GLOBAL              web2ldap
               90  LOAD_ATTR                app
               92  LOAD_ATTR                core
               94  LOAD_METHOD              ErrorExit
               96  LOAD_STR                 'No search result when reading entry.'
               98  CALL_METHOD_1         1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            86  '86'

 L. 138       102  LOAD_GLOBAL              ldap0
              104  LOAD_ATTR                schema
              106  LOAD_ATTR                models
              108  LOAD_METHOD              Entry
              110  LOAD_DEREF               'app'
              112  LOAD_ATTR                schema
              114  LOAD_DEREF               'app'
              116  LOAD_ATTR                dn
              118  LOAD_FAST                'search_result'
              120  LOAD_ATTR                entry_as
              122  CALL_METHOD_3         3  ''
              124  STORE_FAST               'user_entry'

 L. 141       126  LOAD_DEREF               'app'
              128  LOAD_ATTR                form
              130  LOAD_METHOD              getInputValue
              132  LOAD_STR                 'groupadm_searchroot'
              134  LOAD_DEREF               'app'
              136  LOAD_ATTR                naming_context
              138  BUILD_LIST_1          1 
              140  CALL_METHOD_2         2  ''
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  STORE_FAST               'group_search_root'

 L. 142       148  LOAD_GLOBAL              int
              150  LOAD_DEREF               'app'
              152  LOAD_ATTR                form
              154  LOAD_METHOD              getInputValue
              156  LOAD_STR                 'groupadm_view'
              158  LOAD_STR                 '1'
              160  BUILD_LIST_1          1 
              162  CALL_METHOD_2         2  ''
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'groupadm_view'

 L. 143       172  LOAD_DEREF               'app'
              174  LOAD_ATTR                form
              176  LOAD_METHOD              getInputValue
              178  LOAD_STR                 'groupadm_name'
              180  LOAD_CONST               None
              182  BUILD_LIST_1          1 
              184  CALL_METHOD_2         2  ''
              186  LOAD_CONST               0
              188  BINARY_SUBSCR    
              190  STORE_FAST               'groupadm_name'

 L. 145       192  BUILD_LIST_0          0 
              194  STORE_FAST               'filter_components'

 L. 146       196  LOAD_FAST                'groupadm_defs'
              198  LOAD_METHOD              keys
              200  CALL_METHOD_0         0  ''
              202  GET_ITER         
              204  FOR_ITER            364  'to 364'
              206  STORE_FAST               'oc'

 L. 147       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'groupadm_defs'
              212  LOAD_FAST                'oc'
              214  BINARY_SUBSCR    
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_CONST               3
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   238  'to 238'
              224  LOAD_FAST                'groupadm_defs'
              226  LOAD_FAST                'oc'
              228  BINARY_SUBSCR    
              230  LOAD_CONST               2
              232  BINARY_SUBSCR    
              234  POP_JUMP_IF_TRUE    238  'to 238'

 L. 148       236  JUMP_BACK           204  'to 204'
            238_0  COME_FROM           234  '234'
            238_1  COME_FROM           222  '222'

 L. 149       238  LOAD_FAST                'groupadm_defs'
              240  LOAD_FAST                'oc'
              242  BINARY_SUBSCR    
              244  LOAD_CONST               None
              246  LOAD_CONST               2
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  UNPACK_SEQUENCE_2     2 
              254  STORE_FAST               'group_member_attrtype'
              256  STORE_FAST               'user_entry_attrtype'

 L. 150       258  LOAD_FAST                'user_entry_attrtype'
              260  LOAD_CONST               None
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_FALSE   276  'to 276'

 L. 151       268  LOAD_DEREF               'app'
              270  LOAD_ATTR                dn
              272  STORE_FAST               'user_entry_attrvalue'
              274  JUMP_FORWARD        330  'to 330'
            276_0  COME_FROM           264  '264'

 L. 153       276  SETUP_FINALLY       304  'to 304'

 L. 154       278  LOAD_FAST                'user_entry'
              280  LOAD_FAST                'user_entry_attrtype'
              282  BINARY_SUBSCR    
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_METHOD              decode
              290  LOAD_DEREF               'app'
              292  LOAD_ATTR                ls
              294  LOAD_ATTR                charset
              296  CALL_METHOD_1         1  ''
              298  STORE_FAST               'user_entry_attrvalue'
              300  POP_BLOCK        
              302  JUMP_FORWARD        330  'to 330'
            304_0  COME_FROM_FINALLY   276  '276'

 L. 155       304  DUP_TOP          
              306  LOAD_GLOBAL              KeyError
              308  COMPARE_OP               exception-match
          310_312  POP_JUMP_IF_FALSE   328  'to 328'
              314  POP_TOP          
              316  POP_TOP          
              318  POP_TOP          

 L. 156       320  POP_EXCEPT       
              322  JUMP_BACK           204  'to 204'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
            328_0  COME_FROM           310  '310'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM           302  '302'
            330_2  COME_FROM           274  '274'

 L. 157       330  LOAD_FAST                'filter_components'
              332  LOAD_METHOD              append

 L. 158       334  LOAD_FAST                'oc'
              336  LOAD_METHOD              strip
              338  CALL_METHOD_0         0  ''

 L. 159       340  LOAD_FAST                'group_member_attrtype'
              342  LOAD_METHOD              strip
              344  CALL_METHOD_0         0  ''

 L. 160       346  LOAD_GLOBAL              ldap0
              348  LOAD_ATTR                filter
              350  LOAD_METHOD              escape_str
              352  LOAD_FAST                'user_entry_attrvalue'
              354  CALL_METHOD_1         1  ''

 L. 157       356  BUILD_TUPLE_3         3 
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
              362  JUMP_BACK           204  'to 204'

 L. 167       364  LOAD_DEREF               'app'
              366  LOAD_METHOD              cfg_param
              368  LOAD_STR                 'groupadm_filterstr_template'
              370  LOAD_STR                 '(|%s)'
              372  CALL_METHOD_2         2  ''
              374  STORE_FAST               'groupadm_filterstr_template'

 L. 169       376  LOAD_FAST                'groupadm_filterstr_template'

 L. 170       378  LOAD_STR                 ''
              380  LOAD_METHOD              join

 L. 171       382  LOAD_LISTCOMP            '<code_object <listcomp>>'
              384  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              386  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 173       388  LOAD_FAST                'filter_components'

 L. 171       390  GET_ITER         
              392  CALL_FUNCTION_1       1  ''

 L. 170       394  CALL_METHOD_1         1  ''

 L. 169       396  BINARY_MODULO    
              398  STORE_FAST               'all_group_filterstr'

 L. 177       400  LOAD_FAST                'groupadm_name'
          402_404  POP_JUMP_IF_FALSE   426  'to 426'

 L. 178       406  LOAD_STR                 '(&(cn=*%s*)%s)'

 L. 179       408  LOAD_GLOBAL              ldap0
              410  LOAD_ATTR                filter
              412  LOAD_METHOD              escape_str
              414  LOAD_FAST                'groupadm_name'
              416  CALL_METHOD_1         1  ''

 L. 180       418  LOAD_FAST                'all_group_filterstr'

 L. 178       420  BUILD_TUPLE_2         2 
              422  BINARY_MODULO    
              424  STORE_FAST               'all_group_filterstr'
            426_0  COME_FROM           402  '402'

 L. 183       426  BUILD_MAP_0           0 
              428  STORE_FAST               'all_groups_dict'

 L. 185       430  SETUP_FINALLY       532  'to 532'

 L. 186       432  LOAD_DEREF               'app'
              434  LOAD_ATTR                ls
              436  LOAD_ATTR                l
              438  LOAD_ATTR                search

 L. 187       440  LOAD_GLOBAL              str
              442  LOAD_FAST                'group_search_root'
              444  CALL_FUNCTION_1       1  ''

 L. 188       446  LOAD_GLOBAL              ldap0
              448  LOAD_ATTR                SCOPE_SUBTREE

 L. 189       450  LOAD_FAST                'all_group_filterstr'

 L. 190       452  LOAD_GLOBAL              REQUESTED_GROUP_ATTRS

 L. 186       454  LOAD_CONST               ('attrlist',)
              456  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              458  STORE_FAST               'msg_id'

 L. 192       460  LOAD_DEREF               'app'
              462  LOAD_ATTR                ls
              464  LOAD_ATTR                l
              466  LOAD_METHOD              results
              468  LOAD_FAST                'msg_id'
              470  CALL_METHOD_1         1  ''
              472  GET_ITER         
              474  FOR_ITER            528  'to 528'
              476  STORE_FAST               'res'

 L. 193       478  LOAD_FAST                'res'
              480  LOAD_ATTR                rdata
              482  GET_ITER         
            484_0  COME_FROM           496  '496'
              484  FOR_ITER            524  'to 524'
              486  STORE_FAST               'sre'

 L. 194       488  LOAD_GLOBAL              isinstance
              490  LOAD_FAST                'sre'
              492  LOAD_GLOBAL              SearchResultEntry
              494  CALL_FUNCTION_2       2  ''
          496_498  POP_JUMP_IF_FALSE   484  'to 484'

 L. 195       500  LOAD_GLOBAL              ldap0
              502  LOAD_ATTR                cidict
              504  LOAD_METHOD              CIDict
              506  LOAD_FAST                'sre'
              508  LOAD_ATTR                entry_s
              510  CALL_METHOD_1         1  ''
              512  LOAD_FAST                'all_groups_dict'
              514  LOAD_FAST                'sre'
              516  LOAD_ATTR                dn_s
              518  STORE_SUBSCR     
          520_522  JUMP_BACK           484  'to 484'
          524_526  JUMP_BACK           474  'to 474'
              528  POP_BLOCK        
              530  JUMP_FORWARD        592  'to 592'
            532_0  COME_FROM_FINALLY   430  '430'

 L. 196       532  DUP_TOP          
              534  LOAD_GLOBAL              ldap0
              536  LOAD_ATTR                NO_SUCH_OBJECT
              538  COMPARE_OP               exception-match
          540_542  POP_JUMP_IF_FALSE   558  'to 558'
              544  POP_TOP          
              546  POP_TOP          
              548  POP_TOP          

 L. 197       550  LOAD_STR                 'No such object! Did you choose a valid search base?'
              552  STORE_FAST               'error_msg'
              554  POP_EXCEPT       
              556  JUMP_FORWARD        592  'to 592'
            558_0  COME_FROM           540  '540'

 L. 198       558  DUP_TOP          
              560  LOAD_GLOBAL              ldap0
              562  LOAD_ATTR                SIZELIMIT_EXCEEDED
              564  LOAD_GLOBAL              ldap0
              566  LOAD_ATTR                TIMELIMIT_EXCEEDED
              568  BUILD_TUPLE_2         2 
              570  COMPARE_OP               exception-match
          572_574  POP_JUMP_IF_FALSE   590  'to 590'
              576  POP_TOP          
              578  POP_TOP          
              580  POP_TOP          

 L. 199       582  LOAD_STR                 'Size or time limit exceeded while searching group entries!'
              584  STORE_FAST               'error_msg'
              586  POP_EXCEPT       
              588  JUMP_FORWARD        592  'to 592'
            590_0  COME_FROM           572  '572'
              590  END_FINALLY      
            592_0  COME_FROM           588  '588'
            592_1  COME_FROM           556  '556'
            592_2  COME_FROM           530  '530'

 L. 201       592  LOAD_GLOBAL              sorted
              594  LOAD_FAST                'all_groups_dict'
              596  LOAD_METHOD              keys
              598  CALL_METHOD_0         0  ''
              600  LOAD_GLOBAL              str
              602  LOAD_ATTR                lower
              604  LOAD_CONST               ('key',)
              606  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              608  STORE_FAST               'all_group_entries'

 L. 207       610  LOAD_STR                 'groupadm_add'
              612  LOAD_DEREF               'app'
              614  LOAD_ATTR                form
              616  LOAD_ATTR                input_field_names
              618  COMPARE_OP               in
          620_622  POP_JUMP_IF_TRUE    638  'to 638'

 L. 208       624  LOAD_STR                 'groupadm_remove'
              626  LOAD_DEREF               'app'
              628  LOAD_ATTR                form
              630  LOAD_ATTR                input_field_names
              632  COMPARE_OP               in

 L. 207   634_636  POP_JUMP_IF_FALSE  1184  'to 1184'
            638_0  COME_FROM           620  '620'

 L. 210       638  BUILD_LIST_0          0 
              640  STORE_FAST               'ldaperror_entries'

 L. 211       642  BUILD_LIST_0          0 
              644  STORE_FAST               'successful_group_mods'

 L. 213       646  LOAD_GLOBAL              ACTION2MODTYPE
              648  GET_ITER         
          650_652  FOR_ITER            968  'to 968'
              654  STORE_FAST               'action'

 L. 215       656  LOAD_DEREF               'app'
              658  LOAD_ATTR                form
              660  LOAD_METHOD              getInputValue
              662  LOAD_STR                 'groupadm_%s'
              664  LOAD_FAST                'action'
              666  BINARY_MODULO    
              668  BUILD_LIST_0          0 
              670  CALL_METHOD_2         2  ''
              672  GET_ITER         
            674_0  COME_FROM           862  '862'
          674_676  FOR_ITER            964  'to 964'
              678  STORE_FAST               'action_group_dn'

 L. 216       680  LOAD_FAST                'action_group_dn'
              682  STORE_FAST               'group_dn'

 L. 217       684  LOAD_FAST                'group_dn'
              686  LOAD_FAST                'all_groups_dict'
              688  COMPARE_OP               not-in
          690_692  POP_JUMP_IF_FALSE   698  'to 698'

 L. 220   694_696  JUMP_BACK           674  'to 674'
            698_0  COME_FROM           690  '690'

 L. 221       698  BUILD_LIST_0          0 
              700  STORE_FAST               'modlist'

 L. 222       702  LOAD_FAST                'groupadm_defs_keys'
              704  GET_ITER         
            706_0  COME_FROM           742  '742'
              706  FOR_ITER            860  'to 860'
              708  STORE_FAST               'oc'

 L. 223       710  LOAD_FAST                'oc'
              712  LOAD_METHOD              lower
              714  CALL_METHOD_0         0  ''
              716  LOAD_LISTCOMP            '<code_object <listcomp>>'
              718  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              720  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 225       722  LOAD_FAST                'all_groups_dict'
              724  LOAD_FAST                'group_dn'
              726  BINARY_SUBSCR    
              728  LOAD_METHOD              get
              730  LOAD_STR                 'objectClass'
              732  BUILD_LIST_0          0 
              734  CALL_METHOD_2         2  ''

 L. 223       736  GET_ITER         
              738  CALL_FUNCTION_1       1  ''
              740  COMPARE_OP               in
          742_744  POP_JUMP_IF_FALSE   706  'to 706'

 L. 227       746  LOAD_FAST                'groupadm_defs'
              748  LOAD_FAST                'oc'
              750  BINARY_SUBSCR    
              752  LOAD_CONST               0
              754  LOAD_CONST               2
              756  BUILD_SLICE_2         2 
              758  BINARY_SUBSCR    
              760  UNPACK_SEQUENCE_2     2 
              762  STORE_FAST               'group_member_attrtype'
              764  STORE_FAST               'user_entry_attrtype'

 L. 228       766  LOAD_FAST                'user_entry_attrtype'
              768  LOAD_CONST               None
              770  COMPARE_OP               is
          772_774  POP_JUMP_IF_FALSE   784  'to 784'

 L. 229       776  LOAD_DEREF               'app'
              778  LOAD_ATTR                ldap_dn
              780  STORE_FAST               'member_value'
              782  JUMP_FORWARD        828  'to 828'
            784_0  COME_FROM           772  '772'

 L. 231       784  LOAD_FAST                'user_entry_attrtype'
              786  LOAD_FAST                'user_entry'
              788  COMPARE_OP               not-in
          790_792  POP_JUMP_IF_FALSE   816  'to 816'

 L. 232       794  LOAD_GLOBAL              web2ldap
              796  LOAD_ATTR                app
              798  LOAD_ATTR                core
              800  LOAD_METHOD              ErrorExit

 L. 233       802  LOAD_STR                 'Object class %s requires attribute %s in group entry.'

 L. 234       804  LOAD_FAST                'oc'

 L. 235       806  LOAD_FAST                'user_entry_attrtype'

 L. 233       808  BUILD_TUPLE_2         2 
              810  BINARY_MODULO    

 L. 232       812  CALL_METHOD_1         1  ''
              814  RAISE_VARARGS_1       1  'exception instance'
            816_0  COME_FROM           790  '790'

 L. 238       816  LOAD_FAST                'user_entry'
              818  LOAD_FAST                'user_entry_attrtype'
              820  BINARY_SUBSCR    
              822  LOAD_CONST               0
              824  BINARY_SUBSCR    
              826  STORE_FAST               'member_value'
            828_0  COME_FROM           782  '782'

 L. 239       828  LOAD_FAST                'modlist'
              830  LOAD_METHOD              append

 L. 240       832  LOAD_GLOBAL              ACTION2MODTYPE
              834  LOAD_FAST                'action'
              836  BINARY_SUBSCR    

 L. 241       838  LOAD_FAST                'group_member_attrtype'
              840  LOAD_METHOD              encode
              842  LOAD_STR                 'ascii'
              844  CALL_METHOD_1         1  ''

 L. 242       846  LOAD_FAST                'member_value'
              848  BUILD_LIST_1          1 

 L. 239       850  BUILD_TUPLE_3         3 
              852  CALL_METHOD_1         1  ''
              854  POP_TOP          
          856_858  JUMP_BACK           706  'to 706'

 L. 245       860  LOAD_FAST                'modlist'
          862_864  POP_JUMP_IF_FALSE   674  'to 674'

 L. 246       866  SETUP_FINALLY       886  'to 886'

 L. 247       868  LOAD_DEREF               'app'
              870  LOAD_ATTR                ls
              872  LOAD_METHOD              modify
              874  LOAD_FAST                'group_dn'
              876  LOAD_FAST                'modlist'
              878  CALL_METHOD_2         2  ''
              880  POP_TOP          
              882  POP_BLOCK        
              884  JUMP_FORWARD        946  'to 946'
            886_0  COME_FROM_FINALLY   866  '866'

 L. 248       886  DUP_TOP          
              888  LOAD_GLOBAL              ldap0
              890  LOAD_ATTR                LDAPError
              892  COMPARE_OP               exception-match
          894_896  POP_JUMP_IF_FALSE   944  'to 944'
              898  POP_TOP          
              900  STORE_FAST               'e'
              902  POP_TOP          
              904  SETUP_FINALLY       932  'to 932'

 L. 249       906  LOAD_FAST                'ldaperror_entries'
              908  LOAD_METHOD              append

 L. 250       910  LOAD_FAST                'group_dn'

 L. 251       912  LOAD_FAST                'modlist'

 L. 252       914  LOAD_DEREF               'app'
              916  LOAD_METHOD              ldap_error_msg
              918  LOAD_FAST                'e'
              920  CALL_METHOD_1         1  ''

 L. 249       922  BUILD_TUPLE_3         3 
              924  CALL_METHOD_1         1  ''
              926  POP_TOP          
              928  POP_BLOCK        
              930  BEGIN_FINALLY    
            932_0  COME_FROM_FINALLY   904  '904'
              932  LOAD_CONST               None
              934  STORE_FAST               'e'
              936  DELETE_FAST              'e'
              938  END_FINALLY      
              940  POP_EXCEPT       
              942  JUMP_BACK           674  'to 674'
            944_0  COME_FROM           894  '894'
              944  END_FINALLY      
            946_0  COME_FROM           884  '884'

 L. 255       946  LOAD_FAST                'successful_group_mods'
              948  LOAD_METHOD              append
              950  LOAD_FAST                'group_dn'
              952  LOAD_FAST                'modlist'
              954  BUILD_TUPLE_2         2 
              956  CALL_METHOD_1         1  ''
              958  POP_TOP          
          960_962  JUMP_BACK           674  'to 674'
          964_966  JUMP_BACK           650  'to 650'

 L. 257       968  LOAD_FAST                'successful_group_mods'
          970_972  POP_JUMP_IF_FALSE  1138  'to 1138'

 L. 258       974  LOAD_LISTCOMP            '<code_object <listcomp>>'
              976  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              978  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 260       980  LOAD_FAST                'successful_group_mods'

 L. 258       982  GET_ITER         
              984  CALL_FUNCTION_1       1  ''
              986  STORE_FAST               'group_add_list'

 L. 263       988  LOAD_LISTCOMP            '<code_object <listcomp>>'
              990  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              992  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 265       994  LOAD_FAST                'successful_group_mods'

 L. 263       996  GET_ITER         
              998  CALL_FUNCTION_1       1  ''
             1000  STORE_FAST               'group_remove_list'

 L. 268      1002  LOAD_STR                 '<p class="SuccessMessage">Changed group membership</p>'
             1004  BUILD_LIST_1          1 
             1006  STORE_FAST               'info_msg_list'

 L. 269      1008  LOAD_FAST                'group_add_list'
         1010_1012  POP_JUMP_IF_FALSE  1068  'to 1068'

 L. 270      1014  LOAD_FAST                'info_msg_list'
             1016  LOAD_METHOD              append
             1018  LOAD_STR                 '<p>Added to:</p>'
             1020  CALL_METHOD_1         1  ''
             1022  POP_TOP          

 L. 271      1024  LOAD_FAST                'info_msg_list'
             1026  LOAD_METHOD              append
             1028  LOAD_STR                 '<ul>'
             1030  CALL_METHOD_1         1  ''
             1032  POP_TOP          

 L. 272      1034  LOAD_FAST                'info_msg_list'
             1036  LOAD_METHOD              extend
             1038  LOAD_CLOSURE             'app'
             1040  BUILD_TUPLE_1         1 
             1042  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1044  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1046  MAKE_FUNCTION_8          'closure'

 L. 274      1048  LOAD_FAST                'group_add_list'

 L. 272      1050  GET_ITER         
             1052  CALL_FUNCTION_1       1  ''
             1054  CALL_METHOD_1         1  ''
             1056  POP_TOP          

 L. 276      1058  LOAD_FAST                'info_msg_list'
             1060  LOAD_METHOD              append
             1062  LOAD_STR                 '</ul>'
             1064  CALL_METHOD_1         1  ''
             1066  POP_TOP          
           1068_0  COME_FROM          1010  '1010'

 L. 277      1068  LOAD_FAST                'group_remove_list'
         1070_1072  POP_JUMP_IF_FALSE  1128  'to 1128'

 L. 278      1074  LOAD_FAST                'info_msg_list'
             1076  LOAD_METHOD              append
             1078  LOAD_STR                 '<p>Removed from:</p>'
             1080  CALL_METHOD_1         1  ''
             1082  POP_TOP          

 L. 279      1084  LOAD_FAST                'info_msg_list'
             1086  LOAD_METHOD              append
             1088  LOAD_STR                 '<ul>'
             1090  CALL_METHOD_1         1  ''
             1092  POP_TOP          

 L. 280      1094  LOAD_FAST                'info_msg_list'
             1096  LOAD_METHOD              extend
             1098  LOAD_CLOSURE             'app'
             1100  BUILD_TUPLE_1         1 
             1102  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1104  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1106  MAKE_FUNCTION_8          'closure'

 L. 282      1108  LOAD_FAST                'group_remove_list'

 L. 280      1110  GET_ITER         
             1112  CALL_FUNCTION_1       1  ''
             1114  CALL_METHOD_1         1  ''
             1116  POP_TOP          

 L. 284      1118  LOAD_FAST                'info_msg_list'
             1120  LOAD_METHOD              append
             1122  LOAD_STR                 '</ul>'
             1124  CALL_METHOD_1         1  ''
             1126  POP_TOP          
           1128_0  COME_FROM          1070  '1070'

 L. 285      1128  LOAD_STR                 '\n'
             1130  LOAD_METHOD              join
             1132  LOAD_FAST                'info_msg_list'
             1134  CALL_METHOD_1         1  ''
             1136  STORE_FAST               'info_msg'
           1138_0  COME_FROM           970  '970'

 L. 287      1138  LOAD_FAST                'ldaperror_entries'
         1140_1142  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 288      1144  LOAD_FAST                'error_msg'
             1146  BUILD_LIST_1          1 
             1148  STORE_FAST               'error_msg_list'

 L. 289      1150  LOAD_FAST                'error_msg_list'
             1152  LOAD_METHOD              extend
             1154  LOAD_CLOSURE             'app'
             1156  BUILD_TUPLE_1         1 
             1158  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1160  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1162  MAKE_FUNCTION_8          'closure'

 L. 294      1164  LOAD_FAST                'ldaperror_entries'

 L. 289      1166  GET_ITER         
             1168  CALL_FUNCTION_1       1  ''
             1170  CALL_METHOD_1         1  ''
             1172  POP_TOP          

 L. 296      1174  LOAD_STR                 '<br>'
             1176  LOAD_METHOD              join
             1178  LOAD_FAST                'error_msg_list'
             1180  CALL_METHOD_1         1  ''
             1182  STORE_FAST               'error_msg'
           1184_0  COME_FROM          1140  '1140'
           1184_1  COME_FROM           634  '634'

 L. 302      1184  LOAD_STR                 '(|%s)'

 L. 303      1186  LOAD_STR                 ''
             1188  LOAD_METHOD              join

 L. 304      1190  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1192  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1194  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 306      1196  LOAD_FAST                'filter_components'

 L. 304      1198  GET_ITER         
             1200  CALL_FUNCTION_1       1  ''

 L. 303      1202  CALL_METHOD_1         1  ''

 L. 302      1204  BINARY_MODULO    
             1206  STORE_FAST               'remove_group_filterstr'

 L. 311      1208  BUILD_MAP_0           0 
             1210  STORE_DEREF              'remove_groups_dict'

 L. 313      1212  SETUP_FINALLY      1314  'to 1314'

 L. 314      1214  LOAD_DEREF               'app'
             1216  LOAD_ATTR                ls
             1218  LOAD_ATTR                l
             1220  LOAD_ATTR                search

 L. 315      1222  LOAD_GLOBAL              str
             1224  LOAD_FAST                'group_search_root'
             1226  CALL_FUNCTION_1       1  ''

 L. 316      1228  LOAD_GLOBAL              ldap0
             1230  LOAD_ATTR                SCOPE_SUBTREE

 L. 317      1232  LOAD_FAST                'remove_group_filterstr'

 L. 318      1234  LOAD_GLOBAL              REQUESTED_GROUP_ATTRS

 L. 314      1236  LOAD_CONST               ('attrlist',)
             1238  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1240  STORE_FAST               'msg_id'

 L. 320      1242  LOAD_DEREF               'app'
             1244  LOAD_ATTR                ls
             1246  LOAD_ATTR                l
             1248  LOAD_METHOD              results
             1250  LOAD_FAST                'msg_id'
             1252  CALL_METHOD_1         1  ''
             1254  GET_ITER         
             1256  FOR_ITER           1310  'to 1310'
             1258  STORE_FAST               'res'

 L. 321      1260  LOAD_FAST                'res'
             1262  LOAD_ATTR                rdata
             1264  GET_ITER         
           1266_0  COME_FROM          1278  '1278'
             1266  FOR_ITER           1306  'to 1306'
             1268  STORE_FAST               'sre'

 L. 322      1270  LOAD_GLOBAL              isinstance
             1272  LOAD_FAST                'sre'
             1274  LOAD_GLOBAL              SearchResultEntry
             1276  CALL_FUNCTION_2       2  ''
         1278_1280  POP_JUMP_IF_FALSE  1266  'to 1266'

 L. 323      1282  LOAD_GLOBAL              ldap0
             1284  LOAD_ATTR                cidict
             1286  LOAD_METHOD              CIDict
             1288  LOAD_FAST                'sre'
             1290  LOAD_ATTR                entry_s
             1292  CALL_METHOD_1         1  ''
             1294  LOAD_DEREF               'remove_groups_dict'
             1296  LOAD_FAST                'sre'
             1298  LOAD_ATTR                dn_s
             1300  STORE_SUBSCR     
         1302_1304  JUMP_BACK          1266  'to 1266'
         1306_1308  JUMP_BACK          1256  'to 1256'
             1310  POP_BLOCK        
             1312  JUMP_FORWARD       1374  'to 1374'
           1314_0  COME_FROM_FINALLY  1212  '1212'

 L. 324      1314  DUP_TOP          
             1316  LOAD_GLOBAL              ldap0
             1318  LOAD_ATTR                NO_SUCH_OBJECT
             1320  COMPARE_OP               exception-match
         1322_1324  POP_JUMP_IF_FALSE  1340  'to 1340'
             1326  POP_TOP          
             1328  POP_TOP          
             1330  POP_TOP          

 L. 325      1332  LOAD_STR                 'No such object! Did you choose a valid search base?'
             1334  STORE_FAST               'error_msg'
             1336  POP_EXCEPT       
             1338  JUMP_FORWARD       1374  'to 1374'
           1340_0  COME_FROM          1322  '1322'

 L. 326      1340  DUP_TOP          
             1342  LOAD_GLOBAL              ldap0
             1344  LOAD_ATTR                SIZELIMIT_EXCEEDED
             1346  LOAD_GLOBAL              ldap0
             1348  LOAD_ATTR                TIMELIMIT_EXCEEDED
             1350  BUILD_TUPLE_2         2 
             1352  COMPARE_OP               exception-match
         1354_1356  POP_JUMP_IF_FALSE  1372  'to 1372'
             1358  POP_TOP          
             1360  POP_TOP          
             1362  POP_TOP          

 L. 327      1364  LOAD_STR                 'Size or time limit exceeded while searching group entries!'
             1366  STORE_FAST               'error_msg'
             1368  POP_EXCEPT       
             1370  JUMP_FORWARD       1374  'to 1374'
           1372_0  COME_FROM          1354  '1354'
             1372  END_FINALLY      
           1374_0  COME_FROM          1370  '1370'
           1374_1  COME_FROM          1338  '1338'
           1374_2  COME_FROM          1312  '1312'

 L. 329      1374  LOAD_FAST                'all_groups_dict'
             1376  LOAD_METHOD              update
             1378  LOAD_DEREF               'remove_groups_dict'
             1380  CALL_METHOD_1         1  ''
             1382  POP_TOP          

 L. 331      1384  LOAD_GLOBAL              sorted
             1386  LOAD_DEREF               'remove_groups_dict'
             1388  LOAD_METHOD              keys
             1390  CALL_METHOD_0         0  ''
             1392  LOAD_GLOBAL              str
             1394  LOAD_ATTR                lower
             1396  LOAD_CONST               ('key',)
             1398  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1400  STORE_FAST               'remove_groups'

 L. 333      1402  LOAD_FAST                'all_groups_dict'
         1404_1406  POP_JUMP_IF_TRUE   1412  'to 1412'

 L. 334      1408  LOAD_STR                 'No group entries found. Did you choose a valid search base or valid name?'
             1410  STORE_FAST               'info_msg'
           1412_0  COME_FROM          1404  '1404'

 L. 340      1412  LOAD_CLOSURE             'remove_groups_dict'
             1414  BUILD_TUPLE_1         1 
             1416  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1418  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1420  MAKE_FUNCTION_8          'closure'

 L. 342      1422  LOAD_FAST                'all_group_entries'

 L. 340      1424  GET_ITER         
             1426  CALL_FUNCTION_1       1  ''
             1428  STORE_FAST               'add_groups'

 L. 350      1430  LOAD_GLOBAL              web2ldap
             1432  LOAD_ATTR                app
             1434  LOAD_ATTR                gui
             1436  LOAD_ATTR                top_section

 L. 351      1438  LOAD_DEREF               'app'

 L. 352      1440  LOAD_STR                 'Group membership'

 L. 353      1442  LOAD_GLOBAL              web2ldap
             1444  LOAD_ATTR                app
             1446  LOAD_ATTR                gui
             1448  LOAD_METHOD              main_menu
             1450  LOAD_DEREF               'app'
             1452  CALL_METHOD_1         1  ''

 L. 354      1454  BUILD_LIST_0          0 

 L. 350      1456  LOAD_CONST               ('context_menu_list',)
             1458  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1460  POP_TOP          

 L. 357      1462  LOAD_GLOBAL              web2ldap
             1464  LOAD_ATTR                app
             1466  LOAD_ATTR                gui
             1468  LOAD_ATTR                search_root_field

 L. 358      1470  LOAD_DEREF               'app'

 L. 359      1472  LOAD_STR                 'groupadm_searchroot'

 L. 360      1474  LOAD_GLOBAL              str
             1476  LOAD_FAST                'group_search_root'
             1478  CALL_FUNCTION_1       1  ''

 L. 357      1480  LOAD_CONST               ('name', 'default')
             1482  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1484  STORE_FAST               'group_search_root_field'

 L. 363      1486  LOAD_FAST                'error_msg'
         1488_1490  POP_JUMP_IF_FALSE  1508  'to 1508'

 L. 364      1492  LOAD_DEREF               'app'
             1494  LOAD_ATTR                outf
             1496  LOAD_METHOD              write
             1498  LOAD_STR                 '<p class="ErrorMessage">%s</p>'
             1500  LOAD_FAST                'error_msg'
             1502  BINARY_MODULO    
             1504  CALL_METHOD_1         1  ''
             1506  POP_TOP          
           1508_0  COME_FROM          1488  '1488'

 L. 365      1508  LOAD_FAST                'info_msg'
         1510_1512  POP_JUMP_IF_FALSE  1530  'to 1530'

 L. 366      1514  LOAD_DEREF               'app'
             1516  LOAD_ATTR                outf
             1518  LOAD_METHOD              write
             1520  LOAD_STR                 '<p class="InfoMessage">%s</p>'
             1522  LOAD_FAST                'info_msg'
             1524  BINARY_MODULO    
             1526  CALL_METHOD_1         1  ''
             1528  POP_TOP          
           1530_0  COME_FROM          1510  '1510'

 L. 368      1530  LOAD_FAST                'all_groups_dict'
         1532_1534  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 370      1536  LOAD_DEREF               'app'
             1538  LOAD_METHOD              cfg_param
             1540  LOAD_STR                 'groupadm_optgroup_bounds'
             1542  LOAD_CONST               (1, None)
             1544  CALL_METHOD_2         2  ''
             1546  STORE_FAST               'optgroup_bounds'

 L. 372      1548  LOAD_DEREF               'app'
             1550  LOAD_ATTR                outf
             1552  LOAD_METHOD              write

 L. 373      1554  LOAD_STR                 '\n            %s\n%s\n%s\n\n              <input type="submit" value="Change Group Membership">\n              <table summary="Group select fields">\n                <tr>\n                  <td width="50%%">Add to...</td>\n                  <td width="50%%">Remove from...</td>\n                </tr>\n                <tr>\n                  <td width="50%%">%s</td>\n                  <td width="50%%">%s</td>\n                </tr>\n              </table>\n            </form>\n            '

 L. 389      1556  LOAD_DEREF               'app'
             1558  LOAD_METHOD              begin_form
             1560  LOAD_STR                 'groupadm'
             1562  LOAD_STR                 'POST'
             1564  CALL_METHOD_2         2  ''

 L. 390      1566  LOAD_DEREF               'app'
             1568  LOAD_ATTR                form
             1570  LOAD_METHOD              hiddenFieldHTML
             1572  LOAD_STR                 'dn'
             1574  LOAD_DEREF               'app'
             1576  LOAD_ATTR                dn
             1578  LOAD_STR                 ''
             1580  CALL_METHOD_3         3  ''

 L. 391      1582  LOAD_DEREF               'app'
             1584  LOAD_ATTR                form
             1586  LOAD_METHOD              hiddenFieldHTML
             1588  LOAD_STR                 'groupadm_searchroot'
             1590  LOAD_GLOBAL              str
             1592  LOAD_FAST                'group_search_root'
             1594  CALL_FUNCTION_1       1  ''
             1596  LOAD_STR                 ''
             1598  CALL_METHOD_3         3  ''

 L. 392      1600  LOAD_GLOBAL              group_select_field

 L. 393      1602  LOAD_DEREF               'app'

 L. 394      1604  LOAD_FAST                'all_groups_dict'

 L. 395      1606  LOAD_STR                 'groupadm_add'

 L. 396      1608  LOAD_STR                 'Groups to add to'

 L. 397      1610  LOAD_FAST                'group_search_root'

 L. 398      1612  LOAD_FAST                'add_groups'

 L. 399      1614  LOAD_FAST                'optgroup_bounds'

 L. 392      1616  CALL_FUNCTION_7       7  ''

 L. 401      1618  LOAD_GLOBAL              group_select_field

 L. 402      1620  LOAD_DEREF               'app'

 L. 403      1622  LOAD_DEREF               'remove_groups_dict'

 L. 404      1624  LOAD_STR                 'groupadm_remove'

 L. 405      1626  LOAD_STR                 'Groups to remove from'

 L. 406      1628  LOAD_FAST                'group_search_root'

 L. 407      1630  LOAD_FAST                'remove_groups'

 L. 408      1632  LOAD_FAST                'optgroup_bounds'

 L. 401      1634  CALL_FUNCTION_7       7  ''

 L. 387      1636  BUILD_TUPLE_5         5 

 L. 373      1638  BINARY_MODULO    

 L. 372      1640  CALL_METHOD_1         1  ''
             1642  POP_TOP          
           1644_0  COME_FROM          1532  '1532'

 L. 413      1644  LOAD_DEREF               'app'
             1646  LOAD_ATTR                outf
             1648  LOAD_METHOD              write

 L. 414      1650  LOAD_STR                 '%s\n%s\n\n          <p><input type="submit" value="List"> group entries below: %s.</p>\n          <p>where group name contains: %s</p>\n          <p>List %s groups.</p>\n        </form>\n        '

 L. 421      1652  LOAD_DEREF               'app'
             1654  LOAD_METHOD              begin_form
             1656  LOAD_STR                 'groupadm'
             1658  LOAD_STR                 'GET'
             1660  CALL_METHOD_2         2  ''

 L. 422      1662  LOAD_DEREF               'app'
             1664  LOAD_ATTR                form
             1666  LOAD_METHOD              hiddenFieldHTML
             1668  LOAD_STR                 'dn'
             1670  LOAD_DEREF               'app'
             1672  LOAD_ATTR                dn
             1674  LOAD_STR                 ''
             1676  CALL_METHOD_3         3  ''

 L. 423      1678  LOAD_FAST                'group_search_root_field'
             1680  LOAD_ATTR                input_html
             1682  LOAD_STR                 'Search root for searching group entries'
             1684  LOAD_CONST               ('title',)
             1686  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 424      1688  LOAD_DEREF               'app'
             1690  LOAD_ATTR                form
             1692  LOAD_ATTR                field
             1694  LOAD_STR                 'groupadm_name'
             1696  BINARY_SUBSCR    
             1698  LOAD_METHOD              input_html
             1700  CALL_METHOD_0         0  ''

 L. 425      1702  LOAD_DEREF               'app'
             1704  LOAD_ATTR                form
             1706  LOAD_ATTR                field
             1708  LOAD_STR                 'groupadm_view'
             1710  BINARY_SUBSCR    
             1712  LOAD_ATTR                input_html

 L. 426      1714  LOAD_STR                 'Group entries list'

 L. 427      1716  LOAD_GLOBAL              str
             1718  LOAD_FAST                'groupadm_view'
             1720  CALL_FUNCTION_1       1  ''

 L. 425      1722  LOAD_CONST               ('title', 'default')
             1724  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 419      1726  BUILD_TUPLE_5         5 

 L. 414      1728  BINARY_MODULO    

 L. 413      1730  CALL_METHOD_1         1  ''
             1732  POP_TOP          

 L. 432      1734  LOAD_FAST                'groupadm_view'
         1736_1738  POP_JUMP_IF_FALSE  1890  'to 1890'

 L. 433      1740  LOAD_DEREF               'app'
             1742  LOAD_ATTR                outf
             1744  LOAD_METHOD              write
             1746  LOAD_STR                 '<dl>\n'
             1748  CALL_METHOD_1         1  ''
             1750  POP_TOP          

 L. 435      1752  LOAD_FAST                'remove_groups'
             1754  LOAD_FAST                'all_group_entries'
             1756  LOAD_CONST               (1, 2)
             1758  BUILD_CONST_KEY_MAP_2     2 
             1760  LOAD_FAST                'groupadm_view'
             1762  BINARY_SUBSCR    
             1764  GET_ITER         
             1766  FOR_ITER           1878  'to 1878'
             1768  STORE_FAST               'group_dn'

 L. 436      1770  LOAD_FAST                'all_groups_dict'
             1772  LOAD_FAST                'group_dn'
             1774  BINARY_SUBSCR    
             1776  STORE_FAST               'group_entry'

 L. 437      1778  LOAD_DEREF               'app'
             1780  LOAD_ATTR                outf
             1782  LOAD_METHOD              write
             1784  LOAD_STR                 '<dt>%s | %s</dt>\n<dd>%s<br>\n(%s)<br>\n%s</dd>\n'

 L. 438      1786  LOAD_STR                 ', '
             1788  LOAD_METHOD              join
             1790  LOAD_FAST                'group_entry'
             1792  LOAD_METHOD              get
             1794  LOAD_STR                 'cn'
             1796  BUILD_LIST_0          0 
             1798  CALL_METHOD_2         2  ''
             1800  CALL_METHOD_1         1  ''

 L. 439      1802  LOAD_DEREF               'app'
             1804  LOAD_ATTR                anchor

 L. 440      1806  LOAD_STR                 'read'

 L. 440      1808  LOAD_STR                 'Read'

 L. 441      1810  LOAD_STR                 'dn'
             1812  LOAD_FAST                'group_dn'
             1814  BUILD_TUPLE_2         2 
             1816  BUILD_LIST_1          1 

 L. 442      1818  LOAD_STR                 'Display group entry'

 L. 439      1820  LOAD_CONST               ('title',)
             1822  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 444      1824  LOAD_DEREF               'app'
             1826  LOAD_ATTR                form
             1828  LOAD_METHOD              utf2display
             1830  LOAD_FAST                'group_dn'
             1832  CALL_METHOD_1         1  ''

 L. 445      1834  LOAD_STR                 ', '
             1836  LOAD_METHOD              join
             1838  LOAD_FAST                'group_entry'
             1840  LOAD_METHOD              get
             1842  LOAD_STR                 'objectClass'
             1844  BUILD_LIST_0          0 
             1846  CALL_METHOD_2         2  ''
             1848  CALL_METHOD_1         1  ''

 L. 446      1850  LOAD_STR                 '<br>'
             1852  LOAD_METHOD              join
             1854  LOAD_FAST                'group_entry'
             1856  LOAD_METHOD              get
             1858  LOAD_STR                 'description'
             1860  BUILD_LIST_0          0 
             1862  CALL_METHOD_2         2  ''
             1864  CALL_METHOD_1         1  ''

 L. 437      1866  BUILD_TUPLE_5         5 
             1868  BINARY_MODULO    
             1870  CALL_METHOD_1         1  ''
             1872  POP_TOP          
         1874_1876  JUMP_BACK          1766  'to 1766'

 L. 448      1878  LOAD_DEREF               'app'
             1880  LOAD_ATTR                outf
             1882  LOAD_METHOD              write
             1884  LOAD_STR                 '</dl>\n'
             1886  CALL_METHOD_1         1  ''
             1888  POP_TOP          
           1890_0  COME_FROM          1736  '1736'

 L. 450      1890  LOAD_GLOBAL              web2ldap
             1892  LOAD_ATTR                app
             1894  LOAD_ATTR                gui
             1896  LOAD_METHOD              footer
             1898  LOAD_DEREF               'app'
             1900  CALL_METHOD_1         1  ''
             1902  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 324