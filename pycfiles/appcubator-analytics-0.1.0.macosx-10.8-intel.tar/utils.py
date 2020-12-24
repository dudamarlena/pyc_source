# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kssworld93/Projects/appcubator-site/venv/lib/python2.7/site-packages/analytics/utils.py
# Compiled at: 2013-07-17 17:55:02
from django.conf import settings
import re, unicodedata
IP_RE = re.compile('\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}')

def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.
    """
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                ip_address = '10.0.0.1'
        except IndexError:
            pass

    return ip_address


def get_timeout():
    """
    Gets any specified timeout from the settings file, or use 10 minutes by
    default
    """
    return getattr(settings, 'TRACKING_TIMEOUT', 10)


def get_cleanup_timeout():
    """
    Gets any specified visitor clean-up timeout from the settings file, or
    use 24 hours by default
    """
    return getattr(settings, 'TRACKING_CLEANUP_TIMEOUT', 24)


def u_clean(s):
    """A strange attempt at cleaning up unicode"""
    uni = ''
    try:
        uni = str(s).decode('iso-8859-1')
    except UnicodeDecodeError:
        try:
            uni = str(s).decode('utf-8')
        except UnicodeDecodeError:
            if s and type(s) in (str, unicode):
                for c in s:
                    try:
                        uni += unicodedata.normalize('NFKC', unicode(c))
                    except UnicodeDecodeError:
                        uni += '-'

    return uni.encode('ascii', 'xmlcharrefreplace')