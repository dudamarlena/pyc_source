# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/groupadm.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 16761 bytes
"""
web2ldap.app.groupadm: add/delete user entry to/from group entries

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

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
                optgroup_list.extend(sorted([dn for dn in optgroup_dict.keys() if dn is not None if dn != colgroup_memberdn if dn != colgroup_authzdn],
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

 L. 207   634_636  POP_JUMP_IF_FALSE  1188  'to 1188'
            638_0  COME_FROM           620  '620'

 L. 210       638  BUILD_LIST_0          0 
              640  STORE_FAST               'ldaperror_entries'

 L. 211       642  BUILD_LIST_0          0 
              644  STORE_FAST               'successful_group_mods'

 L. 213       646  LOAD_GLOBAL              ACTION2MODTYPE
              648  LOAD_METHOD              keys
              650  CALL_METHOD_0         0  ''
              652  GET_ITER         
          654_656  FOR_ITER            972  'to 972'
              658  STORE_FAST               'action'

 L. 215       660  LOAD_DEREF               'app'
              662  LOAD_ATTR                form
              664  LOAD_METHOD              getInputValue
              666  LOAD_STR                 'groupadm_%s'
              668  LOAD_FAST                'action'
              670  BINARY_MODULO    
              672  BUILD_LIST_0          0 
              674  CALL_METHOD_2         2  ''
              676  GET_ITER         
            678_0  COME_FROM           866  '866'
          678_680  FOR_ITER            968  'to 968'
              682  STORE_FAST               'action_group_dn'

 L. 216       684  LOAD_FAST                'action_group_dn'
              686  STORE_FAST               'group_dn'

 L. 217       688  LOAD_FAST                'group_dn'
              690  LOAD_FAST                'all_groups_dict'
              692  COMPARE_OP               not-in
          694_696  POP_JUMP_IF_FALSE   702  'to 702'

 L. 220   698_700  JUMP_BACK           678  'to 678'
            702_0  COME_FROM           694  '694'

 L. 221       702  BUILD_LIST_0          0 
              704  STORE_FAST               'modlist'

 L. 222       706  LOAD_FAST                'groupadm_defs_keys'
              708  GET_ITER         
            710_0  COME_FROM           746  '746'
              710  FOR_ITER            864  'to 864'
              712  STORE_FAST               'oc'

 L. 223       714  LOAD_FAST                'oc'
              716  LOAD_METHOD              lower
              718  CALL_METHOD_0         0  ''
              720  LOAD_LISTCOMP            '<code_object <listcomp>>'
              722  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              724  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 225       726  LOAD_FAST                'all_groups_dict'
              728  LOAD_FAST                'group_dn'
              730  BINARY_SUBSCR    
              732  LOAD_METHOD              get
              734  LOAD_STR                 'objectClass'
              736  BUILD_LIST_0          0 
              738  CALL_METHOD_2         2  ''

 L. 223       740  GET_ITER         
              742  CALL_FUNCTION_1       1  ''
              744  COMPARE_OP               in
          746_748  POP_JUMP_IF_FALSE   710  'to 710'

 L. 227       750  LOAD_FAST                'groupadm_defs'
              752  LOAD_FAST                'oc'
              754  BINARY_SUBSCR    
              756  LOAD_CONST               0
              758  LOAD_CONST               2
              760  BUILD_SLICE_2         2 
              762  BINARY_SUBSCR    
              764  UNPACK_SEQUENCE_2     2 
              766  STORE_FAST               'group_member_attrtype'
              768  STORE_FAST               'user_entry_attrtype'

 L. 228       770  LOAD_FAST                'user_entry_attrtype'
              772  LOAD_CONST               None
              774  COMPARE_OP               is
          776_778  POP_JUMP_IF_FALSE   788  'to 788'

 L. 229       780  LOAD_DEREF               'app'
              782  LOAD_ATTR                ldap_dn
              784  STORE_FAST               'member_value'
              786  JUMP_FORWARD        832  'to 832'
            788_0  COME_FROM           776  '776'

 L. 231       788  LOAD_FAST                'user_entry_attrtype'
              790  LOAD_FAST                'user_entry'
              792  COMPARE_OP               not-in
          794_796  POP_JUMP_IF_FALSE   820  'to 820'

 L. 232       798  LOAD_GLOBAL              web2ldap
              800  LOAD_ATTR                app
              802  LOAD_ATTR                core
              804  LOAD_METHOD              ErrorExit

 L. 233       806  LOAD_STR                 'Object class %s requires attribute %s in group entry.'

 L. 234       808  LOAD_FAST                'oc'

 L. 235       810  LOAD_FAST                'user_entry_attrtype'

 L. 233       812  BUILD_TUPLE_2         2 
              814  BINARY_MODULO    

 L. 232       816  CALL_METHOD_1         1  ''
              818  RAISE_VARARGS_1       1  'exception instance'
            820_0  COME_FROM           794  '794'

 L. 238       820  LOAD_FAST                'user_entry'
              822  LOAD_FAST                'user_entry_attrtype'
              824  BINARY_SUBSCR    
              826  LOAD_CONST               0
              828  BINARY_SUBSCR    
              830  STORE_FAST               'member_value'
            832_0  COME_FROM           786  '786'

 L. 239       832  LOAD_FAST                'modlist'
              834  LOAD_METHOD              append

 L. 240       836  LOAD_GLOBAL              ACTION2MODTYPE
              838  LOAD_FAST                'action'
              840  BINARY_SUBSCR    

 L. 241       842  LOAD_FAST                'group_member_attrtype'
              844  LOAD_METHOD              encode
              846  LOAD_STR                 'ascii'
              848  CALL_METHOD_1         1  ''

 L. 242       850  LOAD_FAST                'member_value'
              852  BUILD_LIST_1          1 

 L. 239       854  BUILD_TUPLE_3         3 
              856  CALL_METHOD_1         1  ''
              858  POP_TOP          
          860_862  JUMP_BACK           710  'to 710'

 L. 245       864  LOAD_FAST                'modlist'
          866_868  POP_JUMP_IF_FALSE   678  'to 678'

 L. 246       870  SETUP_FINALLY       890  'to 890'

 L. 247       872  LOAD_DEREF               'app'
              874  LOAD_ATTR                ls
              876  LOAD_METHOD              modify
              878  LOAD_FAST                'group_dn'
              880  LOAD_FAST                'modlist'
              882  CALL_METHOD_2         2  ''
              884  POP_TOP          
              886  POP_BLOCK        
              888  JUMP_FORWARD        950  'to 950'
            890_0  COME_FROM_FINALLY   870  '870'

 L. 248       890  DUP_TOP          
              892  LOAD_GLOBAL              ldap0
              894  LOAD_ATTR                LDAPError
              896  COMPARE_OP               exception-match
          898_900  POP_JUMP_IF_FALSE   948  'to 948'
              902  POP_TOP          
              904  STORE_FAST               'e'
              906  POP_TOP          
              908  SETUP_FINALLY       936  'to 936'

 L. 249       910  LOAD_FAST                'ldaperror_entries'
              912  LOAD_METHOD              append

 L. 250       914  LOAD_FAST                'group_dn'

 L. 251       916  LOAD_FAST                'modlist'

 L. 252       918  LOAD_DEREF               'app'
              920  LOAD_METHOD              ldap_error_msg
              922  LOAD_FAST                'e'
              924  CALL_METHOD_1         1  ''

 L. 249       926  BUILD_TUPLE_3         3 
              928  CALL_METHOD_1         1  ''
              930  POP_TOP          
              932  POP_BLOCK        
              934  BEGIN_FINALLY    
            936_0  COME_FROM_FINALLY   908  '908'
              936  LOAD_CONST               None
              938  STORE_FAST               'e'
              940  DELETE_FAST              'e'
              942  END_FINALLY      
              944  POP_EXCEPT       
              946  JUMP_BACK           678  'to 678'
            948_0  COME_FROM           898  '898'
              948  END_FINALLY      
            950_0  COME_FROM           888  '888'

 L. 255       950  LOAD_FAST                'successful_group_mods'
              952  LOAD_METHOD              append
              954  LOAD_FAST                'group_dn'
              956  LOAD_FAST                'modlist'
              958  BUILD_TUPLE_2         2 
              960  CALL_METHOD_1         1  ''
              962  POP_TOP          
          964_966  JUMP_BACK           678  'to 678'
          968_970  JUMP_BACK           654  'to 654'

 L. 257       972  LOAD_FAST                'successful_group_mods'
          974_976  POP_JUMP_IF_FALSE  1142  'to 1142'

 L. 258       978  LOAD_LISTCOMP            '<code_object <listcomp>>'
              980  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              982  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 260       984  LOAD_FAST                'successful_group_mods'

 L. 258       986  GET_ITER         
              988  CALL_FUNCTION_1       1  ''
              990  STORE_FAST               'group_add_list'

 L. 263       992  LOAD_LISTCOMP            '<code_object <listcomp>>'
              994  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
              996  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 265       998  LOAD_FAST                'successful_group_mods'

 L. 263      1000  GET_ITER         
             1002  CALL_FUNCTION_1       1  ''
             1004  STORE_FAST               'group_remove_list'

 L. 268      1006  LOAD_STR                 '<p class="SuccessMessage">Changed group membership</p>'
             1008  BUILD_LIST_1          1 
             1010  STORE_FAST               'info_msg_list'

 L. 269      1012  LOAD_FAST                'group_add_list'
         1014_1016  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 270      1018  LOAD_FAST                'info_msg_list'
             1020  LOAD_METHOD              append
             1022  LOAD_STR                 '<p>Added to:</p>'
             1024  CALL_METHOD_1         1  ''
             1026  POP_TOP          

 L. 271      1028  LOAD_FAST                'info_msg_list'
             1030  LOAD_METHOD              append
             1032  LOAD_STR                 '<ul>'
             1034  CALL_METHOD_1         1  ''
             1036  POP_TOP          

 L. 272      1038  LOAD_FAST                'info_msg_list'
             1040  LOAD_METHOD              extend
             1042  LOAD_CLOSURE             'app'
             1044  BUILD_TUPLE_1         1 
             1046  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1048  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1050  MAKE_FUNCTION_8          'closure'

 L. 274      1052  LOAD_FAST                'group_add_list'

 L. 272      1054  GET_ITER         
             1056  CALL_FUNCTION_1       1  ''
             1058  CALL_METHOD_1         1  ''
             1060  POP_TOP          

 L. 276      1062  LOAD_FAST                'info_msg_list'
             1064  LOAD_METHOD              append
             1066  LOAD_STR                 '</ul>'
             1068  CALL_METHOD_1         1  ''
             1070  POP_TOP          
           1072_0  COME_FROM          1014  '1014'

 L. 277      1072  LOAD_FAST                'group_remove_list'
         1074_1076  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 278      1078  LOAD_FAST                'info_msg_list'
             1080  LOAD_METHOD              append
             1082  LOAD_STR                 '<p>Removed from:</p>'
             1084  CALL_METHOD_1         1  ''
             1086  POP_TOP          

 L. 279      1088  LOAD_FAST                'info_msg_list'
             1090  LOAD_METHOD              append
             1092  LOAD_STR                 '<ul>'
             1094  CALL_METHOD_1         1  ''
             1096  POP_TOP          

 L. 280      1098  LOAD_FAST                'info_msg_list'
             1100  LOAD_METHOD              extend
             1102  LOAD_CLOSURE             'app'
             1104  BUILD_TUPLE_1         1 
             1106  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1108  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1110  MAKE_FUNCTION_8          'closure'

 L. 282      1112  LOAD_FAST                'group_remove_list'

 L. 280      1114  GET_ITER         
             1116  CALL_FUNCTION_1       1  ''
             1118  CALL_METHOD_1         1  ''
             1120  POP_TOP          

 L. 284      1122  LOAD_FAST                'info_msg_list'
             1124  LOAD_METHOD              append
             1126  LOAD_STR                 '</ul>'
             1128  CALL_METHOD_1         1  ''
             1130  POP_TOP          
           1132_0  COME_FROM          1074  '1074'

 L. 285      1132  LOAD_STR                 '\n'
             1134  LOAD_METHOD              join
             1136  LOAD_FAST                'info_msg_list'
             1138  CALL_METHOD_1         1  ''
             1140  STORE_FAST               'info_msg'
           1142_0  COME_FROM           974  '974'

 L. 287      1142  LOAD_FAST                'ldaperror_entries'
         1144_1146  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 288      1148  LOAD_FAST                'error_msg'
             1150  BUILD_LIST_1          1 
             1152  STORE_FAST               'error_msg_list'

 L. 289      1154  LOAD_FAST                'error_msg_list'
             1156  LOAD_METHOD              extend
             1158  LOAD_CLOSURE             'app'
             1160  BUILD_TUPLE_1         1 
             1162  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1164  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1166  MAKE_FUNCTION_8          'closure'

 L. 294      1168  LOAD_FAST                'ldaperror_entries'

 L. 289      1170  GET_ITER         
             1172  CALL_FUNCTION_1       1  ''
             1174  CALL_METHOD_1         1  ''
             1176  POP_TOP          

 L. 296      1178  LOAD_STR                 '<br>'
             1180  LOAD_METHOD              join
             1182  LOAD_FAST                'error_msg_list'
             1184  CALL_METHOD_1         1  ''
             1186  STORE_FAST               'error_msg'
           1188_0  COME_FROM          1144  '1144'
           1188_1  COME_FROM           634  '634'

 L. 302      1188  LOAD_STR                 '(|%s)'

 L. 303      1190  LOAD_STR                 ''
             1192  LOAD_METHOD              join

 L. 304      1194  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1196  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1198  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 306      1200  LOAD_FAST                'filter_components'

 L. 304      1202  GET_ITER         
             1204  CALL_FUNCTION_1       1  ''

 L. 303      1206  CALL_METHOD_1         1  ''

 L. 302      1208  BINARY_MODULO    
             1210  STORE_FAST               'remove_group_filterstr'

 L. 311      1212  BUILD_MAP_0           0 
             1214  STORE_DEREF              'remove_groups_dict'

 L. 313      1216  SETUP_FINALLY      1318  'to 1318'

 L. 314      1218  LOAD_DEREF               'app'
             1220  LOAD_ATTR                ls
             1222  LOAD_ATTR                l
             1224  LOAD_ATTR                search

 L. 315      1226  LOAD_GLOBAL              str
             1228  LOAD_FAST                'group_search_root'
             1230  CALL_FUNCTION_1       1  ''

 L. 316      1232  LOAD_GLOBAL              ldap0
             1234  LOAD_ATTR                SCOPE_SUBTREE

 L. 317      1236  LOAD_FAST                'remove_group_filterstr'

 L. 318      1238  LOAD_GLOBAL              REQUESTED_GROUP_ATTRS

 L. 314      1240  LOAD_CONST               ('attrlist',)
             1242  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1244  STORE_FAST               'msg_id'

 L. 320      1246  LOAD_DEREF               'app'
             1248  LOAD_ATTR                ls
             1250  LOAD_ATTR                l
             1252  LOAD_METHOD              results
             1254  LOAD_FAST                'msg_id'
             1256  CALL_METHOD_1         1  ''
             1258  GET_ITER         
             1260  FOR_ITER           1314  'to 1314'
             1262  STORE_FAST               'res'

 L. 321      1264  LOAD_FAST                'res'
             1266  LOAD_ATTR                rdata
             1268  GET_ITER         
           1270_0  COME_FROM          1282  '1282'
             1270  FOR_ITER           1310  'to 1310'
             1272  STORE_FAST               'sre'

 L. 322      1274  LOAD_GLOBAL              isinstance
             1276  LOAD_FAST                'sre'
             1278  LOAD_GLOBAL              SearchResultEntry
             1280  CALL_FUNCTION_2       2  ''
         1282_1284  POP_JUMP_IF_FALSE  1270  'to 1270'

 L. 323      1286  LOAD_GLOBAL              ldap0
             1288  LOAD_ATTR                cidict
             1290  LOAD_METHOD              CIDict
             1292  LOAD_FAST                'sre'
             1294  LOAD_ATTR                entry_s
             1296  CALL_METHOD_1         1  ''
             1298  LOAD_DEREF               'remove_groups_dict'
             1300  LOAD_FAST                'sre'
             1302  LOAD_ATTR                dn_s
             1304  STORE_SUBSCR     
         1306_1308  JUMP_BACK          1270  'to 1270'
         1310_1312  JUMP_BACK          1260  'to 1260'
             1314  POP_BLOCK        
             1316  JUMP_FORWARD       1378  'to 1378'
           1318_0  COME_FROM_FINALLY  1216  '1216'

 L. 324      1318  DUP_TOP          
             1320  LOAD_GLOBAL              ldap0
             1322  LOAD_ATTR                NO_SUCH_OBJECT
             1324  COMPARE_OP               exception-match
         1326_1328  POP_JUMP_IF_FALSE  1344  'to 1344'
             1330  POP_TOP          
             1332  POP_TOP          
             1334  POP_TOP          

 L. 325      1336  LOAD_STR                 'No such object! Did you choose a valid search base?'
             1338  STORE_FAST               'error_msg'
             1340  POP_EXCEPT       
             1342  JUMP_FORWARD       1378  'to 1378'
           1344_0  COME_FROM          1326  '1326'

 L. 326      1344  DUP_TOP          
             1346  LOAD_GLOBAL              ldap0
             1348  LOAD_ATTR                SIZELIMIT_EXCEEDED
             1350  LOAD_GLOBAL              ldap0
             1352  LOAD_ATTR                TIMELIMIT_EXCEEDED
             1354  BUILD_TUPLE_2         2 
             1356  COMPARE_OP               exception-match
         1358_1360  POP_JUMP_IF_FALSE  1376  'to 1376'
             1362  POP_TOP          
             1364  POP_TOP          
             1366  POP_TOP          

 L. 327      1368  LOAD_STR                 'Size or time limit exceeded while searching group entries!'
             1370  STORE_FAST               'error_msg'
             1372  POP_EXCEPT       
             1374  JUMP_FORWARD       1378  'to 1378'
           1376_0  COME_FROM          1358  '1358'
             1376  END_FINALLY      
           1378_0  COME_FROM          1374  '1374'
           1378_1  COME_FROM          1342  '1342'
           1378_2  COME_FROM          1316  '1316'

 L. 329      1378  LOAD_GLOBAL              sorted
             1380  LOAD_DEREF               'remove_groups_dict'
             1382  LOAD_METHOD              keys
             1384  CALL_METHOD_0         0  ''
             1386  LOAD_GLOBAL              str
             1388  LOAD_ATTR                lower
             1390  LOAD_CONST               ('key',)
             1392  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1394  STORE_FAST               'remove_group_dns'

 L. 331      1396  LOAD_FAST                'all_groups_dict'
             1398  LOAD_METHOD              update
             1400  LOAD_DEREF               'remove_groups_dict'
             1402  CALL_METHOD_1         1  ''
             1404  POP_TOP          

 L. 333      1406  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1408  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1410  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 335      1412  LOAD_FAST                'remove_group_dns'

 L. 333      1414  GET_ITER         
             1416  CALL_FUNCTION_1       1  ''
             1418  STORE_FAST               'remove_groups'

 L. 338      1420  LOAD_FAST                'all_groups_dict'
         1422_1424  POP_JUMP_IF_TRUE   1430  'to 1430'

 L. 339      1426  LOAD_STR                 'No group entries found. Did you choose a valid search base or valid name?'
             1428  STORE_FAST               'info_msg'
           1430_0  COME_FROM          1422  '1422'

 L. 345      1430  LOAD_CLOSURE             'remove_groups_dict'
             1432  BUILD_TUPLE_1         1 
             1434  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1436  LOAD_STR                 'w2l_groupadm.<locals>.<listcomp>'
             1438  MAKE_FUNCTION_8          'closure'

 L. 347      1440  LOAD_FAST                'all_group_entries'

 L. 345      1442  GET_ITER         
             1444  CALL_FUNCTION_1       1  ''
             1446  STORE_FAST               'add_groups'

 L. 355      1448  LOAD_GLOBAL              web2ldap
             1450  LOAD_ATTR                app
             1452  LOAD_ATTR                gui
             1454  LOAD_ATTR                top_section

 L. 356      1456  LOAD_DEREF               'app'

 L. 357      1458  LOAD_STR                 'Group membership'

 L. 358      1460  LOAD_GLOBAL              web2ldap
             1462  LOAD_ATTR                app
             1464  LOAD_ATTR                gui
             1466  LOAD_METHOD              main_menu
             1468  LOAD_DEREF               'app'
             1470  CALL_METHOD_1         1  ''

 L. 359      1472  BUILD_LIST_0          0 

 L. 355      1474  LOAD_CONST               ('context_menu_list',)
             1476  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1478  POP_TOP          

 L. 362      1480  LOAD_GLOBAL              web2ldap
             1482  LOAD_ATTR                app
             1484  LOAD_ATTR                gui
             1486  LOAD_ATTR                search_root_field

 L. 363      1488  LOAD_DEREF               'app'

 L. 364      1490  LOAD_STR                 'groupadm_searchroot'

 L. 362      1492  LOAD_CONST               ('name',)
             1494  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1496  STORE_FAST               'group_search_root_field'

 L. 366      1498  LOAD_DEREF               'app'
             1500  LOAD_ATTR                form
             1502  LOAD_ATTR                accept_charset
             1504  LOAD_FAST                'group_search_root_field'
             1506  STORE_ATTR               charset

 L. 367      1508  LOAD_FAST                'group_search_root_field'
             1510  LOAD_METHOD              set_default
             1512  LOAD_GLOBAL              str
             1514  LOAD_FAST                'group_search_root'
             1516  CALL_FUNCTION_1       1  ''
             1518  CALL_METHOD_1         1  ''
             1520  POP_TOP          

 L. 369      1522  LOAD_FAST                'error_msg'
         1524_1526  POP_JUMP_IF_FALSE  1544  'to 1544'

 L. 370      1528  LOAD_DEREF               'app'
             1530  LOAD_ATTR                outf
             1532  LOAD_METHOD              write
             1534  LOAD_STR                 '<p class="ErrorMessage">%s</p>'
             1536  LOAD_FAST                'error_msg'
             1538  BINARY_MODULO    
             1540  CALL_METHOD_1         1  ''
             1542  POP_TOP          
           1544_0  COME_FROM          1524  '1524'

 L. 371      1544  LOAD_FAST                'info_msg'
         1546_1548  POP_JUMP_IF_FALSE  1566  'to 1566'

 L. 372      1550  LOAD_DEREF               'app'
             1552  LOAD_ATTR                outf
             1554  LOAD_METHOD              write
             1556  LOAD_STR                 '<p class="InfoMessage">%s</p>'
             1558  LOAD_FAST                'info_msg'
             1560  BINARY_MODULO    
             1562  CALL_METHOD_1         1  ''
             1564  POP_TOP          
           1566_0  COME_FROM          1546  '1546'

 L. 374      1566  LOAD_FAST                'all_groups_dict'
         1568_1570  POP_JUMP_IF_FALSE  1680  'to 1680'

 L. 376      1572  LOAD_DEREF               'app'
             1574  LOAD_METHOD              cfg_param
             1576  LOAD_STR                 'groupadm_optgroup_bounds'
             1578  LOAD_CONST               (1, None)
             1580  CALL_METHOD_2         2  ''
             1582  STORE_FAST               'optgroup_bounds'

 L. 378      1584  LOAD_DEREF               'app'
             1586  LOAD_ATTR                outf
             1588  LOAD_METHOD              write

 L. 379      1590  LOAD_STR                 '\n            %s\n%s\n%s\n\n              <input type="submit" value="Change Group Membership">\n              <table summary="Group select fields">\n                <tr>\n                  <td width="50%%">Add to...</td>\n                  <td width="50%%">Remove from...</td>\n                </tr>\n                <tr>\n                  <td width="50%%">%s</td>\n                  <td width="50%%">%s</td>\n                </tr>\n              </table>\n            </form>\n            '

 L. 395      1592  LOAD_DEREF               'app'
             1594  LOAD_METHOD              begin_form
             1596  LOAD_STR                 'groupadm'
             1598  LOAD_STR                 'POST'
             1600  CALL_METHOD_2         2  ''

 L. 396      1602  LOAD_DEREF               'app'
             1604  LOAD_ATTR                form
             1606  LOAD_METHOD              hiddenFieldHTML
             1608  LOAD_STR                 'dn'
             1610  LOAD_DEREF               'app'
             1612  LOAD_ATTR                dn
             1614  LOAD_STR                 ''
             1616  CALL_METHOD_3         3  ''

 L. 397      1618  LOAD_DEREF               'app'
             1620  LOAD_ATTR                form
             1622  LOAD_METHOD              hiddenFieldHTML
             1624  LOAD_STR                 'groupadm_searchroot'
             1626  LOAD_GLOBAL              str
             1628  LOAD_FAST                'group_search_root'
             1630  CALL_FUNCTION_1       1  ''
             1632  LOAD_STR                 ''
             1634  CALL_METHOD_3         3  ''

 L. 398      1636  LOAD_GLOBAL              group_select_field

 L. 399      1638  LOAD_DEREF               'app'

 L. 400      1640  LOAD_FAST                'all_groups_dict'

 L. 401      1642  LOAD_STR                 'groupadm_add'

 L. 402      1644  LOAD_STR                 'Groups to add to'

 L. 403      1646  LOAD_FAST                'group_search_root'

 L. 404      1648  LOAD_FAST                'add_groups'

 L. 405      1650  LOAD_FAST                'optgroup_bounds'

 L. 398      1652  CALL_FUNCTION_7       7  ''

 L. 407      1654  LOAD_GLOBAL              group_select_field

 L. 408      1656  LOAD_DEREF               'app'

 L. 409      1658  LOAD_DEREF               'remove_groups_dict'

 L. 410      1660  LOAD_STR                 'groupadm_remove'

 L. 411      1662  LOAD_STR                 'Groups to remove from'

 L. 412      1664  LOAD_FAST                'group_search_root'

 L. 413      1666  LOAD_FAST                'remove_groups'

 L. 414      1668  LOAD_FAST                'optgroup_bounds'

 L. 407      1670  CALL_FUNCTION_7       7  ''

 L. 393      1672  BUILD_TUPLE_5         5 

 L. 379      1674  BINARY_MODULO    

 L. 378      1676  CALL_METHOD_1         1  ''
             1678  POP_TOP          
           1680_0  COME_FROM          1568  '1568'

 L. 419      1680  LOAD_DEREF               'app'
             1682  LOAD_ATTR                outf
             1684  LOAD_METHOD              write

 L. 420      1686  LOAD_STR                 '%s\n%s\n\n          <p><input type="submit" value="List"> group entries below: %s.</p>\n          <p>where group name contains: %s</p>\n          <p>List %s groups.</p>\n        </form>\n        '

 L. 427      1688  LOAD_DEREF               'app'
             1690  LOAD_METHOD              begin_form
             1692  LOAD_STR                 'groupadm'
             1694  LOAD_STR                 'GET'
             1696  CALL_METHOD_2         2  ''

 L. 428      1698  LOAD_DEREF               'app'
             1700  LOAD_ATTR                form
             1702  LOAD_METHOD              hiddenFieldHTML
             1704  LOAD_STR                 'dn'
             1706  LOAD_DEREF               'app'
             1708  LOAD_ATTR                dn
             1710  LOAD_STR                 ''
             1712  CALL_METHOD_3         3  ''

 L. 429      1714  LOAD_FAST                'group_search_root_field'
             1716  LOAD_ATTR                input_html
             1718  LOAD_STR                 'Search root for searching group entries'
             1720  LOAD_CONST               ('title',)
             1722  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 430      1724  LOAD_DEREF               'app'
             1726  LOAD_ATTR                form
             1728  LOAD_ATTR                field
             1730  LOAD_STR                 'groupadm_name'
             1732  BINARY_SUBSCR    
             1734  LOAD_METHOD              input_html
             1736  CALL_METHOD_0         0  ''

 L. 431      1738  LOAD_DEREF               'app'
             1740  LOAD_ATTR                form
             1742  LOAD_ATTR                field
             1744  LOAD_STR                 'groupadm_view'
             1746  BINARY_SUBSCR    
             1748  LOAD_ATTR                input_html

 L. 432      1750  LOAD_STR                 'Group entries list'

 L. 433      1752  LOAD_GLOBAL              str
             1754  LOAD_FAST                'groupadm_view'
             1756  CALL_FUNCTION_1       1  ''

 L. 431      1758  LOAD_CONST               ('title', 'default')
             1760  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 425      1762  BUILD_TUPLE_5         5 

 L. 420      1764  BINARY_MODULO    

 L. 419      1766  CALL_METHOD_1         1  ''
             1768  POP_TOP          

 L. 438      1770  LOAD_FAST                'groupadm_view'
         1772_1774  POP_JUMP_IF_FALSE  1926  'to 1926'

 L. 439      1776  LOAD_DEREF               'app'
             1778  LOAD_ATTR                outf
             1780  LOAD_METHOD              write
             1782  LOAD_STR                 '<dl>\n'
             1784  CALL_METHOD_1         1  ''
             1786  POP_TOP          

 L. 441      1788  LOAD_FAST                'remove_groups'
             1790  LOAD_FAST                'all_group_entries'
             1792  LOAD_CONST               (1, 2)
             1794  BUILD_CONST_KEY_MAP_2     2 
             1796  LOAD_FAST                'groupadm_view'
             1798  BINARY_SUBSCR    
             1800  GET_ITER         
             1802  FOR_ITER           1914  'to 1914'
             1804  STORE_FAST               'group_dn'

 L. 442      1806  LOAD_FAST                'all_groups_dict'
             1808  LOAD_FAST                'group_dn'
             1810  BINARY_SUBSCR    
             1812  STORE_FAST               'group_entry'

 L. 443      1814  LOAD_DEREF               'app'
             1816  LOAD_ATTR                outf
             1818  LOAD_METHOD              write
             1820  LOAD_STR                 '<dt>%s | %s</dt>\n<dd>%s<br>\n(%s)<br>\n%s</dd>\n'

 L. 444      1822  LOAD_STR                 ', '
             1824  LOAD_METHOD              join
             1826  LOAD_FAST                'group_entry'
             1828  LOAD_METHOD              get
             1830  LOAD_STR                 'cn'
             1832  BUILD_LIST_0          0 
             1834  CALL_METHOD_2         2  ''
             1836  CALL_METHOD_1         1  ''

 L. 445      1838  LOAD_DEREF               'app'
             1840  LOAD_ATTR                anchor

 L. 446      1842  LOAD_STR                 'read'

 L. 446      1844  LOAD_STR                 'Read'

 L. 447      1846  LOAD_STR                 'dn'
             1848  LOAD_FAST                'group_dn'
             1850  BUILD_TUPLE_2         2 
             1852  BUILD_LIST_1          1 

 L. 448      1854  LOAD_STR                 'Display group entry'

 L. 445      1856  LOAD_CONST               ('title',)
             1858  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 450      1860  LOAD_DEREF               'app'
             1862  LOAD_ATTR                form
             1864  LOAD_METHOD              utf2display
             1866  LOAD_FAST                'group_dn'
             1868  CALL_METHOD_1         1  ''

 L. 451      1870  LOAD_STR                 ', '
             1872  LOAD_METHOD              join
             1874  LOAD_FAST                'group_entry'
             1876  LOAD_METHOD              get
             1878  LOAD_STR                 'objectClass'
             1880  BUILD_LIST_0          0 
             1882  CALL_METHOD_2         2  ''
             1884  CALL_METHOD_1         1  ''

 L. 452      1886  LOAD_STR                 '<br>'
             1888  LOAD_METHOD              join
             1890  LOAD_FAST                'group_entry'
             1892  LOAD_METHOD              get
             1894  LOAD_STR                 'description'
             1896  BUILD_LIST_0          0 
             1898  CALL_METHOD_2         2  ''
             1900  CALL_METHOD_1         1  ''

 L. 443      1902  BUILD_TUPLE_5         5 
             1904  BINARY_MODULO    
             1906  CALL_METHOD_1         1  ''
             1908  POP_TOP          
         1910_1912  JUMP_BACK          1802  'to 1802'

 L. 454      1914  LOAD_DEREF               'app'
             1916  LOAD_ATTR                outf
             1918  LOAD_METHOD              write
             1920  LOAD_STR                 '</dl>\n'
             1922  CALL_METHOD_1         1  ''
             1924  POP_TOP          
           1926_0  COME_FROM          1772  '1772'

 L. 456      1926  LOAD_GLOBAL              web2ldap
             1928  LOAD_ATTR                app
             1930  LOAD_ATTR                gui
             1932  LOAD_METHOD              footer
             1934  LOAD_DEREF               'app'
             1936  CALL_METHOD_1         1  ''
             1938  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 324