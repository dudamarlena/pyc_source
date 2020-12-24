# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/utilities/sanitise_redirects.py
# Compiled at: 2014-08-27 19:26:12
import urlparse
from signalbox.exceptions import SuspiciousActivityException

def sanitise_user_supplied_redirect(request, redirect_to):
    """Make sure users can't add ?success_url=http://nastyurl.com to redirects.

    Borrowed from https://github.com/django/django/blob/master/django/contrib/auth/views.py
    """
    netloc = urlparse.urlparse(redirect_to)[1]
    if netloc and netloc != request.get_host():
        raise SuspiciousActivityException('Suspicious redirect spotted.')
    return redirect_to