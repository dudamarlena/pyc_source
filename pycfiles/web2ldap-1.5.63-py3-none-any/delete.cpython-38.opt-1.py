# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/delete.py
# Compiled at: 2019-12-16 17:14:31
# Size of source mod 2**32: 17253 bytes
"""
web2ldap.app.delete: delete one entry or several entries

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, ldap0
from ldap0.res import SearchResultEntry
import web2ldap.web.forms, web2ldap.ldaputil.asynch, web2ldap.ldapsession, web2ldap.ldaputil, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.gui
from web2ldap.log import logger
DELETE_SUBTREE_FORM_TMPL = '\n<p class="WarningMessage">\n  Delete entries found below {text_dn}?<br>\n  {text_num_sub_ordinates}\n  {text_num_all_sub_ordinates}\n</p>\n<table>\n  <tr>\n    <td>Scope:</td>\n    <td>{field_delete_scope}</td>\n  </tr>\n  <tr>\n    <td>Use tree delete control:</td>\n    <td>\n      <input type="checkbox"\n             name="delete_ctrl"\n             value="{value_delete_ctrl_oid}"{value_delete_ctrl_checked}>\n    </td>\n  </tr>\n</table>\n<p><strong>\n    Use recursive delete with extreme care!\n    Might take some time.\n</strong></p>\n'
DELETE_FORM_TEMPLATE = '\n  {form_begin}\n    {inner_form}\n    <dl>\n      <dt>Use extended controls:</dt>\n      <dd>{field_delete_ctrl}</dd>\n    </dl>\n    <p class="WarningMessage">Are you sure?</p>\n    {field_hidden_dn}\n    <input type="submit" name="delete_confirm" value="yes">\n    <input type="submit" name="delete_confirm" value="no">\n  </form>\n'
DELETE_SEARCH_FORM_TMPL = '\n<p class="WarningMessage">\n  Delete entries found with search?\n</p>\n<table>\n<tr>\n  <td>Search base:</td><td>{text_dn}</td>\n</tr>\n<tr>\n  <td>Search scope:</td><td>{text_scope}</td>\n</tr>\n<tr>\n  <td>Delete filter:</td>\n  <td>\n    {value_delete_filter}\n  </td>\n</tr>\n<tr>\n  <td># affected entries / referrals:</td>\n  <td>\n    {num_entries} / {num_referrals}\n  </td>\n</tr>\n</table>\n<input type="hidden" name="filterstr" value="{value_delete_filter}">\n<input type="hidden" name="scope" value="{value_delete_scope}">\n'
DELETE_ENTRIES_SUCCESS_TMPL = '\n<p class="SuccessMessage">Deleted entries.</p>\n<table>\n  <tr><td>Deleted entries:</td><td>%d</td></tr>\n  <tr><td>Search base:</td><td>%s</td></tr>\n  <tr><td>Search scope:</td><td>%s</td></tr>\n  <tr><td>Time elapsed:</td><td>%0.2f seconds</td></tr>\n  <tr><td>Skipped:</td><td>%d</td></tr>\n</table>\n'

class DeleteLeafs(web2ldap.ldaputil.asynch.AsyncSearchHandler):
    __doc__ = '\n    Class for deleting entries which are results of a search.\n\n    DNs of Non-leaf entries are collected in DeleteLeafs.nonLeafEntries.\n    '
    _entryResultTypes = {
     ldap0.RES_SEARCH_ENTRY,
     ldap0.RES_SEARCH_RESULT}

    def __init__(self, l, tree_delete_ctrl, delete_server_ctrls):
        web2ldap.ldaputil.asynch.AsyncSearchHandler.__init__(self, l)
        self.req_ctrls = delete_server_ctrls
        self.tree_delete_ctrl = tree_delete_ctrl

    def start_search(self, searchRoot, searchScope, filterStr):
        if searchScope == ldap0.SCOPE_BASE:
            raise ValueError('Parameter searchScope must not be ldap0.SCOPE_BASE.')
        self.nonLeafEntries = []
        self.nonDeletableEntries = []
        self.deletedEntries = 0
        self.noSuchObjectCounter = 0
        web2ldap.ldaputil.asynch.AsyncSearchHandler.start_search(self,
          searchRoot,
          searchScope,
          filterStr=filterStr,
          attrList=[
         'hasSubordinates',
         'subordinateCount',
         'numSubordinates',
         'numAllSubordinates',
         'msDS-Approx-Immed-Subordinates'])

    def _process_result(self, resultItem):
        if not isinstance(resultItem, SearchResultEntry):
            return
        dn, entry = resultItem.dn_s, resultItem.entry_s
        try:
            hasSubordinates = entry['hasSubordinates'][0].upper() == 'TRUE'
        except KeyError:
            hasSubordinates = None
            try:
                subordinateCount = int(entry.get('subordinateCount', entry.get('numSubordinates', entry.get('numAllSubordinates', entry['msDS-Approx-Immed-Subordinates'])))[0])
            except KeyError:
                subordinateCount = None

        else:
            subordinateCount = None
        if not self.tree_delete_ctrl:
            if not hasSubordinates:
                if (subordinateCount or 0) > 0:
                    logger.debug('Skipping deletion of non-leaf entry %r', dn)
                    self.nonLeafEntries.append(dn)
                    return None
        logger.debug('Deleting entry %r', dn)
        try:
            self._l.delete_s(dn, req_ctrls=(self.req_ctrls))
        except ldap0.NO_SUCH_OBJECT:
            self.noSuchObjectCounter += 1
        except ldap0.INSUFFICIENT_ACCESS:
            self.nonDeletableEntries.append(dn)
        except ldap0.NOT_ALLOWED_ON_NONLEAF:
            if hasSubordinates is None and subordinateCount is None:
                self.nonLeafEntries.append(dn)
            else:
                raise ValueError('Non-leaf entry %r has hasSubordinates %r and subordinateCount %r' % (
                 dn, hasSubordinates, subordinateCount))
        else:
            self.deletedEntries += 1


def delete_entries--- This code section failed: ---

 L. 215         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'start_time'

 L. 216         8  LOAD_FAST                'start_time'
               10  LOAD_FAST                'delete_timelimit'
               12  BINARY_ADD       
               14  STORE_FAST               'end_time'

 L. 217        16  LOAD_FAST                'delete_filter'
               18  JUMP_IF_TRUE_OR_POP    22  'to 22'
               20  LOAD_STR                 '(objectClass=*)'
             22_0  COME_FROM            18  '18'
               22  STORE_FAST               'delete_filter'

 L. 218        24  LOAD_FAST                'scope'
               26  LOAD_GLOBAL              ldap0
               28  LOAD_ATTR                SCOPE_SUBTREE
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    66  'to 66'
               34  LOAD_FAST                'tree_delete_control'
               36  POP_JUMP_IF_FALSE    66  'to 66'

 L. 220        38  LOAD_FAST                'app'
               40  LOAD_ATTR                ls
               42  LOAD_ATTR                l
               44  LOAD_ATTR                delete_s
               46  LOAD_FAST                'dn'
               48  LOAD_FAST                'delete_server_ctrls'
               50  LOAD_CONST               ('req_ctrls',)
               52  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               54  POP_TOP          

 L. 221        56  LOAD_CONST               1
               58  LOAD_GLOBAL              set
               60  CALL_FUNCTION_0       0  ''
               62  BUILD_TUPLE_2         2 
               64  RETURN_VALUE     
             66_0  COME_FROM            36  '36'
             66_1  COME_FROM            32  '32'

 L. 222        66  LOAD_GLOBAL              DeleteLeafs
               68  LOAD_FAST                'app'
               70  LOAD_ATTR                ls
               72  LOAD_ATTR                l
               74  LOAD_FAST                'tree_delete_control'
               76  LOAD_FAST                'delete_server_ctrls'
               78  CALL_FUNCTION_3       3  ''
               80  STORE_FAST               'leafs_deleter'

 L. 223        82  LOAD_CONST               0
               84  STORE_FAST               'deleted_entries_count'

 L. 224        86  LOAD_GLOBAL              set
               88  CALL_FUNCTION_0       0  ''
               90  STORE_FAST               'non_leaf_entries'

 L. 225        92  LOAD_GLOBAL              set
               94  CALL_FUNCTION_0       0  ''
               96  STORE_FAST               'non_deletable_entries'

 L. 226        98  LOAD_GLOBAL              time
              100  LOAD_METHOD              time
              102  CALL_METHOD_0         0  ''
              104  LOAD_FAST                'end_time'
              106  COMPARE_OP               <=
          108_110  POP_JUMP_IF_FALSE   270  'to 270'

 L. 227       112  SETUP_FINALLY       142  'to 142'

 L. 228       114  LOAD_FAST                'leafs_deleter'
              116  LOAD_ATTR                start_search
              118  LOAD_FAST                'dn'
              120  LOAD_FAST                'scope'
              122  LOAD_FAST                'delete_filter'
              124  LOAD_CONST               ('filterStr',)
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  POP_TOP          

 L. 229       130  LOAD_FAST                'leafs_deleter'
              132  LOAD_METHOD              process_results
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          
              138  POP_BLOCK        
              140  JUMP_FORWARD        230  'to 230'
            142_0  COME_FROM_FINALLY   112  '112'

 L. 230       142  DUP_TOP          
              144  LOAD_GLOBAL              ldap0
              146  LOAD_ATTR                NO_SUCH_OBJECT
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   168  'to 168'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 231       158  POP_EXCEPT       
          160_162  JUMP_ABSOLUTE       280  'to 280'
              164  POP_EXCEPT       
              166  JUMP_BACK            98  'to 98'
            168_0  COME_FROM           150  '150'

 L. 232       168  DUP_TOP          
              170  LOAD_GLOBAL              ldap0
              172  LOAD_ATTR                SIZELIMIT_EXCEEDED
              174  LOAD_GLOBAL              ldap0
              176  LOAD_ATTR                ADMINLIMIT_EXCEEDED
              178  BUILD_TUPLE_2         2 
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   228  'to 228'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 233       190  LOAD_FAST                'deleted_entries_count'
              192  LOAD_FAST                'leafs_deleter'
              194  LOAD_ATTR                deletedEntries
              196  INPLACE_ADD      
              198  STORE_FAST               'deleted_entries_count'

 L. 234       200  LOAD_FAST                'non_leaf_entries'
              202  LOAD_METHOD              update
              204  LOAD_FAST                'leafs_deleter'
              206  LOAD_ATTR                nonLeafEntries
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          

 L. 235       212  LOAD_FAST                'non_deletable_entries'
              214  LOAD_METHOD              update
              216  LOAD_FAST                'leafs_deleter'
              218  LOAD_ATTR                nonDeletableEntries
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
              224  POP_EXCEPT       
              226  JUMP_BACK            98  'to 98'
            228_0  COME_FROM           182  '182'
              228  END_FINALLY      
            230_0  COME_FROM           140  '140'

 L. 237       230  LOAD_FAST                'deleted_entries_count'
              232  LOAD_FAST                'leafs_deleter'
              234  LOAD_ATTR                deletedEntries
              236  INPLACE_ADD      
              238  STORE_FAST               'deleted_entries_count'

 L. 238       240  LOAD_FAST                'non_leaf_entries'
              242  LOAD_METHOD              update
              244  LOAD_FAST                'leafs_deleter'
              246  LOAD_ATTR                nonLeafEntries
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          

 L. 239       252  LOAD_FAST                'non_deletable_entries'
              254  LOAD_METHOD              update
              256  LOAD_FAST                'leafs_deleter'
              258  LOAD_ATTR                nonDeletableEntries
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          

 L. 240   264_266  BREAK_LOOP          280  'to 280'
              268  JUMP_BACK            98  'to 98'
            270_0  COME_FROM           108  '108'

 L. 242       270  LOAD_FAST                'non_deletable_entries'
              272  LOAD_METHOD              update
              274  LOAD_FAST                'non_leaf_entries'
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
            280_0  COME_FROM           474  '474'

 L. 243       280  LOAD_FAST                'non_leaf_entries'
          282_284  POP_JUMP_IF_FALSE   496  'to 496'
              286  LOAD_GLOBAL              time
              288  LOAD_METHOD              time
              290  CALL_METHOD_0         0  ''
              292  LOAD_FAST                'end_time'
              294  COMPARE_OP               <=
          296_298  POP_JUMP_IF_FALSE   496  'to 496'

 L. 244       300  LOAD_FAST                'non_leaf_entries'
              302  LOAD_METHOD              pop
              304  CALL_METHOD_0         0  ''
              306  STORE_FAST               'dn'

 L. 245       308  LOAD_FAST                'dn'
              310  LOAD_FAST                'non_deletable_entries'
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   322  'to 322'

 L. 246   318_320  JUMP_BACK           280  'to 280'
            322_0  COME_FROM           314  '314'

 L. 247       322  SETUP_FINALLY       354  'to 354'

 L. 248       324  LOAD_FAST                'leafs_deleter'
              326  LOAD_ATTR                start_search
              328  LOAD_FAST                'dn'
              330  LOAD_GLOBAL              ldap0
              332  LOAD_ATTR                SCOPE_SUBTREE
              334  LOAD_FAST                'delete_filter'
              336  LOAD_CONST               ('filterStr',)
              338  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              340  POP_TOP          

 L. 249       342  LOAD_FAST                'leafs_deleter'
              344  LOAD_METHOD              process_results
              346  CALL_METHOD_0         0  ''
              348  POP_TOP          
              350  POP_BLOCK        
              352  JUMP_FORWARD        416  'to 416'
            354_0  COME_FROM_FINALLY   322  '322'

 L. 250       354  DUP_TOP          
              356  LOAD_GLOBAL              ldap0
              358  LOAD_ATTR                SIZELIMIT_EXCEEDED
              360  LOAD_GLOBAL              ldap0
              362  LOAD_ATTR                ADMINLIMIT_EXCEEDED
              364  BUILD_TUPLE_2         2 
              366  COMPARE_OP               exception-match
          368_370  POP_JUMP_IF_FALSE   414  'to 414'
              372  POP_TOP          
              374  POP_TOP          
              376  POP_TOP          

 L. 251       378  LOAD_FAST                'deleted_entries_count'
              380  LOAD_FAST                'leafs_deleter'
              382  LOAD_ATTR                deletedEntries
              384  INPLACE_ADD      
              386  STORE_FAST               'deleted_entries_count'

 L. 252       388  LOAD_FAST                'non_leaf_entries'
              390  LOAD_METHOD              add
              392  LOAD_FAST                'dn'
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          

 L. 253       398  LOAD_FAST                'non_leaf_entries'
              400  LOAD_METHOD              update
              402  LOAD_FAST                'leafs_deleter'
              404  LOAD_ATTR                nonLeafEntries
              406  CALL_METHOD_1         1  ''
              408  POP_TOP          
              410  POP_EXCEPT       
              412  JUMP_FORWARD        464  'to 464'
            414_0  COME_FROM           368  '368'
              414  END_FINALLY      
            416_0  COME_FROM           352  '352'

 L. 255       416  LOAD_FAST                'deleted_entries_count'
              418  LOAD_FAST                'leafs_deleter'
              420  LOAD_ATTR                deletedEntries
              422  INPLACE_ADD      
              424  STORE_FAST               'deleted_entries_count'

 L. 256       426  LOAD_FAST                'leafs_deleter'
              428  LOAD_ATTR                deletedEntries
              430  LOAD_CONST               0
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE   452  'to 452'

 L. 257       438  LOAD_FAST                'non_deletable_entries'
              440  LOAD_METHOD              add
              442  LOAD_FAST                'dn'
              444  CALL_METHOD_1         1  ''
              446  POP_TOP          

 L. 258   448_450  JUMP_BACK           280  'to 280'
            452_0  COME_FROM           434  '434'

 L. 259       452  LOAD_FAST                'non_leaf_entries'
              454  LOAD_METHOD              update
              456  LOAD_FAST                'leafs_deleter'
              458  LOAD_ATTR                nonLeafEntries
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
            464_0  COME_FROM           412  '412'

 L. 260       464  LOAD_GLOBAL              time
              466  LOAD_METHOD              time
              468  CALL_METHOD_0         0  ''
              470  LOAD_FAST                'end_time'
              472  COMPARE_OP               >
          474_476  POP_JUMP_IF_FALSE   280  'to 280'

 L. 261       478  LOAD_FAST                'non_deletable_entries'
              480  LOAD_METHOD              update
              482  LOAD_FAST                'non_leaf_entries'
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          

 L. 262   488_490  BREAK_LOOP          506  'to 506'
          492_494  JUMP_BACK           280  'to 280'
            496_0  COME_FROM           296  '296'
            496_1  COME_FROM           282  '282'

 L. 264       496  LOAD_FAST                'non_deletable_entries'
              498  LOAD_METHOD              update
              500  LOAD_FAST                'non_leaf_entries'
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          

 L. 265       506  LOAD_FAST                'deleted_entries_count'
              508  LOAD_FAST                'non_deletable_entries'
              510  BUILD_TUPLE_2         2 
              512  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 164


def del_singleentry_form(app):
    return '<p class="WarningMessage">Delete whole entry %s?</p>' % app.display_dn(app.dn)


def del_subtree_form(app, scope):
    delete_scope_field = web2ldap.web.forms.Select('scope',
      'Scope of delete operation', 1, options=(
     (
      str(ldap0.SCOPE_BASE), 'Only this entry'),
     (
      str(ldap0.SCOPE_ONELEVEL), 'All entries below this entry (recursive)'),
     (
      str(ldap0.SCOPE_SUBTREE), 'All entries including this entry (recursive)')),
      default=(str(scope)))
    hasSubordinates, numSubordinates, numAllSubordinates = app.ls.get_sub_ordinates(app.dn)
    if not hasSubordinates:
        return del_singleentry_form(app)
    else:
        if numSubordinates:
            numSubordinates_html = '<p>Number of direct subordinates: %d</p>' % numSubordinates
        else:
            numSubordinates_html = ''
        if numAllSubordinates:
            numAllSubordinates_html = '<p>Total number of subordinates: %d</p>' % numAllSubordinates
        else:
            numAllSubordinates_html = ''
    return DELETE_SUBTREE_FORM_TMPL.format(text_dn=(app.display_dn(app.dn)),
      text_num_sub_ordinates=numSubordinates_html,
      text_num_all_sub_ordinates=numAllSubordinates_html,
      field_delete_scope=(delete_scope_field.input_html()),
      value_delete_ctrl_oid=(web2ldap.ldapsession.CONTROL_TREEDELETE),
      value_delete_ctrl_checked=(' checked' * int(web2ldap.ldapsession.CONTROL_TREEDELETE in app.ls.supportedControl and not app.ls.is_openldap)))


def del_attr_form(app, entry, delete_attr):
    return '\n    <p class="WarningMessage">Delete following attribute(s) of entry %s?</p>\n    <p>%s</p>\n    ' % (
     app.display_dn(app.dn),
     '\n'.join(['<input type="checkbox" name="delete_attr" value="%s"%s>%s<br>' % (
      app.form.utf2display(attr_type, sp_entity='  '),
      ' checked' * (attr_type in entry),
      app.form.utf2display(attr_type)) for attr_type in delete_attr]))


def del_search_form(app, scope, delete_filter):
    try:
        num_entries, num_referrals = app.ls.count((app.dn),
          scope,
          delete_filter,
          sizelimit=1000)
    except web2ldap.ldapsession.LDAPLimitErrors:
        num_entries, num_referrals = ('unknown', 'unknown')
    else:
        if num_entries is None:
            num_entries = 'unknown'
        else:
            num_entries = str(num_entries)


def w2l_delete(app):
    delete_confirm = app.form.getInputValue('delete_confirm', [None])[0]
    delete_attr = app.form.getInputValue('delete_attr', [a.decode('ascii') for a in app.ldap_url.attrs or []])
    delete_filter = app.form.getInputValue('filterstr', [app.ldap_url.filterstr])[0]
    delete_attr.sort()
    if delete_attr:
        scope = ldap0.SCOPE_BASE
    else:
        scope = int(app.form.getInputValue('scope', [str(app.ldap_url.scope or ldap0.SCOPE_BASE)])[0])
    delete_ctrl_oids = app.form.getInputValue('delete_ctrl', [])
    delete_ctrl_tree_delete = web2ldap.ldapsession.CONTROL_TREEDELETE in delete_ctrl_oids
    if delete_confirm is None:
        ldap_res = app.ls.l.read_s((app.dn),
          filterstr='(objectClass=*)',
          attrlist=delete_attr,
          cache_ttl=(-1.0))
        entry = ldap0.schema.models.Entry(app.schema, app.dn, ldap_res.entry_as)
        if delete_attr:
            inner_form = del_attr_form(app, entry, delete_attr)
        else:
            if delete_filter:
                inner_form = del_search_form(app, scope, delete_filter)
            else:
                inner_form = del_subtree_form(app, scope)
        web2ldap.app.gui.top_section(app,
          'Delete entry?',
          (web2ldap.app.gui.main_menu(app)),
          context_menu_list=[])
        app.outf.write(DELETE_FORM_TEMPLATE.format(form_begin=(app.begin_form('delete', 'POST')),
          inner_form=inner_form,
          field_delete_ctrl=app.form.field['delete_ctrl'].input_html(default=delete_ctrl_oids),
          field_hidden_dn=(app.form.hiddenFieldHTML('dn', app.dn, ''))))
        web2ldap.app.gui.footer(app)
        return None
    if delete_confirm != 'yes':
        app.simple_message('Canceled delete',
          '<p class="SuccessMessage">Canceled delete.</p>',
          main_menu_list=(web2ldap.app.gui.main_menu(app)),
          context_menu_list=(web2ldap.app.gui.ContextMenuSingleEntry(app)))
        return
    conn_server_ctrls = set([server_ctrl.controlType for server_ctrl in app.ls.l._req_ctrls['**all**'] + app.ls.l._req_ctrls['**write**'] + app.ls.l._req_ctrls['delete']])
    delete_server_ctrls = [ldap0.controls.LDAPControl(ctrl_oid, True, None) for ctrl_oid in delete_ctrl_oids if ctrl_oid if ctrl_oid not in conn_server_ctrls] or None
    if scope != ldap0.SCOPE_BASE:
        begin_time_stamp = time.time()
        deleted_entries_count, non_deletable_entries = delete_entries(app, app.dn, scope, delete_ctrl_tree_delete, delete_server_ctrls, delete_filter)
        end_time_stamp = time.time()
        old_dn = app.dn
        if scope == ldap0.SCOPE_SUBTREE:
            if delete_filter is None:
                app.dn = app.parent_dn
            app.simple_message('Deleted entries',
              (DELETE_ENTRIES_SUCCESS_TMPL % (
             deleted_entries_count,
             app.display_dn(old_dn),
             ldap0.ldapurl.SEARCH_SCOPE_STR[scope],
             end_time_stamp - begin_time_stamp,
             len(non_deletable_entries))),
              main_menu_list=(web2ldap.app.gui.main_menu(app)),
              context_menu_list=[])
        else:
            pass
    if scope == ldap0.SCOPE_BASE and delete_attr:
        mod_list = [(
         ldap0.MOD_DELETE, attr_type.encode('ascii'), None) for attr_type in delete_attr]
        app.ls.modify((app.dn), mod_list, req_ctrls=delete_server_ctrls)
        app.simple_message('Deleted Attribute(s)',
          ('\n            <p class="SuccessMessage">Deleted attribute(s) from entry %s</p>\n            <ul>\n              <li>\n              %s\n              </li>\n            </ul>\n            ' % (
         app.display_dn(app.dn),
         '</li>\n<li>'.join([app.form.hiddenFieldHTML('delete_attr', attr_type, attr_type) for attr_type in delete_attr]))),
          main_menu_list=(web2ldap.app.gui.main_menu(app)),
          context_menu_list=(web2ldap.app.gui.ContextMenuSingleEntry(app)))
    else:
        if scope == ldap0.SCOPE_BASE:
            app.ls.l.delete_s(app.dn)
            old_dn = app.dn
            app.dn = app.parent_dn
            app.simple_message('Deleted Entry',
              ('<p class="SuccessMessage">Deleted entry: %s</p>' % app.display_dn(old_dn)),
              main_menu_list=(web2ldap.app.gui.main_menu(app)),
              context_menu_list=[])