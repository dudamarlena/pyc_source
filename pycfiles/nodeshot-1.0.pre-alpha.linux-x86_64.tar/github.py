# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/profiles/social_auth_extra/github.py
# Compiled at: 2014-05-07 09:54:09
"""
Fixed Github Backend for social auth
"""
from social_auth.backends.contrib.github import GithubBackend as BaseGithubBackend, GithubAuth

class GithubBackend(BaseGithubBackend):
    """Github OAuth authentication backend"""

    def get_user_details(self, response):
        """Return user details from Github account"""
        name = response.get('name') or ''
        details = {'username': response.get('login')}
        try:
            email = self._fetch_emails(response.get('access_token'))[0]
            if isinstance(email, dict):
                email = email['email']
        except IndexError:
            details['email'] = ''
        else:
            details['email'] = email

        try:
            first_name, last_name = name.split(' ', 1)
        except ValueError:
            details['first_name'] = name
        else:
            details['first_name'] = first_name
            details['last_name'] = last_name

        return details


BACKENDS = {'github': GithubAuth}