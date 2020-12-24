# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/add.py
# Compiled at: 2020-05-04 07:52:07
# Size of source mod 2**32: 7645 bytes
"""
web2ldap.app.add: add an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

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

 L.  41         0  LOAD_FAST                'app'
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

 L.  45        48  LOAD_FAST                'app'
               50  LOAD_ATTR                form
               52  LOAD_ATTR                field
               54  LOAD_STR                 'in_at'
               56  BINARY_SUBSCR    
               58  LOAD_ATTR                value
               60  LOAD_FAST                'del_row_num'
               62  DELETE_SUBSCR    

 L.  46        64  LOAD_FAST                'app'
               66  LOAD_ATTR                form
               68  LOAD_ATTR                field
               70  LOAD_STR                 'in_av'
               72  BINARY_SUBSCR    
               74  LOAD_ATTR                value
               76  LOAD_FAST                'del_row_num'
               78  DELETE_SUBSCR    

 L.  48        80  LOAD_FAST                'app'
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

 L.  51       126  LOAD_FAST                'app'
              128  LOAD_ATTR                form
              130  LOAD_ATTR                field
              132  LOAD_STR                 'in_at'
              134  BINARY_SUBSCR    
              136  LOAD_ATTR                value
              138  LOAD_METHOD              insert
              140  LOAD_FAST                'insert_row_num'
              142  LOAD_CONST               1
              144  BINARY_ADD       
              146  LOAD_FAST                'app'
              148  LOAD_ATTR                form
              150  LOAD_ATTR                field
              152  LOAD_STR                 'in_at'
              154  BINARY_SUBSCR    
              156  LOAD_ATTR                value
              158  LOAD_FAST                'insert_row_num'
              160  BINARY_SUBSCR    
              162  CALL_METHOD_2         2  ''
              164  POP_TOP          

 L.  52       166  LOAD_FAST                'app'
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

 L.  54       192  LOAD_FAST                'app'
              194  LOAD_ATTR                form
              196  LOAD_ATTR                field
              198  LOAD_STR                 'in_avi'
              200  BINARY_SUBSCR    
              202  LOAD_ATTR                value
              204  LOAD_METHOD              insert
              206  LOAD_FAST                'insert_row_num'
              208  LOAD_CONST               1
              210  BINARY_ADD       
              212  LOAD_FAST                'app'
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

 L.  56       232  LOAD_FAST                'app'
              234  LOAD_ATTR                form
              236  LOAD_METHOD              getInputValue
              238  LOAD_STR                 'add_clonedn'
              240  LOAD_CONST               None
              242  BUILD_LIST_1          1 
              244  CALL_METHOD_2         2  ''
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  STORE_FAST               'add_clonedn'

 L.  57       252  LOAD_FAST                'app'
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
              290  LOAD_FAST                'app'
              292  LOAD_FAST                'add_clonedn'
              294  LOAD_FAST                'app'
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
              362  LOAD_FAST                'app'
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
              384  LOAD_FAST                'app'
              386  LOAD_FAST                'add_template'
              388  CALL_METHOD_2         2  ''
              390  UNPACK_SEQUENCE_2     2 
              392  STORE_FAST               'add_dn'
              394  STORE_FAST               'entry'

 L.  67       396  LOAD_GLOBAL              DNObj
              398  LOAD_METHOD              from_str
              400  LOAD_FAST                'add_dn'
              402  LOAD_METHOD              decode
              404  LOAD_FAST                'app'
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
              448  LOAD_FAST                'app'
              450  LOAD_ATTR                dn
            452_0  COME_FROM           444  '444'
              452  STORE_FAST               'add_basedn'

 L.  70       454  LOAD_GLOBAL              ldap0
              456  LOAD_ATTR                schema
              458  LOAD_ATTR                models
              460  LOAD_METHOD              Entry
              462  LOAD_FAST                'app'
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
              484  LOAD_FAST                'app'
              486  CALL_METHOD_1         1  ''
              488  UNPACK_SEQUENCE_2     2 
              490  STORE_FAST               'entry'
              492  STORE_FAST               'invalid_attrs'

 L.  73       494  LOAD_FAST                'app'
              496  LOAD_ATTR                form
              498  LOAD_METHOD              getInputValue
              500  LOAD_STR                 'add_rdn'
              502  LOAD_STR                 ''
              504  BUILD_LIST_1          1 
              506  CALL_METHOD_2         2  ''
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  STORE_FAST               'add_rdn'

 L.  74       514  LOAD_FAST                'app'
              516  LOAD_ATTR                form
              518  LOAD_METHOD              getInputValue
              520  LOAD_STR                 'add_basedn'
              522  LOAD_FAST                'app'
              524  LOAD_ATTR                dn
              526  BUILD_LIST_1          1 
              528  CALL_METHOD_2         2  ''
              530  LOAD_CONST               0
              532  BINARY_SUBSCR    
              534  STORE_FAST               'add_basedn'
            536_0  COME_FROM           474  '474'
            536_1  COME_FROM           368  '368'

 L.  76       536  LOAD_FAST                'invalid_attrs'
          538_540  POP_JUMP_IF_FALSE   560  'to 560'

 L.  77       542  LOAD_GLOBAL              web2ldap
              544  LOAD_ATTR                app
              546  LOAD_ATTR                gui
              548  LOAD_METHOD              invalid_syntax_message
              550  LOAD_FAST                'app'
              552  LOAD_FAST                'invalid_attrs'
              554  CALL_METHOD_2         2  ''
              556  STORE_FAST               'error_msg'
              558  JUMP_FORWARD        564  'to 564'
            560_0  COME_FROM           538  '538'

 L.  79       560  LOAD_STR                 ''
              562  STORE_FAST               'error_msg'
            564_0  COME_FROM           558  '558'

 L.  82       564  LOAD_FAST                'add_clonedn'

 L.  81   566_568  POP_JUMP_IF_TRUE    630  'to 630'

 L.  82       570  LOAD_FAST                'add_template'

 L.  81   572_574  POP_JUMP_IF_TRUE    630  'to 630'

 L.  83       576  LOAD_FAST                'entry'

 L.  81   578_580  POP_JUMP_IF_FALSE   630  'to 630'

 L.  84       582  LOAD_FAST                'invalid_attrs'

 L.  81   584_586  POP_JUMP_IF_TRUE    630  'to 630'

 L.  85       588  LOAD_STR                 'in_mr'
              590  LOAD_FAST                'app'
              592  LOAD_ATTR                form
              594  LOAD_ATTR                input_field_names
              596  COMPARE_OP               in

 L.  81   598_600  POP_JUMP_IF_TRUE    630  'to 630'

 L.  86       602  LOAD_STR                 'in_oc'
              604  LOAD_FAST                'app'
              606  LOAD_ATTR                form
              608  LOAD_ATTR                input_field_names
              610  COMPARE_OP               in

 L.  81   612_614  POP_JUMP_IF_TRUE    630  'to 630'

 L.  87       616  LOAD_STR                 'in_ft'
              618  LOAD_FAST                'app'
              620  LOAD_ATTR                form
              622  LOAD_ATTR                input_field_names
              624  COMPARE_OP               in

 L.  81   626_628  POP_JUMP_IF_FALSE   660  'to 660'
            630_0  COME_FROM           612  '612'
            630_1  COME_FROM           598  '598'
            630_2  COME_FROM           584  '584'
            630_3  COME_FROM           578  '578'
            630_4  COME_FROM           572  '572'
            630_5  COME_FROM           566  '566'

 L.  89       630  LOAD_GLOBAL              web2ldap
              632  LOAD_ATTR                app
              634  LOAD_ATTR                addmodifyform
              636  LOAD_ATTR                w2l_addform

 L.  90       638  LOAD_FAST                'app'

 L.  91       640  LOAD_FAST                'add_rdn'

 L.  91       642  LOAD_FAST                'add_basedn'

 L.  91       644  LOAD_FAST                'entry'

 L.  92       646  LOAD_FAST                'error_msg'

 L.  93       648  LOAD_FAST                'invalid_attrs'

 L.  89       650  LOAD_CONST               ('msg', 'invalid_attrs')
              652  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              654  POP_TOP          

 L.  95       656  LOAD_CONST               None
              658  RETURN_VALUE     
            660_0  COME_FROM           626  '626'

 L.  98       660  LOAD_FAST                'entry'
              662  LOAD_METHOD              items
              664  CALL_METHOD_0         0  ''
              666  GET_ITER         
              668  FOR_ITER            698  'to 698'
              670  UNPACK_SEQUENCE_2     2 
              672  STORE_FAST               'attr_type'
              674  STORE_FAST               'attr_values'

 L.  99       676  LOAD_LISTCOMP            '<code_object <listcomp>>'
              678  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
              680  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              682  LOAD_FAST                'attr_values'
              684  GET_ITER         
              686  CALL_FUNCTION_1       1  ''
              688  LOAD_FAST                'entry'
              690  LOAD_FAST                'attr_type'
              692  STORE_SUBSCR     
          694_696  JUMP_BACK           668  'to 668'

 L. 103       698  SETUP_FINALLY       726  'to 726'

 L. 104       700  LOAD_GLOBAL              list
              702  LOAD_GLOBAL              DNObj
              704  LOAD_METHOD              from_str
              706  LOAD_FAST                'add_rdn'
              708  CALL_METHOD_1         1  ''
              710  LOAD_METHOD              rdn_attrs
              712  CALL_METHOD_0         0  ''
              714  LOAD_METHOD              items
              716  CALL_METHOD_0         0  ''
              718  CALL_FUNCTION_1       1  ''
              720  STORE_FAST               'rdn_list'
              722  POP_BLOCK        
              724  JUMP_FORWARD        776  'to 776'
            726_0  COME_FROM_FINALLY   698  '698'

 L. 105       726  DUP_TOP          
              728  LOAD_GLOBAL              ldap0
              730  LOAD_ATTR                DECODING_ERROR
              732  COMPARE_OP               exception-match
          734_736  POP_JUMP_IF_FALSE   774  'to 774'
              738  POP_TOP          
              740  POP_TOP          
              742  POP_TOP          

 L. 106       744  LOAD_GLOBAL              web2ldap
              746  LOAD_ATTR                app
              748  LOAD_ATTR                addmodifyform
              750  LOAD_ATTR                w2l_addform

 L. 107       752  LOAD_FAST                'app'

 L. 108       754  LOAD_FAST                'add_rdn'

 L. 108       756  LOAD_FAST                'add_basedn'

 L. 108       758  LOAD_FAST                'entry'

 L. 109       760  LOAD_STR                 'Wrong format of RDN string.'

 L. 106       762  LOAD_CONST               ('msg',)
              764  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              766  POP_TOP          

 L. 111       768  POP_EXCEPT       
              770  LOAD_CONST               None
              772  RETURN_VALUE     
            774_0  COME_FROM           734  '734'
              774  END_FINALLY      
            776_0  COME_FROM           724  '724'

 L. 114       776  LOAD_GLOBAL              range
              778  LOAD_GLOBAL              len
              780  LOAD_FAST                'rdn_list'
              782  CALL_FUNCTION_1       1  ''
              784  CALL_FUNCTION_1       1  ''
              786  GET_ITER         
              788  FOR_ITER            958  'to 958'
              790  STORE_FAST               'i'

 L. 115       792  LOAD_FAST                'rdn_list'
              794  LOAD_FAST                'i'
              796  BINARY_SUBSCR    
              798  UNPACK_SEQUENCE_2     2 
              800  STORE_FAST               'rdn_attr_type'
              802  STORE_FAST               'rdn_attr_value'

 L. 117       804  LOAD_FAST                'rdn_attr_type'
              806  LOAD_METHOD              lower
              808  CALL_METHOD_0         0  ''
              810  LOAD_METHOD              startswith
              812  LOAD_STR                 'oid.'
              814  CALL_METHOD_1         1  ''
          816_818  POP_JUMP_IF_FALSE   832  'to 832'

 L. 118       820  LOAD_FAST                'rdn_attr_type'
              822  LOAD_CONST               4
              824  LOAD_CONST               None
              826  BUILD_SLICE_2         2 
              828  BINARY_SUBSCR    
              830  STORE_FAST               'rdn_attr_type'
            832_0  COME_FROM           816  '816'

 L. 119       832  LOAD_FAST                'rdn_attr_type'
              834  LOAD_FAST                'entry'
              836  COMPARE_OP               in
          838_840  POP_JUMP_IF_FALSE   912  'to 912'

 L. 120       842  LOAD_FAST                'rdn_attr_value'

 L. 119   844_846  POP_JUMP_IF_TRUE    866  'to 866'

 L. 120       848  LOAD_GLOBAL              len
              850  LOAD_FAST                'entry'
              852  LOAD_FAST                'rdn_attr_type'
              854  BINARY_SUBSCR    
              856  CALL_FUNCTION_1       1  ''
              858  LOAD_CONST               1
              860  COMPARE_OP               ==

 L. 119   862_864  POP_JUMP_IF_TRUE    880  'to 880'
            866_0  COME_FROM           844  '844'

 L. 121       866  LOAD_FAST                'rdn_attr_value'
              868  LOAD_FAST                'entry'
              870  LOAD_FAST                'rdn_attr_type'
              872  BINARY_SUBSCR    
              874  COMPARE_OP               in

 L. 119   876_878  POP_JUMP_IF_FALSE   912  'to 912'
            880_0  COME_FROM           862  '862'

 L. 123       880  LOAD_FAST                'rdn_attr_type'
              882  LOAD_FAST                'entry'
              884  LOAD_FAST                'rdn_attr_type'
              886  BINARY_SUBSCR    
              888  LOAD_CONST               0
              890  BINARY_SUBSCR    
              892  LOAD_METHOD              decode
              894  LOAD_FAST                'app'
              896  LOAD_ATTR                ls
              898  LOAD_ATTR                charset
              900  CALL_METHOD_1         1  ''
              902  BUILD_TUPLE_2         2 
              904  LOAD_FAST                'rdn_list'
              906  LOAD_FAST                'i'
              908  STORE_SUBSCR     
              910  JUMP_BACK           788  'to 788'
            912_0  COME_FROM           876  '876'
            912_1  COME_FROM           838  '838'

 L. 125       912  LOAD_GLOBAL              web2ldap
              914  LOAD_ATTR                app
              916  LOAD_ATTR                addmodifyform
              918  LOAD_ATTR                w2l_addform

 L. 126       920  LOAD_FAST                'app'

 L. 127       922  LOAD_FAST                'add_rdn'

 L. 128       924  LOAD_FAST                'add_basedn'

 L. 128       926  LOAD_FAST                'entry'

 L. 129       928  LOAD_STR                 'Attribute <var>%s</var> required for RDN not in entry data.'

 L. 130       930  LOAD_FAST                'app'
              932  LOAD_ATTR                form
              934  LOAD_METHOD              utf2display
              936  LOAD_FAST                'rdn_attr_type'
              938  CALL_METHOD_1         1  ''

 L. 129       940  BINARY_MODULO    

 L. 125       942  LOAD_CONST               ('msg',)
              944  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              946  POP_TOP          

 L. 133       948  POP_TOP          
              950  LOAD_CONST               None
              952  RETURN_VALUE     
          954_956  JUMP_BACK           788  'to 788'

 L. 136       958  LOAD_GLOBAL              DNObj
              960  LOAD_GLOBAL              tuple
              962  LOAD_FAST                'rdn_list'
              964  CALL_FUNCTION_1       1  ''
              966  BUILD_TUPLE_1         1 
              968  CALL_FUNCTION_1       1  ''
              970  STORE_FAST               'rdn'

 L. 139       972  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              974  LOAD_STR                 'w2l_add.<locals>.<dictcomp>'
              976  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 141       978  LOAD_FAST                'entry'
              980  LOAD_METHOD              items
              982  CALL_METHOD_0         0  ''

 L. 139       984  GET_ITER         
              986  CALL_FUNCTION_1       1  ''
              988  STORE_FAST               'add_entry'

 L. 145       990  LOAD_FAST                'add_entry'
          992_994  POP_JUMP_IF_TRUE   1010  'to 1010'

 L. 146       996  LOAD_GLOBAL              web2ldap
              998  LOAD_ATTR                app
             1000  LOAD_ATTR                core
             1002  LOAD_METHOD              ErrorExit
             1004  LOAD_STR                 'Cannot add entry without attribute values.'
             1006  CALL_METHOD_1         1  ''
             1008  RAISE_VARARGS_1       1  'exception instance'
           1010_0  COME_FROM           992  '992'

 L. 148      1010  LOAD_FAST                'app'
             1012  LOAD_ATTR                dn
         1014_1016  POP_JUMP_IF_FALSE  1034  'to 1034'

 L. 149      1018  LOAD_FAST                'rdn'
             1020  LOAD_GLOBAL              DNObj
             1022  LOAD_METHOD              from_str
             1024  LOAD_FAST                'add_basedn'
             1026  CALL_METHOD_1         1  ''
             1028  BINARY_ADD       
             1030  STORE_FAST               'new_dn'
             1032  JUMP_FORWARD       1038  'to 1038'
           1034_0  COME_FROM          1014  '1014'

 L. 152      1034  LOAD_FAST                'rdn'
             1036  STORE_FAST               'new_dn'
           1038_0  COME_FROM          1032  '1032'

 L. 154      1038  LOAD_GLOBAL              PostReadControl
             1040  LOAD_ATTR                controlType
             1042  LOAD_FAST                'app'
             1044  LOAD_ATTR                ls
             1046  LOAD_ATTR                supportedControl
             1048  COMPARE_OP               in
         1050_1052  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 155      1054  LOAD_GLOBAL              PostReadControl
             1056  LOAD_CONST               False
             1058  LOAD_STR                 'entryUUID'
             1060  BUILD_LIST_1          1 
             1062  LOAD_CONST               ('criticality', 'attrList')
             1064  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1066  BUILD_LIST_1          1 
             1068  STORE_FAST               'add_req_ctrls'
             1070  JUMP_FORWARD       1076  'to 1076'
           1072_0  COME_FROM          1050  '1050'

 L. 157      1072  LOAD_CONST               None
             1074  STORE_FAST               'add_req_ctrls'
           1076_0  COME_FROM          1070  '1070'

 L. 160      1076  SETUP_FINALLY      1106  'to 1106'

 L. 161      1078  LOAD_FAST                'app'
             1080  LOAD_ATTR                ls
             1082  LOAD_ATTR                l
             1084  LOAD_ATTR                add_s

 L. 162      1086  LOAD_GLOBAL              str
             1088  LOAD_FAST                'new_dn'
             1090  CALL_FUNCTION_1       1  ''

 L. 163      1092  LOAD_FAST                'add_entry'

 L. 164      1094  LOAD_FAST                'add_req_ctrls'

 L. 161      1096  LOAD_CONST               ('req_ctrls',)
             1098  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1100  STORE_FAST               'add_result'
             1102  POP_BLOCK        
             1104  JUMP_FORWARD       1296  'to 1296'
           1106_0  COME_FROM_FINALLY  1076  '1076'

 L. 166      1106  DUP_TOP          
             1108  LOAD_GLOBAL              ldap0
             1110  LOAD_ATTR                NO_SUCH_OBJECT
             1112  COMPARE_OP               exception-match
         1114_1116  POP_JUMP_IF_FALSE  1190  'to 1190'
             1118  POP_TOP          
             1120  STORE_FAST               'e'
             1122  POP_TOP          
             1124  SETUP_FINALLY      1178  'to 1178'

 L. 167      1126  LOAD_GLOBAL              web2ldap
             1128  LOAD_ATTR                app
             1130  LOAD_ATTR                core
             1132  LOAD_METHOD              ErrorExit

 L. 168      1134  LOAD_STR                 '\n            %s<br>\n            Probably this superiour entry does not exist:<br>%s<br>\n            Maybe wrong base DN in LDIF template?<br>\n            '

 L. 173      1136  LOAD_FAST                'app'
             1138  LOAD_METHOD              ldap_error_msg
             1140  LOAD_FAST                'e'
             1142  CALL_METHOD_1         1  ''

 L. 174      1144  LOAD_FAST                'app'
             1146  LOAD_ATTR                display_dn
             1148  LOAD_FAST                'add_basedn'
             1150  LOAD_METHOD              decode
             1152  LOAD_FAST                'app'
             1154  LOAD_ATTR                ls
             1156  LOAD_ATTR                charset
             1158  CALL_METHOD_1         1  ''
             1160  LOAD_CONST               0
             1162  LOAD_CONST               ('commandbutton',)
             1164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 172      1166  BUILD_TUPLE_2         2 

 L. 168      1168  BINARY_MODULO    

 L. 167      1170  CALL_METHOD_1         1  ''
             1172  RAISE_VARARGS_1       1  'exception instance'
             1174  POP_BLOCK        
             1176  BEGIN_FINALLY    
           1178_0  COME_FROM_FINALLY  1124  '1124'
             1178  LOAD_CONST               None
             1180  STORE_FAST               'e'
             1182  DELETE_FAST              'e'
             1184  END_FINALLY      
             1186  POP_EXCEPT       
             1188  JUMP_FORWARD       1416  'to 1416'
           1190_0  COME_FROM          1114  '1114'

 L. 177      1190  DUP_TOP          

 L. 178      1192  LOAD_GLOBAL              ldap0
             1194  LOAD_ATTR                ALREADY_EXISTS

 L. 179      1196  LOAD_GLOBAL              ldap0
             1198  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 180      1200  LOAD_GLOBAL              ldap0
             1202  LOAD_ATTR                INVALID_DN_SYNTAX

 L. 181      1204  LOAD_GLOBAL              ldap0
             1206  LOAD_ATTR                INVALID_SYNTAX

 L. 182      1208  LOAD_GLOBAL              ldap0
             1210  LOAD_ATTR                NAMING_VIOLATION

 L. 183      1212  LOAD_GLOBAL              ldap0
             1214  LOAD_ATTR                OBJECT_CLASS_VIOLATION

 L. 184      1216  LOAD_GLOBAL              ldap0
             1218  LOAD_ATTR                OTHER

 L. 185      1220  LOAD_GLOBAL              ldap0
             1222  LOAD_ATTR                TYPE_OR_VALUE_EXISTS

 L. 186      1224  LOAD_GLOBAL              ldap0
             1226  LOAD_ATTR                UNDEFINED_TYPE

 L. 187      1228  LOAD_GLOBAL              ldap0
             1230  LOAD_ATTR                UNWILLING_TO_PERFORM

 L. 177      1232  BUILD_TUPLE_10       10 
             1234  COMPARE_OP               exception-match
         1236_1238  POP_JUMP_IF_FALSE  1294  'to 1294'
             1240  POP_TOP          
             1242  STORE_FAST               'e'
             1244  POP_TOP          
             1246  SETUP_FINALLY      1282  'to 1282'

 L. 190      1248  LOAD_GLOBAL              web2ldap
             1250  LOAD_ATTR                app
             1252  LOAD_ATTR                addmodifyform
             1254  LOAD_ATTR                w2l_addform

 L. 191      1256  LOAD_FAST                'app'

 L. 192      1258  LOAD_FAST                'add_rdn'

 L. 192      1260  LOAD_FAST                'add_basedn'

 L. 192      1262  LOAD_FAST                'entry'

 L. 193      1264  LOAD_FAST                'app'
             1266  LOAD_METHOD              ldap_error_msg
             1268  LOAD_FAST                'e'
             1270  CALL_METHOD_1         1  ''

 L. 190      1272  LOAD_CONST               ('msg',)
             1274  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1276  POP_TOP          
             1278  POP_BLOCK        
             1280  BEGIN_FINALLY    
           1282_0  COME_FROM_FINALLY  1246  '1246'
             1282  LOAD_CONST               None
             1284  STORE_FAST               'e'
             1286  DELETE_FAST              'e'
             1288  END_FINALLY      
             1290  POP_EXCEPT       
             1292  JUMP_FORWARD       1416  'to 1416'
           1294_0  COME_FROM          1236  '1236'
             1294  END_FINALLY      
           1296_0  COME_FROM          1104  '1104'

 L. 197      1296  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1298  LOAD_STR                 'w2l_add.<locals>.<listcomp>'
             1300  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 199      1302  LOAD_FAST                'add_result'
             1304  LOAD_ATTR                ctrls
         1306_1308  JUMP_IF_TRUE_OR_POP  1312  'to 1312'
             1310  BUILD_LIST_0          0 
           1312_0  COME_FROM          1306  '1306'

 L. 197      1312  GET_ITER         
             1314  CALL_FUNCTION_1       1  ''
             1316  STORE_FAST               'prec_ctrls'

 L. 202      1318  LOAD_FAST                'prec_ctrls'
         1320_1322  POP_JUMP_IF_FALSE  1336  'to 1336'

 L. 203      1324  LOAD_FAST                'prec_ctrls'
             1326  LOAD_CONST               0
             1328  BINARY_SUBSCR    
             1330  LOAD_ATTR                res
             1332  LOAD_ATTR                dn_s
             1334  STORE_FAST               'new_dn'
           1336_0  COME_FROM          1320  '1320'

 L. 204      1336  LOAD_FAST                'app'
             1338  LOAD_ATTR                simple_message

 L. 205      1340  LOAD_STR                 'Added Entry'

 L. 206      1342  LOAD_STR                 '\n            <p class="SuccessMessage">Successfully added new entry.</p>\n            <p>%s</p>\n            <dl>\n              <dt>Distinguished name:</dt>\n              <dd>%s</dd>\n            </dl>\n            '

 L. 214      1344  LOAD_FAST                'app'
             1346  LOAD_ATTR                anchor

 L. 215      1348  LOAD_STR                 'read'

 L. 215      1350  LOAD_STR                 'Read added entry'

 L. 216      1352  LOAD_STR                 'dn'
             1354  LOAD_GLOBAL              str
             1356  LOAD_FAST                'new_dn'
             1358  CALL_FUNCTION_1       1  ''
             1360  BUILD_TUPLE_2         2 
             1362  BUILD_LIST_1          1 

 L. 217      1364  LOAD_STR                 'Display added entry %s'
             1366  LOAD_FAST                'new_dn'
             1368  BUILD_TUPLE_1         1 
             1370  BINARY_MODULO    

 L. 214      1372  LOAD_CONST               ('title',)
             1374  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 219      1376  LOAD_FAST                'app'
             1378  LOAD_ATTR                display_dn
             1380  LOAD_GLOBAL              str
             1382  LOAD_FAST                'new_dn'
             1384  CALL_FUNCTION_1       1  ''
             1386  LOAD_CONST               0
             1388  LOAD_CONST               ('commandbutton',)
             1390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 213      1392  BUILD_TUPLE_2         2 

 L. 206      1394  BINARY_MODULO    

 L. 221      1396  LOAD_GLOBAL              web2ldap
             1398  LOAD_ATTR                app
             1400  LOAD_ATTR                gui
             1402  LOAD_METHOD              main_menu
             1404  LOAD_FAST                'app'
             1406  CALL_METHOD_1         1  ''

 L. 222      1408  BUILD_LIST_0          0 

 L. 204      1410  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1412  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1414  POP_TOP          
           1416_0  COME_FROM          1292  '1292'
           1416_1  COME_FROM          1188  '1188'

Parse error at or near `LOAD_CONST' instruction at offset 770