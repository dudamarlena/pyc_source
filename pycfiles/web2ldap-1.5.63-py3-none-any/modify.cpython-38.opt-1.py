# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/modify.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 8045 bytes
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

 L. 107       586  LOAD_GLOBAL              set
              588  LOAD_LISTCOMP            '<code_object <listcomp>>'
              590  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              592  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 109       594  LOAD_DEREF               'app'
              596  LOAD_ATTR                form
              598  LOAD_METHOD              getInputValue
              600  LOAD_STR                 'in_oldattrtypes'
              602  BUILD_LIST_0          0 
              604  CALL_METHOD_2         2  ''

 L. 107       606  GET_ITER         
              608  CALL_FUNCTION_1       1  ''
              610  CALL_FUNCTION_1       1  ''
              612  STORE_DEREF              'in_oldattrtypes'

 L. 112       614  SETUP_FINALLY       648  'to 648'

 L. 113       616  LOAD_GLOBAL              web2ldap
              618  LOAD_ATTR                app
              620  LOAD_ATTR                addmodifyform
              622  LOAD_METHOD              read_old_entry
              624  LOAD_DEREF               'app'
              626  LOAD_DEREF               'app'
              628  LOAD_ATTR                dn
              630  LOAD_DEREF               'app'
              632  LOAD_ATTR                schema
              634  LOAD_FAST                'in_assertion'
              636  CALL_METHOD_4         4  ''
              638  UNPACK_SEQUENCE_2     2 
              640  STORE_FAST               'old_entry'
              642  STORE_FAST               'dummy'
              644  POP_BLOCK        
              646  JUMP_FORWARD        686  'to 686'
            648_0  COME_FROM_FINALLY   614  '614'

 L. 114       648  DUP_TOP          
              650  LOAD_GLOBAL              ldap0
              652  LOAD_ATTR                NO_SUCH_OBJECT
              654  COMPARE_OP               exception-match
          656_658  POP_JUMP_IF_FALSE   684  'to 684'
              660  POP_TOP          
              662  POP_TOP          
              664  POP_TOP          

 L. 115       666  LOAD_GLOBAL              web2ldap
              668  LOAD_ATTR                app
              670  LOAD_ATTR                core
              672  LOAD_METHOD              ErrorExit
              674  LOAD_STR                 'Old entry was removed or modified in between! You have to edit it again.'
              676  CALL_METHOD_1         1  ''
              678  RAISE_VARARGS_1       1  'exception instance'
              680  POP_EXCEPT       
              682  JUMP_FORWARD        686  'to 686'
            684_0  COME_FROM           656  '656'
              684  END_FINALLY      
            686_0  COME_FROM           682  '682'
            686_1  COME_FROM           646  '646'

 L. 118       686  LOAD_FAST                'new_entry'
              688  LOAD_METHOD              items
              690  CALL_METHOD_0         0  ''
              692  GET_ITER         
              694  FOR_ITER            724  'to 724'
              696  UNPACK_SEQUENCE_2     2 
              698  STORE_FAST               'attr_type'
              700  STORE_FAST               'attr_values'

 L. 119       702  LOAD_LISTCOMP            '<code_object <listcomp>>'
              704  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              706  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              708  LOAD_FAST                'attr_values'
              710  GET_ITER         
              712  CALL_FUNCTION_1       1  ''
              714  LOAD_FAST                'new_entry'
              716  LOAD_FAST                'attr_type'
              718  STORE_SUBSCR     
          720_722  JUMP_BACK           694  'to 694'

 L. 122       724  LOAD_GLOBAL              ldap0
              726  LOAD_ATTR                schema
              728  LOAD_ATTR                models
              730  LOAD_METHOD              SchemaElementOIDSet

 L. 123       732  LOAD_DEREF               'app'
              734  LOAD_ATTR                schema

 L. 124       736  LOAD_GLOBAL              AttributeType

 L. 125       738  LOAD_GLOBAL              web2ldap
              740  LOAD_ATTR                app
              742  LOAD_ATTR                add
              744  LOAD_ATTR                ADD_IGNORE_ATTR_TYPES

 L. 122       746  CALL_METHOD_3         3  ''
              748  STORE_FAST               'ignore_attr_types'

 L. 128       750  LOAD_DEREF               'app'
              752  LOAD_ATTR                ls
              754  LOAD_ATTR                relax_rules
          756_758  POP_JUMP_IF_TRUE    798  'to 798'

 L. 131       760  LOAD_FAST                'ignore_attr_types'
              762  LOAD_METHOD              update
              764  LOAD_DEREF               'app'
              766  LOAD_ATTR                schema
              768  LOAD_ATTR                no_user_mod_attr_oids
              770  CALL_METHOD_1         1  ''
              772  POP_TOP          

 L. 133       774  LOAD_FAST                'ignore_attr_types'
              776  LOAD_METHOD              update
              778  LOAD_GLOBAL              web2ldap
              780  LOAD_ATTR                app
              782  LOAD_ATTR                addmodifyform
              784  LOAD_METHOD              ConfiguredConstantAttributes
              786  LOAD_DEREF               'app'
              788  CALL_METHOD_1         1  ''
              790  LOAD_METHOD              values
              792  CALL_METHOD_0         0  ''
              794  CALL_METHOD_1         1  ''
              796  POP_TOP          
            798_0  COME_FROM           756  '756'

 L. 138       798  LOAD_FAST                'ignore_attr_types'
              800  LOAD_METHOD              update
              802  LOAD_CLOSURE             'in_oldattrtypes'
              804  BUILD_TUPLE_1         1 
              806  LOAD_LISTCOMP            '<code_object <listcomp>>'
              808  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              810  MAKE_FUNCTION_8          'closure'

 L. 140       812  LOAD_FAST                'old_entry'
              814  LOAD_METHOD              keys
              816  CALL_METHOD_0         0  ''

 L. 138       818  GET_ITER         
              820  CALL_FUNCTION_1       1  ''
              822  CALL_METHOD_1         1  ''
              824  POP_TOP          

 L. 144       826  LOAD_FAST                'old_entry'
              828  LOAD_METHOD              get_structural_oc
              830  CALL_METHOD_0         0  ''
              832  STORE_FAST               'old_entry_structural_oc'

 L. 146       834  LOAD_FAST                'old_entry'
              836  LOAD_METHOD              keys
              838  CALL_METHOD_0         0  ''
              840  GET_ITER         
            842_0  COME_FROM           866  '866'
              842  FOR_ITER            884  'to 884'
              844  STORE_FAST               'attr_type'

 L. 147       846  LOAD_GLOBAL              syntax_registry
              848  LOAD_METHOD              get_syntax
              850  LOAD_DEREF               'app'
              852  LOAD_ATTR                schema
              854  LOAD_FAST                'attr_type'
              856  LOAD_FAST                'old_entry_structural_oc'
              858  CALL_METHOD_3         3  ''
              860  STORE_FAST               'syntax_class'

 L. 148       862  LOAD_FAST                'syntax_class'
              864  LOAD_ATTR                editable
          866_868  POP_JUMP_IF_TRUE    842  'to 842'

 L. 149       870  LOAD_FAST                'ignore_attr_types'
              872  LOAD_METHOD              add
              874  LOAD_FAST                'attr_type'
              876  CALL_METHOD_1         1  ''
              878  POP_TOP          
          880_882  JUMP_BACK           842  'to 842'

 L. 151       884  LOAD_FAST                'ignore_attr_types'
              886  LOAD_METHOD              discard
              888  LOAD_STR                 '2.5.4.0'
              890  CALL_METHOD_1         1  ''
              892  POP_TOP          

 L. 152       894  LOAD_FAST                'ignore_attr_types'
              896  LOAD_METHOD              discard
              898  LOAD_STR                 'objectClass'
              900  CALL_METHOD_1         1  ''
              902  POP_TOP          

 L. 155       904  LOAD_GLOBAL              modify_modlist

 L. 156       906  LOAD_DEREF               'app'
              908  LOAD_ATTR                schema

 L. 157       910  LOAD_FAST                'old_entry'

 L. 157       912  LOAD_FAST                'new_entry'

 L. 158       914  LOAD_FAST                'ignore_attr_types'

 L. 159       916  LOAD_CONST               False

 L. 155       918  LOAD_CONST               ('ignore_attr_types', 'ignore_oldexistent')
              920  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              922  STORE_FAST               'modlist'

 L. 163       924  LOAD_FAST                'new_entry'
              926  LOAD_METHOD              get_structural_oc
              928  CALL_METHOD_0         0  ''
              930  STORE_FAST               'new_entry_structural_oc'

 L. 164       932  LOAD_FAST                'new_entry'
              934  LOAD_METHOD              keys
              936  CALL_METHOD_0         0  ''
              938  GET_ITER         
            940_0  COME_FROM          1002  '1002'
            940_1  COME_FROM           974  '974'
            940_2  COME_FROM           964  '964'
              940  FOR_ITER           1038  'to 1038'
              942  STORE_FAST               'attr_type'

 L. 165       944  LOAD_GLOBAL              syntax_registry
              946  LOAD_METHOD              get_syntax
              948  LOAD_DEREF               'app'
              950  LOAD_ATTR                schema
              952  LOAD_FAST                'attr_type'
              954  LOAD_FAST                'new_entry_structural_oc'
              956  CALL_METHOD_3         3  ''
              958  STORE_FAST               'syntax_class'

 L. 166       960  LOAD_FAST                'syntax_class'
              962  LOAD_ATTR                editable
          964_966  POP_JUMP_IF_TRUE    940  'to 940'

 L. 167       968  LOAD_FAST                'new_entry'
              970  LOAD_FAST                'attr_type'
              972  BINARY_SUBSCR    

 L. 166   974_976  POP_JUMP_IF_FALSE   940  'to 940'

 L. 168       978  LOAD_FAST                'attr_type'
              980  LOAD_FAST                'old_entry'
              982  COMPARE_OP               not-in

 L. 166   984_986  POP_JUMP_IF_TRUE   1006  'to 1006'

 L. 168       988  LOAD_FAST                'new_entry'
              990  LOAD_FAST                'attr_type'
              992  BINARY_SUBSCR    
              994  LOAD_FAST                'old_entry'
              996  LOAD_FAST                'attr_type'
              998  BINARY_SUBSCR    
             1000  COMPARE_OP               !=

 L. 166  1002_1004  POP_JUMP_IF_FALSE   940  'to 940'
           1006_0  COME_FROM           984  '984'

 L. 169      1006  LOAD_FAST                'modlist'
             1008  LOAD_METHOD              append
             1010  LOAD_GLOBAL              ldap0
             1012  LOAD_ATTR                MOD_REPLACE
             1014  LOAD_FAST                'attr_type'
             1016  LOAD_METHOD              encode
             1018  LOAD_STR                 'ascii'
             1020  CALL_METHOD_1         1  ''
             1022  LOAD_FAST                'new_entry'
             1024  LOAD_FAST                'attr_type'
             1026  BINARY_SUBSCR    
             1028  BUILD_TUPLE_3         3 
             1030  CALL_METHOD_1         1  ''
             1032  POP_TOP          
         1034_1036  JUMP_BACK           940  'to 940'

 L. 171      1038  LOAD_FAST                'modlist'
         1040_1042  POP_JUMP_IF_TRUE   1104  'to 1104'

 L. 173      1044  LOAD_DEREF               'app'
             1046  LOAD_ATTR                simple_message

 L. 174      1048  LOAD_STR                 'Modify result'

 L. 175      1050  LOAD_STR                 '<p class="SuccessMessage">No attributes modified of entry %s</p>'

 L. 176      1052  LOAD_DEREF               'app'
             1054  LOAD_ATTR                display_dn
             1056  LOAD_DEREF               'app'
             1058  LOAD_ATTR                dn
             1060  LOAD_CONST               True
             1062  LOAD_CONST               ('commandbutton',)
             1064  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 175      1066  BUILD_TUPLE_1         1 
             1068  BINARY_MODULO    

 L. 178      1070  LOAD_GLOBAL              web2ldap
             1072  LOAD_ATTR                app
             1074  LOAD_ATTR                gui
             1076  LOAD_METHOD              main_menu
             1078  LOAD_DEREF               'app'
             1080  CALL_METHOD_1         1  ''

 L. 179      1082  LOAD_GLOBAL              web2ldap
             1084  LOAD_ATTR                app
             1086  LOAD_ATTR                gui
             1088  LOAD_METHOD              ContextMenuSingleEntry
             1090  LOAD_DEREF               'app'
             1092  CALL_METHOD_1         1  ''

 L. 173      1094  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1096  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1098  POP_TOP          

 L. 181      1100  LOAD_CONST               None
             1102  RETURN_VALUE     
           1104_0  COME_FROM          1040  '1040'

 L. 185      1104  SETUP_FINALLY      1130  'to 1130'

 L. 186      1106  LOAD_DEREF               'app'
             1108  LOAD_ATTR                ls
             1110  LOAD_ATTR                modify

 L. 187      1112  LOAD_DEREF               'app'
             1114  LOAD_ATTR                dn

 L. 188      1116  LOAD_FAST                'modlist'

 L. 189      1118  LOAD_FAST                'in_assertion'

 L. 186      1120  LOAD_CONST               ('assertion_filter',)
             1122  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1124  POP_TOP          
             1126  POP_BLOCK        
             1128  JUMP_FORWARD       1270  'to 1270'
           1130_0  COME_FROM_FINALLY  1104  '1104'

 L. 191      1130  DUP_TOP          
             1132  LOAD_GLOBAL              ldap0
             1134  LOAD_ATTR                ASSERTION_FAILED
             1136  COMPARE_OP               exception-match
         1138_1140  POP_JUMP_IF_FALSE  1166  'to 1166'
             1142  POP_TOP          
             1144  POP_TOP          
             1146  POP_TOP          

 L. 192      1148  LOAD_GLOBAL              web2ldap
             1150  LOAD_ATTR                app
             1152  LOAD_ATTR                core
             1154  LOAD_METHOD              ErrorExit

 L. 193      1156  LOAD_STR                 'Assertion failed => Entry was removed or modified in between! You have to edit it again.'

 L. 192      1158  CALL_METHOD_1         1  ''
             1160  RAISE_VARARGS_1       1  'exception instance'
             1162  POP_EXCEPT       
             1164  JUMP_FORWARD       1270  'to 1270'
           1166_0  COME_FROM          1138  '1138'

 L. 197      1166  DUP_TOP          

 L. 198      1168  LOAD_GLOBAL              ldap0
             1170  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 199      1172  LOAD_GLOBAL              ldap0
             1174  LOAD_ATTR                INVALID_DN_SYNTAX

 L. 200      1176  LOAD_GLOBAL              ldap0
             1178  LOAD_ATTR                INVALID_SYNTAX

 L. 201      1180  LOAD_GLOBAL              ldap0
             1182  LOAD_ATTR                NAMING_VIOLATION

 L. 202      1184  LOAD_GLOBAL              ldap0
             1186  LOAD_ATTR                OBJECT_CLASS_VIOLATION

 L. 203      1188  LOAD_GLOBAL              ldap0
             1190  LOAD_ATTR                OTHER

 L. 204      1192  LOAD_GLOBAL              ldap0
             1194  LOAD_ATTR                TYPE_OR_VALUE_EXISTS

 L. 205      1196  LOAD_GLOBAL              ldap0
             1198  LOAD_ATTR                UNDEFINED_TYPE

 L. 206      1200  LOAD_GLOBAL              ldap0
             1202  LOAD_ATTR                UNWILLING_TO_PERFORM

 L. 197      1204  BUILD_TUPLE_9         9 
             1206  COMPARE_OP               exception-match
         1208_1210  POP_JUMP_IF_FALSE  1268  'to 1268'
             1212  POP_TOP          
             1214  STORE_FAST               'e'
             1216  POP_TOP          
             1218  SETUP_FINALLY      1256  'to 1256'

 L. 209      1220  LOAD_GLOBAL              web2ldap
             1222  LOAD_ATTR                app
             1224  LOAD_ATTR                addmodifyform
             1226  LOAD_ATTR                w2l_modifyform

 L. 210      1228  LOAD_DEREF               'app'

 L. 211      1230  LOAD_FAST                'new_entry'

 L. 212      1232  LOAD_DEREF               'app'
             1234  LOAD_METHOD              ldap_error_msg
             1236  LOAD_FAST                'e'
             1238  CALL_METHOD_1         1  ''

 L. 209      1240  LOAD_CONST               ('msg',)
             1242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1244  POP_TOP          

 L. 214      1246  POP_BLOCK        
             1248  POP_EXCEPT       
             1250  CALL_FINALLY       1256  'to 1256'
             1252  LOAD_CONST               None
             1254  RETURN_VALUE     
           1256_0  COME_FROM          1250  '1250'
           1256_1  COME_FROM_FINALLY  1218  '1218'
             1256  LOAD_CONST               None
             1258  STORE_FAST               'e'
             1260  DELETE_FAST              'e'
             1262  END_FINALLY      
             1264  POP_EXCEPT       
             1266  JUMP_FORWARD       1270  'to 1270'
           1268_0  COME_FROM          1208  '1208'
             1268  END_FINALLY      
           1270_0  COME_FROM          1266  '1266'
           1270_1  COME_FROM          1164  '1164'
           1270_2  COME_FROM          1128  '1128'

 L. 217      1270  LOAD_DEREF               'app'
             1272  LOAD_ATTR                simple_message

 L. 218      1274  LOAD_STR                 'Modify result'

 L. 219      1276  LOAD_STR                 '<p class="SuccessMessage">Modified entry %s</p><dt>LDIF change record:</dt>\n<dd>%s</dd>'

 L. 220      1278  LOAD_DEREF               'app'
             1280  LOAD_ATTR                display_dn
             1282  LOAD_DEREF               'app'
             1284  LOAD_ATTR                dn
             1286  LOAD_CONST               True
             1288  LOAD_CONST               ('commandbutton',)
             1290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 221      1292  LOAD_GLOBAL              modlist_ldif
             1294  LOAD_DEREF               'app'
             1296  LOAD_ATTR                dn
             1298  LOAD_DEREF               'app'
             1300  LOAD_ATTR                form
             1302  LOAD_FAST                'modlist'
             1304  CALL_FUNCTION_3       3  ''

 L. 219      1306  BUILD_TUPLE_2         2 
             1308  BINARY_MODULO    

 L. 223      1310  LOAD_GLOBAL              web2ldap
             1312  LOAD_ATTR                app
             1314  LOAD_ATTR                gui
             1316  LOAD_METHOD              main_menu
             1318  LOAD_DEREF               'app'
             1320  CALL_METHOD_1         1  ''

 L. 224      1322  LOAD_GLOBAL              web2ldap
             1324  LOAD_ATTR                app
             1326  LOAD_ATTR                gui
             1328  LOAD_METHOD              ContextMenuSingleEntry
             1330  LOAD_DEREF               'app'
             1332  CALL_METHOD_1         1  ''

 L. 217      1334  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1336  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1338  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 1250