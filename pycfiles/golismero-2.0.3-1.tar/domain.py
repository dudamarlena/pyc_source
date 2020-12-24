# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/resource/domain.py
# Compiled at: 2014-01-13 19:15:58
"""
Domain name.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Domain']
from . import Resource
from .. import identity
from ...config import Config
from ...net.web_utils import split_hostname
from ...text.text_utils import to_utf8
from netaddr import IPAddress
import re

class Domain(Resource):
    """
    Domain name.

    This data type maps the domain names to the IP addresses they resolve to.
    """
    resource_type = Resource.RESOURCE_DOMAIN
    _re_is_domain = re.compile('^[A-Za-z0-9][A-Za-z0-9\\_\\-\\.]*[A-Za-z0-9]$')

    def __init__(self, hostname):
        """
        :param hostname: Domain name.
        :type hostname: str
        """
        hostname = to_utf8(hostname)
        if not isinstance(hostname, str):
            raise TypeError('Expected string, got %r instead' % type(hostname))
        if not hostname:
            raise ValueError('Missing hostname')
        try:
            if hostname.startswith('[') and hostname.endswith(']'):
                IPAddress(hostname[1:-1], version=6)
            else:
                IPAddress(hostname)
        except Exception:
            pass
        else:
            raise ValueError('This is an IP address (%s) not a domain!' % hostname)

        if not self._re_is_domain.match(hostname):
            raise ValueError('Invalid domain name: %r' % hostname)
        self.__hostname = hostname
        super(Domain, self).__init__()
        self.depth = 0

    def __str__(self):
        return self.hostname

    def __repr__(self):
        return '<Domain name=%r>' % self.hostname

    @property
    def display_name(self):
        return 'Domain Name'

    def is_in_scope(self, scope=None):
        if scope is None:
            scope = Config.audit_scope
        return self.hostname in scope

    @identity
    def hostname(self):
        """
        :return: Domain name.
        :rtype: str
        """
        return self.__hostname

    @property
    def root(self):
        """
        :return: Root domain. i.e: www.mysite.com -> mysite.com
        :rtype: str
        """
        _, domain, suffix = split_hostname(self.hostname)
        if suffix:
            return '%s.%s' % (domain, suffix)
        return domain

    @property
    def discovered(self):
        domain = self.hostname
        result = []
        subdomain, domain, suffix = split_hostname(domain)
        if subdomain:
            prefix = ('.').join((domain, suffix))
            for part in reversed(subdomain.split('.')):
                if prefix in Config.audit_scope:
                    result.append(Domain(prefix))
                prefix = ('.').join((part, prefix))

        return result