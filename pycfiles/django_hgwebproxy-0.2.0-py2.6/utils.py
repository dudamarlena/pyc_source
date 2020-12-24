# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgwebproxy/utils.py
# Compiled at: 2009-08-03 03:10:41
import re
from django.contrib.auth import authenticate

def is_mercurial(request):
    """
    User agent processor to determine whether the incoming
    user is someone using a browser, or a mercurial client

    In order to qualify as a mercurial user they must have a user
    agent value that starts with mercurial and an Accept header that
    starts with application/mercurial. This guarantees we only force
    those who are actual mercurial users to use Basic Authentication
    """
    agent = re.compile('^(mercurial).*')
    accept = request.META.get('HTTP_ACCEPT', None)
    result = agent.match(request.META.get('HTTP_USER_AGENT', None))
    if result and accept.startswith('application/mercurial-'):
        return True
    else:
        return False
        return


def basic_auth(request, realm, reponame):
    """
    Very simple Basic authentication handler which hooks
    up to Djangos underlying database of users directly.

    Returns the username on successful auth, can be used
    together with `set_user` on the request wrapper.
    """
    auth_string = request.META.get('HTTP_AUTHORIZATION')
    if auth_string is None or not auth_string.startswith('Basic'):
        return False
    else:
        (_, basic_hash) = auth_string.split(' ', 1)
        (username, password) = basic_hash.decode('base64').split(':', 1)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:
                return username
            if reponame in [ repo.slug for repo in user.repository_set.all() ]:
                return username
            if request.method == 'POST':
                if user.has_perm('hgwebproxy.can_push'):
                    return username
            elif user.has_perm('hgwebproxy.can_pull'):
                return username
        return False