# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/traccas/pycas.py
# Compiled at: 2008-05-04 19:21:03
import urllib, urllib2

class PyCAS(object):
    """A class for working with a CAS server."""
    __module__ = __name__

    def __init__(self, url, renew=False, **kwords):
        self.url = url
        self.renew = renew
        self.paths = {'login_path': '/login', 'logout_path': '/login', 'validate_path': '/validate'}
        self.paths.update(kwords)

    def login_url(self, service):
        """Return the login URL for the given service."""
        base = self.url + self.paths['login_path'] + '?service=' + urllib.quote_plus(service)
        if self.renew:
            base += '&renew=true'
        return base

    def logout_url(self, url=None):
        """Return the logout URL."""
        base = self.url + self.paths['logout_path']
        if url:
            base += '?url=' + urllib.quote_plus(url)
        return base

    def validate_url(self, service, ticket):
        """Return the validation URL for the given service. (For CAS 1.0)"""
        base = self.url + self.paths['validate_path'] + '?service=' + urllib.quote_plus(service) + '&ticket=' + urllib.quote_plus(ticket)
        if self.renew:
            base += '&renew=true'
        return base

    def validate_ticket(self, service, ticket):
        """Validate the given ticket against the given service."""
        f = urllib2.urlopen(self.validate_url(service, ticket))
        valid = f.readline()
        valid = valid.strip() == 'yes'
        user = f.readline().strip()
        return (
         valid, user)