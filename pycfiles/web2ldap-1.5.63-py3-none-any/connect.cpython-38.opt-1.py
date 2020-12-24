# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/connect.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 2011 bytes
"""
web2ldap.app.connect: present connect dialogue for choosing server

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, web2ldapcnf, web2ldapcnf.hosts, web2ldap.web.forms, web2ldap.app.core, web2ldap.app.gui

def w2l_connect(app, h1_msg='Connect', error_msg=''):
    """
    Display the landing page with a connect form
    """
    connect_template_str = web2ldap.app.gui.read_template(app,
      None, 'connect form', tmpl_filename=(web2ldapcnf.connect_template))
    if web2ldapcnf.hosts.ldap_uri_list:
        uri_select_field = web2ldap.web.forms.Select('ldapurl',
          'LDAP uri',
          1,
          options=(web2ldapcnf.hosts.ldap_uri_list))
        uri_select_field.charset = 'utf-8'
        uri_select_field_html = uri_select_field.input_html(title='List of pre-configured directories to connect to')
    else:
        uri_select_field_html = ''
    if error_msg:
        error_msg = '<p class="ErrorMessage">%s</p>' % error_msg
    app.simple_message('Connect',
      connect_template_str.format(text_scriptname=(app.env.get('SCRIPT_NAME', '')),
      text_heading=h1_msg,
      text_error=error_msg,
      form_begin=(app.begin_form('searchform', 'GET')),
      field_uri_select=uri_select_field_html,
      disable_start=({False:'', 
     True:'<!--'}[web2ldapcnf.hosts.restricted_ldap_uri_list]),
      disable_end=({False:'', 
     True:'-->'}[web2ldapcnf.hosts.restricted_ldap_uri_list]),
      value_currenttime=(time.strftime('%Y%m%d%H%M%SZ', time.gmtime()))),
      main_menu_list=(web2ldap.app.gui.simple_main_menu(app)),
      context_menu_list=[])