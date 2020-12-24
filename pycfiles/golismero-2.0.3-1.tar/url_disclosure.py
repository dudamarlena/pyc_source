# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/information_disclosure/url_disclosure.py
# Compiled at: 2014-02-05 05:46:42
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'UrlDisclosure']
from .. import UrlVulnerability
from posixpath import split

class UrlDisclosure(UrlVulnerability):
    """
    URL Disclosure.

    These are URLs that are accessible but not linked from the web site itself.
    It may indicate a poor attempt at concealing information.
    For example:
    - Backup files: http://www.example.com/ **index.php.old**
    - Alternative file names: http://www.example.com/ **index4.php**
    - Remnants of deployment: http://www.example.com/ **build.xml**
    - Poorly configured servers: http://www.example.com/ **error_log**
    - Forgotten server files: http://www.example.com/ **server-status**

    Remove any sensitive information that may have been left behind. If it's
    not possible to remove it, block access to it from the HTTP server.
    """
    DEFAULTS = UrlVulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'informational'
    DEFAULTS['cwe'] = 'CWE-200'
    DEFAULTS['cvss_base'] = '2.9'
    DEFAULTS['references'] = ('https://www.owasp.org/index.php/Information_Leakage', )

    @property
    def discovered_path(self):
        """
        Discovered part of the URL.

        >>> from golismero.api.data.resource.url import Url
        >>> from golismero.api.data.vulnerability.information_disclosure.url_disclosure import UrlDisclosure
        >>> url = Url('http://www.example.com/path/to_the/file/index.php.old')
        >>> url_disclosure = UrlDisclosure(url)
        >>> url_disclosure
        <UrlDisclosure url='http://www.example.com/path/to_the/file/index.php.old'>
        >>> url_disclosure.discovered
        'index.php.old'

        :returns: Discovered part of the URL.
        :rtype: str
        """
        return split(self.url.parsed_url.path)[1]