# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/referral.py
# Compiled at: 2020-05-04 07:51:22
# Size of source mod 2**32: 3580 bytes
"""
web2ldap.app.referral: chase LDAP referrals

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time
from ldap0.ldapurl import LDAPUrl
import web2ldap.app.core, web2ldap.app.gui, web2ldap.app.cnf
ERR_MSG_DIV = '\n<h1>Error</h1>\n<p class="ErrorMessage">\n  %s\n</p>\n'

def w2l_chasereferral--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL              web2ldap
                2  LOAD_ATTR                app
                4  LOAD_ATTR                gui
                6  LOAD_ATTR                top_section

 L.  36         8  LOAD_FAST                'app'

 L.  37        10  LOAD_STR                 'Referral received'

 L.  38        12  LOAD_GLOBAL              web2ldap
               14  LOAD_ATTR                app
               16  LOAD_ATTR                gui
               18  LOAD_METHOD              main_menu
               20  LOAD_FAST                'app'
               22  CALL_METHOD_1         1  ''

 L.  39        24  BUILD_LIST_0          0 

 L.  35        26  LOAD_CONST               ('context_menu_list',)
               28  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               30  POP_TOP          

 L.  43        32  SETUP_FINALLY        82  'to 82'

 L.  44        34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 'w2l_chasereferral.<locals>.<listcomp>'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  46        40  LOAD_FAST                'ref_exc'
               42  LOAD_ATTR                args
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_METHOD              get
               50  LOAD_STR                 'info'
               52  LOAD_CONST               b''
               54  CALL_METHOD_2         2  ''
               56  LOAD_METHOD              decode
               58  LOAD_FAST                'app'
               60  LOAD_ATTR                ls
               62  LOAD_ATTR                charset
               64  CALL_METHOD_1         1  ''
               66  LOAD_METHOD              split
               68  LOAD_STR                 '\n'
               70  CALL_METHOD_1         1  ''

 L.  44        72  GET_ITER         
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'ldap_url_info'
               78  POP_BLOCK        
               80  JUMP_FORWARD        156  'to 156'
             82_0  COME_FROM_FINALLY    32  '32'

 L.  48        82  DUP_TOP          
               84  LOAD_GLOBAL              ValueError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   154  'to 154'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.  49        96  LOAD_FAST                'app'
               98  LOAD_ATTR                outf
              100  LOAD_METHOD              write

 L.  50       102  LOAD_GLOBAL              ERR_MSG_DIV

 L.  51       104  LOAD_STR                 'Error extracting referral LDAP URL from %s.'

 L.  52       106  LOAD_FAST                'app'
              108  LOAD_ATTR                form
              110  LOAD_METHOD              utf2display
              112  LOAD_GLOBAL              str
              114  LOAD_GLOBAL              repr
              116  LOAD_FAST                'ref_exc'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_STR                 'ascii'
              122  CALL_FUNCTION_2       2  ''
              124  CALL_METHOD_1         1  ''

 L.  51       126  BINARY_MODULO    

 L.  50       128  BINARY_MODULO    

 L.  49       130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.  56       134  LOAD_GLOBAL              web2ldap
              136  LOAD_ATTR                app
              138  LOAD_ATTR                gui
              140  LOAD_METHOD              footer
              142  LOAD_FAST                'app'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L.  57       148  POP_EXCEPT       
              150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM            88  '88'
              154  END_FINALLY      
            156_0  COME_FROM            80  '80'

 L.  59       156  SETUP_FINALLY       170  'to 170'

 L.  60       158  LOAD_FAST                'ldap_url_info'
              160  LOAD_CONST               1
              162  BINARY_SUBSCR    
              164  STORE_FAST               'ldap_url_info'
              166  POP_BLOCK        
              168  JUMP_FORWARD        244  'to 244'
            170_0  COME_FROM_FINALLY   156  '156'

 L.  61       170  DUP_TOP          
              172  LOAD_GLOBAL              IndexError
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   242  'to 242'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          

 L.  62       184  LOAD_FAST                'app'
              186  LOAD_ATTR                outf
              188  LOAD_METHOD              write

 L.  63       190  LOAD_GLOBAL              ERR_MSG_DIV

 L.  64       192  LOAD_STR                 'Error extracting referral LDAP URL from %s.'

 L.  65       194  LOAD_FAST                'app'
              196  LOAD_ATTR                form
              198  LOAD_METHOD              utf2display
              200  LOAD_GLOBAL              repr
              202  LOAD_FAST                'ldap_url_info'
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_METHOD              decode
              208  LOAD_STR                 'ascii'
              210  CALL_METHOD_1         1  ''
              212  CALL_METHOD_1         1  ''

 L.  64       214  BINARY_MODULO    

 L.  63       216  BINARY_MODULO    

 L.  62       218  CALL_METHOD_1         1  ''
              220  POP_TOP          

 L.  69       222  LOAD_GLOBAL              web2ldap
              224  LOAD_ATTR                app
              226  LOAD_ATTR                gui
              228  LOAD_METHOD              footer
              230  LOAD_FAST                'app'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L.  70       236  POP_EXCEPT       
              238  LOAD_CONST               None
              240  RETURN_VALUE     
            242_0  COME_FROM           176  '176'
              242  END_FINALLY      
            244_0  COME_FROM           168  '168'

 L.  73       244  SETUP_FINALLY       272  'to 272'

 L.  74       246  LOAD_GLOBAL              LDAPUrl
              248  LOAD_FAST                'ldap_url_info'
              250  LOAD_FAST                'ldap_url_info'
              252  LOAD_METHOD              find
              254  LOAD_STR                 'ldap:'
              256  CALL_METHOD_1         1  ''
              258  LOAD_CONST               None
              260  BUILD_SLICE_2         2 
              262  BINARY_SUBSCR    
              264  CALL_FUNCTION_1       1  ''
              266  STORE_FAST               'ref_url'
              268  POP_BLOCK        
              270  JUMP_FORWARD        388  'to 388'
            272_0  COME_FROM_FINALLY   244  '244'

 L.  75       272  DUP_TOP          
              274  LOAD_GLOBAL              ValueError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   386  'to 386'
              282  POP_TOP          
              284  STORE_FAST               'value_error'
              286  POP_TOP          
              288  SETUP_FINALLY       374  'to 374'

 L.  76       290  LOAD_FAST                'app'
              292  LOAD_ATTR                outf
              294  LOAD_METHOD              write

 L.  77       296  LOAD_GLOBAL              ERR_MSG_DIV

 L.  78       298  LOAD_STR                 'Error parsing referral URL %s: %s'

 L.  79       300  LOAD_FAST                'app'
              302  LOAD_ATTR                form
              304  LOAD_METHOD              utf2display
              306  LOAD_GLOBAL              repr
              308  LOAD_FAST                'ldap_url_info'
              310  CALL_FUNCTION_1       1  ''
              312  LOAD_METHOD              decode
              314  LOAD_STR                 'ascii'
              316  CALL_METHOD_1         1  ''
              318  CALL_METHOD_1         1  ''

 L.  80       320  LOAD_FAST                'app'
              322  LOAD_ATTR                form
              324  LOAD_METHOD              utf2display
              326  LOAD_GLOBAL              str
              328  LOAD_FAST                'value_error'
              330  CALL_FUNCTION_1       1  ''
              332  LOAD_METHOD              decode
              334  LOAD_STR                 'ascii'
              336  CALL_METHOD_1         1  ''
              338  CALL_METHOD_1         1  ''

 L.  78       340  BUILD_TUPLE_2         2 
              342  BINARY_MODULO    

 L.  77       344  BINARY_MODULO    

 L.  76       346  CALL_METHOD_1         1  ''
              348  POP_TOP          

 L.  84       350  LOAD_GLOBAL              web2ldap
              352  LOAD_ATTR                app
              354  LOAD_ATTR                gui
              356  LOAD_METHOD              footer
              358  LOAD_FAST                'app'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

 L.  85       364  POP_BLOCK        
              366  POP_EXCEPT       
              368  CALL_FINALLY        374  'to 374'
              370  LOAD_CONST               None
              372  RETURN_VALUE     
            374_0  COME_FROM           368  '368'
            374_1  COME_FROM_FINALLY   288  '288'
              374  LOAD_CONST               None
              376  STORE_FAST               'value_error'
              378  DELETE_FAST              'value_error'
              380  END_FINALLY      
              382  POP_EXCEPT       
              384  JUMP_FORWARD        388  'to 388'
            386_0  COME_FROM           278  '278'
              386  END_FINALLY      
            388_0  COME_FROM           384  '384'
            388_1  COME_FROM           270  '270'

 L.  87       388  LOAD_GLOBAL              web2ldap
              390  LOAD_ATTR                app
              392  LOAD_ATTR                gui
              394  LOAD_METHOD              read_template

 L.  88       396  LOAD_FAST                'app'

 L.  88       398  LOAD_STR                 'login_template'

 L.  88       400  LOAD_STR                 'referral login form'

 L.  87       402  CALL_METHOD_3         3  ''
              404  STORE_FAST               'login_template_str'

 L.  91       406  LOAD_GLOBAL              web2ldap
              408  LOAD_ATTR                app
              410  LOAD_ATTR                gui
              412  LOAD_ATTR                search_root_field

 L.  92       414  LOAD_FAST                'app'

 L.  93       416  LOAD_STR                 'login_search_root'

 L.  91       418  LOAD_CONST               ('name',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  STORE_FAST               'login_search_root_field'

 L.  95       424  LOAD_FAST                'login_template_str'
              426  LOAD_ATTR                format

 L.  96       428  LOAD_FAST                'app'
              430  LOAD_ATTR                form
              432  LOAD_ATTR                field
              434  LOAD_STR                 'login_mech'
              436  BINARY_SUBSCR    
              438  LOAD_METHOD              input_html
              440  CALL_METHOD_0         0  ''

 L.  97       442  LOAD_FAST                'app'
              444  LOAD_ATTR                form
              446  LOAD_METHOD              utf2display
              448  LOAD_FAST                'app'
              450  LOAD_ATTR                ls
              452  LOAD_ATTR                who
              454  CALL_METHOD_1         1  ''

 L.  98       456  LOAD_FAST                'app'
              458  LOAD_ATTR                form
              460  LOAD_METHOD              utf2display
              462  LOAD_FAST                'app'
              464  LOAD_ATTR                binddn_mapping
              466  CALL_METHOD_1         1  ''

 L.  99       468  LOAD_FAST                'login_search_root_field'
              470  LOAD_METHOD              input_html
              472  CALL_METHOD_0         0  ''

 L. 100       474  LOAD_FAST                'app'
              476  LOAD_ATTR                form
              478  LOAD_ATTR                field
              480  LOAD_STR                 'login_authzid_prefix'
              482  BINARY_SUBSCR    
              484  LOAD_METHOD              input_html
              486  CALL_METHOD_0         0  ''

 L. 101       488  LOAD_STR                 'Chase Referral'

 L. 102       490  LOAD_GLOBAL              time
              492  LOAD_METHOD              strftime
              494  LOAD_STR                 '%Y%m%d%H%M%SZ'
              496  LOAD_GLOBAL              time
              498  LOAD_METHOD              gmtime
              500  CALL_METHOD_0         0  ''
              502  CALL_METHOD_2         2  ''

 L.  95       504  LOAD_CONST               ('field_login_mech', 'value_ldap_who', 'value_ldap_mapping', 'field_login_search_root', 'field_login_authzid_prefix', 'value_submit', 'value_currenttime')
              506  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              508  STORE_FAST               'login_fields'

 L. 105       510  LOAD_FAST                'app'
              512  LOAD_ATTR                outf
              514  LOAD_METHOD              write

 L. 106       516  LOAD_STR                 '\n        <h1>Referral received</h1>\n        <p>\n          Referral URL:<br>%s\n        </p>\n        %s\n%s\n%s\n%s\n        '

 L. 113       518  LOAD_FAST                'app'
              520  LOAD_ATTR                form
              522  LOAD_METHOD              utf2display
              524  LOAD_FAST                'ref_url'
              526  LOAD_METHOD              unparse
              528  CALL_METHOD_0         0  ''
              530  CALL_METHOD_1         1  ''

 L. 114       532  LOAD_FAST                'app'
              534  LOAD_METHOD              begin_form
              536  LOAD_FAST                'app'
              538  LOAD_ATTR                command
              540  LOAD_STR                 'POST'
              542  CALL_METHOD_2         2  ''

 L. 115       544  LOAD_FAST                'app'
              546  LOAD_ATTR                form
              548  LOAD_METHOD              hiddenFieldHTML
              550  LOAD_STR                 'host'
              552  LOAD_FAST                'ref_url'
              554  LOAD_ATTR                hostport
              556  LOAD_STR                 ''
              558  CALL_METHOD_3         3  ''

 L. 116       560  LOAD_FAST                'app'
              562  LOAD_ATTR                form
              564  LOAD_METHOD              hiddenFieldHTML
              566  LOAD_STR                 'dn'
              568  LOAD_FAST                'ref_url'
              570  LOAD_ATTR                dn
              572  LOAD_STR                 ''
              574  CALL_METHOD_3         3  ''

 L. 117       576  LOAD_FAST                'login_fields'

 L. 112       578  BUILD_TUPLE_5         5 

 L. 106       580  BINARY_MODULO    

 L. 105       582  CALL_METHOD_1         1  ''
              584  POP_TOP          

 L. 120       586  LOAD_FAST                'app'
              588  LOAD_ATTR                form
              590  LOAD_ATTR                hidden_fields

 L. 121       592  LOAD_FAST                'app'
              594  LOAD_ATTR                outf

 L. 122       596  LOAD_STR                 'sid'
              598  LOAD_STR                 'host'
              600  LOAD_STR                 'dn'
              602  LOAD_STR                 'who'
              604  LOAD_STR                 'cred'
              606  LOAD_STR                 'login_search_root'
              608  BUILD_SET_6           6 

 L. 120       610  LOAD_CONST               ('ignore_fields',)
              612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              614  POP_TOP          

 L. 124       616  LOAD_FAST                'app'
              618  LOAD_ATTR                outf
              620  LOAD_METHOD              write
              622  LOAD_STR                 '</form>\n'
              624  CALL_METHOD_1         1  ''
              626  POP_TOP          

 L. 126       628  LOAD_GLOBAL              web2ldap
              630  LOAD_ATTR                app
              632  LOAD_ATTR                gui
              634  LOAD_METHOD              footer
              636  LOAD_FAST                'app'
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 150