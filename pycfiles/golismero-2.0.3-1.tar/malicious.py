# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/malware/malicious.py
# Compiled at: 2014-02-05 05:56:52
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'MaliciousUrl', 'MaliciousDomain', 'MaliciousIP', 'MaliciousASN']
from . import Malware
from .. import Vulnerability, UrlVulnerability, DomainVulnerability, IPVulnerability
from ... import identity

class MaliciousUrl(UrlVulnerability):
    """
    Malicious URL Detected.

    A URL was found that could contain output links to a malicious site or
    malware. This may be the result of a security intrusion, or a successful
    persistent XSS attack by a nefarious entity.

    You should review your website and ensure that your site was not
    compromised by a security intrusion.
    """
    DEFAULTS = Malware.DEFAULTS.copy()
    DEFAULTS['cvss_base'] = '4.3'


class MaliciousDomain(DomainVulnerability):
    """
    Malicious Domain Detected.

    A domain was found that could contain output links to a malicious site or
    malware. This may be the result of a security intrusion, or a successful
    DNS poisoning attack by a nefarious entity.

    You should review your website and ensure that your site was not
    compromised by a security intrusion.
    """
    DEFAULTS = Malware.DEFAULTS.copy()
    DEFAULTS['cvss_base'] = '4.3'


class MaliciousIP(IPVulnerability):
    """
    Malicious IP Detected.

    An IP was found that could contain output links to a malicious site or
    malware. This may be the result of a security intrusion, or a successful
    persistent XSS attack by a nefarious entity.

    You should review your website and ensure that your site was not
    compromised by a security intrusion.
    """
    DEFAULTS = Malware.DEFAULTS.copy()
    DEFAULTS['cvss_base'] = '5.8'


class MaliciousASN(Vulnerability):
    """
    Malicious ASN Detected.

    An Autonomous System Number (ASN) was found that could contain a malicious
    site or malware. This may be the result of a security intrusion, or a
    successful BGP reconfiguration attack by a nefarious entity.

    You should review your website and ensure that your site was not
    compromised by a security intrusion.
    """
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['cvss_base'] = '6.8'

    def __init__(self, asn, **kwargs):
        """
        :param asn: ASN where the vulnerability was found.
        :type asn: ASN

        """
        self.__asn_id = asn.identity
        super(MaliciousASN, self).__init__(**kwargs)
        self.add_information(asn)

    __init__.__doc__ += Vulnerability.__init__.__doc__

    @identity
    def asn_id(self):
        """
        :returns: Identity hash of the ASN
            where the vulnerability was found.
        :rtype: str
        """
        return self.__asn_id

    @property
    def asn(self):
        """
        :returns: ASN where the vulnerability was found.
        :rtype: ASN
        """
        return self.resolve(self.asn_id)