# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stackoverflow/auth_stackoverflow.py
# Compiled at: 2014-02-22 10:22:35
from BeautifulSoup import BeautifulSoup
from stackoverflow.base import StackOverflowBase

class StackOverflow_SOAuth(StackOverflowBase):

    def authenticate(self):
        if self.is_authenticated():
            return
        r = self.session.get('http://%s/users/login' % self.site)
        fkey = BeautifulSoup(r.text).find(attrs={'name': 'fkey'})['value']
        payload = {'openid_identifier': 'https://openid.stackexchange.com', 'openid_username': '', 
           'oauth_version': '', 
           'oauth_server': '', 
           'fkey': fkey}
        r = self.session.post('http://%s/users/authenticate' % self.site, allow_redirects=True, data=payload)
        fkey = BeautifulSoup(r.text).find(attrs={'name': 'fkey'})
        fkey = fkey['value'] if fkey else ''
        session_name = BeautifulSoup(r.text).find(attrs={'name': 'session'})
        session_name = session_name['value'] if session_name else ''
        payload = {'email': self.username, 'password': self.password, 
           'fkey': fkey, 
           'session': session_name}
        r = self.session.post('https://openid.stackexchange.com/account/login/submit', data=payload)
        error = BeautifulSoup(r.text).findAll(attrs={'class': 'error'})
        if len(error) != 0:
            raise Exception('Error: %s' % error[0].text)