# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/gui.py
# Compiled at: 2020-05-04 07:51:46
# Size of source mod 2**32: 22258 bytes
"""
web2ldap.app.gui: basic functions for GUI elements

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, os
from hashlib import md5
import ldap0, ldap0.ldapurl
from ldap0.ldapurl import LDAPUrl
import ldap0.filter
from ldap0.dn import DNObj
from ldap0.res import SearchResultEntry
import web2ldapcnf, web2ldap.web.forms
from web2ldap.web import escape_html
import web2ldap.__about__, web2ldap.ldaputil, web2ldap.msbase, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.schema.syntaxes, web2ldap.app.searchform
from web2ldap.msbase import GrabKeys
import web2ldap.ldaputil
from web2ldap.ldaputil import logdb_filter
host_pattern = '[a-zA-Z0-9_.:\\[\\]-]+'
HIDDEN_FIELD = '<input type="hidden" name="%s" value="%s">%s\n'
HTML_FOOTER = '\n  <p class="ScrollLink">\n    <a href="#web2ldap_top">&uarr; TOP</a>\n  </p>\n  <a id="web2ldap_bottom"></a>\n</div>\n<div id="Footer">\n  <footer>\n  </footer>\n</div>\n</body>\n</html>\n'

def GetVariantFilename(pathname, variantlist):
    """
    returns variant filename
    """
    checked_set = set()
    for v in variantlist:
        v = v.lower().split('-', 1)[0]
        if v == 'en':
            variant_filename = pathname
        else:
            variant_filename = '.'.join((pathname, v))
        if v not in checked_set and os.path.isfile(variant_filename):
            break
        else:
            checked_set.add(v)
    else:
        variant_filename = pathname
        return variant_filename


def read_template(app, config_key, form_desc='', tmpl_filename=None):
    if not tmpl_filename:
        tmpl_filename = app.cfg_param(config_key, None)
    if not tmpl_filename:
        raise web2ldap.app.core.ErrorExit('No template specified for %s.' % form_desc)
    tmpl_filename = web2ldap.app.gui.GetVariantFilename(tmpl_filename, app.form.accept_language)
    try:
        with open(tmpl_filename, 'rb') as (tmpl_fileobj):
            tmpl_str = tmpl_fileobj.read().decode('utf-8')
    except IOError:
        raise web2ldap.app.core.ErrorExit('I/O error during reading %s template file.' % form_desc)
    else:
        return tmpl_str


def dn_anchor_hash(dn):
    return str(md5(dn.encode('utf-8')).hexdigest())


def ts2repr(time_divisors, ts_sep, ts_value: str) -> str:
    rest = int(ts_value)
    result = []
    for desc, divisor in time_divisors:
        mult = rest // divisor
        rest = rest % divisor
        if mult > 0:
            result.append('%d %s' % (mult, desc))
        if rest == 0:
            break
        return ts_sep.join(result)


def repr2ts(time_divisors, ts_sep, value):
    l1 = [v.strip().split(' ') for v in value.split(ts_sep)]
    l2 = [(int(v), d.strip()) for v, d in l1]
    time_divisors_dict = dict(time_divisors)
    result = 0
    for value, desc in l2:
        try:
            result += value * time_divisors_dict[desc]
        except KeyError:
            raise ValueError
        else:
            del time_divisors_dict[desc]
    else:
        return str(result)


def command_div(commandlist, div_id='CommandDiv', separator=' ', semantic_tag='nav'):
    if semantic_tag:
        start_tag = '<%s>' % semantic_tag
        end_tag = '<%s>' % semantic_tag
    else:
        start_tag = ''
        end_tag = ''
    if commandlist:
        return '%s<p id="%s" class="CT">\n%s\n</p>%s\n' % (
         start_tag,
         div_id,
         separator.join(commandlist),
         end_tag)
    return ''


def simple_main_menu(app):
    main_menu = [
     app.anchor('', 'Connect', [])]
    if web2ldap.app.handler.check_access(app.env, 'monitor'):
        main_menu.append(app.anchor('monitor', 'Monitor', []))
    if web2ldap.app.handler.check_access(app.env, 'locate'):
        main_menu.append(app.anchor('locate', 'DNS lookup', []))
    return main_menu


def ContextMenuSingleEntry(app, vcard_link=0, dds_link=0, entry_uuid=None):
    """
    Output the context menu for a single entry
    """
    dn_disp = app.dn or 'Root DSE'
    result = [
     app.anchor('read',
       'Raw', [
      (
       'dn', app.dn),
      ('read_output', 'table'),
      ('read_expandattr', '*')],
       title=('Display entry\r\n%s\r\nas raw attribute type/value list' % dn_disp))]
    if app.dn:
        ldap_url_obj = app.ls.ldap_url('', add_login=False)
        result.extend([
         app.anchor('login',
           'Bind as', [
          (
           'ldapurl', str(ldap_url_obj)),
          (
           'dn', app.dn),
          (
           'login_who', app.dn)],
           title=('Connect and bind new session as\r\n%s' % app.dn)),
         app.anchor('modify', 'Modify', [('dn', app.dn)], title=('Modify entry\r\n%s' % app.dn)),
         app.anchor('rename', 'Rename', [('dn', app.dn)], title=('Rename/move entry\r\n%s' % app.dn)),
         app.anchor('delete', 'Delete', [('dn', app.dn)], title=('Delete entry and/or subtree\r\n%s' % app.dn)),
         app.anchor('passwd', 'Password', [('dn', app.dn), ('passwd_who', app.dn)], title=('Set password for entry\r\n%s' % app.dn)),
         app.anchor('groupadm', 'Groups', [('dn', app.dn)], title=('Change group membership of entry\r\n%s' % app.dn)),
         app.anchor('add',
           'Clone', [
          (
           'dn', app.parent_dn),
          (
           'add_clonedn', app.dn),
          ('in_ft', 'Template')],
           title=('Clone entry\r\n%s\r\nbeneath %s' % (app.dn, app.parent_dn)))])
    if vcard_link:
        result.append(app.anchor('read',
          'vCard', [
         (
          'dn', app.dn), ('read_output', 'vcard')],
          title=('Export entry\r\n%s\r\nas vCard' % dn_disp)))
    if dds_link:
        result.append(app.anchor('dds',
          'Refresh', [
         (
          'dn', app.dn)],
          title=('Refresh dynamic entry %s' % dn_disp)))
    if app.audit_context:
        accesslog_any_filterstr = logdb_filter('auditObject', app.dn, entry_uuid)
        accesslog_write_filterstr = logdb_filter('auditWriteObject', app.dn, entry_uuid)
        result.extend([
         app.anchor('search',
           'Audit access', [
          (
           'dn', app.audit_context),
          (
           'filterstr', accesslog_any_filterstr),
          (
           'scope', str(ldap0.SCOPE_ONELEVEL))],
           title=('Complete audit trail for entry\r\n%s' % app.dn)),
         app.anchor('search',
           'Audit writes', [
          (
           'dn', app.audit_context),
          (
           'filterstr', accesslog_write_filterstr),
          (
           'scope', str(ldap0.SCOPE_ONELEVEL))],
           title=('Audit trail of write access to entry\r\n%s' % app.dn))])
    try:
        changelog_dn = app.ls.rootDSE['changelog'][0].decode(app.ls.charset)
    except KeyError:
        pass
    else:
        changelog_filterstr = logdb_filter('changeLogEntry', app.dn, entry_uuid)
        result.append(app.anchor('search',
          'Change log', [
         (
          'dn', changelog_dn),
         (
          'filterstr', changelog_filterstr),
         (
          'scope', str(ldap0.SCOPE_ONELEVEL))],
          title='Audit trail of write access to current entry'))
    try:
        monitor_context_dn = app.ls.rootDSE['monitorContext'][0].decode(app.ls.charset)
    except KeyError:
        pass
    else:
        result.append(app.anchor('search',
          'User conns', [
         (
          'dn', monitor_context_dn),
         (
          'filterstr',
          '(&(objectClass=monitorConnection)(monitorConnectionAuthzDN=%s))' % (
           ldap0.filter.escape_str(app.dn),)),
         (
          'scope', str(ldap0.SCOPE_SUBTREE))],
          title='Find connections of this user in monitor database'))
    return result


def display_authz_dn(app, who=None, entry=None):
    if who is None:
        if hasattr(app.ls, 'who'):
            if app.ls.who:
                who = app.ls.who
                entry = app.ls.userEntry
            else:
                return 'anonymous'
        elif ldap0.dn.is_dn(who):
            result = app.display_dn(who, commandbutton=False)
            bound_as_templates = ldap0.cidict.CIDict(app.cfg_param('boundas_template', {}))
            if entry is None:
                read_attrs = set(['objectClass'])
                for oc in bound_as_templates.keys():
                    read_attrs.update(GrabKeys(bound_as_templates[oc]).keys)
                else:
                    try:
                        user_res = app.ls.l.read_s(who, attrlist=read_attrs)
                    except ldap0.LDAPError:
                        entry = None
                    else:
                        if user_res is None:
                            entry = {}

        else:
            entry = user_res.entry_as
        if entry:
            display_entry = web2ldap.app.read.DisplayEntry(app, app.dn, app.schema, entry, 'readSep', True)
            user_structural_oc = display_entry.entry.get_structural_oc()
            for oc in bound_as_templates.keys():
                if app.schema.get_oid(ldap0.schema.models.ObjectClass, oc) == user_structural_oc:
                    try:
                        result = bound_as_templates[oc] % display_entry
                    except KeyError:
                        pass

    else:
        result = app.form.utf2display(who)
    return result


def main_menu(app):
    """
    Returns list of main menu items
    """
    cl = []
    if app.ls is not None and app.ls.uri is not None:
        if app.dn:
            if app.dn_obj != app.naming_context:
                cl.append(app.anchor('search',
                  'Up', (
                 (
                  'dn', app.parent_dn),
                 (
                  'scope', web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL),
                 ('searchform_mode', 'adv'),
                 ('search_attr', 'objectClass'),
                 (
                  'search_option', web2ldap.app.searchform.SEARCH_OPT_ATTR_EXISTS),
                 ('search_string', '')),
                  title=('List direct subordinates of %s' % (app.parent_dn or 'Root DSE'))))
        cl.extend((
         app.anchor('search',
           'Down', (
          (
           'dn', app.dn),
          (
           'scope', web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL),
          ('searchform_mode', 'adv'),
          ('search_attr', 'objectClass'),
          (
           'search_option', web2ldap.app.searchform.SEARCH_OPT_ATTR_EXISTS),
          ('search_string', '')),
           title=('List direct subordinates of %s' % (app.dn or 'Root DSE'))),
         app.anchor('searchform',
           'Search', (
          (
           'dn', app.dn),),
           title='Enter search criteria in input form')))
        cl.append(app.anchor('dit',
          'Tree', [
         (
          'dn', app.dn)],
          title=('Display tree around %s' % (app.dn or 'Root DSE')),
          anchor_id=(dn_anchor_hash(app.dn_obj))))
        cl.append(app.anchor('read',
          'Read', [
         (
          'dn', app.dn), ('read_nocache', '1')],
          title=('Display entry %s' % (app.dn or 'Root DSE'))))
        cl.extend((
         app.anchor('add',
           'New entry', [
          (
           'dn', app.dn)],
           title=('Add a new entry below of %s' % (app.dn or 'Root DSE'))),
         app.anchor('conninfo', 'ConnInfo', [('dn', app.dn)], title='Show information about HTTP and LDAP connections'),
         app.anchor('params', 'Params', [('dn', app.dn)], title='Tweak parameters used for LDAP operations (controls etc.)'),
         app.anchor('login', 'Bind', [('dn', app.dn)], title='Login to directory'),
         app.anchor('oid', 'Schema', [('dn', app.dn)], title='Browse/view subschema')))
        cl.append(app.anchor('disconnect', 'Disconnect', (), title='Disconnect from LDAP server'))
    else:
        cl.append(app.anchor('', 'Connect', (), title='New connection to LDAP server'))
    return cl


def dit_navigation(app):
    result = [app.anchor('read',
      (app.form.utf2display(str(app.dn_obj.slice(i, i + 1)) or '[Root DSE]')),
      [
     (
      'dn', str(app.dn_obj.slice(i, None)))],
      title=('Jump to %s' % str(app.dn_obj.slice(i, None)))) for i in range(len(app.dn_obj))]
    result.append(app.anchor('read',
      '[Root DSE]', [
     ('dn', '')],
      title='Jump to root DSE'))
    return result


def top_section(app, title, main_menu_list, context_menu_list=None, main_div_id='Message'):
    Header(app, 'text/html', app.form.accept_charset)
    top_template_str = web2ldap.app.gui.read_template(app, 'top_template', 'top section')
    script_name = escape_html(app.form.script_name)
    template_dict = {'main_div_id':main_div_id, 
     'accept_charset':app.form.accept_charset, 
     'refresh_time':str(web2ldapcnf.session_remove + 10), 
     'sid':app.sid or '', 
     'title_text':title, 
     'script_name':script_name, 
     'web2ldap_version':escape_html(web2ldap.__about__.__version__), 
     'command':app.command, 
     'ldap_url':'', 
     'ldap_uri':'-/-', 
     'description':'', 
     'who':'-/-', 
     'dn':'-/-', 
     'dit_navi':'-/-', 
     'main_menu':command_div(main_menu_list,
       div_id='MainMenu',
       separator='\n',
       semantic_tag=None), 
     'context_menu':command_div(context_menu_list,
       div_id='ContextMenu',
       separator='\n',
       semantic_tag=None)}
    template_dict.update([(k, escape_html(str(v))) for k, v in app.env.items()])
    if app.ls is not None:
        if app.ls.uri is not None:
            template_dict.update({'ldap_url':app.ls.ldap_url(app.dn), 
             'ldap_uri':app.form.utf2display(app.ls.uri), 
             'description':escape_html(app.cfg_param('description', '')), 
             'dit_navi':',\n'.join(dit_navigation(app)), 
             'dn':app.form.utf2display(app.dn)})
            template_dict['who'] = display_authz_dn(app)
    app.outf.write((top_template_str.format)(**template_dict))


def ldap_url_anchor(app, data):
    if isinstance(data, LDAPUrl):
        l = data
    else:
        l = LDAPUrl(ldapUrl=data)
    command_func = {True:'read', 
     False:'search'}[(l.scope == ldap0.SCOPE_BASE)]
    if l.hostport:
        command_text = 'Connect'
        return app.anchor(command_func, 'Connect and %s' % command_func, (
         (
          'ldapurl', str(l)),))
    command_text = {True:'Read',  False:'Search'}[(l.scope == ldap0.SCOPE_BASE)]
    return app.anchor(command_func, command_text, [
     (
      'dn', l.dn),
     (
      'filterstr', l.filterstr or '(objectClass=*)'),
     (
      'scope', str(l.scope or ldap0.SCOPE_SUBTREE))])


def attrtype_select_field(app, field_name, field_desc, attr_list, default_attr_options=None):
    """
    Return web2ldap.web.forms.Select instance for choosing attribute type names
    """
    attr_options_dict = {}
    for attr_type in default_attr_options or list(app.schema.sed[ldap0.schema.models.AttributeType].keys()) + attr_list:
        attr_type_se = app.schema.get_obj(ldap0.schema.models.AttributeType, attr_type)
        if attr_type_se:
            if attr_type_se.names:
                attr_type_name = attr_type_se.names[0]
            else:
                attr_type_name = attr_type
            attr_type_desc = attr_type_se.desc
        else:
            attr_type_name = attr_type
            attr_type_desc = None
        attr_options_dict[attr_type_name] = (
         attr_type_name, attr_type_desc)
    else:
        sorted_attr_options = [(
         at, attr_options_dict[at][0], attr_options_dict[at][1]) for at in sorted((attr_options_dict.keys()), key=(str.lower))]
        attr_select = web2ldap.web.forms.Select(field_name,
          field_desc, 1, options=sorted_attr_options)
        attr_select.charset = app.form.accept_charset
        return attr_select


def gen_headers(content_type, charset, more_headers=None):
    current_datetime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time()))
    headers = []
    if content_type.startswith('text/'):
        content_type = '%s;charset=%s' % (content_type, charset)
    headers.append(('Content-Type', content_type))
    headers.append(('Date', current_datetime))
    headers.append(('Last-Modified', current_datetime))
    headers.append(('Expires', current_datetime))
    for h, v in web2ldapcnf.http_headers.items():
        headers.append((h, v))
    else:
        headers.extend(more_headers or [])
        return headers


def Header(app, content_type, charset, more_headers=None):
    headers = gen_headers(content_type=content_type,
      charset=charset,
      more_headers=more_headers)
    app.outf.reset()
    if app.form.next_cookie:
        for _, cookie in app.form.next_cookie.items():
            headers.append(('Set-Cookie', str(cookie)[12:]))

    if app.form.env.get('HTTPS', 'off') == 'on':
        if 'Strict-Transport-Security' not in web2ldapcnf.http_headers:
            headers.append(('Strict-Transport-Security', 'max-age=15768000 ; includeSubDomains'))
    app.outf.set_headers(headers)
    return headers


def footer(app):
    app.outf.write(HTML_FOOTER)


def search_root_field(app, name='dn', text='Search Root', default=None, search_root_searchurl=None, naming_contexts=None):
    """
    Returns input field for search root
    """

    def sortkey_func(d):
        if isinstance(d, DNObj):
            return str(reversed(d)).lower()
        try:
            dn, _ = d
        except ValueError:
            dn = d
        else:
            if not dn:
                return ''
            return str(reversed(DNObj.from_str(dn))).lower()

    dn_select_list = set(map(str, app.ls.namingContexts))
    if app.dn:
        dn_select_list.update(map(str, [app.dn_obj] + app.dn_obj.parents()))
    elif search_root_searchurl:
        slu = ldap0.ldapurl.LDAPUrl(search_root_searchurl)
        try:
            ldap_results = app.ls.l.search_s((slu.dn),
              (slu.scope),
              (slu.filterstr),
              attrlist=[
             '1.1'])
        except ldap0.LDAPError:
            pass
        else:
            dn_select_list.update([r.dn_s for r in ldap_results if isinstance(r, SearchResultEntry)])
    if '' in dn_select_list:
        dn_select_list.remove('')
    dn_select_list.add(('', '- World -'))
    srf = web2ldap.web.forms.Select(name,
      text, 1, size=1,
      options=sorted(dn_select_list,
      key=sortkey_func),
      default=(default or str(app.naming_context) or app.dn),
      ignoreCase=1)
    srf.charset = app.form.accept_charset
    return srf


def invalid_syntax_message(app, invalid_attrs):
    invalid_attr_types_ui = [app.form.utf2display(at) for at in sorted(invalid_attrs.keys())]
    return 'Wrong syntax in following attributes: %s' % ', '.join(['<a class="CL" href="#in_a_%s">%s</a>' % (at_ui, at_ui) for at_ui in invalid_attr_types_ui])


def exception_message(app, h1_msg, error_msg):
    """
    h1_msg
      Unicode string with text for the <h1> heading
    error_msg
      Raw string with HTML with text describing the exception
      (Security note: Must already be quoted/escaped!)
    """
    top_section(app, 'Error', (main_menu(app)), context_menu_list=[])
    app.outf.write('\n        <h1>{heading}</h1>\n        <p class="ErrorMessage">\n          {error_msg}\n        </p>\n        '.format(heading=(app.form.utf2display(h1_msg)),
      error_msg=error_msg))
    footer(app)