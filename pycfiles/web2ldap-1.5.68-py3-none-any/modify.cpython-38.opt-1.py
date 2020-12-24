# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/modify.py
# Compiled at: 2020-04-23 17:02:52
# Size of source mod 2**32: 8018 bytes
"""
web2ldap.app.modify: modify an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
from io import BytesIO
import ldap0, ldap0.ldif, ldap0.schema
from ldap0.schema.models import AttributeType
from ldap0.schema.util import modify_modlist
import web2ldap.ldapsession, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.gui, web2ldap.app.addmodifyform, web2ldap.app.add, web2ldap.app.schema
from web2ldap.app.schema.syntaxes import syntax_registry

def modlist_ldif(dn, form, modlist):
    """
    Return a string containing a HTML-formatted LDIF change record
    """
    s = []
    s.append('<pre>')
    f = BytesIO()
    ldif_writer = ldap0.ldif.LDIFWriter(f)
    ldif_writer.unparse(dn.encode('utf-8'), modlist)
    s.append(form.utf2display(f.getvalue().decode('utf-8')).replace('\n', '<br>'))
    s.append('</pre>')
    return ''.join(s)


def w2l_modify--- This code section failed: ---

 L.  53         0  LOAD_DEREF               'app'
                2  LOAD_ATTR                form
                4  LOAD_METHOD              getInputValue
                6  LOAD_STR                 'in_assertion'
                8  LOAD_STR                 '(objectClass=*)'
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_2         2  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'in_assertion'

 L.  55        20  LOAD_DEREF               'app'
               22  LOAD_ATTR                form
               24  LOAD_METHOD              getInputValue
               26  LOAD_STR                 'in_mr'
               28  LOAD_STR                 '.'
               30  BUILD_LIST_1          1 
               32  CALL_METHOD_2         2  ''
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  STORE_FAST               'input_modrow'

 L.  57        40  LOAD_FAST                'input_modrow'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_STR                 '-'
               48  COMPARE_OP               ==
            50_52  POP_JUMP_IF_FALSE   290  'to 290'

 L.  58        54  LOAD_GLOBAL              int
               56  LOAD_FAST                'input_modrow'
               58  LOAD_CONST               1
               60  LOAD_CONST               None
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'del_row_num'

 L.  59        70  LOAD_GLOBAL              len
               72  LOAD_DEREF               'app'
               74  LOAD_ATTR                form
               76  LOAD_ATTR                field
               78  LOAD_STR                 'in_at'
               80  BINARY_SUBSCR    
               82  LOAD_ATTR                value
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'in_at_len'

 L.  60        88  LOAD_FAST                'in_at_len'
               90  LOAD_FAST                'del_row_num'
               92  LOAD_CONST               2
               94  BINARY_ADD       
               96  COMPARE_OP               >=
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L.  61       100  LOAD_DEREF               'app'
              102  LOAD_ATTR                form
              104  LOAD_ATTR                field
              106  LOAD_STR                 'in_at'
              108  BINARY_SUBSCR    
              110  LOAD_ATTR                value
              112  LOAD_FAST                'del_row_num'
              114  BINARY_SUBSCR    
              116  LOAD_DEREF               'app'
              118  LOAD_ATTR                form
              120  LOAD_ATTR                field
              122  LOAD_STR                 'in_at'
              124  BINARY_SUBSCR    
              126  LOAD_ATTR                value
              128  LOAD_FAST                'del_row_num'
              130  LOAD_CONST               1
              132  BINARY_ADD       
              134  BINARY_SUBSCR    
              136  COMPARE_OP               ==

 L.  60       138  POP_JUMP_IF_TRUE    188  'to 188'
            140_0  COME_FROM            98  '98'

 L.  62       140  LOAD_FAST                'in_at_len'
              142  LOAD_CONST               1
              144  COMPARE_OP               >=

 L.  60       146  POP_JUMP_IF_FALSE   230  'to 230'

 L.  63       148  LOAD_DEREF               'app'
              150  LOAD_ATTR                form
              152  LOAD_ATTR                field
              154  LOAD_STR                 'in_at'
              156  BINARY_SUBSCR    
              158  LOAD_ATTR                value
              160  LOAD_FAST                'del_row_num'
              162  BINARY_SUBSCR    
              164  LOAD_DEREF               'app'
              166  LOAD_ATTR                form
              168  LOAD_ATTR                field
              170  LOAD_STR                 'in_at'
              172  BINARY_SUBSCR    
              174  LOAD_ATTR                value
              176  LOAD_FAST                'del_row_num'
              178  LOAD_CONST               1
              180  BINARY_SUBTRACT  
              182  BINARY_SUBSCR    
              184  COMPARE_OP               ==

 L.  60       186  POP_JUMP_IF_FALSE   230  'to 230'
            188_0  COME_FROM           138  '138'

 L.  65       188  LOAD_DEREF               'app'
              190  LOAD_ATTR                form
              192  LOAD_ATTR                field
              194  LOAD_STR                 'in_at'
              196  BINARY_SUBSCR    
              198  LOAD_ATTR                value
              200  LOAD_METHOD              pop
              202  LOAD_FAST                'del_row_num'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L.  66       208  LOAD_DEREF               'app'
              210  LOAD_ATTR                form
              212  LOAD_ATTR                field
              214  LOAD_STR                 'in_av'
              216  BINARY_SUBSCR    
              218  LOAD_ATTR                value
              220  LOAD_METHOD              pop
              222  LOAD_FAST                'del_row_num'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          
              228  JUMP_FORWARD        248  'to 248'
            230_0  COME_FROM           186  '186'
            230_1  COME_FROM           146  '146'

 L.  69       230  LOAD_STR                 ''
              232  LOAD_DEREF               'app'
              234  LOAD_ATTR                form
              236  LOAD_ATTR                field
              238  LOAD_STR                 'in_av'
              240  BINARY_SUBSCR    
              242  LOAD_ATTR                value
              244  LOAD_FAST                'del_row_num'
              246  STORE_SUBSCR     
            248_0  COME_FROM           228  '228'

 L.  70       248  LOAD_GLOBAL              map
              250  LOAD_GLOBAL              str
              252  LOAD_GLOBAL              range
              254  LOAD_CONST               0
              256  LOAD_GLOBAL              len
              258  LOAD_DEREF               'app'
              260  LOAD_ATTR                form
              262  LOAD_ATTR                field
              264  LOAD_STR                 'in_av'
              266  BINARY_SUBSCR    
              268  LOAD_ATTR                value
              270  CALL_FUNCTION_1       1  ''
              272  CALL_FUNCTION_2       2  ''
              274  CALL_FUNCTION_2       2  ''
              276  LOAD_DEREF               'app'
              278  LOAD_ATTR                form
              280  LOAD_ATTR                field
              282  LOAD_STR                 'in_avi'
              284  BINARY_SUBSCR    
              286  STORE_ATTR               value
              288  JUMP_FORWARD        426  'to 426'
            290_0  COME_FROM            50  '50'

 L.  71       290  LOAD_FAST                'input_modrow'
              292  LOAD_CONST               0
              294  BINARY_SUBSCR    
              296  LOAD_STR                 '+'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   426  'to 426'

 L.  72       304  LOAD_GLOBAL              int
              306  LOAD_FAST                'input_modrow'
              308  LOAD_CONST               1
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  BINARY_SUBSCR    
              316  CALL_FUNCTION_1       1  ''
              318  STORE_FAST               'insert_row_num'

 L.  73       320  LOAD_DEREF               'app'
              322  LOAD_ATTR                form
              324  LOAD_ATTR                field
              326  LOAD_STR                 'in_at'
              328  BINARY_SUBSCR    
              330  LOAD_ATTR                value
              332  LOAD_METHOD              insert
              334  LOAD_FAST                'insert_row_num'
              336  LOAD_CONST               1
              338  BINARY_ADD       
              340  LOAD_DEREF               'app'
              342  LOAD_ATTR                form
              344  LOAD_ATTR                field
              346  LOAD_STR                 'in_at'
              348  BINARY_SUBSCR    
              350  LOAD_ATTR                value
              352  LOAD_FAST                'insert_row_num'
              354  BINARY_SUBSCR    
              356  CALL_METHOD_2         2  ''
              358  POP_TOP          

 L.  74       360  LOAD_DEREF               'app'
              362  LOAD_ATTR                form
              364  LOAD_ATTR                field
              366  LOAD_STR                 'in_av'
              368  BINARY_SUBSCR    
              370  LOAD_ATTR                value
              372  LOAD_METHOD              insert
              374  LOAD_FAST                'insert_row_num'
              376  LOAD_CONST               1
              378  BINARY_ADD       
              380  LOAD_STR                 ''
              382  CALL_METHOD_2         2  ''
              384  POP_TOP          

 L.  75       386  LOAD_GLOBAL              map
              388  LOAD_GLOBAL              str
              390  LOAD_GLOBAL              range
              392  LOAD_CONST               0
              394  LOAD_GLOBAL              len
              396  LOAD_DEREF               'app'
              398  LOAD_ATTR                form
              400  LOAD_ATTR                field
              402  LOAD_STR                 'in_av'
              404  BINARY_SUBSCR    
              406  LOAD_ATTR                value
              408  CALL_FUNCTION_1       1  ''
              410  CALL_FUNCTION_2       2  ''
              412  CALL_FUNCTION_2       2  ''
              414  LOAD_DEREF               'app'
              416  LOAD_ATTR                form
              418  LOAD_ATTR                field
              420  LOAD_STR                 'in_avi'
              422  BINARY_SUBSCR    
              424  STORE_ATTR               value
            426_0  COME_FROM           300  '300'
            426_1  COME_FROM           288  '288'

 L.  77       426  LOAD_GLOBAL              web2ldap
              428  LOAD_ATTR                app
              430  LOAD_ATTR                addmodifyform
              432  LOAD_METHOD              get_entry_input
              434  LOAD_DEREF               'app'
              436  CALL_METHOD_1         1  ''
              438  UNPACK_SEQUENCE_2     2 
              440  STORE_FAST               'new_entry'
              442  STORE_FAST               'invalid_attrs'

 L.  79       444  LOAD_FAST                'invalid_attrs'
          446_448  POP_JUMP_IF_FALSE   502  'to 502'

 L.  80       450  LOAD_CLOSURE             'app'
              452  BUILD_TUPLE_1         1 
              454  LOAD_LISTCOMP            '<code_object <listcomp>>'
              456  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              458  MAKE_FUNCTION_8          'closure'

 L.  82       460  LOAD_GLOBAL              sorted
              462  LOAD_FAST                'invalid_attrs'
              464  LOAD_METHOD              keys
              466  CALL_METHOD_0         0  ''
              468  CALL_FUNCTION_1       1  ''

 L.  80       470  GET_ITER         
              472  CALL_FUNCTION_1       1  ''
              474  STORE_FAST               'invalid_attr_types_ui'

 L.  84       476  LOAD_STR                 'Wrong syntax in following attributes: %s'

 L.  85       478  LOAD_STR                 ', '
              480  LOAD_METHOD              join
              482  LOAD_LISTCOMP            '<code_object <listcomp>>'
              484  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              486  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  87       488  LOAD_FAST                'invalid_attr_types_ui'

 L.  85       490  GET_ITER         
              492  CALL_FUNCTION_1       1  ''
              494  CALL_METHOD_1         1  ''

 L.  84       496  BINARY_MODULO    
              498  STORE_FAST               'error_msg'
              500  JUMP_FORWARD        506  'to 506'
            502_0  COME_FROM           446  '446'

 L.  91       502  LOAD_STR                 ''
              504  STORE_FAST               'error_msg'
            506_0  COME_FROM           500  '500'

 L.  94       506  LOAD_STR                 'in_ft'
              508  LOAD_DEREF               'app'
              510  LOAD_ATTR                form
              512  LOAD_ATTR                input_field_names
              514  COMPARE_OP               in
          516_518  POP_JUMP_IF_TRUE    560  'to 560'

 L.  95       520  LOAD_STR                 'in_oc'
              522  LOAD_DEREF               'app'
              524  LOAD_ATTR                form
              526  LOAD_ATTR                input_field_names
              528  COMPARE_OP               in

 L.  94   530_532  POP_JUMP_IF_TRUE    560  'to 560'

 L.  96       534  LOAD_STR                 'in_mr'
              536  LOAD_DEREF               'app'
              538  LOAD_ATTR                form
              540  LOAD_ATTR                input_field_names
              542  COMPARE_OP               in

 L.  94   544_546  POP_JUMP_IF_TRUE    560  'to 560'

 L.  97       548  LOAD_FAST                'new_entry'

 L.  94   550_552  POP_JUMP_IF_FALSE   560  'to 560'

 L.  98       554  LOAD_FAST                'invalid_attrs'

 L.  94   556_558  POP_JUMP_IF_FALSE   586  'to 586'
            560_0  COME_FROM           550  '550'
            560_1  COME_FROM           544  '544'
            560_2  COME_FROM           530  '530'
            560_3  COME_FROM           516  '516'

 L.  99       560  LOAD_GLOBAL              web2ldap
              562  LOAD_ATTR                app
              564  LOAD_ATTR                addmodifyform
              566  LOAD_ATTR                w2l_modifyform

 L. 100       568  LOAD_DEREF               'app'

 L. 101       570  LOAD_FAST                'new_entry'

 L. 102       572  LOAD_FAST                'error_msg'

 L. 103       574  LOAD_FAST                'invalid_attrs'

 L.  99       576  LOAD_CONST               ('msg', 'invalid_attrs')
              578  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              580  POP_TOP          

 L. 105       582  LOAD_CONST               None
              584  RETURN_VALUE     
            586_0  COME_FROM           556  '556'

 L. 107       586  LOAD_SETCOMP             '<code_object <setcomp>>'
              588  LOAD_STR                 'w2l_modify.<locals>.<setcomp>'
              590  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              592  LOAD_DEREF               'app'
              594  LOAD_ATTR                form
              596  LOAD_METHOD              getInputValue
              598  LOAD_STR                 'in_oldattrtypes'
              600  BUILD_LIST_0          0 
              602  CALL_METHOD_2         2  ''
              604  GET_ITER         
              606  CALL_FUNCTION_1       1  ''
              608  STORE_DEREF              'in_oldattrtypes'

 L. 109       610  SETUP_FINALLY       644  'to 644'

 L. 110       612  LOAD_GLOBAL              web2ldap
              614  LOAD_ATTR                app
              616  LOAD_ATTR                addmodifyform
              618  LOAD_METHOD              read_old_entry
              620  LOAD_DEREF               'app'
              622  LOAD_DEREF               'app'
              624  LOAD_ATTR                dn
              626  LOAD_DEREF               'app'
              628  LOAD_ATTR                schema
              630  LOAD_FAST                'in_assertion'
              632  CALL_METHOD_4         4  ''
              634  UNPACK_SEQUENCE_2     2 
              636  STORE_FAST               'old_entry'
              638  STORE_FAST               'dummy'
              640  POP_BLOCK        
              642  JUMP_FORWARD        682  'to 682'
            644_0  COME_FROM_FINALLY   610  '610'

 L. 111       644  DUP_TOP          
              646  LOAD_GLOBAL              ldap0
              648  LOAD_ATTR                NO_SUCH_OBJECT
              650  COMPARE_OP               exception-match
          652_654  POP_JUMP_IF_FALSE   680  'to 680'
              656  POP_TOP          
              658  POP_TOP          
              660  POP_TOP          

 L. 112       662  LOAD_GLOBAL              web2ldap
              664  LOAD_ATTR                app
              666  LOAD_ATTR                core
              668  LOAD_METHOD              ErrorExit
              670  LOAD_STR                 'Old entry was removed or modified in between! You have to edit it again.'
              672  CALL_METHOD_1         1  ''
              674  RAISE_VARARGS_1       1  'exception instance'
              676  POP_EXCEPT       
              678  JUMP_FORWARD        682  'to 682'
            680_0  COME_FROM           652  '652'
              680  END_FINALLY      
            682_0  COME_FROM           678  '678'
            682_1  COME_FROM           642  '642'

 L. 115       682  LOAD_FAST                'new_entry'
              684  LOAD_METHOD              items
              686  CALL_METHOD_0         0  ''
              688  GET_ITER         
              690  FOR_ITER            720  'to 720'
              692  UNPACK_SEQUENCE_2     2 
              694  STORE_FAST               'attr_type'
              696  STORE_FAST               'attr_values'

 L. 116       698  LOAD_LISTCOMP            '<code_object <listcomp>>'
              700  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              702  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              704  LOAD_FAST                'attr_values'
              706  GET_ITER         
              708  CALL_FUNCTION_1       1  ''
              710  LOAD_FAST                'new_entry'
              712  LOAD_FAST                'attr_type'
              714  STORE_SUBSCR     
          716_718  JUMP_BACK           690  'to 690'

 L. 119       720  LOAD_GLOBAL              ldap0
              722  LOAD_ATTR                schema
              724  LOAD_ATTR                models
              726  LOAD_METHOD              SchemaElementOIDSet

 L. 120       728  LOAD_DEREF               'app'
              730  LOAD_ATTR                schema

 L. 121       732  LOAD_GLOBAL              AttributeType

 L. 122       734  LOAD_GLOBAL              web2ldap
              736  LOAD_ATTR                app
              738  LOAD_ATTR                add
              740  LOAD_ATTR                ADD_IGNORE_ATTR_TYPES

 L. 119       742  CALL_METHOD_3         3  ''
              744  STORE_FAST               'ignore_attr_types'

 L. 125       746  LOAD_DEREF               'app'
              748  LOAD_ATTR                ls
              750  LOAD_ATTR                relax_rules
          752_754  POP_JUMP_IF_TRUE    794  'to 794'

 L. 128       756  LOAD_FAST                'ignore_attr_types'
              758  LOAD_METHOD              update
              760  LOAD_DEREF               'app'
              762  LOAD_ATTR                schema
              764  LOAD_ATTR                no_user_mod_attr_oids
              766  CALL_METHOD_1         1  ''
              768  POP_TOP          

 L. 130       770  LOAD_FAST                'ignore_attr_types'
              772  LOAD_METHOD              update
              774  LOAD_GLOBAL              web2ldap
              776  LOAD_ATTR                app
              778  LOAD_ATTR                addmodifyform
              780  LOAD_METHOD              ConfiguredConstantAttributes
              782  LOAD_DEREF               'app'
              784  CALL_METHOD_1         1  ''
              786  LOAD_METHOD              values
              788  CALL_METHOD_0         0  ''
              790  CALL_METHOD_1         1  ''
              792  POP_TOP          
            794_0  COME_FROM           752  '752'

 L. 135       794  LOAD_FAST                'ignore_attr_types'
              796  LOAD_METHOD              update
              798  LOAD_CLOSURE             'in_oldattrtypes'
              800  BUILD_TUPLE_1         1 
              802  LOAD_LISTCOMP            '<code_object <listcomp>>'
              804  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              806  MAKE_FUNCTION_8          'closure'

 L. 137       808  LOAD_FAST                'old_entry'
              810  LOAD_METHOD              keys
              812  CALL_METHOD_0         0  ''

 L. 135       814  GET_ITER         
              816  CALL_FUNCTION_1       1  ''
              818  CALL_METHOD_1         1  ''
              820  POP_TOP          

 L. 141       822  LOAD_FAST                'old_entry'
              824  LOAD_METHOD              get_structural_oc
              826  CALL_METHOD_0         0  ''
              828  STORE_FAST               'old_entry_structural_oc'

 L. 143       830  LOAD_FAST                'old_entry'
              832  LOAD_METHOD              keys
              834  CALL_METHOD_0         0  ''
              836  GET_ITER         
            838_0  COME_FROM           862  '862'
              838  FOR_ITER            880  'to 880'
              840  STORE_FAST               'attr_type'

 L. 144       842  LOAD_GLOBAL              syntax_registry
              844  LOAD_METHOD              get_syntax
              846  LOAD_DEREF               'app'
              848  LOAD_ATTR                schema
              850  LOAD_FAST                'attr_type'
              852  LOAD_FAST                'old_entry_structural_oc'
              854  CALL_METHOD_3         3  ''
              856  STORE_FAST               'syntax_class'

 L. 145       858  LOAD_FAST                'syntax_class'
              860  LOAD_ATTR                editable
          862_864  POP_JUMP_IF_TRUE    838  'to 838'

 L. 146       866  LOAD_FAST                'ignore_attr_types'
              868  LOAD_METHOD              add
              870  LOAD_FAST                'attr_type'
              872  CALL_METHOD_1         1  ''
              874  POP_TOP          
          876_878  JUMP_BACK           838  'to 838'

 L. 148       880  LOAD_FAST                'ignore_attr_types'
              882  LOAD_METHOD              discard
              884  LOAD_STR                 '2.5.4.0'
              886  CALL_METHOD_1         1  ''
              888  POP_TOP          

 L. 149       890  LOAD_FAST                'ignore_attr_types'
              892  LOAD_METHOD              discard
              894  LOAD_STR                 'objectClass'
              896  CALL_METHOD_1         1  ''
              898  POP_TOP          

 L. 152       900  LOAD_GLOBAL              modify_modlist

 L. 153       902  LOAD_DEREF               'app'
              904  LOAD_ATTR                schema

 L. 154       906  LOAD_FAST                'old_entry'

 L. 154       908  LOAD_FAST                'new_entry'

 L. 155       910  LOAD_FAST                'ignore_attr_types'

 L. 156       912  LOAD_CONST               False

 L. 152       914  LOAD_CONST               ('ignore_attr_types', 'ignore_oldexistent')
              916  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              918  STORE_FAST               'modlist'

 L. 160       920  LOAD_FAST                'new_entry'
              922  LOAD_METHOD              get_structural_oc
              924  CALL_METHOD_0         0  ''
              926  STORE_FAST               'new_entry_structural_oc'

 L. 161       928  LOAD_FAST                'new_entry'
              930  LOAD_METHOD              keys
              932  CALL_METHOD_0         0  ''
              934  GET_ITER         
            936_0  COME_FROM           998  '998'
            936_1  COME_FROM           970  '970'
            936_2  COME_FROM           960  '960'
              936  FOR_ITER           1034  'to 1034'
              938  STORE_FAST               'attr_type'

 L. 162       940  LOAD_GLOBAL              syntax_registry
              942  LOAD_METHOD              get_syntax
              944  LOAD_DEREF               'app'
              946  LOAD_ATTR                schema
              948  LOAD_FAST                'attr_type'
              950  LOAD_FAST                'new_entry_structural_oc'
              952  CALL_METHOD_3         3  ''
              954  STORE_FAST               'syntax_class'

 L. 163       956  LOAD_FAST                'syntax_class'
              958  LOAD_ATTR                editable
          960_962  POP_JUMP_IF_TRUE    936  'to 936'

 L. 164       964  LOAD_FAST                'new_entry'
              966  LOAD_FAST                'attr_type'
              968  BINARY_SUBSCR    

 L. 163   970_972  POP_JUMP_IF_FALSE   936  'to 936'

 L. 165       974  LOAD_FAST                'attr_type'
              976  LOAD_FAST                'old_entry'
              978  COMPARE_OP               not-in

 L. 163   980_982  POP_JUMP_IF_TRUE   1002  'to 1002'

 L. 165       984  LOAD_FAST                'new_entry'
              986  LOAD_FAST                'attr_type'
              988  BINARY_SUBSCR    
              990  LOAD_FAST                'old_entry'
              992  LOAD_FAST                'attr_type'
              994  BINARY_SUBSCR    
              996  COMPARE_OP               !=

 L. 163  998_1000  POP_JUMP_IF_FALSE   936  'to 936'
           1002_0  COME_FROM           980  '980'

 L. 166      1002  LOAD_FAST                'modlist'
             1004  LOAD_METHOD              append
             1006  LOAD_GLOBAL              ldap0
             1008  LOAD_ATTR                MOD_REPLACE
             1010  LOAD_FAST                'attr_type'
             1012  LOAD_METHOD              encode
             1014  LOAD_STR                 'ascii'
             1016  CALL_METHOD_1         1  ''
             1018  LOAD_FAST                'new_entry'
             1020  LOAD_FAST                'attr_type'
             1022  BINARY_SUBSCR    
             1024  BUILD_TUPLE_3         3 
             1026  CALL_METHOD_1         1  ''
             1028  POP_TOP          
         1030_1032  JUMP_BACK           936  'to 936'

 L. 168      1034  LOAD_FAST                'modlist'
         1036_1038  POP_JUMP_IF_TRUE   1100  'to 1100'

 L. 170      1040  LOAD_DEREF               'app'
             1042  LOAD_ATTR                simple_message

 L. 171      1044  LOAD_STR                 'Modify result'

 L. 172      1046  LOAD_STR                 '<p class="SuccessMessage">No attributes modified of entry %s</p>'

 L. 173      1048  LOAD_DEREF               'app'
             1050  LOAD_ATTR                display_dn
             1052  LOAD_DEREF               'app'
             1054  LOAD_ATTR                dn
             1056  LOAD_CONST               True
             1058  LOAD_CONST               ('commandbutton',)
             1060  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 172      1062  BUILD_TUPLE_1         1 
             1064  BINARY_MODULO    

 L. 175      1066  LOAD_GLOBAL              web2ldap
             1068  LOAD_ATTR                app
             1070  LOAD_ATTR                gui
             1072  LOAD_METHOD              main_menu
             1074  LOAD_DEREF               'app'
             1076  CALL_METHOD_1         1  ''

 L. 176      1078  LOAD_GLOBAL              web2ldap
             1080  LOAD_ATTR                app
             1082  LOAD_ATTR                gui
             1084  LOAD_METHOD              ContextMenuSingleEntry
             1086  LOAD_DEREF               'app'
             1088  CALL_METHOD_1         1  ''

 L. 170      1090  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1092  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1094  POP_TOP          

 L. 178      1096  LOAD_CONST               None
             1098  RETURN_VALUE     
           1100_0  COME_FROM          1036  '1036'

 L. 182      1100  SETUP_FINALLY      1126  'to 1126'

 L. 183      1102  LOAD_DEREF               'app'
             1104  LOAD_ATTR                ls
             1106  LOAD_ATTR                modify

 L. 184      1108  LOAD_DEREF               'app'
             1110  LOAD_ATTR                dn

 L. 185      1112  LOAD_FAST                'modlist'

 L. 186      1114  LOAD_FAST                'in_assertion'

 L. 183      1116  LOAD_CONST               ('assertion_filter',)
             1118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1120  POP_TOP          
             1122  POP_BLOCK        
             1124  JUMP_FORWARD       1266  'to 1266'
           1126_0  COME_FROM_FINALLY  1100  '1100'

 L. 188      1126  DUP_TOP          
             1128  LOAD_GLOBAL              ldap0
             1130  LOAD_ATTR                ASSERTION_FAILED
             1132  COMPARE_OP               exception-match
         1134_1136  POP_JUMP_IF_FALSE  1162  'to 1162'
             1138  POP_TOP          
             1140  POP_TOP          
             1142  POP_TOP          

 L. 189      1144  LOAD_GLOBAL              web2ldap
             1146  LOAD_ATTR                app
             1148  LOAD_ATTR                core
             1150  LOAD_METHOD              ErrorExit

 L. 190      1152  LOAD_STR                 'Assertion failed => Entry was removed or modified in between! You have to edit it again.'

 L. 189      1154  CALL_METHOD_1         1  ''
             1156  RAISE_VARARGS_1       1  'exception instance'
             1158  POP_EXCEPT       
             1160  JUMP_FORWARD       1266  'to 1266'
           1162_0  COME_FROM          1134  '1134'

 L. 194      1162  DUP_TOP          

 L. 195      1164  LOAD_GLOBAL              ldap0
             1166  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 196      1168  LOAD_GLOBAL              ldap0
             1170  LOAD_ATTR                INVALID_DN_SYNTAX

 L. 197      1172  LOAD_GLOBAL              ldap0
             1174  LOAD_ATTR                INVALID_SYNTAX

 L. 198      1176  LOAD_GLOBAL              ldap0
             1178  LOAD_ATTR                NAMING_VIOLATION

 L. 199      1180  LOAD_GLOBAL              ldap0
             1182  LOAD_ATTR                OBJECT_CLASS_VIOLATION

 L. 200      1184  LOAD_GLOBAL              ldap0
             1186  LOAD_ATTR                OTHER

 L. 201      1188  LOAD_GLOBAL              ldap0
             1190  LOAD_ATTR                TYPE_OR_VALUE_EXISTS

 L. 202      1192  LOAD_GLOBAL              ldap0
             1194  LOAD_ATTR                UNDEFINED_TYPE

 L. 203      1196  LOAD_GLOBAL              ldap0
             1198  LOAD_ATTR                UNWILLING_TO_PERFORM

 L. 194      1200  BUILD_TUPLE_9         9 
             1202  COMPARE_OP               exception-match
         1204_1206  POP_JUMP_IF_FALSE  1264  'to 1264'
             1208  POP_TOP          
             1210  STORE_FAST               'e'
             1212  POP_TOP          
             1214  SETUP_FINALLY      1252  'to 1252'

 L. 206      1216  LOAD_GLOBAL              web2ldap
             1218  LOAD_ATTR                app
             1220  LOAD_ATTR                addmodifyform
             1222  LOAD_ATTR                w2l_modifyform

 L. 207      1224  LOAD_DEREF               'app'

 L. 208      1226  LOAD_FAST                'new_entry'

 L. 209      1228  LOAD_DEREF               'app'
             1230  LOAD_METHOD              ldap_error_msg
             1232  LOAD_FAST                'e'
             1234  CALL_METHOD_1         1  ''

 L. 206      1236  LOAD_CONST               ('msg',)
             1238  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1240  POP_TOP          

 L. 211      1242  POP_BLOCK        
             1244  POP_EXCEPT       
             1246  CALL_FINALLY       1252  'to 1252'
             1248  LOAD_CONST               None
             1250  RETURN_VALUE     
           1252_0  COME_FROM          1246  '1246'
           1252_1  COME_FROM_FINALLY  1214  '1214'
             1252  LOAD_CONST               None
             1254  STORE_FAST               'e'
             1256  DELETE_FAST              'e'
             1258  END_FINALLY      
             1260  POP_EXCEPT       
             1262  JUMP_FORWARD       1266  'to 1266'
           1264_0  COME_FROM          1204  '1204'
             1264  END_FINALLY      
           1266_0  COME_FROM          1262  '1262'
           1266_1  COME_FROM          1160  '1160'
           1266_2  COME_FROM          1124  '1124'

 L. 214      1266  LOAD_DEREF               'app'
             1268  LOAD_ATTR                simple_message

 L. 215      1270  LOAD_STR                 'Modify result'

 L. 216      1272  LOAD_STR                 '<p class="SuccessMessage">Modified entry %s</p><dt>LDIF change record:</dt>\n<dd>%s</dd>'

 L. 217      1274  LOAD_DEREF               'app'
             1276  LOAD_ATTR                display_dn
             1278  LOAD_DEREF               'app'
             1280  LOAD_ATTR                dn
             1282  LOAD_CONST               True
             1284  LOAD_CONST               ('commandbutton',)
             1286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 218      1288  LOAD_GLOBAL              modlist_ldif
             1290  LOAD_DEREF               'app'
             1292  LOAD_ATTR                dn
             1294  LOAD_DEREF               'app'
             1296  LOAD_ATTR                form
             1298  LOAD_FAST                'modlist'
             1300  CALL_FUNCTION_3       3  ''

 L. 216      1302  BUILD_TUPLE_2         2 
             1304  BINARY_MODULO    

 L. 220      1306  LOAD_GLOBAL              web2ldap
             1308  LOAD_ATTR                app
             1310  LOAD_ATTR                gui
             1312  LOAD_METHOD              main_menu
             1314  LOAD_DEREF               'app'
             1316  CALL_METHOD_1         1  ''

 L. 221      1318  LOAD_GLOBAL              web2ldap
             1320  LOAD_ATTR                app
             1322  LOAD_ATTR                gui
             1324  LOAD_METHOD              ContextMenuSingleEntry
             1326  LOAD_DEREF               'app'
             1328  CALL_METHOD_1         1  ''

 L. 214      1330  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1332  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1334  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 1246