# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/conninfo.py
# Compiled at: 2019-12-20 17:20:43
# Size of source mod 2**32: 12451 bytes
"""
web2ldap.app.conninfo: Display (SSL) connection data

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, ldap0, ldap0.filter, web2ldapcnf, web2ldap.utctime, web2ldap.ldaputil, web2ldap.app.core, web2ldap.app.gui
from web2ldap.app.session import session_store
CONNINFO_LDAP_TEMPLATE = '\n<h1>LDAP Connection Parameters</h1>\n<h2>LDAP connection</h2>\n<table summary="LDAP connection">\n  <tr>\n    <td>Connected to:</td>\n    <td>%s<br>(LDAPv%d, %s, %s)</td>\n  </tr>\n  <tr>\n    <td>Connected since:</td>\n    <td>%s (%d secs)</td>\n  </tr>\n  <tr>\n    <td>Reconnect counter:</td>\n    <td>%d</td>\n  </tr>\n  <tr>\n    <td>Server vendor info:</td>\n    <td>%s %s</td>\n  </tr>\n  <tr>\n    <td>Bound as:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>Result <em>Who am I?</em>:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>Bind mechanism used:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>SASL auth info:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>SASL user name:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>SASL SSF info:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>Current DN:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>Parent DN:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>Naming Context:</td>\n    <td>%s</td>\n  </tr>\n  <tr>\n    <td>%d last search bases:</td>\n    <td>%s</td>\n  </tr>\n</table>\n'
CONNINFO_LDAP_CACHE_TEMPLATE = '\n<h3>LDAP cache information</h3>\n<p>%s</p>\n<table id="LDAPCacheTable" summary="LDAP cache information">\n  <tr>\n    <td>Cached searches:</td>\n    <td>%d</td>\n  </tr>\n  <tr>\n    <td>Cached subschema DN mappings:</td>\n    <td>%d</td>\n  </tr>\n  <tr>\n    <td>Cached subschema subentries:</td>\n    <td>%d</td>\n  </tr>\n  <tr>\n    <td>Cache hit ratio:</td>\n    <td>%0.1f %%</td>\n  </tr>\n</table>\n'
CONNINFO_HTTP_TEMPLATE = '\n<h2>HTTP connection</h2>\n<table summary="HTTP connection">\n  <tr><td>Your IP address:</td><td>%s</td></tr>\n  <tr><td>direct remote address/port:</td><td>%s:%s</td></tr>\n  <tr><td>Server signature:</td><td>%s</td></tr>\n  <tr><td>Preferred language:</td><td>%s</td></tr>\n  <tr><td>Character set/encoding:</td><td>%s</td></tr>\n  <tr>\n    <td>Cross-check vars in use:</td>\n    <td>\n      <table summary="Cross-check vars">\n        %s\n      </table>\n    </td>\n  </tr>\n  <tr><td>User-Agent header:</td><td>%s</td></tr>\n</table>\n'

def w2l_conninfo(app):
    protocol_version = app.ls.l.get_option(ldap0.OPT_PROTOCOL_VERSION)
    conninfo_flushcaches = int(app.form.getInputValue('conninfo_flushcaches', ['0'])[0])
    if conninfo_flushcaches:
        app.ls.flush_cache()
    else:
        context_menu_list = []
        config_dn_list = []
        monitored_info = None
        if 'monitorContext' in app.ls.rootDSE:
            monitor_context_dn = app.ls.rootDSE['monitorContext'][0].decode(app.ls.charset)
            context_menu_list.append(app.anchor('read', 'Monitor', [
             (
              'dn', monitor_context_dn)]))
            try:
                monitored_info = app.ls.l.read_s(monitor_context_dn,
                  attrlist=[
                 'monitoredInfo']).entry_s['monitoredInfo'][0]
            except (ldap0.LDAPError, KeyError):
                pass
            else:
                context_menu_list.append(app.anchor('search',
                  'My connections', [
                 (
                  'dn', monitor_context_dn),
                 (
                  'filterstr',
                  '(&(objectClass=monitorConnection)(monitorConnectionAuthzDN=%s))' % ldap0.filter.escape_str(app.ls.who or '')),
                 (
                  'scope', str(ldap0.SCOPE_SUBTREE))],
                  title='Find own connections in Monitor database'))
        else:
            config_dn_list.append(('CN=MONITOR', 'Monitor'))
        if 'changelog' in app.ls.rootDSE:
            context_menu_list.append(app.anchor('read', 'Change log', [
             (
              'dn', app.ls.rootDSE['changelog'][0])]))
        else:
            config_dn_list.append(('cn=changelog', 'Change log'))
        if 'configContext' in app.ls.rootDSE:
            context_menu_list.append(app.anchor('read', 'Config', [
             (
              'dn', app.ls.rootDSE['configContext'][0])]))
        else:
            if 'configurationNamingContext' in app.ls.rootDSE:
                context_menu_list.append(app.anchor('read', 'AD Configuration', [
                 (
                  'dn', app.ls.rootDSE['configurationNamingContext'][0])]))
            else:
                if 'ibm-configurationnamingcontext' in app.ls.rootDSE:
                    context_menu_list.append(app.anchor('read', 'IBM DS Configuration', [
                     (
                      'dn', app.ls.rootDSE['ibm-configurationnamingcontext'][0])]))
                else:
                    config_dn_list.extend([
                     ('CN=CONFIG', 'Config'),
                     ('CN=Configuration', 'Configuration'),
                     ('cn=ldbm', 'LDBM Database'),
                     ('ou=system', 'System')])
    if app.audit_context:
        context_menu_list.extend([
         app.anchor('read', 'Audit DB', [
          (
           'dn', app.audit_context)]),
         app.anchor('search',
           'Audit my access', [
          (
           'dn', app.audit_context),
          (
           'filterstr', '(&(objectClass=auditObject)(reqAuthzID=%s))' % ldap0.filter.escape_str(app.ls.who or '')),
          (
           'scope', str(ldap0.SCOPE_ONELEVEL))],
           title='Complete audit trail for currently bound identity'),
         app.anchor('search',
           'Audit my writes', [
          (
           'dn', app.audit_context),
          (
           'filterstr', '(&(objectClass=auditWriteObject)(reqAuthzID=%s))' % ldap0.filter.escape_str(app.ls.who or '')),
          (
           'scope', str(ldap0.SCOPE_ONELEVEL))],
           title='Audit trail of write access by currently bound identity'),
         app.anchor('search',
           'Last logins', [
          (
           'dn', app.audit_context),
          (
           'filterstr', '(&(objectClass=auditBind)(reqDN=%s))' % ldap0.filter.escape_str(app.ls.who or '')),
          (
           'scope', str(ldap0.SCOPE_ONELEVEL))],
           title='Audit trail of last logins (binds) by currently bound identity')])
    for config_dn, txt in config_dn_list:
        try:
            app.ls.l.read_s(config_dn, attrlist=['1.1'])
        except ldap0.LDAPError:
            pass
        else:
            context_menu_list.append(app.anchor('read', txt, [
             (
              'dn', config_dn)]))
    else:
        if 'schemaNamingContext' in app.ls.rootDSE:
            context_menu_list.append(app.anchor('read', 'AD Schema Configuration', [
             (
              'dn', app.ls.rootDSE['schemaNamingContext'][0])]))
        else:
            web2ldap.app.gui.top_section(app,
              'Connection Info',
              (web2ldap.app.gui.main_menu(app)),
              context_menu_list=context_menu_list)
            if app.ls.who:
                who_html = '%s<br>( %s )' % (
                 app.display_dn((app.ls.who), commandbutton=False),
                 web2ldapcnf.command_link_separator.join((
                  app.anchor('read',
                    'Read', [
                   (
                    'dn', app.ls.who)],
                    title=('Read bound entry\r\n%s' % app.ls.who)),
                  app.anchor('passwd',
                    'Password', [
                   (
                    'dn', app.ls.who), ('passwd_who', app.ls.who)],
                    title=('Set password of entry\r\n%s' % app.ls.who)))))
            else:
                who_html = 'anonymous'
            try:
                whoami_result = '&quot;%s&quot;' % app.form.utf2display(app.ls.l.whoami_s())
            except ldap0.LDAPError as ldap_err:
                try:
                    whoami_result = '<strong>Failed:</strong> %s' % app.ldap_error_msg(ldap_err)
                finally:
                    ldap_err = None
                    del ldap_err

            else:
                if app.ls.sasl_auth:
                    sasl_mech = 'SASL/%s' % app.ls.sasl_mech
                    sasl_auth_info = '<table>%s</table>' % '\n'.join(['<tr><td>%s</td><td>%s</td></tr>' % (
                     app.form.utf2display(ldap0.OPT_NAMES.get(k, str(k)).decode('ascii')),
                     app.form.utf2display(repr(v).decode(app.ls.charset))) for k, v in app.ls.sasl_auth.cb_value_dict.items() if v])
                else:
                    sasl_mech = 'simple'
                    sasl_auth_info = 'SASL not used'
        try:
            sasl_user_name = app.ls.l.get_option(ldap0.OPT_X_SASL_USERNAME).decode(app.ls.charset)
        except ldap0.LDAPError as ldap_err:
            try:
                sasl_user_name = 'error reading option: %s' % app.ldap_error_msg(ldap_err)
            finally:
                ldap_err = None
                del ldap_err

        except ValueError:
            sasl_user_name = ''
        else:
            try:
                sasl_ssf = str(app.ls.l.get_option(ldap0.OPT_X_SASL_SSF))
            except ldap0.LDAPError as ldap_err:
                try:
                    sasl_ssf = 'error reading option: %s' % app.ldap_error_msg(ldap_err)
                finally:
                    ldap_err = None
                    del ldap_err

            except ValueError:
                sasl_ssf = 'option not available'
            else:
                app.outf.write(CONNINFO_LDAP_TEMPLATE % (
                 app.ls.uri,
                 protocol_version,
                 app.ls.charset.upper(),
                 {False:'not secured', 
                  True:'secured'}[app.ls.secureConn],
                 web2ldap.utctime.strftimeiso8601(time.gmtime(app.ls.connStartTime)),
                 time.time() - app.ls.connStartTime,
                 app.ls.l._reconnects_done,
                 app.form.utf2display(app.ls.vendorName or monitored_info or {True:'OpenLDAP', 
                  False:''}[app.ls.is_openldap] or 'unknown'),
                 app.form.utf2display(app.ls.vendorVersion or ''),
                 who_html,
                 whoami_result,
                 app.form.utf2display(sasl_mech),
                 sasl_auth_info,
                 sasl_user_name,
                 app.form.utf2display(sasl_ssf),
                 app.form.utf2display(app.dn or '- World -'),
                 app.form.utf2display(app.parent_dn if app.parent_dn is not None else ''),
                 app.form.utf2display(str(app.naming_context)),
                 min(len(app.ls.l.last_search_bases), app.ls.l.last_search_bases.maxlen),
                 '<br>'.join([app.display_dn(search_base, commandbutton=True) for search_base in app.ls.l.last_search_bases])))
                app.outf.write(CONNINFO_LDAP_CACHE_TEMPLATE % (
                 app.anchor('conninfo',
                   'Flush all caches', [
                  (
                   'dn', app.dn), ('conninfo_flushcaches', '1')],
                   title='Flush all cached information for this LDAP connection'),
                 len(app.ls.l._cache),
                 len(app.ls._schema_dn_cache),
                 len(app.ls._schema_cache),
                 app.ls.l.cache_hit_ratio()))
                cross_check_vars = session_store.sessiondict[('__session_checkvars__' + app.sid)].items()
                cross_check_vars_html = '\n'.join(['<tr><td>%s</td><td>%s</td></tr>' % (
                 app.form.utf2display(k),
                 app.form.utf2display(v)) for k, v in sorted(cross_check_vars)])
                app.outf.write(CONNINFO_HTTP_TEMPLATE % (
                 app.ls.onBehalf,
                 app.form.utf2display(str(app.env.get('REMOTE_ADDR', ''))),
                 app.form.utf2display(str(app.env.get('REMOTE_PORT', ''))),
                 app.env.get('SERVER_SIGNATURE', ''),
                 app.form.utf2display(str(', '.join(app.form.accept_language))),
                 app.form.utf2display(app.form.accept_charset.upper()),
                 cross_check_vars_html,
                 app.form.utf2display(app.env.get('HTTP_USER_AGENT', ''))))
                web2ldap.app.gui.footer(app)