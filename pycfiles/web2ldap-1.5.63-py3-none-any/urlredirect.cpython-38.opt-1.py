# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/urlredirect.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1699 bytes
"""
web2ldap.app.urlredirect: handle URL redirection

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import urllib.parse, web2ldapcnf
from web2ldap.app.session import session_store

def w2l_urlredirect(app):
    redirect_ok = app.form.query_string in web2ldapcnf.good_redirect_targets
    if not redirect_ok:
        try:
            tu = urllib.parse.urlparse(app.form.query_string)
        except Exception:
            redirect_ok = False
            error_msg = 'Rejected non-parseable redirect URL!'
        else:
            redirect_ok = True
            if not (tu and tu.scheme and tu.netloc):
                redirect_ok = False
                error_msg = 'Rejected malformed/suspicious redirect URL!'
            if app.sid not in session_store.sessiondict:
                redirect_ok = False
                error_msg = 'Rejected redirect without session-ID!'
    elif redirect_ok:
        app.url_redirect(('Redirecting to %s...' % app.form.query_string),
          refresh_time=0,
          target_url=(app.form.query_string))
    else:
        app.url_redirect(error_msg)