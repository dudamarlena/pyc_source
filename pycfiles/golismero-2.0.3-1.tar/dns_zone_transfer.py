# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/information_disclosure/dns_zone_transfer.py
# Compiled at: 2014-02-05 05:31:56
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'DNSZoneTransfer']
from .. import Vulnerability
from ... import identity

class DNSZoneTransfer(Vulnerability):
    """
    DNS Zone Transfer Enabled.

    When DNS zone transfers are enabled, the DNS server allows any user to
    download the entire set of domain names defined by that server. This may
    help an adversary to gather information prior to an attack.

    The details on how to disable zone transfers is specific to the DNS server
    being used. Please consult the documentation of your DNS server software
    on how to do this.
    """
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'high'
    DEFAULTS['capec'] = 'CAPEC-291'
    DEFAULTS['cwe'] = ('CWE-276', 'CWE-16')
    DEFAULTS['cvss_base'] = '6.0'
    DEFAULTS['references'] = ('https://en.wikipedia.org/wiki/DNS_zone_transfer', 'https://www.owasp.org/index.php/Information_Leakage')

    def __init__(self, ns_server, port=53, **kwargs):
        """
        :param ns_server: Nameserver address.
        :type ns_server: str

        :param port: Open port in name server.
        :type port: int

        """
        if not isinstance(port, int):
            raise TypeError("Expected int, got '%s'" % type(port))
        if not isinstance(ns_server, basestring):
            raise TypeError("Expected str, got '%s'" % type(ns_server))
        if port < 1 or port > 65535:
            raise ValueError('Port value must be between the range: 0-65535.')
        self.__ns_server = ns_server
        self.__port = port
        super(DNSZoneTransfer, self).__init__(**kwargs)

    __init__.__doc__ += Vulnerability.__init__.__doc__

    @identity
    def ns_server(self):
        """
        :return: an string with the nameserver address.
        :rtype: str
        """
        return self.__ns_server

    @identity
    def port(self):
        """
        :return: opened port in name server.
        :rtype: int
        """
        return self.__port