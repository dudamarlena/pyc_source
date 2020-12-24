# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/gittle/utils/urls.py
# Compiled at: 2013-09-03 02:36:01
from urlparse import urlparse
from funky import first_true

def is_http_url(url, parsed):
    if parsed.scheme in ('http', 'https'):
        return parsed.scheme
    else:
        return


def is_git_url(url, parsed):
    if parsed.scheme == 'git':
        return parsed.scheme
    else:
        return


def is_ssh_url(url, parsed):
    if parsed.scheme == 'git+ssh':
        return parsed.scheme
    else:
        return


def get_protocol(url):
    schemers = [
     is_git_url,
     is_ssh_url,
     is_http_url]
    parsed = urlparse(url)
    try:
        return first_true([ schemer(url, parsed) for schemer in schemers
                          ])
    except:
        pass

    return


def get_password(url):
    pass


def get_user(url):
    pass


def parse_url(url, defaults=None):
    """Parse a url corresponding to a git repository
    """
    DEFAULTS = {'protocol': 'git+ssh'}
    defaults = defaults or DEFAULTS
    protocol = get_protocol() or defaults.get('protocol')
    return {'domain': domain, 
       'protocol': protocol, 
       'user': user, 
       'password': password, 
       'path': path}