# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/bulkmod.py
# Compiled at: 2019-12-10 15:31:52
# Size of source mod 2**32: 18661 bytes
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


def bulkmod_input_form(app, bulkmod_submit, dn, scope, bulkmod_filter, bulkmod_newsuperior, bulkmod_at, bulkmod_op, bulkmod_av, bulkmod_cp, input_errors):
    bulkmod_at = bulkmod_at or ['']
    bulkmod_op = bulkmod_op or ['']
    bulkmod_av = bulkmod_av or ['']
    error_attrs = sorted(set([bulkmod_at[i] for i in input_errors]))
    if error_attrs:
        Msg = '<p class="ErrorMessage">Invalid input: %s</p>' % ', '.join(map(app.form.utf2display, error_attrs))
    else:
        Msg = '<p class="WarningMessage">Input bulk modify parameters here.</p>'
    if bulkmod_submit and bulkmod_submit.startswith('-'):
        del_row_num = int(bulkmod_submit[1:])
        if len(bulkmod_at) > 1:
            del bulkmod_at[del_row_num]
            del bulkmod_op[del_row_num]
            del bulkmod_av[del_row_num]
    elif bulkmod_submit and bulkmod_submit.startswith('+'):
        insert_row_num = int(bulkmod_submit[1:])
        if len(bulkmod_at) < web2ldapcnf.max_searchparams:
            bulkmod_at.insert(insert_row_num + 1, bulkmod_at[insert_row_num])
            bulkmod_op.insert(insert_row_num + 1, bulkmod_op[insert_row_num])
            bulkmod_av.insert(insert_row_num + 1, '')
    bulkmod_attr_select = web2ldap.app.gui.attrtype_select_field(app,
      'bulkmod_at',
      'Attribute type',
      [], default_attr_options=None)
    web2ldap.app.gui.top_section(app, 'Bulk modification input', web2ldap.app.gui.main_menu(app))
    input_fields = '\n'.join(['\n        <tr>\n          <td><button type="submit" name="bulkmod_submit" value="+%d">+</button></td>\n          <td><button type="submit" name="bulkmod_submit" value="-%d">-</button></td>\n          <td>%s</td><td>%s</td><td>%s %s</td>\n        </tr>\n        ' % (
     i, i,
     bulkmod_attr_select.input_html(default=(bulkmod_at[i])),
     app.form.field['bulkmod_op'].input_html(default=(bulkmod_op[i])),
     app.form.field['bulkmod_av'].input_html(default=(bulkmod_av[i])),
     (i in input_errors) * '&larr; Input error!') for i in range(len(bulkmod_at))])
    app.outf.write('\n        {form_begin}\n        {text_msg}\n        <fieldset>\n          <legend>Search parameters</legend>\n          <table>\n            <tr>\n              <td>Search base:</td><td>{field_hidden_dn}</td>\n            </tr>\n            <tr>\n              <td>Search scope:</td><td>{field_hidden_scope}</td>\n            </tr>\n            <tr>\n              <td>Search filter:</td>\n              <td>\n                {field_hidden_filterstr}\n              </td>\n            </tr>\n          </table>\n        </fieldset>\n        <fieldset>\n          <legend>Bulk modify input</legend>\n          <p><input type="submit" name="bulkmod_submit" value="Next&gt;&gt;"></p>\n          <table>\n          <tr>\n            <td colspan="2">Superior DN:</td><td colspan="3">{field_bulkmod_newsuperior}</td>\n          </tr>\n          <tr>\n            <td colspan="2">Copy entries:</td><td colspan="3">{field_bulkmod_cp}</td>\n          </tr>\n          {input_fields}\n          </table>\n        </fieldset>\n        <fieldset>\n          <legend>Extended controls</legend>\n          {field_bulkmod_ctrl}\n        </fieldset>\n        </form>\n        '.format(text_msg=Msg,
      form_begin=(app.begin_form('bulkmod', 'POST')),
      field_bulkmod_ctrl=app.form.field['bulkmod_ctrl'].input_html(default=(app.form.field['bulkmod_ctrl'].value)),
      input_fields=input_fields,
      field_hidden_dn=(app.form.hiddenFieldHTML('dn', app.dn, app.dn)),
      field_hidden_filterstr=(app.form.hiddenFieldHTML('filterstr', bulkmod_filter, bulkmod_filter)),
      field_hidden_scope=(app.form.hiddenFieldHTML('scope', str(scope), str(ldap0.ldapurl.SEARCH_SCOPE_STR[scope]))),
      field_bulkmod_newsuperior=app.form.field['bulkmod_newsuperior'].input_html(default=bulkmod_newsuperior,
      title='New superior DN where all entries are moved beneath'),
      field_bulkmod_cp=app.form.field['bulkmod_cp'].input_html(checked=bulkmod_cp)))
    web2ldap.app.gui.footer(app)


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
        app.outf.write(BULKMOD_CONFIRMATION_FORM_TMPL.format(form_begin=(app.begin_form('bulkmod', 'POST')),
          field_bulkmod_ctrl=('\n'.join(['<li>%s (%s)</li>' % (
         app.form.utf2display(OID_REG.get(ctrl_oid, (ctrl_oid,))[0]),
         app.form.utf2display(ctrl_oid)) for ctrl_oid in app.form.field['bulkmod_ctrl'].value or []]) or '- none -'),
          field_hidden_dn=(app.form.hiddenFieldHTML('dn', dn, dn)),
          field_hidden_filterstr=(app.form.hiddenFieldHTML('filterstr', bulkmod_filter, bulkmod_filter)),
          field_hidden_scope=(app.form.hiddenFieldHTML('scope', str(scope), str(ldap0.ldapurl.SEARCH_SCOPE_STR[scope]))),
          field_bulkmod_newsuperior=(app.form.hiddenFieldHTML('bulkmod_newsuperior', bulkmod_newsuperior, bulkmod_newsuperior)),
          text_bulkmod_cp=({False:'Move', 
         True:'Copy'}[bulkmod_cp]),
          num_entries=num_entries,
          num_referrals=num_referrals,
          text_ldifchangerecord=bulk_mod_list_ldif,
          hidden_fields=app.form.hiddenInputHTML(ignoreFieldNames=[
         'dn', 'scope', 'filterstr', 'bulkmod_submit', 'bulkmod_newsuperior'])))
        web2ldap.app.gui.footer(app)


def w2l_bulkmod--- This code section failed: ---

 L. 326         0  LOAD_FAST                'app'
                2  LOAD_ATTR                form
                4  LOAD_METHOD              getInputValue
                6  LOAD_STR                 'bulkmod_submit'
                8  LOAD_CONST               None
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_2         2  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'bulkmod_submit'

 L. 328        20  LOAD_FAST                'app'
               22  LOAD_ATTR                form
               24  LOAD_METHOD              getInputValue
               26  LOAD_STR                 'bulkmod_at'
               28  BUILD_LIST_0          0 
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'bulkmod_at'

 L. 329        34  LOAD_FAST                'app'
               36  LOAD_ATTR                form
               38  LOAD_METHOD              getInputValue
               40  LOAD_STR                 'bulkmod_op'
               42  BUILD_LIST_0          0 
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'bulkmod_op'

 L. 330        48  LOAD_FAST                'app'
               50  LOAD_ATTR                form
               52  LOAD_METHOD              getInputValue
               54  LOAD_STR                 'bulkmod_av'
               56  BUILD_LIST_0          0 
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'bulkmod_av'

 L. 332        62  LOAD_FAST                'app'
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

 L. 334        86  LOAD_GLOBAL              int
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

 L. 336       124  LOAD_FAST                'app'
              126  LOAD_ATTR                form
              128  LOAD_METHOD              getInputValue

 L. 337       130  LOAD_STR                 'filterstr'

 L. 338       132  LOAD_FAST                'app'
              134  LOAD_ATTR                ldap_url
              136  LOAD_ATTR                filterstr
              138  JUMP_IF_TRUE_OR_POP   142  'to 142'
              140  LOAD_STR                 ''
            142_0  COME_FROM           138  '138'
              142  BUILD_LIST_1          1 

 L. 336       144  CALL_METHOD_2         2  ''

 L. 339       146  LOAD_CONST               0

 L. 336       148  BINARY_SUBSCR    
              150  JUMP_IF_TRUE_OR_POP   154  'to 154'

 L. 339       152  LOAD_STR                 '(objectClass=*)'
            154_0  COME_FROM           150  '150'

 L. 336       154  STORE_FAST               'bulkmod_filter'

 L. 340       156  LOAD_FAST                'app'
              158  LOAD_ATTR                form
              160  LOAD_METHOD              getInputValue
              162  LOAD_STR                 'bulkmod_newsuperior'
              164  LOAD_STR                 ''
              166  BUILD_LIST_1          1 
              168  CALL_METHOD_2         2  ''
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  STORE_FAST               'bulkmod_newsuperior'

 L. 344       176  LOAD_FAST                'app'
              178  LOAD_ATTR                form
              180  LOAD_METHOD              getInputValue
              182  LOAD_STR                 'bulkmod_ctrl'
              184  BUILD_LIST_0          0 
              186  CALL_METHOD_2         2  ''
              188  STORE_FAST               'bulkmod_ctrl_oids'

 L. 346       190  LOAD_GLOBAL              len
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

 L. 347       224  LOAD_GLOBAL              web2ldap
              226  LOAD_ATTR                app
              228  LOAD_ATTR                core
              230  LOAD_METHOD              ErrorExit
              232  LOAD_STR                 'Invalid bulk modification input.'
              234  CALL_METHOD_1         1  ''
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           218  '218'

 L. 349       238  LOAD_GLOBAL              input_modlist

 L. 350       240  LOAD_FAST                'app'

 L. 351       242  LOAD_FAST                'bulkmod_at'

 L. 351       244  LOAD_FAST                'bulkmod_op'

 L. 351       246  LOAD_FAST                'bulkmod_av'

 L. 349       248  CALL_FUNCTION_4       4  ''
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'bulk_mod_list'
              254  STORE_FAST               'input_errors'

 L. 354       256  LOAD_FAST                'bulkmod_submit'
              258  LOAD_STR                 'Cancel'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   296  'to 296'

 L. 356       266  LOAD_FAST                'app'
              268  LOAD_ATTR                simple_message

 L. 357       270  LOAD_STR                 'Canceled bulk modification.'

 L. 358       272  LOAD_STR                 '<p class="SuccessMessage">Canceled bulk modification.</p>'

 L. 359       274  LOAD_GLOBAL              web2ldap
              276  LOAD_ATTR                app
              278  LOAD_ATTR                gui
              280  LOAD_METHOD              main_menu
              282  LOAD_FAST                'app'
              284  CALL_METHOD_1         1  ''

 L. 356       286  LOAD_CONST               ('main_menu_list',)
              288  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              290  POP_TOP          
          292_294  JUMP_FORWARD       1224  'to 1224'
            296_0  COME_FROM           262  '262'

 L. 362       296  LOAD_FAST                'bulk_mod_list'
          298_300  POP_JUMP_IF_TRUE    308  'to 308'
              302  LOAD_FAST                'bulkmod_newsuperior'
          304_306  POP_JUMP_IF_FALSE   358  'to 358'
            308_0  COME_FROM           298  '298'

 L. 363       308  LOAD_FAST                'input_errors'

 L. 362   310_312  POP_JUMP_IF_TRUE    358  'to 358'

 L. 364       314  LOAD_FAST                'bulkmod_submit'
              316  LOAD_CONST               None
              318  COMPARE_OP               is

 L. 362   320_322  POP_JUMP_IF_TRUE    358  'to 358'

 L. 365       324  LOAD_FAST                'bulkmod_submit'
              326  LOAD_STR                 '<<Back'
              328  COMPARE_OP               ==

 L. 362   330_332  POP_JUMP_IF_TRUE    358  'to 358'

 L. 366       334  LOAD_FAST                'bulkmod_submit'
              336  LOAD_METHOD              startswith
              338  LOAD_STR                 '+'
              340  CALL_METHOD_1         1  ''

 L. 362   342_344  POP_JUMP_IF_TRUE    358  'to 358'

 L. 367       346  LOAD_FAST                'bulkmod_submit'
              348  LOAD_METHOD              startswith
              350  LOAD_STR                 '-'
              352  CALL_METHOD_1         1  ''

 L. 362   354_356  POP_JUMP_IF_FALSE   392  'to 392'
            358_0  COME_FROM           342  '342'
            358_1  COME_FROM           330  '330'
            358_2  COME_FROM           320  '320'
            358_3  COME_FROM           310  '310'
            358_4  COME_FROM           304  '304'

 L. 369       358  LOAD_GLOBAL              bulkmod_input_form

 L. 370       360  LOAD_FAST                'app'

 L. 371       362  LOAD_FAST                'bulkmod_submit'

 L. 372       364  LOAD_FAST                'app'
              366  LOAD_ATTR                dn

 L. 372       368  LOAD_FAST                'scope'

 L. 372       370  LOAD_FAST                'bulkmod_filter'

 L. 373       372  LOAD_FAST                'bulkmod_newsuperior'

 L. 374       374  LOAD_FAST                'bulkmod_at'

 L. 374       376  LOAD_FAST                'bulkmod_op'

 L. 374       378  LOAD_FAST                'bulkmod_av'

 L. 374       380  LOAD_FAST                'bulkmod_cp'

 L. 375       382  LOAD_FAST                'input_errors'

 L. 369       384  CALL_FUNCTION_11     11  ''
              386  POP_TOP          
          388_390  JUMP_FORWARD       1224  'to 1224'
            392_0  COME_FROM           354  '354'

 L. 378       392  LOAD_FAST                'bulkmod_submit'
              394  LOAD_STR                 'Next>>'
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   428  'to 428'

 L. 380       402  LOAD_GLOBAL              bulkmod_confirmation_form

 L. 381       404  LOAD_FAST                'app'

 L. 382       406  LOAD_FAST                'app'
              408  LOAD_ATTR                dn

 L. 382       410  LOAD_FAST                'scope'

 L. 382       412  LOAD_FAST                'bulkmod_filter'

 L. 383       414  LOAD_FAST                'bulkmod_newsuperior'

 L. 383       416  LOAD_FAST                'bulk_mod_list'

 L. 383       418  LOAD_FAST                'bulkmod_cp'

 L. 380       420  CALL_FUNCTION_7       7  ''
              422  POP_TOP          
          424_426  JUMP_FORWARD       1224  'to 1224'
            428_0  COME_FROM           398  '398'

 L. 386       428  LOAD_FAST                'bulkmod_submit'
              430  LOAD_STR                 'Apply'
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 389       438  LOAD_FAST                'app'
              440  LOAD_ATTR                form
              442  LOAD_METHOD              getInputValue
              444  LOAD_STR                 'bulkmod_ctrl'
              446  BUILD_LIST_0          0 
              448  CALL_METHOD_2         2  ''
              450  STORE_FAST               'bulkmod_ctrl_oids'

 L. 390       452  LOAD_GLOBAL              set
              454  LOAD_LISTCOMP            '<code_object <listcomp>>'
              456  LOAD_STR                 'w2l_bulkmod.<locals>.<listcomp>'
              458  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 392       460  LOAD_FAST                'app'
              462  LOAD_ATTR                ls
              464  LOAD_ATTR                l
              466  LOAD_ATTR                _req_ctrls
              468  LOAD_STR                 '**all**'
              470  BINARY_SUBSCR    
              472  LOAD_FAST                'app'
              474  LOAD_ATTR                ls
              476  LOAD_ATTR                l
              478  LOAD_ATTR                _req_ctrls
              480  LOAD_STR                 '**write**'
              482  BINARY_SUBSCR    
              484  BINARY_ADD       
              486  LOAD_FAST                'app'
              488  LOAD_ATTR                ls
              490  LOAD_ATTR                l
              492  LOAD_ATTR                _req_ctrls
              494  LOAD_STR                 'modify'
              496  BINARY_SUBSCR    
              498  BINARY_ADD       

 L. 390       500  GET_ITER         
              502  CALL_FUNCTION_1       1  ''
              504  CALL_FUNCTION_1       1  ''
              506  STORE_DEREF              'conn_server_ctrls'

 L. 394       508  LOAD_GLOBAL              list
              510  LOAD_GLOBAL              set
              512  LOAD_CLOSURE             'conn_server_ctrls'
              514  BUILD_TUPLE_1         1 
              516  LOAD_LISTCOMP            '<code_object <listcomp>>'
              518  LOAD_STR                 'w2l_bulkmod.<locals>.<listcomp>'
              520  MAKE_FUNCTION_8          'closure'

 L. 396       522  LOAD_FAST                'bulkmod_ctrl_oids'

 L. 394       524  GET_ITER         
              526  CALL_FUNCTION_1       1  ''
              528  CALL_FUNCTION_1       1  ''
              530  CALL_FUNCTION_1       1  ''
          532_534  JUMP_IF_TRUE_OR_POP   538  'to 538'

 L. 398       536  LOAD_CONST               None
            538_0  COME_FROM           532  '532'

 L. 394       538  STORE_FAST               'bulkmod_server_ctrls'

 L. 400       540  BUILD_LIST_0          0 
              542  STORE_FAST               'ldap_error_html'

 L. 402       544  LOAD_GLOBAL              time
              546  LOAD_METHOD              time
              548  CALL_METHOD_0         0  ''
              550  STORE_FAST               'begin_time_stamp'

 L. 405       552  LOAD_FAST                'app'
              554  LOAD_ATTR                ls
              556  LOAD_ATTR                l
              558  LOAD_ATTR                search

 L. 406       560  LOAD_FAST                'app'
              562  LOAD_ATTR                dn

 L. 407       564  LOAD_FAST                'scope'

 L. 408       566  LOAD_FAST                'bulkmod_filter'

 L. 409       568  LOAD_FAST                'bulkmod_cp'
          570_572  POP_JUMP_IF_FALSE   580  'to 580'
              574  LOAD_STR                 '*'
              576  BUILD_LIST_1          1 
              578  JUMP_FORWARD        584  'to 584'
            580_0  COME_FROM           570  '570'
              580  LOAD_STR                 '1.1'
              582  BUILD_LIST_1          1 
            584_0  COME_FROM           578  '578'

 L. 405       584  LOAD_CONST               ('attrlist',)
              586  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              588  STORE_FAST               'ldap_msgid'

 L. 412       590  BUILD_LIST_0          0 
              592  STORE_FAST               'result_ldif_html'

 L. 415       594  LOAD_FAST                'app'
              596  LOAD_ATTR                ls
              598  LOAD_ATTR                l
              600  LOAD_METHOD              results
              602  LOAD_FAST                'ldap_msgid'
              604  CALL_METHOD_1         1  ''
              606  GET_ITER         
          608_610  FOR_ITER           1022  'to 1022'
              612  STORE_FAST               'res'

 L. 418       614  LOAD_FAST                'res'
              616  LOAD_ATTR                rtype
              618  LOAD_GLOBAL              ldap0
              620  LOAD_ATTR                RES_SEARCH_REFERENCE
              622  COMPARE_OP               ==
          624_626  POP_JUMP_IF_FALSE   632  'to 632'

 L. 420   628_630  JUMP_BACK           608  'to 608'
            632_0  COME_FROM           624  '624'

 L. 422       632  LOAD_FAST                'res'
              634  LOAD_ATTR                rdata
              636  GET_ITER         
            638_0  COME_FROM           774  '774'
          638_640  FOR_ITER           1018  'to 1018'
              642  STORE_FAST               'rdat'

 L. 425       644  LOAD_FAST                'bulk_mod_list'
          646_648  POP_JUMP_IF_FALSE   772  'to 772'

 L. 426       650  SETUP_FINALLY       678  'to 678'

 L. 427       652  LOAD_FAST                'app'
              654  LOAD_ATTR                ls
              656  LOAD_ATTR                l
              658  LOAD_ATTR                modify_s
              660  LOAD_FAST                'rdat'
              662  LOAD_ATTR                dn_s
              664  LOAD_FAST                'bulk_mod_list'
              666  LOAD_FAST                'bulkmod_server_ctrls'
              668  LOAD_CONST               ('req_ctrls',)
              670  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              672  POP_TOP          
              674  POP_BLOCK        
              676  JUMP_FORWARD        750  'to 750'
            678_0  COME_FROM_FINALLY   650  '650'

 L. 428       678  DUP_TOP          
              680  LOAD_GLOBAL              ldap0
              682  LOAD_ATTR                LDAPError
              684  COMPARE_OP               exception-match
          686_688  POP_JUMP_IF_FALSE   748  'to 748'
              690  POP_TOP          
              692  STORE_FAST               'e'
              694  POP_TOP          
              696  SETUP_FINALLY       736  'to 736'

 L. 429       698  LOAD_FAST                'ldap_error_html'
              700  LOAD_METHOD              append

 L. 430       702  LOAD_STR                 '<dt>%s</dt><dd>%s</dd>'

 L. 431       704  LOAD_FAST                'app'
              706  LOAD_ATTR                form
              708  LOAD_METHOD              utf2display
              710  LOAD_FAST                'rdat'
              712  LOAD_ATTR                dn_s
              714  CALL_METHOD_1         1  ''

 L. 432       716  LOAD_FAST                'app'
              718  LOAD_METHOD              ldap_error_msg
              720  LOAD_FAST                'e'
              722  CALL_METHOD_1         1  ''

 L. 430       724  BUILD_TUPLE_2         2 
              726  BINARY_MODULO    

 L. 429       728  CALL_METHOD_1         1  ''
              730  POP_TOP          
              732  POP_BLOCK        
              734  BEGIN_FINALLY    
            736_0  COME_FROM_FINALLY   696  '696'
              736  LOAD_CONST               None
              738  STORE_FAST               'e'
              740  DELETE_FAST              'e'
              742  END_FINALLY      
              744  POP_EXCEPT       
              746  JUMP_FORWARD        772  'to 772'
            748_0  COME_FROM           686  '686'
              748  END_FINALLY      
            750_0  COME_FROM           676  '676'

 L. 436       750  LOAD_FAST                'result_ldif_html'
              752  LOAD_METHOD              append
              754  LOAD_GLOBAL              modlist_ldif

 L. 437       756  LOAD_FAST                'rdat'
              758  LOAD_ATTR                dn_s

 L. 437       760  LOAD_FAST                'app'
              762  LOAD_ATTR                form

 L. 437       764  LOAD_FAST                'bulk_mod_list'

 L. 436       766  CALL_FUNCTION_3       3  ''
              768  CALL_METHOD_1         1  ''
              770  POP_TOP          
            772_0  COME_FROM           746  '746'
            772_1  COME_FROM           646  '646'

 L. 441       772  LOAD_FAST                'bulkmod_newsuperior'
          774_776  POP_JUMP_IF_FALSE   638  'to 638'

 L. 442       778  LOAD_GLOBAL              str
              780  LOAD_GLOBAL              DNObj
              782  LOAD_METHOD              from_str
              784  LOAD_FAST                'rdat'
              786  LOAD_ATTR                dn_s
              788  CALL_METHOD_1         1  ''
              790  LOAD_METHOD              rdn
              792  CALL_METHOD_0         0  ''
              794  CALL_FUNCTION_1       1  ''
              796  STORE_FAST               'old_rdn'

 L. 443       798  SETUP_FINALLY       888  'to 888'

 L. 444       800  LOAD_FAST                'bulkmod_cp'
          802_804  POP_JUMP_IF_FALSE   854  'to 854'

 L. 445       806  LOAD_STR                 ','
              808  LOAD_METHOD              join

 L. 446       810  LOAD_FAST                'old_rdn'

 L. 447       812  LOAD_FAST                'bulkmod_newsuperior'

 L. 445       814  BUILD_TUPLE_2         2 
              816  CALL_METHOD_1         1  ''
              818  STORE_FAST               'new_ldap_dn'

 L. 449       820  LOAD_FAST                'rdat'
              822  LOAD_ATTR                entry_b
          824_826  POP_JUMP_IF_TRUE    834  'to 834'

 L. 450       828  LOAD_GLOBAL              ldap0
              830  LOAD_ATTR                NO_SUCH_OBJECT
              832  RAISE_VARARGS_1       1  'exception instance'
            834_0  COME_FROM           824  '824'

 L. 451       834  LOAD_FAST                'app'
              836  LOAD_ATTR                ls
              838  LOAD_ATTR                l
              840  LOAD_METHOD              add_s
              842  LOAD_FAST                'new_ldap_dn'
              844  LOAD_FAST                'rdat'
              846  LOAD_ATTR                entry_as
              848  CALL_METHOD_2         2  ''
              850  POP_TOP          
              852  JUMP_FORWARD        884  'to 884'
            854_0  COME_FROM           802  '802'

 L. 453       854  LOAD_FAST                'app'
              856  LOAD_ATTR                ls
              858  LOAD_ATTR                rename

 L. 454       860  LOAD_FAST                'rdat'
              862  LOAD_ATTR                dn_s

 L. 455       864  LOAD_FAST                'old_rdn'

 L. 456       866  LOAD_FAST                'bulkmod_newsuperior'

 L. 457       868  LOAD_FAST                'app'
              870  LOAD_METHOD              cfg_param
              872  LOAD_STR                 'bulkmod_delold'
              874  LOAD_CONST               0
              876  CALL_METHOD_2         2  ''

 L. 453       878  LOAD_CONST               ('new_superior', 'delold')
              880  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              882  POP_TOP          
            884_0  COME_FROM           852  '852'
              884  POP_BLOCK        
              886  JUMP_FORWARD        966  'to 966'
            888_0  COME_FROM_FINALLY   798  '798'

 L. 459       888  DUP_TOP          
              890  LOAD_GLOBAL              ldap0
              892  LOAD_ATTR                LDAPError
              894  COMPARE_OP               exception-match
          896_898  POP_JUMP_IF_FALSE   964  'to 964'
              900  POP_TOP          
              902  STORE_FAST               'e'
              904  POP_TOP          
              906  SETUP_FINALLY       952  'to 952'

 L. 460       908  LOAD_FAST                'ldap_error_html'
              910  LOAD_METHOD              append

 L. 461       912  LOAD_STR                 '<dt>%s</dt><dd>%s</dd>'

 L. 462       914  LOAD_FAST                'app'
              916  LOAD_ATTR                form
              918  LOAD_METHOD              utf2display
              920  LOAD_FAST                'rdat'
              922  LOAD_ATTR                dn_s
              924  CALL_METHOD_1         1  ''

 L. 463       926  LOAD_FAST                'app'
              928  LOAD_ATTR                form
              930  LOAD_METHOD              utf2display
              932  LOAD_GLOBAL              str
              934  LOAD_FAST                'e'
              936  CALL_FUNCTION_1       1  ''
              938  CALL_METHOD_1         1  ''

 L. 461       940  BUILD_TUPLE_2         2 
              942  BINARY_MODULO    

 L. 460       944  CALL_METHOD_1         1  ''
              946  POP_TOP          
              948  POP_BLOCK        
              950  BEGIN_FINALLY    
            952_0  COME_FROM_FINALLY   906  '906'
              952  LOAD_CONST               None
              954  STORE_FAST               'e'
              956  DELETE_FAST              'e'
              958  END_FINALLY      
              960  POP_EXCEPT       
              962  JUMP_BACK           638  'to 638'
            964_0  COME_FROM           896  '896'
              964  END_FINALLY      
            966_0  COME_FROM           886  '886'

 L. 467       966  LOAD_FAST                'result_ldif_html'
              968  LOAD_METHOD              append

 L. 468       970  LOAD_STR                 '<p>%s %s beneath %s</p>'

 L. 469       972  LOAD_STR                 'Moved'
              974  LOAD_STR                 'Copied'
              976  LOAD_CONST               (False, True)
              978  BUILD_CONST_KEY_MAP_2     2 
              980  LOAD_FAST                'bulkmod_cp'
              982  BINARY_SUBSCR    

 L. 470       984  LOAD_FAST                'app'
              986  LOAD_ATTR                form
              988  LOAD_METHOD              utf2display
              990  LOAD_FAST                'rdat'
              992  LOAD_ATTR                dn_s
              994  CALL_METHOD_1         1  ''

 L. 471       996  LOAD_FAST                'app'
              998  LOAD_ATTR                form
             1000  LOAD_METHOD              utf2display
             1002  LOAD_FAST                'bulkmod_newsuperior'
             1004  CALL_METHOD_1         1  ''

 L. 468      1006  BUILD_TUPLE_3         3 
             1008  BINARY_MODULO    

 L. 467      1010  CALL_METHOD_1         1  ''
             1012  POP_TOP          
         1014_1016  JUMP_BACK           638  'to 638'
         1018_1020  JUMP_BACK           608  'to 608'

 L. 475      1022  LOAD_GLOBAL              time
             1024  LOAD_METHOD              time
             1026  CALL_METHOD_0         0  ''
             1028  STORE_FAST               'end_time_stamp'

 L. 477      1030  LOAD_STR                 ''
             1032  STORE_FAST               'error_messages'

 L. 478      1034  LOAD_FAST                'ldap_error_html'
         1036_1038  POP_JUMP_IF_FALSE  1056  'to 1056'

 L. 479      1040  LOAD_STR                 '<strong>Errors</strong><dl>%s</dl>'

 L. 480      1042  LOAD_STR                 '\n'
             1044  LOAD_METHOD              join
             1046  LOAD_FAST                'ldap_error_html'
             1048  CALL_METHOD_1         1  ''

 L. 479      1050  BUILD_TUPLE_1         1 
             1052  BINARY_MODULO    
             1054  STORE_FAST               'error_messages'
           1056_0  COME_FROM          1036  '1036'

 L. 482      1056  LOAD_STR                 ''
             1058  STORE_FAST               'change_records'

 L. 483      1060  LOAD_FAST                'result_ldif_html'
         1062_1064  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 484      1066  LOAD_STR                 '<strong>Successfully applied changes</strong><p>%s</p>'

 L. 485      1068  LOAD_STR                 '\n'
             1070  LOAD_METHOD              join
             1072  LOAD_FAST                'result_ldif_html'
             1074  CALL_METHOD_1         1  ''

 L. 484      1076  BUILD_TUPLE_1         1 
             1078  BINARY_MODULO    
             1080  STORE_FAST               'change_records'
           1082_0  COME_FROM          1062  '1062'

 L. 488      1082  LOAD_GLOBAL              len
             1084  LOAD_FAST                'result_ldif_html'
             1086  CALL_FUNCTION_1       1  ''
             1088  STORE_FAST               'num_mods'

 L. 489      1090  LOAD_GLOBAL              len
             1092  LOAD_FAST                'ldap_error_html'
             1094  CALL_FUNCTION_1       1  ''
             1096  STORE_FAST               'num_errors'

 L. 490      1098  LOAD_FAST                'num_mods'
             1100  LOAD_FAST                'num_errors'
             1102  BINARY_ADD       
             1104  STORE_FAST               'num_sum'

 L. 491      1106  LOAD_FAST                'app'
             1108  LOAD_ATTR                simple_message

 L. 492      1110  LOAD_STR                 'Modified entries'

 L. 493      1112  LOAD_STR                 '\n            <p class="SuccessMessage">Modified entries.</p>\n            <table>\n              <tr>\n                <td>Modified entries:</td>\n                <td>%d</td>\n                <td>\n                  <meter min="0" max="%d" value="%d" optimum="%d" title="entries">%d</meter>\n                </td>\n              </tr>\n              <tr>\n                <td>Errors:</td>\n                <td>%d</td>\n                <td>\n                  <meter min="0" max="%d" value="%d" optimum="0" title="entries">%d</meter>\n                </td>\n              </tr>\n              <tr><td>Search base:</td><td>%s</td></tr>\n              <tr><td>Search scope:</td><td>%s</td></tr>\n              <tr><td>Time elapsed:</td><td>%0.2f seconds</td></tr>\n            </table>\n            %s\n            %s\n              <p><input type="submit" name="bulkmod_submit" value="&lt;&lt;Back"></p>\n            </form>\n            %s\n            %s\n            '

 L. 521      1114  LOAD_FAST                'num_mods'

 L. 522      1116  LOAD_FAST                'num_sum'

 L. 522      1118  LOAD_FAST                'num_mods'

 L. 522      1120  LOAD_FAST                'num_sum'

 L. 522      1122  LOAD_FAST                'num_mods'

 L. 523      1124  LOAD_FAST                'num_errors'

 L. 524      1126  LOAD_FAST                'num_sum'

 L. 524      1128  LOAD_FAST                'num_errors'

 L. 524      1130  LOAD_FAST                'num_errors'

 L. 525      1132  LOAD_FAST                'app'
             1134  LOAD_METHOD              display_dn
             1136  LOAD_FAST                'app'
             1138  LOAD_ATTR                dn
             1140  CALL_METHOD_1         1  ''

 L. 526      1142  LOAD_GLOBAL              ldap0
             1144  LOAD_ATTR                ldapurl
             1146  LOAD_ATTR                SEARCH_SCOPE_STR
             1148  LOAD_FAST                'scope'
             1150  BINARY_SUBSCR    

 L. 527      1152  LOAD_FAST                'end_time_stamp'
             1154  LOAD_FAST                'begin_time_stamp'
             1156  BINARY_SUBTRACT  

 L. 528      1158  LOAD_FAST                'app'
             1160  LOAD_METHOD              begin_form
             1162  LOAD_STR                 'bulkmod'
             1164  LOAD_STR                 'POST'
             1166  CALL_METHOD_2         2  ''

 L. 529      1168  LOAD_FAST                'app'
             1170  LOAD_ATTR                form
             1172  LOAD_ATTR                hiddenInputHTML
             1174  LOAD_STR                 'bulkmod_submit'
             1176  BUILD_LIST_1          1 
             1178  LOAD_CONST               ('ignoreFieldNames',)
             1180  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 530      1182  LOAD_FAST                'error_messages'

 L. 531      1184  LOAD_FAST                'change_records'

 L. 520      1186  BUILD_TUPLE_16       16 

 L. 493      1188  BINARY_MODULO    

 L. 533      1190  LOAD_GLOBAL              web2ldap
             1192  LOAD_ATTR                app
             1194  LOAD_ATTR                gui
             1196  LOAD_METHOD              main_menu
             1198  LOAD_FAST                'app'
             1200  CALL_METHOD_1         1  ''

 L. 491      1202  LOAD_CONST               ('main_menu_list',)
             1204  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1206  POP_TOP          
             1208  JUMP_FORWARD       1224  'to 1224'
           1210_0  COME_FROM           434  '434'

 L. 538      1210  LOAD_GLOBAL              web2ldap
             1212  LOAD_ATTR                app
             1214  LOAD_ATTR                core
             1216  LOAD_METHOD              ErrorExit
             1218  LOAD_STR                 'Invalid bulk modification form data.'
             1220  CALL_METHOD_1         1  ''
             1222  RAISE_VARARGS_1       1  'exception instance'
           1224_0  COME_FROM          1208  '1208'
           1224_1  COME_FROM           424  '424'
           1224_2  COME_FROM           388  '388'
           1224_3  COME_FROM           292  '292'

Parse error at or near `JUMP_FORWARD' instruction at offset 388_390