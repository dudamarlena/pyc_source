# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/bulkmod.py
# Compiled at: 2020-04-26 10:23:03
# Size of source mod 2**32: 18657 bytes
"""
web2ldap.app.bulkmod: modify several entries found by prior search

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, ldap0
from ldap0.dn import DNObj
import web2ldapcnf, web2ldap.ldapsession, web2ldap.ldaputil, web2ldap.app.cnf, web2ldap.app.gui, web2ldap.app.params
from web2ldap.ldaputil.oidreg import OID_REG
from web2ldap.app.schema.syntaxes import syntax_registry, LDAPSyntaxValueError
from web2ldap.app.modify import modlist_ldif
BULKMOD_CONFIRMATION_FORM_TMPL = '\n{form_begin}\n<p class="WarningMessage">\n  Apply changes to entries found with search?\n</p>\n<table>\n  <tr>\n    <td>Search base:</td><td>{field_hidden_dn}</td>\n  </tr>\n  <tr>\n    <td>Search scope:</td><td>{field_hidden_scope}</td>\n  </tr>\n  <tr>\n    <td>Search filter:</td>\n    <td>\n      {field_hidden_filterstr}\n    </td>\n  </tr>\n  <tr>\n    <td># affected entries / referrals:</td>\n    <td>\n      {num_entries} / {num_referrals}\n    </td>\n  </tr>\n</table>\n<dl>\n  <dt>LDIF change record:</dt>\n  <dd>\n    {text_ldifchangerecord}\n  </dd>\n  <dt>\n    <strong>{text_bulkmod_cp}</strong> all entries beneath this new superior DN:\n  </dt>\n  <dd><strong>{field_bulkmod_newsuperior}</strong></dd>\n  <dt>Use extended controls:</dt>\n  <dd><ul>{field_bulkmod_ctrl}<ul></dd>\n</dl>\n{hidden_fields}\n<p class="WarningMessage">Are you sure?</p>\n<input type="submit" name="bulkmod_submit" value="&lt;&lt;Back">\n<input type="submit" name="bulkmod_submit" value="Apply">\n<input type="submit" name="bulkmod_submit" value="Cancel">\n\'</form>\n'

def input_modlist(app, bulkmod_at, bulkmod_op, bulkmod_av):
    mod_dict = {}
    input_errors = set()
    for i in range(len(bulkmod_at)):
        mod_op_str = bulkmod_op[i]
        if not mod_op_str:
            pass
        else:
            mod_op = int(mod_op_str)
            mod_type = bulkmod_at[i]
            if not mod_type:
                pass
            else:
                attr_instance = syntax_registry.get_at(app,
                  '', (app.schema), mod_type, None, entry=None)
            try:
                mod_val = attr_instance.sanitize((bulkmod_av[i] or '').encode(app.ls.charset))
            except LDAPSyntaxValueError:
                mod_val = ''
                input_errors.add(i)
            else:
                try:
                    attr_instance.validate(mod_val)
                except LDAPSyntaxValueError:
                    input_errors.add(i)
                else:
                    if mod_op == ldap0.MOD_INCREMENT:
                        mod_dict[(mod_op, mod_type)] = set([None])
    else:
        if not mod_val:
            if mod_op == ldap0.MOD_DELETE:
                mod_dict[(mod_op, mod_type)] = set([None])
        if mod_val and mod_op in {ldap0.MOD_DELETE, ldap0.MOD_ADD, ldap0.MOD_REPLACE}:
            try:
                mod_dict[(mod_op, mod_type)].add(mod_val)
            except KeyError:
                mod_dict[(mod_op, mod_type)] = set([mod_val])

        mod_list = []

    for mod_op, mod_type in input_errors or mod_dict.keys():
        mod_vals = mod_dict[(mod_op, mod_type)]
        if mod_op == ldap0.MOD_DELETE:
            if None in mod_vals:
                mod_vals = None
        mod_list.append((mod_op, mod_type.encode('ascii'), mod_vals))
    else:
        for i, m in enumerate(mod_list):
            if m[2] is not None:
                mod_list[i] = (
                 m[0], m[1], list(m[2]))
            else:
                return (
                 mod_list, input_errors)


def bulkmod_input_form--- This code section failed: ---

 L. 139         0  LOAD_DEREF               'bulkmod_at'
                2  JUMP_IF_TRUE_OR_POP     8  'to 8'
                4  LOAD_STR                 ''
                6  BUILD_LIST_1          1 
              8_0  COME_FROM             2  '2'
                8  STORE_DEREF              'bulkmod_at'

 L. 140        10  LOAD_DEREF               'bulkmod_op'
               12  JUMP_IF_TRUE_OR_POP    18  'to 18'
               14  LOAD_STR                 ''
               16  BUILD_LIST_1          1 
             18_0  COME_FROM            12  '12'
               18  STORE_DEREF              'bulkmod_op'

 L. 141        20  LOAD_DEREF               'bulkmod_av'
               22  JUMP_IF_TRUE_OR_POP    28  'to 28'
               24  LOAD_STR                 ''
               26  BUILD_LIST_1          1 
             28_0  COME_FROM            22  '22'
               28  STORE_DEREF              'bulkmod_av'

 L. 142        30  LOAD_GLOBAL              sorted
               32  LOAD_CLOSURE             'bulkmod_at'
               34  BUILD_TUPLE_1         1 
               36  LOAD_SETCOMP             '<code_object <setcomp>>'
               38  LOAD_STR                 'bulkmod_input_form.<locals>.<setcomp>'
               40  MAKE_FUNCTION_8          'closure'
               42  LOAD_DEREF               'input_errors'
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'error_attrs'

 L. 143        52  LOAD_FAST                'error_attrs'
               54  POP_JUMP_IF_FALSE    82  'to 82'

 L. 144        56  LOAD_STR                 '<p class="ErrorMessage">Invalid input: %s</p>'

 L. 145        58  LOAD_STR                 ', '
               60  LOAD_METHOD              join
               62  LOAD_GLOBAL              map
               64  LOAD_DEREF               'app'
               66  LOAD_ATTR                form
               68  LOAD_ATTR                utf2display
               70  LOAD_FAST                'error_attrs'
               72  CALL_FUNCTION_2       2  ''
               74  CALL_METHOD_1         1  ''

 L. 144        76  BINARY_MODULO    
               78  STORE_FAST               'Msg'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            54  '54'

 L. 148        82  LOAD_STR                 '<p class="WarningMessage">Input bulk modify parameters here.</p>'
               84  STORE_FAST               'Msg'
             86_0  COME_FROM            80  '80'

 L. 149        86  LOAD_FAST                'bulkmod_submit'
               88  POP_JUMP_IF_FALSE   148  'to 148'
               90  LOAD_FAST                'bulkmod_submit'
               92  LOAD_METHOD              startswith
               94  LOAD_STR                 '-'
               96  CALL_METHOD_1         1  ''
               98  POP_JUMP_IF_FALSE   148  'to 148'

 L. 150       100  LOAD_GLOBAL              int
              102  LOAD_FAST                'bulkmod_submit'
              104  LOAD_CONST               1
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'del_row_num'

 L. 151       116  LOAD_GLOBAL              len
              118  LOAD_DEREF               'bulkmod_at'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               1
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   248  'to 248'

 L. 152       128  LOAD_DEREF               'bulkmod_at'
              130  LOAD_FAST                'del_row_num'
              132  DELETE_SUBSCR    

 L. 153       134  LOAD_DEREF               'bulkmod_op'
              136  LOAD_FAST                'del_row_num'
              138  DELETE_SUBSCR    

 L. 154       140  LOAD_DEREF               'bulkmod_av'
              142  LOAD_FAST                'del_row_num'
              144  DELETE_SUBSCR    
              146  JUMP_FORWARD        248  'to 248'
            148_0  COME_FROM            98  '98'
            148_1  COME_FROM            88  '88'

 L. 155       148  LOAD_FAST                'bulkmod_submit'
              150  POP_JUMP_IF_FALSE   248  'to 248'
              152  LOAD_FAST                'bulkmod_submit'
              154  LOAD_METHOD              startswith
              156  LOAD_STR                 '+'
              158  CALL_METHOD_1         1  ''
              160  POP_JUMP_IF_FALSE   248  'to 248'

 L. 156       162  LOAD_GLOBAL              int
              164  LOAD_FAST                'bulkmod_submit'
              166  LOAD_CONST               1
              168  LOAD_CONST               None
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'insert_row_num'

 L. 157       178  LOAD_GLOBAL              len
              180  LOAD_DEREF               'bulkmod_at'
              182  CALL_FUNCTION_1       1  ''
              184  LOAD_GLOBAL              web2ldapcnf
              186  LOAD_ATTR                max_searchparams
              188  COMPARE_OP               <
              190  POP_JUMP_IF_FALSE   248  'to 248'

 L. 158       192  LOAD_DEREF               'bulkmod_at'
              194  LOAD_METHOD              insert
              196  LOAD_FAST                'insert_row_num'
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  LOAD_DEREF               'bulkmod_at'
              204  LOAD_FAST                'insert_row_num'
              206  BINARY_SUBSCR    
              208  CALL_METHOD_2         2  ''
              210  POP_TOP          

 L. 159       212  LOAD_DEREF               'bulkmod_op'
              214  LOAD_METHOD              insert
              216  LOAD_FAST                'insert_row_num'
              218  LOAD_CONST               1
              220  BINARY_ADD       
              222  LOAD_DEREF               'bulkmod_op'
              224  LOAD_FAST                'insert_row_num'
              226  BINARY_SUBSCR    
              228  CALL_METHOD_2         2  ''
              230  POP_TOP          

 L. 160       232  LOAD_DEREF               'bulkmod_av'
              234  LOAD_METHOD              insert
              236  LOAD_FAST                'insert_row_num'
              238  LOAD_CONST               1
              240  BINARY_ADD       
              242  LOAD_STR                 ''
              244  CALL_METHOD_2         2  ''
              246  POP_TOP          
            248_0  COME_FROM           190  '190'
            248_1  COME_FROM           160  '160'
            248_2  COME_FROM           150  '150'
            248_3  COME_FROM           146  '146'
            248_4  COME_FROM           126  '126'

 L. 162       248  LOAD_GLOBAL              web2ldap
              250  LOAD_ATTR                app
              252  LOAD_ATTR                gui
              254  LOAD_ATTR                attrtype_select_field

 L. 163       256  LOAD_DEREF               'app'

 L. 164       258  LOAD_STR                 'bulkmod_at'

 L. 165       260  LOAD_STR                 'Attribute type'

 L. 166       262  BUILD_LIST_0          0 

 L. 166       264  LOAD_CONST               None

 L. 162       266  LOAD_CONST               ('default_attr_options',)
              268  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              270  STORE_DEREF              'bulkmod_attr_select'

 L. 169       272  LOAD_GLOBAL              web2ldap
              274  LOAD_ATTR                app
              276  LOAD_ATTR                gui
              278  LOAD_METHOD              top_section

 L. 170       280  LOAD_DEREF               'app'

 L. 171       282  LOAD_STR                 'Bulk modification input'

 L. 172       284  LOAD_GLOBAL              web2ldap
              286  LOAD_ATTR                app
              288  LOAD_ATTR                gui
              290  LOAD_METHOD              main_menu
              292  LOAD_DEREF               'app'
              294  CALL_METHOD_1         1  ''

 L. 169       296  CALL_METHOD_3         3  ''
              298  POP_TOP          

 L. 174       300  LOAD_STR                 '\n'
              302  LOAD_METHOD              join
              304  LOAD_CLOSURE             'app'
              306  LOAD_CLOSURE             'bulkmod_at'
              308  LOAD_CLOSURE             'bulkmod_attr_select'
              310  LOAD_CLOSURE             'bulkmod_av'
              312  LOAD_CLOSURE             'bulkmod_op'
              314  LOAD_CLOSURE             'input_errors'
              316  BUILD_TUPLE_6         6 
              318  LOAD_LISTCOMP            '<code_object <listcomp>>'
              320  LOAD_STR                 'bulkmod_input_form.<locals>.<listcomp>'
              322  MAKE_FUNCTION_8          'closure'

 L. 188       324  LOAD_GLOBAL              range
              326  LOAD_GLOBAL              len
              328  LOAD_DEREF               'bulkmod_at'
              330  CALL_FUNCTION_1       1  ''
              332  CALL_FUNCTION_1       1  ''

 L. 174       334  GET_ITER         
              336  CALL_FUNCTION_1       1  ''
              338  CALL_METHOD_1         1  ''
              340  STORE_FAST               'input_fields'

 L. 191       342  LOAD_DEREF               'app'
              344  LOAD_ATTR                outf
              346  LOAD_METHOD              write

 L. 192       348  LOAD_STR                 '\n        {form_begin}\n        {text_msg}\n        <fieldset>\n          <legend>Search parameters</legend>\n          <table>\n            <tr>\n              <td>Search base:</td><td>{field_hidden_dn}</td>\n            </tr>\n            <tr>\n              <td>Search scope:</td><td>{field_hidden_scope}</td>\n            </tr>\n            <tr>\n              <td>Search filter:</td>\n              <td>\n                {field_hidden_filterstr}\n              </td>\n            </tr>\n          </table>\n        </fieldset>\n        <fieldset>\n          <legend>Bulk modify input</legend>\n          <p><input type="submit" name="bulkmod_submit" value="Next&gt;&gt;"></p>\n          <table>\n          <tr>\n            <td colspan="2">Superior DN:</td><td colspan="3">{field_bulkmod_newsuperior}</td>\n          </tr>\n          <tr>\n            <td colspan="2">Copy entries:</td><td colspan="3">{field_bulkmod_cp}</td>\n          </tr>\n          {input_fields}\n          </table>\n        </fieldset>\n        <fieldset>\n          <legend>Extended controls</legend>\n          {field_bulkmod_ctrl}\n        </fieldset>\n        </form>\n        '
              350  LOAD_ATTR                format

 L. 231       352  LOAD_FAST                'Msg'

 L. 232       354  LOAD_DEREF               'app'
              356  LOAD_METHOD              begin_form
              358  LOAD_STR                 'bulkmod'
              360  LOAD_STR                 'POST'
              362  CALL_METHOD_2         2  ''

 L. 233       364  LOAD_DEREF               'app'
              366  LOAD_ATTR                form
              368  LOAD_ATTR                field
              370  LOAD_STR                 'bulkmod_ctrl'
              372  BINARY_SUBSCR    
              374  LOAD_ATTR                input_html
              376  LOAD_DEREF               'app'
              378  LOAD_ATTR                form
              380  LOAD_ATTR                field
              382  LOAD_STR                 'bulkmod_ctrl'
              384  BINARY_SUBSCR    
              386  LOAD_ATTR                value
              388  LOAD_CONST               ('default',)
              390  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 234       392  LOAD_FAST                'input_fields'

 L. 235       394  LOAD_DEREF               'app'
              396  LOAD_ATTR                form
              398  LOAD_METHOD              hiddenFieldHTML
              400  LOAD_STR                 'dn'
              402  LOAD_DEREF               'app'
              404  LOAD_ATTR                dn
              406  LOAD_DEREF               'app'
              408  LOAD_ATTR                dn
              410  CALL_METHOD_3         3  ''

 L. 236       412  LOAD_DEREF               'app'
              414  LOAD_ATTR                form
              416  LOAD_METHOD              hiddenFieldHTML
              418  LOAD_STR                 'filterstr'
              420  LOAD_FAST                'bulkmod_filter'
              422  LOAD_FAST                'bulkmod_filter'
              424  CALL_METHOD_3         3  ''

 L. 237       426  LOAD_DEREF               'app'
              428  LOAD_ATTR                form
              430  LOAD_METHOD              hiddenFieldHTML

 L. 238       432  LOAD_STR                 'scope'

 L. 239       434  LOAD_GLOBAL              str
              436  LOAD_FAST                'scope'
              438  CALL_FUNCTION_1       1  ''

 L. 240       440  LOAD_GLOBAL              str
              442  LOAD_GLOBAL              ldap0
              444  LOAD_ATTR                ldapurl
              446  LOAD_ATTR                SEARCH_SCOPE_STR
              448  LOAD_FAST                'scope'
              450  BINARY_SUBSCR    
              452  CALL_FUNCTION_1       1  ''

 L. 237       454  CALL_METHOD_3         3  ''

 L. 242       456  LOAD_DEREF               'app'
              458  LOAD_ATTR                form
              460  LOAD_ATTR                field
              462  LOAD_STR                 'bulkmod_newsuperior'
              464  BINARY_SUBSCR    
              466  LOAD_ATTR                input_html

 L. 243       468  LOAD_FAST                'bulkmod_newsuperior'

 L. 244       470  LOAD_STR                 'New superior DN where all entries are moved beneath'

 L. 242       472  LOAD_CONST               ('default', 'title')
              474  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 246       476  LOAD_DEREF               'app'
              478  LOAD_ATTR                form
              480  LOAD_ATTR                field
              482  LOAD_STR                 'bulkmod_cp'
              484  BINARY_SUBSCR    
              486  LOAD_ATTR                input_html
              488  LOAD_FAST                'bulkmod_cp'
              490  LOAD_CONST               ('checked',)
              492  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 192       494  LOAD_CONST               ('text_msg', 'form_begin', 'field_bulkmod_ctrl', 'input_fields', 'field_hidden_dn', 'field_hidden_filterstr', 'field_hidden_scope', 'field_bulkmod_newsuperior', 'field_bulkmod_cp')
              496  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'

 L. 191       498  CALL_METHOD_1         1  ''
              500  POP_TOP          

 L. 249       502  LOAD_GLOBAL              web2ldap
              504  LOAD_ATTR                app
              506  LOAD_ATTR                gui
              508  LOAD_METHOD              footer
              510  LOAD_DEREF               'app'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          

Parse error at or near `LOAD_SETCOMP' instruction at offset 36


def bulkmod_confirmation_form(app, dn, scope, bulkmod_filter, bulkmod_newsuperior, bulk_mod_list, bulkmod_cp):
    try:
        num_entries, num_referrals = app.ls.count((app.dn), scope, bulkmod_filter, sizelimit=1000)
    except web2ldap.ldapsession.LDAPLimitErrors:
        num_entries, num_referrals = ('unknown', 'unknown')
    else:
        if num_entries is None:
            num_entries = 'unknown'
        else:
            num_entries = str(num_entries)
        web2ldap.app.gui.top_section(app,
          'Modify entries?',
          (web2ldap.app.gui.main_menu(app)),
          main_div_id='Input')
        app.outf.write(BULKMOD_CONFIRMATION_FORM_TMPL.format(form_begin=(app.begin_form'bulkmod''POST'),
          field_bulkmod_ctrl=('\n'.join(['<li>%s (%s)</li>' % (
         app.form.utf2display(OID_REG.getctrl_oid(ctrl_oid,)[0]),
         app.form.utf2display(ctrl_oid)) for ctrl_oid in app.form.field['bulkmod_ctrl'].value or []]) or '- none -'),
          field_hidden_dn=(app.form.hiddenFieldHTML'dn'dndn),
          field_hidden_filterstr=(app.form.hiddenFieldHTML'filterstr'bulkmod_filterbulkmod_filter),
          field_hidden_scope=(app.form.hiddenFieldHTML'scope'str(scope)str(ldap0.ldapurl.SEARCH_SCOPE_STR[scope])),
          field_bulkmod_newsuperior=(app.form.hiddenFieldHTML'bulkmod_newsuperior'bulkmod_newsuperiorbulkmod_newsuperior),
          text_bulkmod_cp=({False:'Move', 
         True:'Copy'}[bulkmod_cp]),
          num_entries=num_entries,
          num_referrals=num_referrals,
          text_ldifchangerecord=bulk_mod_list_ldif,
          hidden_fields=app.form.hiddenInputHTML(ignoreFieldNames=[
         'dn', 'scope', 'filterstr', 'bulkmod_submit', 'bulkmod_newsuperior'])))
        web2ldap.app.gui.footer(app)


def w2l_bulkmod--- This code section failed: ---

 L. 327         0  LOAD_FAST                'app'
                2  LOAD_ATTR                form
                4  LOAD_METHOD              getInputValue
                6  LOAD_STR                 'bulkmod_submit'
                8  LOAD_CONST               None
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_2         2  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'bulkmod_submit'

 L. 329        20  LOAD_FAST                'app'
               22  LOAD_ATTR                form
               24  LOAD_METHOD              getInputValue
               26  LOAD_STR                 'bulkmod_at'
               28  BUILD_LIST_0          0 
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'bulkmod_at'

 L. 330        34  LOAD_FAST                'app'
               36  LOAD_ATTR                form
               38  LOAD_METHOD              getInputValue
               40  LOAD_STR                 'bulkmod_op'
               42  BUILD_LIST_0          0 
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'bulkmod_op'

 L. 331        48  LOAD_FAST                'app'
               50  LOAD_ATTR                form
               52  LOAD_METHOD              getInputValue
               54  LOAD_STR                 'bulkmod_av'
               56  BUILD_LIST_0          0 
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'bulkmod_av'

 L. 333        62  LOAD_FAST                'app'
               64  LOAD_ATTR                form
               66  LOAD_METHOD              getInputValue
               68  LOAD_STR                 'bulkmod_cp'
               70  LOAD_STR                 ''
               72  BUILD_LIST_1          1 
               74  CALL_METHOD_2         2  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_STR                 'yes'
               82  COMPARE_OP               ==
               84  STORE_FAST               'bulkmod_cp'

 L. 335        86  LOAD_GLOBAL              int
               88  LOAD_FAST                'app'
               90  LOAD_ATTR                form
               92  LOAD_METHOD              getInputValue
               94  LOAD_STR                 'scope'
               96  LOAD_GLOBAL              str
               98  LOAD_FAST                'app'
              100  LOAD_ATTR                ldap_url
              102  LOAD_ATTR                scope
              104  JUMP_IF_TRUE_OR_POP   110  'to 110'
              106  LOAD_GLOBAL              ldap0
              108  LOAD_ATTR                SCOPE_BASE
            110_0  COME_FROM           104  '104'
              110  CALL_FUNCTION_1       1  ''
              112  BUILD_LIST_1          1 
              114  CALL_METHOD_2         2  ''
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'scope'

 L. 337       124  LOAD_FAST                'app'
              126  LOAD_ATTR                form
              128  LOAD_METHOD              getInputValue

 L. 338       130  LOAD_STR                 'filterstr'

 L. 339       132  LOAD_FAST                'app'
              134  LOAD_ATTR                ldap_url
              136  LOAD_ATTR                filterstr
              138  JUMP_IF_TRUE_OR_POP   142  'to 142'
              140  LOAD_STR                 ''
            142_0  COME_FROM           138  '138'
              142  BUILD_LIST_1          1 

 L. 337       144  CALL_METHOD_2         2  ''

 L. 340       146  LOAD_CONST               0

 L. 337       148  BINARY_SUBSCR    
              150  JUMP_IF_TRUE_OR_POP   154  'to 154'

 L. 340       152  LOAD_STR                 '(objectClass=*)'
            154_0  COME_FROM           150  '150'

 L. 337       154  STORE_FAST               'bulkmod_filter'

 L. 341       156  LOAD_FAST                'app'
              158  LOAD_ATTR                form
              160  LOAD_METHOD              getInputValue
              162  LOAD_STR                 'bulkmod_newsuperior'
              164  LOAD_STR                 ''
              166  BUILD_LIST_1          1 
              168  CALL_METHOD_2         2  ''
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  STORE_FAST               'bulkmod_newsuperior'

 L. 345       176  LOAD_FAST                'app'
              178  LOAD_ATTR                form
              180  LOAD_METHOD              getInputValue
              182  LOAD_STR                 'bulkmod_ctrl'
              184  BUILD_LIST_0          0 
              186  CALL_METHOD_2         2  ''
              188  STORE_FAST               'bulkmod_ctrl_oids'

 L. 347       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'bulkmod_at'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_GLOBAL              len
              198  LOAD_FAST                'bulkmod_op'
              200  CALL_FUNCTION_1       1  ''
              202  DUP_TOP          
              204  ROT_THREE        
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   222  'to 222'
              210  LOAD_GLOBAL              len
              212  LOAD_FAST                'bulkmod_av'
              214  CALL_FUNCTION_1       1  ''
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_TRUE    238  'to 238'
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           208  '208'
              222  POP_TOP          
            224_0  COME_FROM           220  '220'

 L. 348       224  LOAD_GLOBAL              web2ldap
              226  LOAD_ATTR                app
              228  LOAD_ATTR                core
              230  LOAD_METHOD              ErrorExit
              232  LOAD_STR                 'Invalid bulk modification input.'
              234  CALL_METHOD_1         1  ''
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           218  '218'

 L. 350       238  LOAD_GLOBAL              input_modlist

 L. 351       240  LOAD_FAST                'app'

 L. 352       242  LOAD_FAST                'bulkmod_at'

 L. 352       244  LOAD_FAST                'bulkmod_op'

 L. 352       246  LOAD_FAST                'bulkmod_av'

 L. 350       248  CALL_FUNCTION_4       4  ''
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'bulk_mod_list'
              254  STORE_FAST               'input_errors'

 L. 355       256  LOAD_FAST                'bulkmod_submit'
              258  LOAD_STR                 'Cancel'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   296  'to 296'

 L. 357       266  LOAD_FAST                'app'
              268  LOAD_ATTR                simple_message

 L. 358       270  LOAD_STR                 'Canceled bulk modification.'

 L. 359       272  LOAD_STR                 '<p class="SuccessMessage">Canceled bulk modification.</p>'

 L. 360       274  LOAD_GLOBAL              web2ldap
              276  LOAD_ATTR                app
              278  LOAD_ATTR                gui
              280  LOAD_METHOD              main_menu
              282  LOAD_FAST                'app'
              284  CALL_METHOD_1         1  ''

 L. 357       286  LOAD_CONST               ('main_menu_list',)
              288  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              290  POP_TOP          
          292_294  JUMP_FORWARD       1216  'to 1216'
            296_0  COME_FROM           262  '262'

 L. 363       296  LOAD_FAST                'bulk_mod_list'
          298_300  POP_JUMP_IF_TRUE    308  'to 308'
              302  LOAD_FAST                'bulkmod_newsuperior'
          304_306  POP_JUMP_IF_FALSE   358  'to 358'
            308_0  COME_FROM           298  '298'

 L. 364       308  LOAD_FAST                'input_errors'

 L. 363   310_312  POP_JUMP_IF_TRUE    358  'to 358'

 L. 365       314  LOAD_FAST                'bulkmod_submit'
              316  LOAD_CONST               None
              318  COMPARE_OP               is

 L. 363   320_322  POP_JUMP_IF_TRUE    358  'to 358'

 L. 366       324  LOAD_FAST                'bulkmod_submit'
              326  LOAD_STR                 '<<Back'
              328  COMPARE_OP               ==

 L. 363   330_332  POP_JUMP_IF_TRUE    358  'to 358'

 L. 367       334  LOAD_FAST                'bulkmod_submit'
              336  LOAD_METHOD              startswith
              338  LOAD_STR                 '+'
              340  CALL_METHOD_1         1  ''

 L. 363   342_344  POP_JUMP_IF_TRUE    358  'to 358'

 L. 368       346  LOAD_FAST                'bulkmod_submit'
              348  LOAD_METHOD              startswith
              350  LOAD_STR                 '-'
              352  CALL_METHOD_1         1  ''

 L. 363   354_356  POP_JUMP_IF_FALSE   392  'to 392'
            358_0  COME_FROM           342  '342'
            358_1  COME_FROM           330  '330'
            358_2  COME_FROM           320  '320'
            358_3  COME_FROM           310  '310'
            358_4  COME_FROM           304  '304'

 L. 370       358  LOAD_GLOBAL              bulkmod_input_form

 L. 371       360  LOAD_FAST                'app'

 L. 372       362  LOAD_FAST                'bulkmod_submit'

 L. 373       364  LOAD_FAST                'app'
              366  LOAD_ATTR                dn

 L. 373       368  LOAD_FAST                'scope'

 L. 373       370  LOAD_FAST                'bulkmod_filter'

 L. 374       372  LOAD_FAST                'bulkmod_newsuperior'

 L. 375       374  LOAD_FAST                'bulkmod_at'

 L. 375       376  LOAD_FAST                'bulkmod_op'

 L. 375       378  LOAD_FAST                'bulkmod_av'

 L. 375       380  LOAD_FAST                'bulkmod_cp'

 L. 376       382  LOAD_FAST                'input_errors'

 L. 370       384  CALL_FUNCTION_11     11  ''
              386  POP_TOP          
          388_390  JUMP_FORWARD       1216  'to 1216'
            392_0  COME_FROM           354  '354'

 L. 379       392  LOAD_FAST                'bulkmod_submit'
              394  LOAD_STR                 'Next>>'
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   428  'to 428'

 L. 381       402  LOAD_GLOBAL              bulkmod_confirmation_form

 L. 382       404  LOAD_FAST                'app'

 L. 383       406  LOAD_FAST                'app'
              408  LOAD_ATTR                dn

 L. 383       410  LOAD_FAST                'scope'

 L. 383       412  LOAD_FAST                'bulkmod_filter'

 L. 384       414  LOAD_FAST                'bulkmod_newsuperior'

 L. 384       416  LOAD_FAST                'bulk_mod_list'

 L. 384       418  LOAD_FAST                'bulkmod_cp'

 L. 381       420  CALL_FUNCTION_7       7  ''
              422  POP_TOP          
          424_426  JUMP_FORWARD       1216  'to 1216'
            428_0  COME_FROM           398  '398'

 L. 387       428  LOAD_FAST                'bulkmod_submit'
              430  LOAD_STR                 'Apply'
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE  1202  'to 1202'

 L. 390       438  LOAD_FAST                'app'
              440  LOAD_ATTR                form
              442  LOAD_METHOD              getInputValue
              444  LOAD_STR                 'bulkmod_ctrl'
              446  BUILD_LIST_0          0 
              448  CALL_METHOD_2         2  ''
              450  STORE_FAST               'bulkmod_ctrl_oids'

 L. 391       452  LOAD_SETCOMP             '<code_object <setcomp>>'
              454  LOAD_STR                 'w2l_bulkmod.<locals>.<setcomp>'
              456  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 393       458  LOAD_FAST                'app'
              460  LOAD_ATTR                ls
              462  LOAD_ATTR                l
              464  LOAD_ATTR                _req_ctrls
              466  LOAD_STR                 '**all**'
              468  BINARY_SUBSCR    
              470  LOAD_FAST                'app'
              472  LOAD_ATTR                ls
              474  LOAD_ATTR                l
              476  LOAD_ATTR                _req_ctrls
              478  LOAD_STR                 '**write**'
              480  BINARY_SUBSCR    
              482  BINARY_ADD       
              484  LOAD_FAST                'app'
              486  LOAD_ATTR                ls
              488  LOAD_ATTR                l
              490  LOAD_ATTR                _req_ctrls
              492  LOAD_STR                 'modify'
              494  BINARY_SUBSCR    
              496  BINARY_ADD       

 L. 391       498  GET_ITER         
              500  CALL_FUNCTION_1       1  ''
              502  STORE_DEREF              'conn_server_ctrls'

 L. 395       504  LOAD_GLOBAL              list
              506  LOAD_CLOSURE             'conn_server_ctrls'
              508  BUILD_TUPLE_1         1 
              510  LOAD_SETCOMP             '<code_object <setcomp>>'
              512  LOAD_STR                 'w2l_bulkmod.<locals>.<setcomp>'
              514  MAKE_FUNCTION_8          'closure'

 L. 397       516  LOAD_FAST                'bulkmod_ctrl_oids'

 L. 395       518  GET_ITER         
              520  CALL_FUNCTION_1       1  ''
              522  CALL_FUNCTION_1       1  ''
          524_526  JUMP_IF_TRUE_OR_POP   530  'to 530'

 L. 399       528  LOAD_CONST               None
            530_0  COME_FROM           524  '524'

 L. 395       530  STORE_FAST               'bulkmod_server_ctrls'

 L. 401       532  BUILD_LIST_0          0 
              534  STORE_FAST               'ldap_error_html'

 L. 403       536  LOAD_GLOBAL              time
              538  LOAD_METHOD              time
              540  CALL_METHOD_0         0  ''
              542  STORE_FAST               'begin_time_stamp'

 L. 406       544  LOAD_FAST                'app'
              546  LOAD_ATTR                ls
              548  LOAD_ATTR                l
              550  LOAD_ATTR                search

 L. 407       552  LOAD_FAST                'app'
              554  LOAD_ATTR                dn

 L. 408       556  LOAD_FAST                'scope'

 L. 409       558  LOAD_FAST                'bulkmod_filter'

 L. 410       560  LOAD_FAST                'bulkmod_cp'
          562_564  POP_JUMP_IF_FALSE   572  'to 572'
              566  LOAD_STR                 '*'
              568  BUILD_LIST_1          1 
              570  JUMP_FORWARD        576  'to 576'
            572_0  COME_FROM           562  '562'
              572  LOAD_STR                 '1.1'
              574  BUILD_LIST_1          1 
            576_0  COME_FROM           570  '570'

 L. 406       576  LOAD_CONST               ('attrlist',)
              578  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              580  STORE_FAST               'ldap_msgid'

 L. 413       582  BUILD_LIST_0          0 
              584  STORE_FAST               'result_ldif_html'

 L. 416       586  LOAD_FAST                'app'
              588  LOAD_ATTR                ls
              590  LOAD_ATTR                l
              592  LOAD_METHOD              results
              594  LOAD_FAST                'ldap_msgid'
              596  CALL_METHOD_1         1  ''
              598  GET_ITER         
          600_602  FOR_ITER           1014  'to 1014'
              604  STORE_FAST               'res'

 L. 419       606  LOAD_FAST                'res'
              608  LOAD_ATTR                rtype
              610  LOAD_GLOBAL              ldap0
              612  LOAD_ATTR                RES_SEARCH_REFERENCE
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   624  'to 624'

 L. 421   620_622  JUMP_BACK           600  'to 600'
            624_0  COME_FROM           616  '616'

 L. 423       624  LOAD_FAST                'res'
              626  LOAD_ATTR                rdata
              628  GET_ITER         
            630_0  COME_FROM           766  '766'
          630_632  FOR_ITER           1010  'to 1010'
              634  STORE_FAST               'rdat'

 L. 426       636  LOAD_FAST                'bulk_mod_list'
          638_640  POP_JUMP_IF_FALSE   764  'to 764'

 L. 427       642  SETUP_FINALLY       670  'to 670'

 L. 428       644  LOAD_FAST                'app'
              646  LOAD_ATTR                ls
              648  LOAD_ATTR                l
              650  LOAD_ATTR                modify_s
              652  LOAD_FAST                'rdat'
              654  LOAD_ATTR                dn_s
              656  LOAD_FAST                'bulk_mod_list'
              658  LOAD_FAST                'bulkmod_server_ctrls'
              660  LOAD_CONST               ('req_ctrls',)
              662  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              664  POP_TOP          
              666  POP_BLOCK        
              668  JUMP_FORWARD        742  'to 742'
            670_0  COME_FROM_FINALLY   642  '642'

 L. 429       670  DUP_TOP          
              672  LOAD_GLOBAL              ldap0
              674  LOAD_ATTR                LDAPError
              676  COMPARE_OP               exception-match
          678_680  POP_JUMP_IF_FALSE   740  'to 740'
              682  POP_TOP          
              684  STORE_FAST               'e'
              686  POP_TOP          
              688  SETUP_FINALLY       728  'to 728'

 L. 430       690  LOAD_FAST                'ldap_error_html'
              692  LOAD_METHOD              append

 L. 431       694  LOAD_STR                 '<dt>%s</dt><dd>%s</dd>'

 L. 432       696  LOAD_FAST                'app'
              698  LOAD_ATTR                form
              700  LOAD_METHOD              utf2display
              702  LOAD_FAST                'rdat'
              704  LOAD_ATTR                dn_s
              706  CALL_METHOD_1         1  ''

 L. 433       708  LOAD_FAST                'app'
              710  LOAD_METHOD              ldap_error_msg
              712  LOAD_FAST                'e'
              714  CALL_METHOD_1         1  ''

 L. 431       716  BUILD_TUPLE_2         2 
              718  BINARY_MODULO    

 L. 430       720  CALL_METHOD_1         1  ''
              722  POP_TOP          
              724  POP_BLOCK        
              726  BEGIN_FINALLY    
            728_0  COME_FROM_FINALLY   688  '688'
              728  LOAD_CONST               None
              730  STORE_FAST               'e'
              732  DELETE_FAST              'e'
              734  END_FINALLY      
              736  POP_EXCEPT       
              738  JUMP_FORWARD        764  'to 764'
            740_0  COME_FROM           678  '678'
              740  END_FINALLY      
            742_0  COME_FROM           668  '668'

 L. 437       742  LOAD_FAST                'result_ldif_html'
              744  LOAD_METHOD              append
              746  LOAD_GLOBAL              modlist_ldif

 L. 438       748  LOAD_FAST                'rdat'
              750  LOAD_ATTR                dn_s

 L. 438       752  LOAD_FAST                'app'
              754  LOAD_ATTR                form

 L. 438       756  LOAD_FAST                'bulk_mod_list'

 L. 437       758  CALL_FUNCTION_3       3  ''
              760  CALL_METHOD_1         1  ''
              762  POP_TOP          
            764_0  COME_FROM           738  '738'
            764_1  COME_FROM           638  '638'

 L. 442       764  LOAD_FAST                'bulkmod_newsuperior'
          766_768  POP_JUMP_IF_FALSE   630  'to 630'

 L. 443       770  LOAD_GLOBAL              str
              772  LOAD_GLOBAL              DNObj
              774  LOAD_METHOD              from_str
              776  LOAD_FAST                'rdat'
              778  LOAD_ATTR                dn_s
              780  CALL_METHOD_1         1  ''
              782  LOAD_METHOD              rdn
              784  CALL_METHOD_0         0  ''
              786  CALL_FUNCTION_1       1  ''
              788  STORE_FAST               'old_rdn'

 L. 444       790  SETUP_FINALLY       880  'to 880'

 L. 445       792  LOAD_FAST                'bulkmod_cp'
          794_796  POP_JUMP_IF_FALSE   846  'to 846'

 L. 446       798  LOAD_STR                 ','
              800  LOAD_METHOD              join

 L. 447       802  LOAD_FAST                'old_rdn'

 L. 448       804  LOAD_FAST                'bulkmod_newsuperior'

 L. 446       806  BUILD_TUPLE_2         2 
              808  CALL_METHOD_1         1  ''
              810  STORE_FAST               'new_ldap_dn'

 L. 450       812  LOAD_FAST                'rdat'
              814  LOAD_ATTR                entry_b
          816_818  POP_JUMP_IF_TRUE    826  'to 826'

 L. 451       820  LOAD_GLOBAL              ldap0
              822  LOAD_ATTR                NO_SUCH_OBJECT
              824  RAISE_VARARGS_1       1  'exception instance'
            826_0  COME_FROM           816  '816'

 L. 452       826  LOAD_FAST                'app'
              828  LOAD_ATTR                ls
              830  LOAD_ATTR                l
              832  LOAD_METHOD              add_s
              834  LOAD_FAST                'new_ldap_dn'
              836  LOAD_FAST                'rdat'
              838  LOAD_ATTR                entry_as
              840  CALL_METHOD_2         2  ''
              842  POP_TOP          
              844  JUMP_FORWARD        876  'to 876'
            846_0  COME_FROM           794  '794'

 L. 454       846  LOAD_FAST                'app'
              848  LOAD_ATTR                ls
              850  LOAD_ATTR                rename

 L. 455       852  LOAD_FAST                'rdat'
              854  LOAD_ATTR                dn_s

 L. 456       856  LOAD_FAST                'old_rdn'

 L. 457       858  LOAD_FAST                'bulkmod_newsuperior'

 L. 458       860  LOAD_FAST                'app'
              862  LOAD_METHOD              cfg_param
              864  LOAD_STR                 'bulkmod_delold'
              866  LOAD_CONST               0
              868  CALL_METHOD_2         2  ''

 L. 454       870  LOAD_CONST               ('new_superior', 'delold')
              872  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              874  POP_TOP          
            876_0  COME_FROM           844  '844'
              876  POP_BLOCK        
              878  JUMP_FORWARD        958  'to 958'
            880_0  COME_FROM_FINALLY   790  '790'

 L. 460       880  DUP_TOP          
              882  LOAD_GLOBAL              ldap0
              884  LOAD_ATTR                LDAPError
              886  COMPARE_OP               exception-match
          888_890  POP_JUMP_IF_FALSE   956  'to 956'
              892  POP_TOP          
              894  STORE_FAST               'e'
              896  POP_TOP          
              898  SETUP_FINALLY       944  'to 944'

 L. 461       900  LOAD_FAST                'ldap_error_html'
              902  LOAD_METHOD              append

 L. 462       904  LOAD_STR                 '<dt>%s</dt><dd>%s</dd>'

 L. 463       906  LOAD_FAST                'app'
              908  LOAD_ATTR                form
              910  LOAD_METHOD              utf2display
              912  LOAD_FAST                'rdat'
              914  LOAD_ATTR                dn_s
              916  CALL_METHOD_1         1  ''

 L. 464       918  LOAD_FAST                'app'
              920  LOAD_ATTR                form
              922  LOAD_METHOD              utf2display
              924  LOAD_GLOBAL              str
              926  LOAD_FAST                'e'
              928  CALL_FUNCTION_1       1  ''
              930  CALL_METHOD_1         1  ''

 L. 462       932  BUILD_TUPLE_2         2 
              934  BINARY_MODULO    

 L. 461       936  CALL_METHOD_1         1  ''
              938  POP_TOP          
              940  POP_BLOCK        
              942  BEGIN_FINALLY    
            944_0  COME_FROM_FINALLY   898  '898'
              944  LOAD_CONST               None
              946  STORE_FAST               'e'
              948  DELETE_FAST              'e'
              950  END_FINALLY      
              952  POP_EXCEPT       
              954  JUMP_BACK           630  'to 630'
            956_0  COME_FROM           888  '888'
              956  END_FINALLY      
            958_0  COME_FROM           878  '878'

 L. 468       958  LOAD_FAST                'result_ldif_html'
              960  LOAD_METHOD              append

 L. 469       962  LOAD_STR                 '<p>%s %s beneath %s</p>'

 L. 470       964  LOAD_STR                 'Moved'
              966  LOAD_STR                 'Copied'
              968  LOAD_CONST               (False, True)
              970  BUILD_CONST_KEY_MAP_2     2 
              972  LOAD_FAST                'bulkmod_cp'
              974  BINARY_SUBSCR    

 L. 471       976  LOAD_FAST                'app'
              978  LOAD_ATTR                form
              980  LOAD_METHOD              utf2display
              982  LOAD_FAST                'rdat'
              984  LOAD_ATTR                dn_s
              986  CALL_METHOD_1         1  ''

 L. 472       988  LOAD_FAST                'app'
              990  LOAD_ATTR                form
              992  LOAD_METHOD              utf2display
              994  LOAD_FAST                'bulkmod_newsuperior'
              996  CALL_METHOD_1         1  ''

 L. 469       998  BUILD_TUPLE_3         3 
             1000  BINARY_MODULO    

 L. 468      1002  CALL_METHOD_1         1  ''
             1004  POP_TOP          
         1006_1008  JUMP_BACK           630  'to 630'
         1010_1012  JUMP_BACK           600  'to 600'

 L. 476      1014  LOAD_GLOBAL              time
             1016  LOAD_METHOD              time
             1018  CALL_METHOD_0         0  ''
             1020  STORE_FAST               'end_time_stamp'

 L. 478      1022  LOAD_STR                 ''
             1024  STORE_FAST               'error_messages'

 L. 479      1026  LOAD_FAST                'ldap_error_html'
         1028_1030  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 480      1032  LOAD_STR                 '<strong>Errors</strong><dl>%s</dl>'

 L. 481      1034  LOAD_STR                 '\n'
             1036  LOAD_METHOD              join
             1038  LOAD_FAST                'ldap_error_html'
             1040  CALL_METHOD_1         1  ''

 L. 480      1042  BUILD_TUPLE_1         1 
             1044  BINARY_MODULO    
             1046  STORE_FAST               'error_messages'
           1048_0  COME_FROM          1028  '1028'

 L. 483      1048  LOAD_STR                 ''
             1050  STORE_FAST               'change_records'

 L. 484      1052  LOAD_FAST                'result_ldif_html'
         1054_1056  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 485      1058  LOAD_STR                 '<strong>Successfully applied changes</strong><p>%s</p>'

 L. 486      1060  LOAD_STR                 '\n'
             1062  LOAD_METHOD              join
             1064  LOAD_FAST                'result_ldif_html'
             1066  CALL_METHOD_1         1  ''

 L. 485      1068  BUILD_TUPLE_1         1 
             1070  BINARY_MODULO    
             1072  STORE_FAST               'change_records'
           1074_0  COME_FROM          1054  '1054'

 L. 489      1074  LOAD_GLOBAL              len
             1076  LOAD_FAST                'result_ldif_html'
             1078  CALL_FUNCTION_1       1  ''
             1080  STORE_FAST               'num_mods'

 L. 490      1082  LOAD_GLOBAL              len
             1084  LOAD_FAST                'ldap_error_html'
             1086  CALL_FUNCTION_1       1  ''
             1088  STORE_FAST               'num_errors'

 L. 491      1090  LOAD_FAST                'num_mods'
             1092  LOAD_FAST                'num_errors'
             1094  BINARY_ADD       
             1096  STORE_FAST               'num_sum'

 L. 492      1098  LOAD_FAST                'app'
             1100  LOAD_ATTR                simple_message

 L. 493      1102  LOAD_STR                 'Modified entries'

 L. 494      1104  LOAD_STR                 '\n            <p class="SuccessMessage">Modified entries.</p>\n            <table>\n              <tr>\n                <td>Modified entries:</td>\n                <td>%d</td>\n                <td>\n                  <meter min="0" max="%d" value="%d" optimum="%d" title="entries">%d</meter>\n                </td>\n              </tr>\n              <tr>\n                <td>Errors:</td>\n                <td>%d</td>\n                <td>\n                  <meter min="0" max="%d" value="%d" optimum="0" title="entries">%d</meter>\n                </td>\n              </tr>\n              <tr><td>Search base:</td><td>%s</td></tr>\n              <tr><td>Search scope:</td><td>%s</td></tr>\n              <tr><td>Time elapsed:</td><td>%0.2f seconds</td></tr>\n            </table>\n            %s\n            %s\n              <p><input type="submit" name="bulkmod_submit" value="&lt;&lt;Back"></p>\n            </form>\n            %s\n            %s\n            '

 L. 522      1106  LOAD_FAST                'num_mods'

 L. 523      1108  LOAD_FAST                'num_sum'

 L. 523      1110  LOAD_FAST                'num_mods'

 L. 523      1112  LOAD_FAST                'num_sum'

 L. 523      1114  LOAD_FAST                'num_mods'

 L. 524      1116  LOAD_FAST                'num_errors'

 L. 525      1118  LOAD_FAST                'num_sum'

 L. 525      1120  LOAD_FAST                'num_errors'

 L. 525      1122  LOAD_FAST                'num_errors'

 L. 526      1124  LOAD_FAST                'app'
             1126  LOAD_METHOD              display_dn
             1128  LOAD_FAST                'app'
             1130  LOAD_ATTR                dn
             1132  CALL_METHOD_1         1  ''

 L. 527      1134  LOAD_GLOBAL              ldap0
             1136  LOAD_ATTR                ldapurl
             1138  LOAD_ATTR                SEARCH_SCOPE_STR
             1140  LOAD_FAST                'scope'
             1142  BINARY_SUBSCR    

 L. 528      1144  LOAD_FAST                'end_time_stamp'
             1146  LOAD_FAST                'begin_time_stamp'
             1148  BINARY_SUBTRACT  

 L. 529      1150  LOAD_FAST                'app'
             1152  LOAD_METHOD              begin_form
             1154  LOAD_STR                 'bulkmod'
             1156  LOAD_STR                 'POST'
             1158  CALL_METHOD_2         2  ''

 L. 530      1160  LOAD_FAST                'app'
             1162  LOAD_ATTR                form
             1164  LOAD_ATTR                hiddenInputHTML
             1166  LOAD_STR                 'bulkmod_submit'
             1168  BUILD_LIST_1          1 
             1170  LOAD_CONST               ('ignoreFieldNames',)
             1172  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 531      1174  LOAD_FAST                'error_messages'

 L. 532      1176  LOAD_FAST                'change_records'

 L. 521      1178  BUILD_TUPLE_16       16 

 L. 494      1180  BINARY_MODULO    

 L. 534      1182  LOAD_GLOBAL              web2ldap
             1184  LOAD_ATTR                app
             1186  LOAD_ATTR                gui
             1188  LOAD_METHOD              main_menu
             1190  LOAD_FAST                'app'
             1192  CALL_METHOD_1         1  ''

 L. 492      1194  LOAD_CONST               ('main_menu_list',)
             1196  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1198  POP_TOP          
             1200  JUMP_FORWARD       1216  'to 1216'
           1202_0  COME_FROM           434  '434'

 L. 539      1202  LOAD_GLOBAL              web2ldap
             1204  LOAD_ATTR                app
             1206  LOAD_ATTR                core
             1208  LOAD_METHOD              ErrorExit
             1210  LOAD_STR                 'Invalid bulk modification form data.'
             1212  CALL_METHOD_1         1  ''
             1214  RAISE_VARARGS_1       1  'exception instance'
           1216_0  COME_FROM          1200  '1200'
           1216_1  COME_FROM           424  '424'
           1216_2  COME_FROM           388  '388'
           1216_3  COME_FROM           292  '292'

Parse error at or near `JUMP_FORWARD' instruction at offset 388_390