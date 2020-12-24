# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/information_disclosure/domain_disclosure.py
# Compiled at: 2014-02-05 05:32:28
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'DomainDisclosure']
from .. import Vulnerability
from ... import identity
from ....net.web_utils import split_hostname
from ....text.text_utils import to_utf8
from netaddr import IPAddress

class DomainDisclosure(Vulnerability):
    """
    Domain Disclosure.

    A domain was found by brute force or leaked by other means.
    """
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'informational'
    DEFAULTS['cwe'] = 'CWE-200'
    DEFAULTS['cvss_base'] = '2.2'
    DEFAULTS['references'] = ('https://www.owasp.org/index.php/Information_Leakage', )

    def __init__(self, hostname, **kwargs):
        """
        :param hostname: Domain name.
        :type hostname: str
        """
        hostname = to_utf8(hostname)
        if not isinstance(hostname, str):
            raise TypeError('Expected string, got %r instead' % type(hostname))
        try:
            if hostname.startswith('[') and hostname.endswith(']'):
                IPAddress(hostname[1:-1], version=6)
            else:
                IPAddress(hostname)
        except Exception:
            pass
        else:
            raise ValueError('This is an IP address (%s) not a domain!' % hostname)

        self.__hostname = hostname
        super(DomainDisclosure, self).__init__(**kwargs)

    __init__.__doc__ += Vulnerability.__init__.__doc__

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