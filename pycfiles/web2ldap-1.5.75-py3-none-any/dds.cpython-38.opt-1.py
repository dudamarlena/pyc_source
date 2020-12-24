# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/dds.py
# Compiled at: 2020-05-04 07:51:57
# Size of source mod 2**32: 3292 bytes
"""
web2ldap.app.dds: refresh entryTTL of dynamic entry with extended operation

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0
from ldap0.extop.dds import RefreshRequest, RefreshResponse
import web2ldap.app.gui
DDS_FORM_TMPL = '\n<h1>Refresh Dynamic Entry</h1>\n{text_info_message}\n{form_begin}\n{field_dn}\n<table>\n  <tr><td>DN of entry:</td><td>{text_dn}</td></tr>\n  <tr>\n    <td>Refresh TTL:</td><td>{field_dds_renewttlnum} {field_dds_renewttlfac}</td>\n  </tr>\n</table>\n  <input type="submit" value="Refresh">\n  </form>\n'

def dds_form(app, msg):
    """
    Output input form for entering TTL for dynamic entry refresh
    """
    if msg:
        msg = '<p class="ErrorMessage">%s</p>' % msg
    else:
        msg = '<p class="Message">Enter time-to-live for refresh request or leave empty for server-side default.</p>'
    web2ldap.app.gui.top_section(app,
      'Refresh dynamic entry', (web2ldap.app.gui.main_menu(app)),
      context_menu_list=(web2ldap.app.gui.ContextMenuSingleEntry(app)))
    app.outf.write(DDS_FORM_TMPL.format(text_info_message=msg,
      form_begin=(app.begin_form('dds', 'POST')),
      field_dn=(app.form.hiddenFieldHTML('dn', app.dn, '')),
      text_dn=(app.display_dn(app.dn)),
      field_dds_renewttlnum=(app.form.field['dds_renewttlnum'].input_html()),
      field_dds_renewttlfac=(app.form.field['dds_renewttlfac'].input_html())))
    web2ldap.app.gui.footer(app)


def w2l_dds(app):
    """
    Dynamic entry refresh operation
    """
    if 'dds_renewttlnum' not in app.form.input_field_names or 'dds_renewttlfac' not in app.form.input_field_names:
        dds_form(app, None)
        return None
    try:
        request_ttl = int(app.form.getInputValue('dds_renewttlnum', [None])[0]) * int(app.form.getInputValue('dds_renewttlfac', [None])[0])
    except ValueError:
        request_ttl = None
    else:
        extreq = RefreshRequest(entryName=(app.dn), requestTtl=request_ttl)
        try:
            extop_resp_obj = app.ls.l.extop_s(extreq, extop_resp_class=RefreshResponse)
        except ldap0.SIZELIMIT_EXCEEDED as ldap_err:
            try:
                dds_form(app, app.ldap_error_msg(ldap_err))
            finally:
                ldap_err = None
                del ldap_err

        else:
            if request_ttl and extop_resp_obj.responseTtl != request_ttl:
                msg = '<p class="WarningMessage">Refreshed entry %s with TTL %d instead of %d.</p>' % (
                 app.display_dn(app.dn),
                 extop_resp_obj.responseTtl, request_ttl)
            else:
                msg = '<p class="SuccessMessage">Refreshed entry %s with TTL %d.</p>' % (
                 app.display_dn(app.dn),
                 extop_resp_obj.responseTtl)
            app.simple_message(message=msg,
              main_menu_list=(web2ldap.app.gui.main_menu(app)),
              context_menu_list=web2ldap.app.gui.ContextMenuSingleEntry(app, dds_link=1))