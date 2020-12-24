# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/searchform.py
# Compiled at: 2020-05-05 11:20:48
# Size of source mod 2**32: 12505 bytes
"""
web2ldap.app.searchform: different search forms

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0, web2ldapcnf, web2ldap.web.forms, web2ldap.app.core, web2ldap.app.gui, web2ldap.app.cnf
SEARCHFORM_MODE_TEXT = {'adv':'Advanced', 
 'base':'Basic', 
 'exp':'Expert'}
SEARCH_OPT_CONTAINS = '({at}=*{av}*)'
SEARCH_OPT_DOESNT_CONTAIN = '(!({at}=*{av}*))'
SEARCH_OPT_ATTR_EXISTS = '({at}=*)'
SEARCH_OPT_ATTR_NOT_EXISTS = '(!({at}=*))'
SEARCH_OPT_IS_EQUAL = '({at}={av})'
SEARCH_OPT_IS_NOT = '(!({at}={av}))'
SEARCH_OPT_BEGINS_WITH = '({at}={av}*)'
SEARCH_OPT_ENDS_WITH = '({at}=*{av})'
SEARCH_OPT_SOUNDS_LIKE = '({at}~={av})'
SEARCH_OPT_GE_THAN = '({at}>={av})'
SEARCH_OPT_LE_THAN = '({at}<={av})'
SEARCH_OPT_DN_ATTR_IS = '({at}:dn:={av})'
SEARCH_OPT_DN_SUBORDINATE = '({at}:dnSubordinateMatch:={av})'
SEARCH_OPT_DN_SUBTREE = '({at}:dnSubtreeMatch:={av})'
SEARCH_OPT_DN_ONE_LEVEL = '({at}:dnOneLevelMatch:={av})'
search_options = (
 (
  SEARCH_OPT_IS_EQUAL, 'attribute value is'),
 (
  SEARCH_OPT_CONTAINS, 'attribute value contains'),
 (
  SEARCH_OPT_DOESNT_CONTAIN, 'attribute value does not contain'),
 (
  SEARCH_OPT_IS_NOT, 'attribute value is not'),
 (
  SEARCH_OPT_BEGINS_WITH, 'attribute value begins with'),
 (
  SEARCH_OPT_ENDS_WITH, 'attribute value ends with'),
 (
  SEARCH_OPT_SOUNDS_LIKE, 'attribute value sounds like'),
 (
  SEARCH_OPT_GE_THAN, 'attribute value greater equal than'),
 (
  SEARCH_OPT_LE_THAN, 'attribute value lesser equal than'),
 (
  SEARCH_OPT_DN_ATTR_IS, 'DN attribute value is'),
 (
  SEARCH_OPT_ATTR_EXISTS, 'entry has attribute'),
 (
  SEARCH_OPT_ATTR_NOT_EXISTS, 'entry does not have attribute'),
 (
  SEARCH_OPT_DN_SUBORDINATE, 'DN is subordinate of'),
 (
  SEARCH_OPT_DN_SUBTREE, 'DN within subtree'),
 (
  SEARCH_OPT_DN_ONE_LEVEL, 'DN is direct child of'))
SEARCH_SCOPE_STR_BASE = '0'
SEARCH_SCOPE_STR_ONELEVEL = '1'
SEARCH_SCOPE_STR_SUBTREE = '2'
SEARCH_SCOPE_STR_SUBORDINATES = '3'
SEARCH_SCOPE_OPTIONS = [
 (
  SEARCH_SCOPE_STR_BASE, 'Base'),
 (
  SEARCH_SCOPE_STR_ONELEVEL, 'One level'),
 (
  SEARCH_SCOPE_STR_SUBTREE, 'Sub tree'),
 (
  SEARCH_SCOPE_STR_SUBORDINATES, 'Subordinate')]
FILTERSTR_FIELDSET_TMPL = '\n<fieldset>\n  <legend>LDAP filter string</legend>\n  <input name="filterstr" maxlength="%d" size="%d" value="%s">\n</fieldset>\n'

def SearchForm_exp(app, filterstr=''):
    """
    Output expert search form
    """
    filterstr = app.form.getInputValue('filterstr', [filterstr])[0]
    result = FILTERSTR_FIELDSET_TMPL % (
     app.form.field['filterstr'].maxLen,
     app.form.field['filterstr'].size,
     app.form.utf2display(filterstr))
    return result


def SearchForm_base(app, searchform_template_name):
    """
    Output basic search form based on a HTML template configured
    with host-specific configuration parameter searchform_template
    """
    searchform_template_cfg = app.cfg_param('searchform_template', '')
    searchform_template = searchform_template_cfg.get(searchform_template_name, None)
    searchform_template_filename = web2ldap.app.gui.GetVariantFilename(searchform_template, app.form.accept_language)
    with open(searchform_template_filename, 'rb') as (fileobj):
        template_str = fileobj.read().decode('utf-8')
    return template_str


def SearchForm_adv(app):
    """advanced search form with select lists"""
    search_submit = app.form.getInputValue('search_submit', [''])[0]
    search_attr_list = app.form.getInputValue('search_attr', [''])
    search_option_list = app.form.getInputValue('search_option', [None] * len(search_attr_list))
    search_mr_list = app.form.getInputValue('search_mr', [None] * len(search_attr_list))
    search_string_list = app.form.getInputValue('search_string', [''] * len(search_attr_list))
    if search_submit.startswith('-'):
        del_row_num = int(search_submit[1:])
        if len(search_attr_list) > 1:
            del search_option_list[del_row_num]
            del search_attr_list[del_row_num]
            del search_mr_list[del_row_num]
            del search_string_list[del_row_num]
    else:
        if search_submit.startswith('+'):
            insert_row_num = int(search_submit[1:])
            if len(search_attr_list) < web2ldapcnf.max_searchparams:
                search_option_list.insert(insert_row_num + 1, search_option_list[insert_row_num])
                search_attr_list.insert(insert_row_num + 1, search_attr_list[insert_row_num])
                search_mr_list.insert(insert_row_num + 1, search_mr_list[insert_row_num])
                search_string_list.insert(insert_row_num + 1, '')
        if not len(search_option_list) == len(search_attr_list) == len(search_string_list):
            raise web2ldap.app.core.ErrorExit('Invalid search form data.')
        search_mode = app.form.getInputValue('search_mode', ['(&%s)'])[0]
        search_mode_select = web2ldap.web.forms.Select('search_mode',
          'Search mode', 1, options=[
         ('(&%s)', 'all'),
         ('(|%s)', 'any')],
          default=search_mode)
        search_mode_select.charset = app.form.accept_charset
        search_attr_select = web2ldap.app.gui.attrtype_select_field(app,
          'search_attr',
          'Search attribute type',
          search_attr_list,
          default_attr_options=(app.cfg_param('search_attrs', [])))
        mr_list = [
         ''] + sorted(app.schema.name2oid[ldap0.schema.models.MatchingRule].keys())
        search_mr_select = web2ldap.web.forms.Select('search_mr',
          'Matching rule used', (web2ldapcnf.max_searchparams),
          options=mr_list)
        search_mr_select.charset = app.form.accept_charset
        search_fields_html_list = []
        for i in range(len(search_attr_list)):
            search_fields_html_list.append('\n'.join((
             '<tr>\n<td rowspan="2">',
             '<button type="submit" name="search_submit" value="+%d">+</button>' % i,
             '<button type="submit" name="search_submit" value="-%d">-</button>' % i,
             '</td>\n<td>',
             search_attr_select.input_html(default=(search_attr_list[i])),
             search_mr_select.input_html(default=(search_mr_list[i])),
             app.form.field['search_option'].input_html(default=(search_option_list[i])),
             '</td></tr>\n<tr><td>',
             app.form.field['search_string'].input_html(default=(search_string_list[i])),
             '</td></tr>')))
        else:
            result = '\n    <fieldset>\n      <legend>Search filter parameters</legend>\n      Match %s of the following.<br>\n      <table>%s</table>\n    </fieldset>\n    ' % (
             search_mode_select.input_html(),
             '\n'.join(search_fields_html_list))
            return result


def w2l_searchform(app, Msg='', filterstr='', scope=ldap0.SCOPE_SUBTREE, search_root=None, searchform_mode=None):
    """Output a search form"""
    if Msg:
        msg_html = '<p class="ErrorMessage">%s</p>' % Msg
    else:
        msg_html = ''
    searchform_mode = searchform_mode or app.form.getInputValue('searchform_mode', ['base'])[0]
    searchform_template_name = app.form.getInputValue('searchform_template', ['_'])[0]
    naming_contexts = app.cfg_param('naming_contexts', None)
    search_root = app.form.getInputValue('search_root', [
     search_root or str(app.naming_context)])[0]
    search_root_field = web2ldap.app.gui.search_root_field(app,
      name='search_root',
      default=search_root,
      search_root_searchurl=(app.cfg_param('searchform_search_root_url', None)))
    ContextMenuList = [app.anchor('searchform', SEARCHFORM_MODE_TEXT[mode], [
     (
      'dn', app.dn),
     (
      'searchform_mode', mode),
     (
      'search_root', search_root),
     (
      'filterstr', filterstr),
     (
      'scope', str(scope))]) for mode in SEARCHFORM_MODE_TEXT if mode != searchform_mode]
    searchform_template_cfg = app.cfg_param('searchform_template', '')
    if isinstance(searchform_template_cfg, dict):
        for sftn in searchform_template_cfg.keys():
            if sftn != '_':
                ContextMenuList.append(app.anchor('searchform', app.form.utf2display(sftn), [
                 (
                  'dn', app.dn),
                 ('searchform_mode', 'base'),
                 (
                  'searchform_template', sftn),
                 (
                  'search_root', search_root),
                 (
                  'filterstr', filterstr),
                 (
                  'scope', str(scope))]))

    if searchform_mode == 'base':
        try:
            inner_searchform_html = SearchForm_base(app, searchform_template_name)
        except IOError:
            msg_html = '\n'.join((
             msg_html,
             '<p class="ErrorMessage">I/O error while loading search form template!</p>'))
            inner_searchform_html = SearchForm_adv(app)
            searchform_mode = 'adv'

    else:
        if searchform_mode == 'exp':
            inner_searchform_html = SearchForm_exp(app, filterstr)
        else:
            if searchform_mode == 'adv':
                inner_searchform_html = SearchForm_adv(app)
            searchoptions_template_filename = web2ldap.app.gui.GetVariantFilename(app.cfg_param('searchoptions_template', None), app.form.accept_language)
            with open(searchoptions_template_filename, 'r') as (template_file):
                searchoptions_template_str = template_file.read()
            web2ldap.app.gui.top_section(app,
              ('%s Search Form' % SEARCHFORM_MODE_TEXT[searchform_mode]),
              (web2ldap.app.gui.main_menu(app)),
              context_menu_list=ContextMenuList,
              main_div_id='Input')
            app.outf.write('\n        {msg_html}\n        {form_search_html}\n          <input type="hidden" name="searchform_mode" value="{searchform_mode}">\n          <input type="hidden" name="searchform_template" value="{searchform_template}">\n          <input type="hidden" name="search_output" value="{search_output}">\n          <p>\n            <input type="submit" name="search_submit" value="Search">\n            <input type="reset" value="Reset">\n          </p>\n          {inner_searchform_html}\n          {form_dn_html}\n          {searchoptions_template_str}\n        </form>\n        '.format(form_search_html=(app.begin_form('search', 'GET')),
              searchform_mode=(app.form.utf2display(searchform_mode)),
              searchform_template=(app.form.utf2display(searchform_template_name)),
              search_output=(app.form.getInputValue('search_output', ['table'])[0]),
              msg_html=msg_html,
              inner_searchform_html=inner_searchform_html,
              form_dn_html=(app.form.hiddenFieldHTML('dn', app.dn, '')),
              searchoptions_template_str=searchoptions_template_str.format(field_search_root=(search_root_field.input_html()),
              field_search_scope=app.form.field['scope'].input_html(default=(app.form.getInputValue('scope', [str(scope)])[0])),
              field_search_resnumber=app.form.field['search_resnumber'].input_html(default=(app.form.getInputValue('search_resnumber', [
             str(app.cfg_param('search_resultsperpage', 10))])[0])),
              field_search_lastmod=app.form.field['search_lastmod'].input_html(default=(app.form.getInputValue('search_lastmod', [str(-1)])[0])),
              value_search_attrs=(app.form.utf2display(app.form.getInputValue('search_attrs', [''])[0])))))
            web2ldap.app.gui.footer(app)