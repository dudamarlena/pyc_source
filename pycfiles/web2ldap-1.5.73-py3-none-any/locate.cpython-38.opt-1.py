# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/locate.py
# Compiled at: 2020-05-04 08:40:18
# Size of source mod 2**32: 10062 bytes
"""
web2ldap.app.locate: Try to locate a LDAP host with various methods.

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import socket
from dns import resolver
import ldap0
from ldap0.dn import DNObj
from ldap0.ldapurl import LDAPUrlExtension, LDAPUrlExtensions
from web2ldap.ldaputil.extldapurl import ExtendedLDAPUrl
import web2ldap.ldaputil, web2ldap.ldaputil.dns, web2ldap.app.gui
LDAP_HOSTNAME_ALIASES = [
 'ldap']
LOCATE_NAME_RFC822 = 0
LOCATE_NAME_DCDN = 1
LOCATE_NAME_DOMAIN = 2
LOCATE_INPUT_FORM_TMPL = '\n<h1>Locate LDAP host via DNS</h1>\n%s\n%s\n<form\n  action="%s/locate"\n  method="GET"\n  enctype="application/x-www-form-urlencoded"\n  accept-charset="%s"\n>\n  <fieldset title="Locate LDAP host by DNS name or DN.">\n    <input type="submit" value="Locate"><br>\n    <p>\n      Search for well-known DNS aliases of LDAP servers and DNS SRV\n      records in a given DNS domain by entering e-mail address, DNS\n      domain or dc-style DN:\n    </p>\n    <p>\n      <input name="locate_name" size="60">\n    </p>\n  </fieldset>\n</form>\n'
LOCATE_HOST_RESULT_TMPL = '\n<p>IP address found for host name %s: %s</p>\n<table>\n  <tr>\n    <td>%s</td>\n    <td><a href="%s">%s</a></td>\n  </tr>\n</table>\n'

def w2l_locate(app):
    """
    Try to locate a LDAP server in DNS by several heuristics
    """
    locate_name = app.form.getInputValue('locate_name', [''])[0].strip()
    msg_html = ''
    outf_lines = []
    if locate_name:
        if ldap0.dn.is_dn(locate_name):
            msg_html = 'Input is considered LDAP distinguished name.'
            locate_domain = DNObj.from_str(locate_name).domain(only_dc=False).encode('idna').decode('ascii')
            locate_name_type = LOCATE_NAME_DCDN
        else:
            if '@' in locate_name:
                msg_html = 'Input is considered e-mail address or user principal name.'
                locate_domain = locate_name.split('@')[(-1)]
                locate_name_type = LOCATE_NAME_RFC822
            else:
                msg_html = 'Input is considered DNS domain name.'
                locate_domain = locate_name
                locate_name_type = LOCATE_NAME_DOMAIN
        if locate_domain:
            dns_list = locate_domain.lower().split('.')
            for dns_index in range(len(dns_list), 0, -1):
                dns_name = '.'.join([label.encode('idna').decode('ascii') for label in dns_list[-dns_index:]])
                search_base = str(DNObj.from_domain(dns_name))
                if dns_name.endswith('de-mail-test.de') or dns_name.endswith('de-mail.de'):
                    search_base = ','.join((search_base, 'cn=de-mail'))
                    lu_extensions = LDAPUrlExtensions({'x-saslmech': LDAPUrlExtension(critical=0,
                                     extype='x-saslmech',
                                     exvalue='EXTERNAL')})
                else:
                    lu_extensions = None
                outf_lines.append('<h1><em>%s</em></h1>\n' % (
                 app.form.utf2display(dns_name),))
                ldap_srv_results = []
                for url_scheme in ('ldap', 'ldaps'):
                    srv_prefix = '_%s._tcp' % url_scheme

            try:
                dns_result = web2ldap.ldaputil.dns.srv_lookup(dns_name,
                  srv_prefix=srv_prefix)
            except (
             resolver.NoAnswer,
             resolver.NoNameservers,
             resolver.NotAbsolute,
             resolver.NoRootSOA,
             resolver.NXDOMAIN,
             socket.error) as e:
                try:
                    outf_lines.append('DNS or socket error when querying %s: %s' % (
                     srv_prefix,
                     app.form.utf2display(str(e))))
                finally:
                    e = None
                    del e

            else:
                if dns_result:
                    ldap_srv_results.append((url_scheme, dns_result))
            if ldap_srv_results:
                outf_lines.append('<h2>Found SRV RRs</h2>\n')
                for url_scheme, srv_result in ldap_srv_results:
                    for priority, weight, port, hostname in srv_result:
                        outf_lines.append('<p>Found SRV record: %s:%d (priority %d, weight %d)</p>' % (
                         hostname, port, priority, weight))
                        try:
                            host_address = socket.gethostbyname(hostname)
                        except socket.error as e:
                            try:
                                outf_lines.append('<p class="ErrorMessage">Did not find IP address for hostname <em>%s</em>.</p>' % app.form.utf2display(hostname.decode('ascii')))
                            finally:
                                e = None
                                del e

                        else:
                            ldap_url = ExtendedLDAPUrl(urlscheme=url_scheme,
                              hostport=('%s:%d' % (hostname, port)),
                              dn=search_base,
                              scope=(ldap0.SCOPE_BASE),
                              extensions=lu_extensions)
                            outf_lines.append('\n                                    <p>IP address found for host name %s: %s</p>\n                                    <table>\n                                      <tr>\n                                        <td>%s</td>\n                                        <td><a href="%s">%s</a></td>\n                                      </tr>\n                                    ' % (
                             hostname,
                             host_address,
                             web2ldap.app.gui.ldap_url_anchor(app, str(ldap_url)),
                             ldap_url.unparse(),
                             ldap_url.unparse()))
                        if locate_name_type == LOCATE_NAME_RFC822:
                            ldap_url = ExtendedLDAPUrl(urlscheme=url_scheme,
                              hostport=('%s:%d' % (hostname, port)),
                              dn=search_base,
                              scope=(ldap0.SCOPE_SUBTREE),
                              filterstr=('(mail=%s)' % locate_name),
                              extensions=lu_extensions)
                            outf_lines.append('<tr>\n                                    <td>%s</td>\n                                    <td><a href="%s">Search %s</a></td>\n                                    </tr>\n                                    ' % (
                             web2ldap.app.gui.ldap_url_anchor(app, ldap_url),
                             ldap_url.unparse(),
                             ldap_url.unparse()))

                else:
                    outf_lines.append('</table>\n')

        else:
            host_addresses = []
            for alias in LDAP_HOSTNAME_ALIASES:
                alias_name = '.'.join([alias, dns_name])
                try:
                    host_address = socket.gethostbyname(alias_name)
                except socket.error:
                    pass
                else:
                    host_addresses.append(host_address)
            else:
                if host_addresses:
                    outf_lines.append('<h2>Found well known aliases</h2>\n')
                    for host_address in host_addresses:
                        ldap_url = ExtendedLDAPUrl(hostport=alias_name,
                          dn=search_base,
                          scope=(ldap0.SCOPE_BASE))
                        outf_lines.append(LOCATE_HOST_RESULT_TMPL % (
                         alias_name,
                         host_address,
                         web2ldap.app.gui.ldap_url_anchor(app, ldap_url),
                         ldap_url.unparse(),
                         ldap_url.unparse()))

    app.simple_message('DNS lookup',
      (LOCATE_INPUT_FORM_TMPL % (
     msg_html,
     '\n'.join(outf_lines),
     app.form.script_name,
     app.form.accept_charset)),
      main_menu_list=(web2ldap.app.gui.simple_main_menu(app)),
      context_menu_list=[])