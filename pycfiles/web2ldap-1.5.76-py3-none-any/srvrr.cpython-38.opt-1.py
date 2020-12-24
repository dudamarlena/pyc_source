# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/srvrr.py
# Compiled at: 2020-05-04 07:51:09
# Size of source mod 2**32: 2111 bytes
"""
web2ldap.app.srvrr: chase SRV RRs

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import web2ldap.web.forms, web2ldap.app.gui
SRVRR_TMPL = '\n<h1>Entry located via DNS</h1>\n%s\n%s\n  %s might be located on different host:\n  <p>%s</p>\n  <fieldset title="User account info">\n    <p>\n      to host:port %s (%s)\n      with identification search below %s.\n    </p>\n    <table summary="User account info">\n      <tr>\n        <td>Bind as</td>\n        <td>\n          <input name="who" maxlength="1024" size="40" value="%s">\n        </td>\n      </tr>\n      <tr>\n        <td>with password</td>\n        <td>\n          <input type="password" name="cred" maxlength="200" size="25" value="">\n        </td>\n      </tr>\n    </table>\n    <p>\n      <input type="submit" value="%s">\n    </p>\n  </fieldset>\n'

def w2l_chasesrvrecord(app, host_list):
    """
    Present an input form to change to a server located via DNS SRV RR
    """
    host_list = [host.decode('idna') for host in host_list]
    host_select_field = web2ldap.web.forms.Select('host',
      'Host selection', 1, options=host_list,
      default=(host_list[0]),
      ignoreCase=1)
    web2ldap.app.gui.top_section(app,
      'LDAP server located via DNS',
      (web2ldap.app.gui.main_menu(app)),
      context_menu_list=[], main_div_id='Input')
    app.outf.write(SRVRR_TMPL % (
     app.begin_form(app.command, 'POST'),
     app.form.hiddenFieldHTML('dn', app.dn, ''),
     app.form.utf2display(app.dn),
     host_select_field.input_html(),
     '', '', '', '',
     'Change host'))
    app.form.hidden_fields((app.outf),
      ignore_fields={
     'ldapurl', 'host', 'dn', 'who', 'cred'})
    app.outf.write('</form>\n')
    web2ldap.app.gui.footer(app)