# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/add.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 7924 bytes
"""
web2ldap.app.add: add an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0, ldap0.modlist
from ldap0.controls.readentry import PostReadControl
from ldap0.dn import DNObj
import web2ldap.web.forms, web2ldap.app.cnf, web2ldap.app.core, web2ldap.app.gui, web2ldap.app.schema, web2ldap.app.addmodifyform
ADD_IGNORE_ATTR_TYPES = {
 'entryDN',
 'entryCSN',
 'governingStructureRule',
 'hasSubordinates',
 'structuralObjectClass',
 'subschemaSubentry',
 'collectiveAttributeSubentries'}

def w2l_add--- This code section failed: ---

 L.  41         0  LOAD_DEREF               'app'
                2  LOAD_ATTR                form
                4  LOAD_METHOD              getInputValue
                6  LOAD_STR                 'in_mr'
                8  LOAD_STR                 '.'
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_2         2  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'input_modrow'

 L.  43        20  LOAD_FAST                'input_modrow'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_STR                 '-'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    98  'to 98'

 L.  44        32  LOAD_GLOBAL              int
               34  LOAD_FAST                'input_modrow'
               36  LOAD_CONST               1
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'del_row_num'

 L.  45        48  LOAD_DEREF               'app'
               50  LOAD_ATTR                form
               52  LOAD_ATTR                field
               54  LOAD_STR                 'in_at'
               56  BINARY_SUBSCR    
               58  LOAD_ATTR                value
               60  LOAD_FAST                'del_row_num'
               62  DELETE_SUBSCR    

 L.  46        64  LOAD_DEREF               'app'
               66  LOAD_ATTR                form
               68  LOAD_ATTR                field
               70  LOAD_STR                 'in_av'
               72  BINARY_SUBSCR    
               74  LOAD_ATTR                value
               76  LOAD_FAST                'del_row_num'
               78  DELETE_SUBSCR    

 L.  48        80  LOAD_DEREF               'app'
               82  LOAD_ATTR                form
               84  LOAD_ATTR                field
               86  LOAD_STR                 'in_avi'
               88  BINARY_SUBSCR    
               90  LOAD_ATTR                value
               92  LOAD_FAST                'del_row_num'
               94  DELETE_SUBSCR    
               96  JUMP_FORWARD        232  'to 232'
             98_0  COME_FROM            30  '30'

 L.  49        98  LOAD_FAST                'input_modrow'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  LOAD_STR                 '+'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   232  'to 232'

 L.  50       110  LOAD_GLOBAL              int
              112  LOAD_FAST                'input_modrow'
              114  LOAD_CONST               1
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'insert_row_num'

 L.  51       126  LOAD_DEREF               'app'
              128  LOAD_ATTR                form
              130  LOAD_ATTR                field
              132  LOAD_STR                 'in_at'
              134  BINARY_SUBSCR    
              136  LOAD_ATTR                value
              138  LOAD_METHOD              insert
              140  LOAD_FAST                'insert_row_num'
              142  LOAD_CONST               1
              144  BINARY_ADD       
              146  LOAD_DEREF               'app'
              148  LOAD_ATTR                form
              150  LOAD_ATTR                field
              152  LOAD_STR                 'in_at'
              154  BINARY_SUBSCR    
              156  LOAD_ATTR                value
              158  LOAD_FAST                'insert_row_num'
              160  BINARY_SUBSCR    
              162  CALL_METHOD_2         2  ''
              164  POP_TOP          

 L.  52       166  LOAD_DEREF               'app'
              168  LOAD_ATTR                form
              170  LOAD_ATTR                field
              172  LOAD_STR                 'in_av'
              174  BINARY_SUBSCR    
              176  LOAD_ATTR                value
              178  LOAD_METHOD              insert
              180  LOAD_FAST                'insert_row_num'
              182  LOAD_CONST               1
              184  BINARY_ADD       
              186  LOAD_STR                 ''
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L.  54       192  LOAD_DEREF               'app'
              194  LOAD_ATTR                form
              196  LOAD_ATTR                field
              198  LOAD_STR                 'in_avi'
              200  BINARY_SUBSCR    
              202  LOAD_ATTR                value
              204  LOAD_METHOD              insert
              206  LOAD_FAST                'insert_row_num'
              208  LOAD_CONST               1
              210  BINARY_ADD       
              212  LOAD_DEREF               'app'
              214  LOAD_ATTR                form
              216  LOAD_ATTR                field
              218  LOAD_STR                 'in_avi'
              220  BINARY_SUBSCR    
              222  LOAD_ATTR                value
              224  LOAD_FAST                'insert_row_num'
              226  BINARY_SUBSCR    
              228  CALL_METHOD_2         2  ''
              230  POP_TOP          
            232_0  COME_FROM           108  '108'
            232_1  COME_FROM            96  '96'

 L.  56       232  LOAD_DEREF               'app'
              234  LOAD_ATTR                form
              236  LOAD_METHOD              getInputValue
              238  LOAD_STR                 'add_clonedn'
              240  LOAD_CONST               None
              242  BUILD_LIST_1          1 
              244  CALL_METHOD_2         2  ''
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  STORE_FAST               'add_clonedn'

 L.  57       252  LOAD_DEREF               'app'
              254  LOAD_ATTR                form
              256  LOAD_METHOD              getInputValue
              258  LOAD_STR                 'add_template'
              260  LOAD_CONST               None
              262  BUILD_LIST_1          1 
              264  CALL_METHOD_2         2  ''
              266  LOAD_CONST               0
              268  BINARY_SUBSCR    
              270  STORE_FAST               'add_template'

 L.  58       272  LOAD_CONST               None
              274  STORE_FAST               'invalid_attrs'

 L.  60       276  LOAD_FAST                'add_clonedn'
          278_280  POP_JUMP_IF_FALSE   370  'to 370'

 L.  61       282  LOAD_GLOBAL              web2ldap
              284  LOAD_ATTR                app
              286  LOAD_ATTR                addmodifyform
              288  LOAD_METHOD              read_old_entry
              290  LOAD_DEREF               'app'
              292  LOAD_FAST                'add_clonedn'
              294  LOAD_DEREF               'app'
              296  LOAD_ATTR                schema
              298  LOAD_CONST               None
              300  LOAD_STR                 '*'
              302  LOAD_STR                 '*'
              304  BUILD_MAP_1           1 
              306  CALL_METHOD_5         5  ''
              308  UNPACK_SEQUENCE_2     2 
              310  STORE_FAST               'entry'
              312  STORE_FAST               '_'

 L.  62       314  LOAD_GLOBAL              DNObj
              316  LOAD_METHOD              from_str
              318  LOAD_FAST                'add_clonedn'
              320  CALL_METHOD_1         1  ''
              322  STORE_FAST               'add_clonedn_obj'

 L.  63       324  LOAD_STR                 '+'
              326  LOAD_METHOD              join
              328  LOAD_LISTCOMP            '<code_object <listcomp>>'
              330  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
              332  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              334  LOAD_FAST                'add_clonedn_obj'
              336  LOAD_CONST               0
              338  BINARY_SUBSCR    
              340  GET_ITER         
              342  CALL_FUNCTION_1       1  ''
              344  CALL_METHOD_1         1  ''
              346  STORE_FAST               'add_rdn'

 L.  64       348  LOAD_GLOBAL              str
              350  LOAD_FAST                'add_clonedn_obj'
              352  LOAD_METHOD              parent
              354  CALL_METHOD_0         0  ''
              356  CALL_FUNCTION_1       1  ''
          358_360  JUMP_IF_TRUE_OR_POP   366  'to 366'
              362  LOAD_DEREF               'app'
              364  LOAD_ATTR                dn
            366_0  COME_FROM           358  '358'
              366  STORE_FAST               'add_basedn'
              368  JUMP_FORWARD        536  'to 536'
            370_0  COME_FROM           278  '278'

 L.  65       370  LOAD_FAST                'add_template'
          372_374  POP_JUMP_IF_FALSE   476  'to 476'

 L.  66       376  LOAD_GLOBAL              web2ldap
              378  LOAD_ATTR                app
              380  LOAD_ATTR                addmodifyform
              382  LOAD_METHOD              ReadLDIFTemplate
              384  LOAD_DEREF               'app'
              386  LOAD_FAST                'add_template'
              388  CALL_METHOD_2         2  ''
              390  UNPACK_SEQUENCE_2     2 
              392  STORE_FAST               'add_dn'
              394  STORE_FAST               'entry'

 L.  67       396  LOAD_GLOBAL              DNObj
              398  LOAD_METHOD              from_str
              400  LOAD_FAST                'add_dn'
              402  LOAD_METHOD              decode
              404  LOAD_DEREF               'app'
              406  LOAD_ATTR                ls
              408  LOAD_ATTR                charset
              410  CALL_METHOD_1         1  ''
              412  CALL_METHOD_1         1  ''
              414  STORE_FAST               'add_dn_obj'

 L.  68       416  LOAD_GLOBAL              str
              418  LOAD_FAST                'add_dn_obj'
              420  LOAD_METHOD              rdn
              422  CALL_METHOD_0         0  ''
              424  CALL_FUNCTION_1       1  ''
              426  LOAD_GLOBAL              str
              428  LOAD_FAST                'add_dn_obj'
              430  LOAD_METHOD              parent
              432  CALL_METHOD_0         0  ''
              434  CALL_FUNCTION_1       1  ''
              436  ROT_TWO          
              438  STORE_FAST               'add_rdn'
              440  STORE_FAST               'add_basedn'

 L.  69       442  LOAD_FAST                'add_basedn'
          444_446  JUMP_IF_TRUE_OR_POP   452  'to 452'
              448  LOAD_DEREF               'app'
              450  LOAD_ATTR                dn
            452_0  COME_FROM           444  '444'
              452  STORE_FAST               'add_basedn'

 L.  70       454  LOAD_GLOBAL              ldap0
              456  LOAD_ATTR                schema
              458  LOAD_ATTR                models
              460  LOAD_METHOD              Entry
              462  LOAD_DEREF               'app'
              464  LOAD_ATTR                schema
              466  LOAD_FAST                'add_basedn'
              468  LOAD_FAST                'entry'
              470  CALL_METHOD_3         3  ''
              472  STORE_FAST               'entry'
              474  JUMP_FORWARD        536  'to 536'
            476_0  COME_FROM           372  '372'

 L.  72       476  LOAD_GLOBAL              web2ldap
              478  LOAD_ATTR                app
              480  LOAD_ATTR                addmodifyform
              482  LOAD_METHOD              get_entry_input
              484  LOAD_DEREF               'app'
              486  CALL_METHOD_1         1  ''
              488  UNPACK_SEQUENCE_2     2 
              490  STORE_FAST               'entry'
              492  STORE_FAST               'invalid_attrs'

 L.  73       494  LOAD_DEREF               'app'
              496  LOAD_ATTR                form
              498  LOAD_METHOD              getInputValue
              500  LOAD_STR                 'add_rdn'
              502  LOAD_STR                 ''
              504  BUILD_LIST_1          1 
              506  CALL_METHOD_2         2  ''
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  STORE_FAST               'add_rdn'

 L.  74       514  LOAD_DEREF               'app'
              516  LOAD_ATTR                form
              518  LOAD_METHOD              getInputValue
              520  LOAD_STR                 'add_basedn'
              522  LOAD_DEREF               'app'
              524  LOAD_ATTR                dn
              526  BUILD_LIST_1          1 
              528  CALL_METHOD_2         2  ''
              530  LOAD_CONST               0
              532  BINARY_SUBSCR    
              534  STORE_FAST               'add_basedn'
            536_0  COME_FROM           474  '474'
            536_1  COME_FROM           368  '368'

 L.  76       536  LOAD_FAST                'invalid_attrs'
          538_540  POP_JUMP_IF_FALSE   594  'to 594'

 L.  77       542  LOAD_CLOSURE             'app'
              544  BUILD_TUPLE_1         1 
              546  LOAD_LISTCOMP            '<code_object <listcomp>>'
              548  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
              550  MAKE_FUNCTION_8          'closure'

 L.  79       552  LOAD_GLOBAL              sorted
              554  LOAD_FAST                'invalid_attrs'
              556  LOAD_METHOD              keys
              558  CALL_METHOD_0         0  ''
              560  CALL_FUNCTION_1       1  ''

 L.  77       562  GET_ITER         
              564  CALL_FUNCTION_1       1  ''
              566  STORE_FAST               'invalid_attr_types_ui'

 L.  81       568  LOAD_STR                 'Wrong syntax in following attributes: %s'

 L.  82       570  LOAD_STR                 ', '
              572  LOAD_METHOD              join
              574  LOAD_LISTCOMP            '<code_object <listcomp>>'
              576  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
              578  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  84       580  LOAD_FAST                'invalid_attr_types_ui'

 L.  82       582  GET_ITER         
              584  CALL_FUNCTION_1       1  ''
              586  CALL_METHOD_1         1  ''

 L.  81       588  BINARY_MODULO    
              590  STORE_FAST               'error_msg'
              592  JUMP_FORWARD        598  'to 598'
            594_0  COME_FROM           538  '538'

 L.  88       594  LOAD_STR                 ''
              596  STORE_FAST               'error_msg'
            598_0  COME_FROM           592  '592'

 L.  91       598  LOAD_FAST                'add_clonedn'

 L.  90   600_602  POP_JUMP_IF_TRUE    664  'to 664'

 L.  91       604  LOAD_FAST                'add_template'

 L.  90   606_608  POP_JUMP_IF_TRUE    664  'to 664'

 L.  92       610  LOAD_FAST                'entry'

 L.  90   612_614  POP_JUMP_IF_FALSE   664  'to 664'

 L.  93       616  LOAD_FAST                'invalid_attrs'

 L.  90   618_620  POP_JUMP_IF_TRUE    664  'to 664'

 L.  94       622  LOAD_STR                 'in_mr'
              624  LOAD_DEREF               'app'
              626  LOAD_ATTR                form
              628  LOAD_ATTR                input_field_names
              630  COMPARE_OP               in

 L.  90   632_634  POP_JUMP_IF_TRUE    664  'to 664'

 L.  95       636  LOAD_STR                 'in_oc'
              638  LOAD_DEREF               'app'
              640  LOAD_ATTR                form
              642  LOAD_ATTR                input_field_names
              644  COMPARE_OP               in

 L.  90   646_648  POP_JUMP_IF_TRUE    664  'to 664'

 L.  96       650  LOAD_STR                 'in_ft'
              652  LOAD_DEREF               'app'
              654  LOAD_ATTR                form
              656  LOAD_ATTR                input_field_names
              658  COMPARE_OP               in

 L.  90   660_662  POP_JUMP_IF_FALSE   694  'to 694'
            664_0  COME_FROM           646  '646'
            664_1  COME_FROM           632  '632'
            664_2  COME_FROM           618  '618'
            664_3  COME_FROM           612  '612'
            664_4  COME_FROM           606  '606'
            664_5  COME_FROM           600  '600'

 L.  98       664  LOAD_GLOBAL              web2ldap
              666  LOAD_ATTR                app
              668  LOAD_ATTR                addmodifyform
              670  LOAD_ATTR                w2l_addform

 L.  99       672  LOAD_DEREF               'app'

 L. 100       674  LOAD_FAST                'add_rdn'

 L. 100       676  LOAD_FAST                'add_basedn'

 L. 100       678  LOAD_FAST                'entry'

 L. 101       680  LOAD_FAST                'error_msg'

 L. 102       682  LOAD_FAST                'invalid_attrs'

 L.  98       684  LOAD_CONST               ('msg', 'invalid_attrs')
              686  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              688  POP_TOP          

 L. 104       690  LOAD_CONST               None
              692  RETURN_VALUE     
            694_0  COME_FROM           660  '660'

 L. 107       694  LOAD_FAST                'entry'
              696  LOAD_METHOD              items
              698  CALL_METHOD_0         0  ''
              700  GET_ITER         
              702  FOR_ITER            732  'to 732'
              704  UNPACK_SEQUENCE_2     2 
              706  STORE_FAST               'attr_type'
              708  STORE_FAST               'attr_values'

 L. 108       710  LOAD_LISTCOMP            '<code_object <listcomp>>'
              712  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
              714  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              716  LOAD_FAST                'attr_values'
              718  GET_ITER         
              720  CALL_FUNCTION_1       1  ''
              722  LOAD_FAST                'entry'
              724  LOAD_FAST                'attr_type'
              726  STORE_SUBSCR     
          728_730  JUMP_BACK           702  'to 702'

 L. 112       732  SETUP_FINALLY       760  'to 760'

 L. 113       734  LOAD_GLOBAL              list
              736  LOAD_GLOBAL              DNObj
              738  LOAD_METHOD              from_str
              740  LOAD_FAST                'add_rdn'
              742  CALL_METHOD_1         1  ''
              744  LOAD_METHOD              rdn_attrs
              746  CALL_METHOD_0         0  ''
              748  LOAD_METHOD              items
              750  CALL_METHOD_0         0  ''
              752  CALL_FUNCTION_1       1  ''
              754  STORE_FAST               'rdn_list'
              756  POP_BLOCK        
              758  JUMP_FORWARD        810  'to 810'
            760_0  COME_FROM_FINALLY   732  '732'

 L. 114       760  DUP_TOP          
              762  LOAD_GLOBAL              ldap0
              764  LOAD_ATTR                DECODING_ERROR
              766  COMPARE_OP               exception-match
          768_770  POP_JUMP_IF_FALSE   808  'to 808'
              772  POP_TOP          
              774  POP_TOP          
              776  POP_TOP          

 L. 115       778  LOAD_GLOBAL              web2ldap
              780  LOAD_ATTR                app
              782  LOAD_ATTR                addmodifyform
              784  LOAD_ATTR                w2l_addform

 L. 116       786  LOAD_DEREF               'app'

 L. 117       788  LOAD_FAST                'add_rdn'

 L. 117       790  LOAD_FAST                'add_basedn'

 L. 117       792  LOAD_FAST                'entry'

 L. 118       794  LOAD_STR                 'Wrong format of RDN string.'

 L. 115       796  LOAD_CONST               ('msg',)
              798  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              800  POP_TOP          

 L. 120       802  POP_EXCEPT       
              804  LOAD_CONST               None
              806  RETURN_VALUE     
            808_0  COME_FROM           768  '768'
              808  END_FINALLY      
            810_0  COME_FROM           758  '758'

 L. 123       810  LOAD_GLOBAL              range
              812  LOAD_GLOBAL              len
              814  LOAD_FAST                'rdn_list'
              816  CALL_FUNCTION_1       1  ''
              818  CALL_FUNCTION_1       1  ''
              820  GET_ITER         
              822  FOR_ITER            992  'to 992'
              824  STORE_FAST               'i'

 L. 124       826  LOAD_FAST                'rdn_list'
              828  LOAD_FAST                'i'
              830  BINARY_SUBSCR    
              832  UNPACK_SEQUENCE_2     2 
              834  STORE_FAST               'rdn_attr_type'
              836  STORE_FAST               'rdn_attr_value'

 L. 126       838  LOAD_FAST                'rdn_attr_type'
              840  LOAD_METHOD              lower
              842  CALL_METHOD_0         0  ''
              844  LOAD_METHOD              startswith
              846  LOAD_STR                 'oid.'
              848  CALL_METHOD_1         1  ''
          850_852  POP_JUMP_IF_FALSE   866  'to 866'

 L. 127       854  LOAD_FAST                'rdn_attr_type'
              856  LOAD_CONST               4
              858  LOAD_CONST               None
              860  BUILD_SLICE_2         2 
              862  BINARY_SUBSCR    
              864  STORE_FAST               'rdn_attr_type'
            866_0  COME_FROM           850  '850'

 L. 128       866  LOAD_FAST                'rdn_attr_type'
              868  LOAD_FAST                'entry'
              870  COMPARE_OP               in
          872_874  POP_JUMP_IF_FALSE   946  'to 946'

 L. 129       876  LOAD_FAST                'rdn_attr_value'

 L. 128   878_880  POP_JUMP_IF_TRUE    900  'to 900'

 L. 129       882  LOAD_GLOBAL              len
              884  LOAD_FAST                'entry'
              886  LOAD_FAST                'rdn_attr_type'
              888  BINARY_SUBSCR    
              890  CALL_FUNCTION_1       1  ''
              892  LOAD_CONST               1
              894  COMPARE_OP               ==

 L. 128   896_898  POP_JUMP_IF_TRUE    914  'to 914'
            900_0  COME_FROM           878  '878'

 L. 130       900  LOAD_FAST                'rdn_attr_value'
              902  LOAD_FAST                'entry'
              904  LOAD_FAST                'rdn_attr_type'
              906  BINARY_SUBSCR    
              908  COMPARE_OP               in

 L. 128   910_912  POP_JUMP_IF_FALSE   946  'to 946'
            914_0  COME_FROM           896  '896'

 L. 132       914  LOAD_FAST                'rdn_attr_type'
              916  LOAD_FAST                'entry'
              918  LOAD_FAST                'rdn_attr_type'
              920  BINARY_SUBSCR    
              922  LOAD_CONST               0
              924  BINARY_SUBSCR    
              926  LOAD_METHOD              decode
              928  LOAD_DEREF               'app'
              930  LOAD_ATTR                ls
              932  LOAD_ATTR                charset
              934  CALL_METHOD_1         1  ''
              936  BUILD_TUPLE_2         2 
              938  LOAD_FAST                'rdn_list'
              940  LOAD_FAST                'i'
              942  STORE_SUBSCR     
              944  JUMP_BACK           822  'to 822'
            946_0  COME_FROM           910  '910'
            946_1  COME_FROM           872  '872'

 L. 134       946  LOAD_GLOBAL              web2ldap
              948  LOAD_ATTR                app
              950  LOAD_ATTR                addmodifyform
              952  LOAD_ATTR                w2l_addform

 L. 135       954  LOAD_DEREF               'app'

 L. 136       956  LOAD_FAST                'add_rdn'

 L. 137       958  LOAD_FAST                'add_basedn'

 L. 137       960  LOAD_FAST                'entry'

 L. 138       962  LOAD_STR                 'Attribute <var>%s</var> required for RDN not in entry data.'

 L. 139       964  LOAD_DEREF               'app'
              966  LOAD_ATTR                form
              968  LOAD_METHOD              utf2display
              970  LOAD_FAST                'rdn_attr_type'
              972  CALL_METHOD_1         1  ''

 L. 138       974  BINARY_MODULO    

 L. 134       976  LOAD_CONST               ('msg',)
              978  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              980  POP_TOP          

 L. 142       982  POP_TOP          
              984  LOAD_CONST               None
              986  RETURN_VALUE     
          988_990  JUMP_BACK           822  'to 822'

 L. 145       992  LOAD_GLOBAL              DNObj
              994  LOAD_GLOBAL              tuple
              996  LOAD_FAST                'rdn_list'
              998  CALL_FUNCTION_1       1  ''
             1000  BUILD_TUPLE_1         1 
             1002  CALL_FUNCTION_1       1  ''
             1004  STORE_FAST               'rdn'

 L. 148      1006  LOAD_DICTCOMP            '<code_object <dictcomp>>'
             1008  LOAD_STR                 'w2l_add.<locals>.<dictcomp>'
             1010  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 150      1012  LOAD_FAST                'entry'
             1014  LOAD_METHOD              items
             1016  CALL_METHOD_0         0  ''

 L. 148      1018  GET_ITER         
             1020  CALL_FUNCTION_1       1  ''
             1022  STORE_FAST               'add_entry'

 L. 154      1024  LOAD_FAST                'add_entry'
         1026_1028  POP_JUMP_IF_TRUE   1044  'to 1044'

 L. 155      1030  LOAD_GLOBAL              web2ldap
             1032  LOAD_ATTR                app
             1034  LOAD_ATTR                core
             1036  LOAD_METHOD              ErrorExit
             1038  LOAD_STR                 'Cannot add entry without attribute values.'
             1040  CALL_METHOD_1         1  ''
             1042  RAISE_VARARGS_1       1  'exception instance'
           1044_0  COME_FROM          1026  '1026'

 L. 157      1044  LOAD_DEREF               'app'
             1046  LOAD_ATTR                dn
         1048_1050  POP_JUMP_IF_FALSE  1068  'to 1068'

 L. 158      1052  LOAD_FAST                'rdn'
             1054  LOAD_GLOBAL              DNObj
             1056  LOAD_METHOD              from_str
             1058  LOAD_FAST                'add_basedn'
             1060  CALL_METHOD_1         1  ''
             1062  BINARY_ADD       
             1064  STORE_FAST               'new_dn'
             1066  JUMP_FORWARD       1072  'to 1072'
           1068_0  COME_FROM          1048  '1048'

 L. 161      1068  LOAD_FAST                'rdn'
             1070  STORE_FAST               'new_dn'
           1072_0  COME_FROM          1066  '1066'

 L. 163      1072  LOAD_GLOBAL              PostReadControl
             1074  LOAD_ATTR                controlType
             1076  LOAD_DEREF               'app'
             1078  LOAD_ATTR                ls
             1080  LOAD_ATTR                supportedControl
             1082  COMPARE_OP               in
         1084_1086  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 164      1088  LOAD_GLOBAL              PostReadControl
             1090  LOAD_CONST               False
             1092  LOAD_STR                 'entryUUID'
             1094  BUILD_LIST_1          1 
             1096  LOAD_CONST               ('criticality', 'attrList')
             1098  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1100  BUILD_LIST_1          1 
             1102  STORE_FAST               'add_req_ctrls'
             1104  JUMP_FORWARD       1110  'to 1110'
           1106_0  COME_FROM          1084  '1084'

 L. 166      1106  LOAD_CONST               None
             1108  STORE_FAST               'add_req_ctrls'
           1110_0  COME_FROM          1104  '1104'

 L. 169      1110  SETUP_FINALLY      1140  'to 1140'

 L. 170      1112  LOAD_DEREF               'app'
             1114  LOAD_ATTR                ls
             1116  LOAD_ATTR                l
             1118  LOAD_ATTR                add_s

 L. 171      1120  LOAD_GLOBAL              str
             1122  LOAD_FAST                'new_dn'
             1124  CALL_FUNCTION_1       1  ''

 L. 172      1126  LOAD_FAST                'add_entry'

 L. 173      1128  LOAD_FAST                'add_req_ctrls'

 L. 170      1130  LOAD_CONST               ('req_ctrls',)
             1132  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1134  STORE_FAST               'add_result'
             1136  POP_BLOCK        
             1138  JUMP_FORWARD       1330  'to 1330'
           1140_0  COME_FROM_FINALLY  1110  '1110'

 L. 175      1140  DUP_TOP          
             1142  LOAD_GLOBAL              ldap0
             1144  LOAD_ATTR                NO_SUCH_OBJECT
             1146  COMPARE_OP               exception-match
         1148_1150  POP_JUMP_IF_FALSE  1224  'to 1224'
             1152  POP_TOP          
             1154  STORE_FAST               'e'
             1156  POP_TOP          
             1158  SETUP_FINALLY      1212  'to 1212'

 L. 176      1160  LOAD_GLOBAL              web2ldap
             1162  LOAD_ATTR                app
             1164  LOAD_ATTR                core
             1166  LOAD_METHOD              ErrorExit

 L. 177      1168  LOAD_STR                 '\n            %s<br>\n            Probably this superiour entry does not exist:<br>%s<br>\n            Maybe wrong base DN in LDIF template?<br>\n            '

 L. 182      1170  LOAD_DEREF               'app'
             1172  LOAD_METHOD              ldap_error_msg
             1174  LOAD_FAST                'e'
             1176  CALL_METHOD_1         1  ''

 L. 183      1178  LOAD_DEREF               'app'
             1180  LOAD_ATTR                display_dn
             1182  LOAD_FAST                'add_basedn'
             1184  LOAD_METHOD              decode
             1186  LOAD_DEREF               'app'
             1188  LOAD_ATTR                ls
             1190  LOAD_ATTR                charset
             1192  CALL_METHOD_1         1  ''
             1194  LOAD_CONST               0
             1196  LOAD_CONST               ('commandbutton',)
             1198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 181      1200  BUILD_TUPLE_2         2 

 L. 177      1202  BINARY_MODULO    

 L. 176      1204  CALL_METHOD_1         1  ''
             1206  RAISE_VARARGS_1       1  'exception instance'
             1208  POP_BLOCK        
             1210  BEGIN_FINALLY    
           1212_0  COME_FROM_FINALLY  1158  '1158'
             1212  LOAD_CONST               None
             1214  STORE_FAST               'e'
             1216  DELETE_FAST              'e'
             1218  END_FINALLY      
             1220  POP_EXCEPT       
             1222  JUMP_FORWARD       1450  'to 1450'
           1224_0  COME_FROM          1148  '1148'

 L. 186      1224  DUP_TOP          

 L. 187      1226  LOAD_GLOBAL              ldap0
             1228  LOAD_ATTR                ALREADY_EXISTS

 L. 188      1230  LOAD_GLOBAL              ldap0
             1232  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 189      1234  LOAD_GLOBAL              ldap0
             1236  LOAD_ATTR                INVALID_DN_SYNTAX

 L. 190      1238  LOAD_GLOBAL              ldap0
             1240  LOAD_ATTR                INVALID_SYNTAX

 L. 191      1242  LOAD_GLOBAL              ldap0
             1244  LOAD_ATTR                NAMING_VIOLATION

 L. 192      1246  LOAD_GLOBAL              ldap0
             1248  LOAD_ATTR                OBJECT_CLASS_VIOLATION

 L. 193      1250  LOAD_GLOBAL              ldap0
             1252  LOAD_ATTR                OTHER

 L. 194      1254  LOAD_GLOBAL              ldap0
             1256  LOAD_ATTR                TYPE_OR_VALUE_EXISTS

 L. 195      1258  LOAD_GLOBAL              ldap0
             1260  LOAD_ATTR                UNDEFINED_TYPE

 L. 196      1262  LOAD_GLOBAL              ldap0
             1264  LOAD_ATTR                UNWILLING_TO_PERFORM

 L. 186      1266  BUILD_TUPLE_10       10 
             1268  COMPARE_OP               exception-match
         1270_1272  POP_JUMP_IF_FALSE  1328  'to 1328'
             1274  POP_TOP          
             1276  STORE_FAST               'e'
             1278  POP_TOP          
             1280  SETUP_FINALLY      1316  'to 1316'

 L. 199      1282  LOAD_GLOBAL              web2ldap
             1284  LOAD_ATTR                app
             1286  LOAD_ATTR                addmodifyform
             1288  LOAD_ATTR                w2l_addform

 L. 200      1290  LOAD_DEREF               'app'

 L. 201      1292  LOAD_FAST                'add_rdn'

 L. 201      1294  LOAD_FAST                'add_basedn'

 L. 201      1296  LOAD_FAST                'entry'

 L. 202      1298  LOAD_DEREF               'app'
             1300  LOAD_METHOD              ldap_error_msg
             1302  LOAD_FAST                'e'
             1304  CALL_METHOD_1         1  ''

 L. 199      1306  LOAD_CONST               ('msg',)
             1308  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1310  POP_TOP          
             1312  POP_BLOCK        
             1314  BEGIN_FINALLY    
           1316_0  COME_FROM_FINALLY  1280  '1280'
             1316  LOAD_CONST               None
             1318  STORE_FAST               'e'
             1320  DELETE_FAST              'e'
             1322  END_FINALLY      
             1324  POP_EXCEPT       
             1326  JUMP_FORWARD       1450  'to 1450'
           1328_0  COME_FROM          1270  '1270'
             1328  END_FINALLY      
           1330_0  COME_FROM          1138  '1138'

 L. 206      1330  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1332  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
             1334  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 208      1336  LOAD_FAST                'add_result'
             1338  LOAD_ATTR                ctrls
         1340_1342  JUMP_IF_TRUE_OR_POP  1346  'to 1346'
             1344  BUILD_LIST_0          0 
           1346_0  COME_FROM          1340  '1340'

 L. 206      1346  GET_ITER         
             1348  CALL_FUNCTION_1       1  ''
             1350  STORE_FAST               'prec_ctrls'

 L. 211      1352  LOAD_FAST                'prec_ctrls'
         1354_1356  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 212      1358  LOAD_FAST                'prec_ctrls'
             1360  LOAD_CONST               0
             1362  BINARY_SUBSCR    
             1364  LOAD_ATTR                res
             1366  LOAD_ATTR                dn_s
             1368  STORE_FAST               'new_dn'
           1370_0  COME_FROM          1354  '1354'

 L. 213      1370  LOAD_DEREF               'app'
             1372  LOAD_ATTR                simple_message

 L. 214      1374  LOAD_STR                 'Added Entry'

 L. 215      1376  LOAD_STR                 '\n            <p class="SuccessMessage">Successfully added new entry.</p>\n            <p>%s</p>\n            <dl>\n              <dt>Distinguished name:</dt>\n              <dd>%s</dd>\n            </dl>\n            '

 L. 223      1378  LOAD_DEREF               'app'
             1380  LOAD_ATTR                anchor

 L. 224      1382  LOAD_STR                 'read'

 L. 224      1384  LOAD_STR                 'Read added entry'

 L. 225      1386  LOAD_STR                 'dn'
             1388  LOAD_GLOBAL              str
             1390  LOAD_FAST                'new_dn'
             1392  CALL_FUNCTION_1       1  ''
             1394  BUILD_TUPLE_2         2 
             1396  BUILD_LIST_1          1 

 L. 226      1398  LOAD_STR                 'Display added entry %s'
             1400  LOAD_FAST                'new_dn'
             1402  BUILD_TUPLE_1         1 
             1404  BINARY_MODULO    

 L. 223      1406  LOAD_CONST               ('title',)
             1408  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 228      1410  LOAD_DEREF               'app'
             1412  LOAD_ATTR                display_dn
             1414  LOAD_GLOBAL              str
             1416  LOAD_FAST                'new_dn'
             1418  CALL_FUNCTION_1       1  ''
             1420  LOAD_CONST               0
             1422  LOAD_CONST               ('commandbutton',)
             1424  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 222      1426  BUILD_TUPLE_2         2 

 L. 215      1428  BINARY_MODULO    

 L. 230      1430  LOAD_GLOBAL              web2ldap
             1432  LOAD_ATTR                app
             1434  LOAD_ATTR                gui
             1436  LOAD_METHOD              main_menu
             1438  LOAD_DEREF               'app'
             1440  CALL_METHOD_1         1  ''

 L. 231      1442  BUILD_LIST_0          0 

 L. 213      1444  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1446  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1448  POP_TOP          
           1450_0  COME_FROM          1326  '1326'
           1450_1  COME_FROM          1222  '1222'

Parse error at or near `LOAD_CONST' instruction at offset 804