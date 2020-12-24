# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/params.py
# Compiled at: 2020-05-04 07:51:28
# Size of source mod 2**32: 5784 bytes
"""
web2ldap.app.params: Display (SSL) connection data

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import web2ldap.ldapsession, web2ldap.app.cnf, web2ldap.app.core, web2ldap.app.gui
from web2ldap.ldaputil.oidreg import OID_REG
from web2ldap.ldapsession import AVAILABLE_BOOLEAN_CONTROLS

def w2l_params(app):
    ldap_deref = app.form.getInputValue('ldap_deref', [])
    if ldap_deref:
        app.ls.l.deref = int(ldap_deref[0])
    web2ldap.app.gui.top_section(app,
      'LDAP Connection Parameters',
      (web2ldap.app.gui.main_menu(app)),
      context_menu_list=[])
    ldapparam_all_controls = app.form.getInputValue('params_all_controls', ['0'])[0] == '1'
    ldapparam_enable_control = app.form.getInputValue('params_enable_control', [None])[0]
    if ldapparam_enable_control:
        if ldapparam_enable_control in AVAILABLE_BOOLEAN_CONTROLS:
            methods, control_class, control_value = AVAILABLE_BOOLEAN_CONTROLS[ldapparam_enable_control]
            for method in methods:
                if control_value is not None:
                    app.ls.l.add_server_control(method, control_class(ldapparam_enable_control, 1, control_value))
                else:
                    app.ls.l.add_server_control(method, control_class(ldapparam_enable_control, 1))

    ldapparam_disable_control = app.form.getInputValue('params_disable_control', [None])[0]
    if ldapparam_disable_control:
        if ldapparam_disable_control in AVAILABLE_BOOLEAN_CONTROLS:
            methods, control_class, control_value = AVAILABLE_BOOLEAN_CONTROLS[ldapparam_disable_control]
            for method in methods:
                app.ls.l.del_server_control(method, ldapparam_disable_control)

    enabled_controls = set()
    for control_oid, control_spec in AVAILABLE_BOOLEAN_CONTROLS.items():
        methods, control_class, control_value = control_spec
        control_enabled = True

    for method in methods:
        control_enabled = control_enabled and control_oid in app.ls.l.get_ctrls(method)
    else:
        if control_enabled:
            enabled_controls.add(control_oid)
        control_table_rows = []
        for control_oid in AVAILABLE_BOOLEAN_CONTROLS:
            control_enabled = control_oid in enabled_controls
            if not (control_enabled or ldapparam_all_controls or control_oid in app.ls.supportedControl):
                pass
            else:
                name, description, _ = OID_REG[control_oid]
                control_table_rows.append('\n            <tr>\n              <td>%s</td>\n              <td>%s%s%s</td>\n              <td>%s</td>\n              <td>%s</td>\n            </tr>\n            ' % (
                 app.anchor('params',
                   ({False:'Enable', 
                  True:'Disable'}[control_enabled]),
                   [
                  (
                   'dn', app.dn),
                  (
                   'params_%s_control' % {False:'enable', 
                    True:'disable'}[control_enabled],
                   control_oid)],
                   title=('%s %s' % (
                  {False:'Enable', 
                   True:'Disable'}[control_enabled],
                  name))),
                 {False:'<strike>', 
                  True:''}[(control_oid in app.ls.supportedControl)],
                 app.form.utf2display(name),
                 {False:'</strike>', 
                  True:''}[(control_oid in app.ls.supportedControl)],
                 app.form.utf2display(control_oid),
                 app.form.utf2display(description)))
        else:
            app.outf.write('\n        <h1>LDAP Options</h1>\n        <p>Jump to another entry by entering its DN:</p>\n        %s\n        <p>Alias dereferencing:</p>\n        %s\n        <h2>LDAPv3 extended controls</h2>\n        <p>List %s controls</p>\n        <table id="booleancontrolstable" summary="Simple boolean controls">\n          <tr>\n            <th>&nbsp;</th>\n            <th>Name</th>\n            <th>OID</th>\n            <th>Description</th>\n          </tr>\n          %s\n            </table>\n          </fieldset>\n        ' % (
             app.form_html('read',
               'Go to', 'GET', [], extrastr=(app.form.field['dn'].input_html())),
             app.form_html('params',
               'Set alias deref', 'GET', [], extrastr=app.form.field['ldap_deref'].input_html(default=(str(app.ls.l.deref)))),
             app.anchor('params',
               ({False:'all', 
              True:'only known'}[ldapparam_all_controls]),
               [
              (
               'dn', app.dn),
              (
               'params_all_controls', str(int(not ldapparam_all_controls)))],
               title=('Show %s controls' % (
              {False:'all', 
               True:'known'}[ldapparam_all_controls],))),
             '\n'.join(control_table_rows)))
            web2ldap.app.gui.footer(app)