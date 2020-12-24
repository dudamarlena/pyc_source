# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/modify.py
# Compiled at: 2020-05-04 07:51:32
# Size of source mod 2**32: 7739 bytes
"""
web2ldap.app.modify: modify an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

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

 L.  53         0  LOAD_FAST                'app'
                2  LOAD_ATTR                form
                4  LOAD_METHOD              getInputValue
                6  LOAD_STR                 'in_assertion'
                8  LOAD_STR                 '(objectClass=*)'
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_2         2  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'in_assertion'

 L.  55        20  LOAD_FAST                'app'
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
               72  LOAD_FAST                'app'
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

 L.  61       100  LOAD_FAST                'app'
              102  LOAD_ATTR                form
              104  LOAD_ATTR                field
              106  LOAD_STR                 'in_at'
              108  BINARY_SUBSCR    
              110  LOAD_ATTR                value
              112  LOAD_FAST                'del_row_num'
              114  BINARY_SUBSCR    
              116  LOAD_FAST                'app'
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

 L.  63       148  LOAD_FAST                'app'
              150  LOAD_ATTR                form
              152  LOAD_ATTR                field
              154  LOAD_STR                 'in_at'
              156  BINARY_SUBSCR    
              158  LOAD_ATTR                value
              160  LOAD_FAST                'del_row_num'
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'app'
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

 L.  65       188  LOAD_FAST                'app'
              190  LOAD_ATTR                form
              192  LOAD_ATTR                field
              194  LOAD_STR                 'in_at'
              196  BINARY_SUBSCR    
              198  LOAD_ATTR                value
              200  LOAD_METHOD              pop
              202  LOAD_FAST                'del_row_num'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L.  66       208  LOAD_FAST                'app'
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
              232  LOAD_FAST                'app'
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
              258  LOAD_FAST                'app'
              260  LOAD_ATTR                form
              262  LOAD_ATTR                field
              264  LOAD_STR                 'in_av'
              266  BINARY_SUBSCR    
              268  LOAD_ATTR                value
              270  CALL_FUNCTION_1       1  ''
              272  CALL_FUNCTION_2       2  ''
              274  CALL_FUNCTION_2       2  ''
              276  LOAD_FAST                'app'
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

 L.  73       320  LOAD_FAST                'app'
              322  LOAD_ATTR                form
              324  LOAD_ATTR                field
              326  LOAD_STR                 'in_at'
              328  BINARY_SUBSCR    
              330  LOAD_ATTR                value
              332  LOAD_METHOD              insert
              334  LOAD_FAST                'insert_row_num'
              336  LOAD_CONST               1
              338  BINARY_ADD       
              340  LOAD_FAST                'app'
              342  LOAD_ATTR                form
              344  LOAD_ATTR                field
              346  LOAD_STR                 'in_at'
              348  BINARY_SUBSCR    
              350  LOAD_ATTR                value
              352  LOAD_FAST                'insert_row_num'
              354  BINARY_SUBSCR    
              356  CALL_METHOD_2         2  ''
              358  POP_TOP          

 L.  74       360  LOAD_FAST                'app'
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
              396  LOAD_FAST                'app'
              398  LOAD_ATTR                form
              400  LOAD_ATTR                field
              402  LOAD_STR                 'in_av'
              404  BINARY_SUBSCR    
              406  LOAD_ATTR                value
              408  CALL_FUNCTION_1       1  ''
              410  CALL_FUNCTION_2       2  ''
              412  CALL_FUNCTION_2       2  ''
              414  LOAD_FAST                'app'
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
              434  LOAD_FAST                'app'
              436  CALL_METHOD_1         1  ''
              438  UNPACK_SEQUENCE_2     2 
              440  STORE_FAST               'new_entry'
              442  STORE_FAST               'invalid_attrs'

 L.  79       444  LOAD_FAST                'invalid_attrs'
          446_448  POP_JUMP_IF_FALSE   468  'to 468'

 L.  80       450  LOAD_GLOBAL              web2ldap
              452  LOAD_ATTR                app
              454  LOAD_ATTR                gui
              456  LOAD_METHOD              invalid_syntax_message
              458  LOAD_FAST                'app'
              460  LOAD_FAST                'invalid_attrs'
              462  CALL_METHOD_2         2  ''
              464  STORE_FAST               'error_msg'
              466  JUMP_FORWARD        472  'to 472'
            468_0  COME_FROM           446  '446'

 L.  82       468  LOAD_STR                 ''
              470  STORE_FAST               'error_msg'
            472_0  COME_FROM           466  '466'

 L.  85       472  LOAD_STR                 'in_ft'
              474  LOAD_FAST                'app'
              476  LOAD_ATTR                form
              478  LOAD_ATTR                input_field_names
              480  COMPARE_OP               in
          482_484  POP_JUMP_IF_TRUE    526  'to 526'

 L.  86       486  LOAD_STR                 'in_oc'
              488  LOAD_FAST                'app'
              490  LOAD_ATTR                form
              492  LOAD_ATTR                input_field_names
              494  COMPARE_OP               in

 L.  85   496_498  POP_JUMP_IF_TRUE    526  'to 526'

 L.  87       500  LOAD_STR                 'in_mr'
              502  LOAD_FAST                'app'
              504  LOAD_ATTR                form
              506  LOAD_ATTR                input_field_names
              508  COMPARE_OP               in

 L.  85   510_512  POP_JUMP_IF_TRUE    526  'to 526'

 L.  88       514  LOAD_FAST                'new_entry'

 L.  85   516_518  POP_JUMP_IF_FALSE   526  'to 526'

 L.  89       520  LOAD_FAST                'invalid_attrs'

 L.  85   522_524  POP_JUMP_IF_FALSE   552  'to 552'
            526_0  COME_FROM           516  '516'
            526_1  COME_FROM           510  '510'
            526_2  COME_FROM           496  '496'
            526_3  COME_FROM           482  '482'

 L.  90       526  LOAD_GLOBAL              web2ldap
              528  LOAD_ATTR                app
              530  LOAD_ATTR                addmodifyform
              532  LOAD_ATTR                w2l_modifyform

 L.  91       534  LOAD_FAST                'app'

 L.  92       536  LOAD_FAST                'new_entry'

 L.  93       538  LOAD_FAST                'error_msg'

 L.  94       540  LOAD_FAST                'invalid_attrs'

 L.  90       542  LOAD_CONST               ('msg', 'invalid_attrs')
              544  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              546  POP_TOP          

 L.  96       548  LOAD_CONST               None
              550  RETURN_VALUE     
            552_0  COME_FROM           522  '522'

 L.  98       552  LOAD_SETCOMP             '<code_object <setcomp>>'
              554  LOAD_STR                 'w2l_modify.<locals>.<setcomp>'
              556  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              558  LOAD_FAST                'app'
              560  LOAD_ATTR                form
              562  LOAD_METHOD              getInputValue
              564  LOAD_STR                 'in_oldattrtypes'
              566  BUILD_LIST_0          0 
              568  CALL_METHOD_2         2  ''
              570  GET_ITER         
              572  CALL_FUNCTION_1       1  ''
              574  STORE_DEREF              'in_oldattrtypes'

 L. 100       576  SETUP_FINALLY       610  'to 610'

 L. 101       578  LOAD_GLOBAL              web2ldap
              580  LOAD_ATTR                app
              582  LOAD_ATTR                addmodifyform
              584  LOAD_METHOD              read_old_entry
              586  LOAD_FAST                'app'
              588  LOAD_FAST                'app'
              590  LOAD_ATTR                dn
              592  LOAD_FAST                'app'
              594  LOAD_ATTR                schema
              596  LOAD_FAST                'in_assertion'
              598  CALL_METHOD_4         4  ''
              600  UNPACK_SEQUENCE_2     2 
              602  STORE_FAST               'old_entry'
              604  STORE_FAST               'dummy'
              606  POP_BLOCK        
              608  JUMP_FORWARD        648  'to 648'
            610_0  COME_FROM_FINALLY   576  '576'

 L. 102       610  DUP_TOP          
              612  LOAD_GLOBAL              ldap0
              614  LOAD_ATTR                NO_SUCH_OBJECT
              616  COMPARE_OP               exception-match
          618_620  POP_JUMP_IF_FALSE   646  'to 646'
              622  POP_TOP          
              624  POP_TOP          
              626  POP_TOP          

 L. 103       628  LOAD_GLOBAL              web2ldap
              630  LOAD_ATTR                app
              632  LOAD_ATTR                core
              634  LOAD_METHOD              ErrorExit
              636  LOAD_STR                 'Old entry was removed or modified in between! You have to edit it again.'
              638  CALL_METHOD_1         1  ''
              640  RAISE_VARARGS_1       1  'exception instance'
              642  POP_EXCEPT       
              644  JUMP_FORWARD        648  'to 648'
            646_0  COME_FROM           618  '618'
              646  END_FINALLY      
            648_0  COME_FROM           644  '644'
            648_1  COME_FROM           608  '608'

 L. 106       648  LOAD_FAST                'new_entry'
              650  LOAD_METHOD              items
              652  CALL_METHOD_0         0  ''
              654  GET_ITER         
              656  FOR_ITER            686  'to 686'
              658  UNPACK_SEQUENCE_2     2 
              660  STORE_FAST               'attr_type'
              662  STORE_FAST               'attr_values'

 L. 107       664  LOAD_LISTCOMP            '<code_object <listcomp>>'
              666  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              668  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              670  LOAD_FAST                'attr_values'
              672  GET_ITER         
              674  CALL_FUNCTION_1       1  ''
              676  LOAD_FAST                'new_entry'
              678  LOAD_FAST                'attr_type'
              680  STORE_SUBSCR     
          682_684  JUMP_BACK           656  'to 656'

 L. 110       686  LOAD_GLOBAL              ldap0
              688  LOAD_ATTR                schema
              690  LOAD_ATTR                models
              692  LOAD_METHOD              SchemaElementOIDSet

 L. 111       694  LOAD_FAST                'app'
              696  LOAD_ATTR                schema

 L. 112       698  LOAD_GLOBAL              AttributeType

 L. 113       700  LOAD_GLOBAL              web2ldap
              702  LOAD_ATTR                app
              704  LOAD_ATTR                add
              706  LOAD_ATTR                ADD_IGNORE_ATTR_TYPES

 L. 110       708  CALL_METHOD_3         3  ''
              710  STORE_FAST               'ignore_attr_types'

 L. 116       712  LOAD_FAST                'app'
              714  LOAD_ATTR                ls
              716  LOAD_ATTR                relax_rules
          718_720  POP_JUMP_IF_TRUE    760  'to 760'

 L. 119       722  LOAD_FAST                'ignore_attr_types'
              724  LOAD_METHOD              update
              726  LOAD_FAST                'app'
              728  LOAD_ATTR                schema
              730  LOAD_ATTR                no_user_mod_attr_oids
              732  CALL_METHOD_1         1  ''
              734  POP_TOP          

 L. 121       736  LOAD_FAST                'ignore_attr_types'
              738  LOAD_METHOD              update
              740  LOAD_GLOBAL              web2ldap
              742  LOAD_ATTR                app
              744  LOAD_ATTR                addmodifyform
              746  LOAD_METHOD              ConfiguredConstantAttributes
              748  LOAD_FAST                'app'
              750  CALL_METHOD_1         1  ''
              752  LOAD_METHOD              values
              754  CALL_METHOD_0         0  ''
              756  CALL_METHOD_1         1  ''
              758  POP_TOP          
            760_0  COME_FROM           718  '718'

 L. 126       760  LOAD_FAST                'ignore_attr_types'
              762  LOAD_METHOD              update
              764  LOAD_CLOSURE             'in_oldattrtypes'
              766  BUILD_TUPLE_1         1 
              768  LOAD_LISTCOMP            '<code_object <listcomp>>'
              770  LOAD_STR                 'w2l_modify.<locals>.<listcomp>'
              772  MAKE_FUNCTION_8          'closure'

 L. 128       774  LOAD_FAST                'old_entry'
              776  LOAD_METHOD              keys
              778  CALL_METHOD_0         0  ''

 L. 126       780  GET_ITER         
              782  CALL_FUNCTION_1       1  ''
              784  CALL_METHOD_1         1  ''
              786  POP_TOP          

 L. 132       788  LOAD_FAST                'old_entry'
              790  LOAD_METHOD              get_structural_oc
              792  CALL_METHOD_0         0  ''
              794  STORE_FAST               'old_entry_structural_oc'

 L. 134       796  LOAD_FAST                'old_entry'
              798  LOAD_METHOD              keys
              800  CALL_METHOD_0         0  ''
              802  GET_ITER         
            804_0  COME_FROM           828  '828'
              804  FOR_ITER            846  'to 846'
              806  STORE_FAST               'attr_type'

 L. 135       808  LOAD_GLOBAL              syntax_registry
              810  LOAD_METHOD              get_syntax
              812  LOAD_FAST                'app'
              814  LOAD_ATTR                schema
              816  LOAD_FAST                'attr_type'
              818  LOAD_FAST                'old_entry_structural_oc'
              820  CALL_METHOD_3         3  ''
              822  STORE_FAST               'syntax_class'

 L. 136       824  LOAD_FAST                'syntax_class'
              826  LOAD_ATTR                editable
          828_830  POP_JUMP_IF_TRUE    804  'to 804'

 L. 137       832  LOAD_FAST                'ignore_attr_types'
              834  LOAD_METHOD              add
              836  LOAD_FAST                'attr_type'
              838  CALL_METHOD_1         1  ''
              840  POP_TOP          
          842_844  JUMP_BACK           804  'to 804'

 L. 139       846  LOAD_FAST                'ignore_attr_types'
              848  LOAD_METHOD              discard
              850  LOAD_STR                 '2.5.4.0'
              852  CALL_METHOD_1         1  ''
              854  POP_TOP          

 L. 140       856  LOAD_FAST                'ignore_attr_types'
              858  LOAD_METHOD              discard
              860  LOAD_STR                 'objectClass'
              862  CALL_METHOD_1         1  ''
              864  POP_TOP          

 L. 143       866  LOAD_GLOBAL              modify_modlist

 L. 144       868  LOAD_FAST                'app'
              870  LOAD_ATTR                schema

 L. 145       872  LOAD_FAST                'old_entry'

 L. 145       874  LOAD_FAST                'new_entry'

 L. 146       876  LOAD_FAST                'ignore_attr_types'

 L. 147       878  LOAD_CONST               False

 L. 143       880  LOAD_CONST               ('ignore_attr_types', 'ignore_oldexistent')
              882  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              884  STORE_FAST               'modlist'

 L. 151       886  LOAD_FAST                'new_entry'
              888  LOAD_METHOD              get_structural_oc
              890  CALL_METHOD_0         0  ''
              892  STORE_FAST               'new_entry_structural_oc'

 L. 152       894  LOAD_FAST                'new_entry'
              896  LOAD_METHOD              keys
              898  CALL_METHOD_0         0  ''
              900  GET_ITER         
            902_0  COME_FROM           964  '964'
            902_1  COME_FROM           936  '936'
            902_2  COME_FROM           926  '926'
              902  FOR_ITER           1000  'to 1000'
              904  STORE_FAST               'attr_type'

 L. 153       906  LOAD_GLOBAL              syntax_registry
              908  LOAD_METHOD              get_syntax
              910  LOAD_FAST                'app'
              912  LOAD_ATTR                schema
              914  LOAD_FAST                'attr_type'
              916  LOAD_FAST                'new_entry_structural_oc'
              918  CALL_METHOD_3         3  ''
              920  STORE_FAST               'syntax_class'

 L. 154       922  LOAD_FAST                'syntax_class'
              924  LOAD_ATTR                editable
          926_928  POP_JUMP_IF_TRUE    902  'to 902'

 L. 155       930  LOAD_FAST                'new_entry'
              932  LOAD_FAST                'attr_type'
              934  BINARY_SUBSCR    

 L. 154   936_938  POP_JUMP_IF_FALSE   902  'to 902'

 L. 156       940  LOAD_FAST                'attr_type'
              942  LOAD_FAST                'old_entry'
              944  COMPARE_OP               not-in

 L. 154   946_948  POP_JUMP_IF_TRUE    968  'to 968'

 L. 156       950  LOAD_FAST                'new_entry'
              952  LOAD_FAST                'attr_type'
              954  BINARY_SUBSCR    
              956  LOAD_FAST                'old_entry'
              958  LOAD_FAST                'attr_type'
              960  BINARY_SUBSCR    
              962  COMPARE_OP               !=

 L. 154   964_966  POP_JUMP_IF_FALSE   902  'to 902'
            968_0  COME_FROM           946  '946'

 L. 157       968  LOAD_FAST                'modlist'
              970  LOAD_METHOD              append
              972  LOAD_GLOBAL              ldap0
              974  LOAD_ATTR                MOD_REPLACE
              976  LOAD_FAST                'attr_type'
              978  LOAD_METHOD              encode
              980  LOAD_STR                 'ascii'
              982  CALL_METHOD_1         1  ''
              984  LOAD_FAST                'new_entry'
              986  LOAD_FAST                'attr_type'
              988  BINARY_SUBSCR    
              990  BUILD_TUPLE_3         3 
              992  CALL_METHOD_1         1  ''
              994  POP_TOP          
          996_998  JUMP_BACK           902  'to 902'

 L. 159      1000  LOAD_FAST                'modlist'
         1002_1004  POP_JUMP_IF_TRUE   1066  'to 1066'

 L. 161      1006  LOAD_FAST                'app'
             1008  LOAD_ATTR                simple_message

 L. 162      1010  LOAD_STR                 'Modify result'

 L. 163      1012  LOAD_STR                 '<p class="SuccessMessage">No attributes modified of entry %s</p>'

 L. 164      1014  LOAD_FAST                'app'
             1016  LOAD_ATTR                display_dn
             1018  LOAD_FAST                'app'
             1020  LOAD_ATTR                dn
             1022  LOAD_CONST               True
             1024  LOAD_CONST               ('commandbutton',)
             1026  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 163      1028  BUILD_TUPLE_1         1 
             1030  BINARY_MODULO    

 L. 166      1032  LOAD_GLOBAL              web2ldap
             1034  LOAD_ATTR                app
             1036  LOAD_ATTR                gui
             1038  LOAD_METHOD              main_menu
             1040  LOAD_FAST                'app'
             1042  CALL_METHOD_1         1  ''

 L. 167      1044  LOAD_GLOBAL              web2ldap
             1046  LOAD_ATTR                app
             1048  LOAD_ATTR                gui
             1050  LOAD_METHOD              ContextMenuSingleEntry
             1052  LOAD_FAST                'app'
             1054  CALL_METHOD_1         1  ''

 L. 161      1056  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1058  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1060  POP_TOP          

 L. 169      1062  LOAD_CONST               None
             1064  RETURN_VALUE     
           1066_0  COME_FROM          1002  '1002'

 L. 173      1066  SETUP_FINALLY      1092  'to 1092'

 L. 174      1068  LOAD_FAST                'app'
             1070  LOAD_ATTR                ls
             1072  LOAD_ATTR                modify

 L. 175      1074  LOAD_FAST                'app'
             1076  LOAD_ATTR                dn

 L. 176      1078  LOAD_FAST                'modlist'

 L. 177      1080  LOAD_FAST                'in_assertion'

 L. 174      1082  LOAD_CONST               ('assertion_filter',)
             1084  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1086  POP_TOP          
             1088  POP_BLOCK        
             1090  JUMP_FORWARD       1232  'to 1232'
           1092_0  COME_FROM_FINALLY  1066  '1066'

 L. 179      1092  DUP_TOP          
             1094  LOAD_GLOBAL              ldap0
             1096  LOAD_ATTR                ASSERTION_FAILED
             1098  COMPARE_OP               exception-match
         1100_1102  POP_JUMP_IF_FALSE  1128  'to 1128'
             1104  POP_TOP          
             1106  POP_TOP          
             1108  POP_TOP          

 L. 180      1110  LOAD_GLOBAL              web2ldap
             1112  LOAD_ATTR                app
             1114  LOAD_ATTR                core
             1116  LOAD_METHOD              ErrorExit

 L. 181      1118  LOAD_STR                 'Assertion failed => Entry was removed or modified in between! You have to edit it again.'

 L. 180      1120  CALL_METHOD_1         1  ''
             1122  RAISE_VARARGS_1       1  'exception instance'
             1124  POP_EXCEPT       
             1126  JUMP_FORWARD       1232  'to 1232'
           1128_0  COME_FROM          1100  '1100'

 L. 185      1128  DUP_TOP          

 L. 186      1130  LOAD_GLOBAL              ldap0
             1132  LOAD_ATTR                CONSTRAINT_VIOLATION

 L. 187      1134  LOAD_GLOBAL              ldap0
             1136  LOAD_ATTR                INVALID_DN_SYNTAX

 L. 188      1138  LOAD_GLOBAL              ldap0
             1140  LOAD_ATTR                INVALID_SYNTAX

 L. 189      1142  LOAD_GLOBAL              ldap0
             1144  LOAD_ATTR                NAMING_VIOLATION

 L. 190      1146  LOAD_GLOBAL              ldap0
             1148  LOAD_ATTR                OBJECT_CLASS_VIOLATION

 L. 191      1150  LOAD_GLOBAL              ldap0
             1152  LOAD_ATTR                OTHER

 L. 192      1154  LOAD_GLOBAL              ldap0
             1156  LOAD_ATTR                TYPE_OR_VALUE_EXISTS

 L. 193      1158  LOAD_GLOBAL              ldap0
             1160  LOAD_ATTR                UNDEFINED_TYPE

 L. 194      1162  LOAD_GLOBAL              ldap0
             1164  LOAD_ATTR                UNWILLING_TO_PERFORM

 L. 185      1166  BUILD_TUPLE_9         9 
             1168  COMPARE_OP               exception-match
         1170_1172  POP_JUMP_IF_FALSE  1230  'to 1230'
             1174  POP_TOP          
             1176  STORE_FAST               'e'
             1178  POP_TOP          
             1180  SETUP_FINALLY      1218  'to 1218'

 L. 197      1182  LOAD_GLOBAL              web2ldap
             1184  LOAD_ATTR                app
             1186  LOAD_ATTR                addmodifyform
             1188  LOAD_ATTR                w2l_modifyform

 L. 198      1190  LOAD_FAST                'app'

 L. 199      1192  LOAD_FAST                'new_entry'

 L. 200      1194  LOAD_FAST                'app'
             1196  LOAD_METHOD              ldap_error_msg
             1198  LOAD_FAST                'e'
             1200  CALL_METHOD_1         1  ''

 L. 197      1202  LOAD_CONST               ('msg',)
             1204  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1206  POP_TOP          

 L. 202      1208  POP_BLOCK        
             1210  POP_EXCEPT       
             1212  CALL_FINALLY       1218  'to 1218'
             1214  LOAD_CONST               None
             1216  RETURN_VALUE     
           1218_0  COME_FROM          1212  '1212'
           1218_1  COME_FROM_FINALLY  1180  '1180'
             1218  LOAD_CONST               None
             1220  STORE_FAST               'e'
             1222  DELETE_FAST              'e'
             1224  END_FINALLY      
             1226  POP_EXCEPT       
             1228  JUMP_FORWARD       1232  'to 1232'
           1230_0  COME_FROM          1170  '1170'
             1230  END_FINALLY      
           1232_0  COME_FROM          1228  '1228'
           1232_1  COME_FROM          1126  '1126'
           1232_2  COME_FROM          1090  '1090'

 L. 205      1232  LOAD_FAST                'app'
             1234  LOAD_ATTR                simple_message

 L. 206      1236  LOAD_STR                 'Modify result'

 L. 207      1238  LOAD_STR                 '<p class="SuccessMessage">Modified entry %s</p><dt>LDIF change record:</dt>\n<dd>%s</dd>'

 L. 208      1240  LOAD_FAST                'app'
             1242  LOAD_ATTR                display_dn
             1244  LOAD_FAST                'app'
             1246  LOAD_ATTR                dn
             1248  LOAD_CONST               True
             1250  LOAD_CONST               ('commandbutton',)
             1252  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 209      1254  LOAD_GLOBAL              modlist_ldif
             1256  LOAD_FAST                'app'
             1258  LOAD_ATTR                dn
             1260  LOAD_FAST                'app'
             1262  LOAD_ATTR                form
             1264  LOAD_FAST                'modlist'
             1266  CALL_FUNCTION_3       3  ''

 L. 207      1268  BUILD_TUPLE_2         2 
             1270  BINARY_MODULO    

 L. 211      1272  LOAD_GLOBAL              web2ldap
             1274  LOAD_ATTR                app
             1276  LOAD_ATTR                gui
             1278  LOAD_METHOD              main_menu
             1280  LOAD_FAST                'app'
             1282  CALL_METHOD_1         1  ''

 L. 212      1284  LOAD_GLOBAL              web2ldap
             1286  LOAD_ATTR                app
             1288  LOAD_ATTR                gui
             1290  LOAD_METHOD              ContextMenuSingleEntry
             1292  LOAD_FAST                'app'
             1294  CALL_METHOD_1         1  ''

 L. 205      1296  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             1298  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1300  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 1212