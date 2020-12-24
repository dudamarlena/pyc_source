# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/rename.py
# Compiled at: 2019-12-14 07:54:37
# Size of source mod 2**32: 8569 bytes
"""
web2ldap.app.rename: modify DN of an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0, ldap0.ldapurl, ldap0.filter, web2ldap.web.forms, web2ldap.ldaputil, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.gui, web2ldap.app.form, web2ldap.app.schema, web2ldap.app.schema.syntaxes
from web2ldap.app.schema.viewer import schema_anchors

def new_superior_field(app, sup_search_url, old_superior_dn):
    """
    returns Select field for choosing a new superior entry
    """

    class NewSuperiorSelectList(web2ldap.app.schema.syntaxes.DynamicDNSelectList):
        __doc__ = '\n        plugin class for choosing a new superior entry\n        '
        attr_value_dict = {'': '- Root Naming Context -'}

        def __init__(self, app, dn, schema, attrType, attrValue, ldap_url):
            self.ldap_url = ldap_url
            web2ldap.app.schema.syntaxes.DynamicDNSelectList.__init__(self,
              app, dn, schema, attrType, attrValue, entry=None)

    if sup_search_url is not None:
        attr_inst = NewSuperiorSelectList(app, app.dn, app.schema, 'rdn', old_superior_dn.encode(app.ls.charset), str(sup_search_url))
        nssf = attr_inst.formField()
        nssf.name = 'rename_newsuperior'
        nssf.text = 'New Superior DN'
    else:
        nssf = web2ldap.app.form.DistinguishedNameInput('rename_newsuperior', 'New Superior DN')
    nssf.charset = app.form.accept_charset
    nssf.set_default(old_superior_dn)
    return nssf


def w2l_rename(app):
    """
    rename an entry
    """
    rename_supsearchurl_cfg = app.cfg_param('rename_supsearchurl', {})
    if not app.dn:
        raise web2ldap.app.core.ErrorExit('Rename operation not possible at - World - or RootDSE.')
    rename_newrdn = app.form.getInputValue('rename_newrdn', [None])[0]
    rename_newsuperior = app.form.getInputValue('rename_newsuperior', [None])[0]
    rename_delold = app.form.getInputValue('rename_delold', ['no'])[0] == 'yes'
    if rename_newrdn:
        old_dn = app.dn
        app.dn, entry_uuid = app.ls.rename((app.dn),
          rename_newrdn,
          rename_newsuperior,
          delold=rename_delold)
        app.simple_message('Renamed/moved entry',
          ('<p class="SuccessMessage">Renamed/moved entry.</p>\n            <dl><dt>Old name:</dt><dd>%s</dd>\n            <dt>New name:</dt><dd>%s</dd></dl>' % (
         app.display_dn(old_dn),
         app.display_dn(app.dn))),
          main_menu_list=(web2ldap.app.gui.main_menu(app)),
          context_menu_list=web2ldap.app.gui.ContextMenuSingleEntry(app,
          entry_uuid=entry_uuid))
        return
    old_rdn = str(app.dn_obj.rdn())
    old_superior = str(app.dn_obj.parent())
    app.form.field['rename_newrdn'].set_default(old_rdn)
    rename_template_str = web2ldap.app.gui.read_template(app, 'rename_template', 'rename form')
    rename_supsearchurl = app.form.getInputValue('rename_supsearchurl', [None])[0]
    try:
        sup_search_url = ldap0.ldapurl.LDAPUrl(rename_supsearchurl_cfg[rename_supsearchurl])
    except KeyError:
        rename_newsupfilter = app.form.getInputValue('rename_newsupfilter', [None])[0]
        sup_search_url = ldap0.ldapurl.LDAPUrl()
        if rename_newsupfilter is not None:
            sup_search_url.urlscheme = 'ldap'
            sup_search_url.filterstr = rename_newsupfilter or app.form.field['rename_newsupfilter'].default
            sup_search_url.dn = app.form.getInputValue('rename_searchroot', [
             ''])[0]
            sup_search_url.scope = int(app.form.getInputValue('scope', [str(ldap0.SCOPE_SUBTREE)])[0])
        else:
            sup_search_url = None
    else:
        if sup_search_url is not None:
            if sup_search_url.dn in {'_', '..', '.'}:
                rename_searchroot_default = None
            else:
                rename_searchroot_default = sup_search_url.dn
            rename_newsupfilter_default = sup_search_url.filterstr
            scope_default = str(sup_search_url.scope)
        else:
            rename_searchroot_default = None
            rename_newsupfilter_default = app.form.field['rename_newsupfilter'].default
            scope_default = str(ldap0.SCOPE_SUBTREE)
        rename_search_root_field = web2ldap.app.gui.search_root_field(app, name='rename_searchroot')
        rename_new_superior_field = new_superior_field(app, sup_search_url, old_superior)
        name_forms_text = ''
        dit_structure_rule_html = ''
        if app.schema.sed[ldap0.schema.models.NameForm]:
            search_result = app.ls.l.read_s((app.dn),
              attrlist=[
             'objectClass', 'structuralObjectClass', 'governingStructureRule'])
            if not search_result:
                raise web2ldap.app.core.ErrorExit('Empty search result when reading entry to be renamed.')
            entry = ldap0.schema.models.Entry(app.schema, app.dn, search_result.entry_as)
            rdn_options = entry.get_rdn_templates()
            if rdn_options:
                name_forms_text = '<p class="WarningMessage">Available name forms for RDN:<br>%s</p>' % '<br>'.join(rdn_options)
            dit_structure_ruleids = entry.get_possible_dit_structure_rules(app.dn)
            for dit_structure_ruleid in dit_structure_ruleids:
                sup_structural_ruleids, sup_structural_oc = app.schema.get_superior_structural_oc_names(dit_structure_ruleid)

            if sup_structural_oc:
                rename_newsupfilter_default = '(|%s)' % ''.join(['(objectClass=%s)' % ldap0.filter.escape_str(oc) for oc in sup_structural_oc])
                dit_structure_rule_html = 'DIT structure rules:<br>%s' % '<br>'.join(schema_anchors(app, sup_structural_ruleids, ldap0.schema.models.DITStructureRule))
        else:
            if rename_supsearchurl_cfg:
                rename_supsearchurl_field = web2ldap.web.forms.Select('rename_supsearchurl',
                  'LDAP URL for searching new superior entry',
                  1,
                  options=[])
                rename_supsearchurl_field.setOptions(rename_supsearchurl_cfg.keys())
            web2ldap.app.gui.top_section(app,
              'Rename Entry',
              (web2ldap.app.gui.main_menu(app)),
              context_menu_list=[])
            app.outf.write(rename_template_str.format(form_begin=(app.begin_form('rename', 'POST')),
              field_hidden_dn=(app.form.hiddenFieldHTML('dn', app.dn, '')),
              field_rename_newrdn=(app.form.field['rename_newrdn'].input_html()),
              field_rename_new_superior=(rename_new_superior_field.input_html()),
              text_name_forms=name_forms_text,
              field_rename_supsearchurl=(rename_supsearchurl_field.input_html()),
              value_rename_newsupfilter=(app.form.utf2display(rename_newsupfilter_default)),
              field_rename_search_root=rename_search_root_field.input_html(default=rename_searchroot_default),
              field_scope=app.form.field['scope'].input_html(default=scope_default),
              text_dit_structure_rule=dit_structure_rule_html))
            web2ldap.app.gui.footer(app)