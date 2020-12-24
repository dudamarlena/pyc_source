# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/ssl/invalid_common_name.py
# Compiled at: 2014-02-05 05:58:20
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'InvalidCommonName']
from . import SSLVulnerability
from ... import identity

class InvalidCommonName(SSLVulnerability):
    """
    Invalid CN Field.

    An invalid CN field was found in a SSL/TLS certificate. This may allow a
    strategically located attacker to snoop on network traffic, or perform a
    Man-In-The-Middle attack against unsuspecting users connecting to this
    host.

    Create a new certificate with the correct CN field.
    """
    DEFAULTS = SSLVulnerability.DEFAULTS.copy()
    DEFAULTS['cwe'] = 'CWE-327'
    DEFAULTS['cvss_base'] = '4'

    def __init__(self, domain, common_name, **kwargs):
        """
        :param domain: Domain where the vulnerability was found.
        :type domain: Domain

        :param common_name: Common name (CN).
        :type common_name: str

        """
        self.__common_name = common_name
        super(InvalidCommonName, self).__init__(domain, **kwargs)

    __init__.__doc__ += SSLVulnerability.__init__.__doc__

    @identity
    def common_name(self):
        """
        :returns: Common name (CN).
        :rtype: str
        """
        return self.__common_name