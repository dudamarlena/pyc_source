# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/main/scope.py
# Compiled at: 2014-01-13 19:15:58
"""
Audit scope checking.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'AuditScope', 'DummyScope']
from ..api.data.resource.domain import Domain
from ..api.data.resource.ip import IP
from ..api.data.resource.url import Url
from ..api.net.dns import DNS
from ..api.net.web_utils import ParsedURL, split_hostname
from ..api.text.text_utils import to_utf8
from netaddr import IPAddress, IPNetwork
from warnings import warn
import re

class AbstractScope(object):

    def __init__(self, audit_config=None):
        """
        :param audit_config: (Optional) Audit configuration.
        :type audit_config: AuditConfig | None
        """
        raise NotImplementedError()

    @property
    def has_scope(self):
        raise NotImplementedError()

    @property
    def addresses(self):
        raise NotImplementedError()

    @property
    def domains(self):
        raise NotImplementedError()

    @property
    def roots(self):
        raise NotImplementedError()

    @property
    def web_pages(self):
        raise NotImplementedError()

    @property
    def targets(self):
        return self.addresses + self.domains + self.roots + self.web_pages

    def add_targets(self, audit_config, dns_resolution=1):
        """
        :param audit_config: Audit configuration.
        :type audit_config: AuditConfig

        :param dns_resolution: DNS resolution mode.
            Use 0 to disable, 1 to enable only for new targets (default),
            or 2 to enable for all targets.
        :type dns_resolution: int
        """
        raise NotImplementedError()

    def get_targets(self):
        """
        Get the audit targets as Data objects.

        :returns: Data objects.
        :rtype: list(Data)
        """
        result = []
        result.extend(IP(address) for address in self.addresses)
        result.extend(Domain(domain) for domain in self.domains)
        result.extend(Domain(root) for root in self.roots)
        result.extend(Url(url) for url in self.web_pages)
        return result

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return '<%s>' % self

    def __contains__(self, target):
        """
        Tests if the given target is included in the current audit scope.

        :param target: Target. May be an URL, a hostname or an IP address.
        :type target: str

        :returns: True if the target is in scope, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError()


class AuditScope(AbstractScope):
    """
    Audit scope.

    Example:

        >>> from golismero.api.config import Config
        >>> 'www.example.com' in Config.audit_scope
        True
        >>> 'www.google.com' in Config.audit_scope
        False
    """
    _re_is_domain = re.compile('^[A-Za-z0-9][A-Za-z0-9\\_\\-\\.]*[A-Za-z0-9]$')

    def __init__(self, audit_config=None):
        self.__domains = set()
        self.__roots = set()
        self.__addresses = set()
        self.__web_pages = set()
        if audit_config is not None:
            self.add_targets(audit_config)
        return

    @property
    def has_scope(self):
        return True

    @property
    def addresses(self):
        return sorted(self.__addresses)

    @property
    def domains(self):
        return sorted(self.__domains)

    @property
    def roots(self):
        return sorted(self.__roots)

    @property
    def web_pages(self):
        return sorted(self.__web_pages)

    def add_targets(self, audit_config, dns_resolution=1):
        if dns_resolution not in (0, 1, 2):
            raise ValueError("Argument 'dns_resolution' can only be 0, 1 or 2, got %r instead" % dns_resolution)
        include_subdomains = audit_config.include_subdomains
        new_domains = set()
        for target in audit_config.targets:
            target = to_utf8(target)
            try:
                if target.startswith('[') and target.endswith(']'):
                    IPAddress(target[1:-1], version=6)
                    address = target[1:-1]
                else:
                    IPAddress(target)
                    address = target
            except Exception:
                address = None

            if address is not None:
                self.__addresses.add(address)
            else:
                try:
                    network = IPNetwork(target)
                except Exception:
                    network = None

                if network is not None:
                    for address in network.iter_hosts():
                        address = str(address)
                        self.__addresses.add(address)

                elif self._re_is_domain.match(target):
                    target = target.lower()
                    if target not in self.__domains:
                        self.__domains.add(target)
                        new_domains.add(target)
                else:
                    try:
                        parsed_url = ParsedURL(target)
                        url = parsed_url.url
                    except Exception:
                        url = None

                    if url is not None:
                        self.__web_pages.add(url)
                        if audit_config.allow_parent:
                            self.__web_pages.add(parsed_url.base_url)
                        host = parsed_url.host
                        try:
                            if host.startswith('[') and host.endswith(']'):
                                IPAddress(host[1:-1], version=6)
                                host = host[1:-1]
                            else:
                                IPAddress(host)
                            self.__addresses.add(host)
                        except Exception:
                            host = host.lower()
                            if host not in self.__domains:
                                self.__domains.add(host)
                                new_domains.add(host)

                    else:
                        raise ValueError("I don't know what to do with this: %s" % target)

        if include_subdomains:
            for hostname in new_domains.copy():
                subdomain, domain, suffix = split_hostname(hostname)
                if subdomain:
                    prefix = ('.').join((domain, suffix))
                    for part in reversed(subdomain.split('.')):
                        if prefix not in self.__roots and prefix not in self.__domains:
                            new_domains.add(prefix)
                        self.__domains.add(prefix)
                        self.__roots.add(prefix)
                        prefix = ('.').join((part, prefix))

                else:
                    self.__roots.add(hostname)

        if dns_resolution:
            if dns_resolution == 1:
                domains_to_resolve = new_domains
            else:
                domains_to_resolve = self.__domains
            for domain in domains_to_resolve:
                resolved_4 = DNS.get_a(domain)
                for register in resolved_4:
                    self.__addresses.add(register.address)

                resolved_6 = DNS.get_aaaa(domain)
                for register in resolved_6:
                    self.__addresses.add(register.address)

                if not resolved_4 and not resolved_6:
                    msg = 'Cannot resolve domain name: %s' % domain
                    warn(msg, RuntimeWarning)

        return

    def __str__(self):
        result = [
         'Audit scope:\n']
        addresses = self.addresses
        if addresses:
            result.append('\nIP addresses:\n')
            for address in addresses:
                result.append('    %s\n' % address)

        domains = [ '*.' + domain for domain in self.roots ]
        domains.extend(self.domains)
        if domains:
            result.append('\nDomains:\n')
            for domain in domains:
                result.append('    %s\n' % domain)

        web_pages = self.web_pages
        if web_pages:
            result.append('\nWeb pages:\n')
            for url in web_pages:
                result.append('    %s\n' % url)

        return ('').join(result)

    def __contains__(self, target):
        if not target:
            return False
        else:
            if not isinstance(target, str):
                if not isinstance(target, unicode):
                    raise TypeError('Expected str, got %r instead' % type(target))
                target = to_utf8(target)
            original = target
            try:
                parsed_url = ParsedURL(target)
            except Exception:
                parsed_url = None

            if parsed_url is not None:
                if not parsed_url.scheme:
                    parsed_url = None
                else:
                    target = parsed_url.host
            try:
                if target.startswith('[') and target.endswith(']'):
                    IPAddress(target[1:-1], version=6)
                    address = target[1:-1]
                else:
                    IPAddress(target)
                    address = target
            except Exception:
                address = None

            if address is not None:
                in_scope = address in self.__addresses
            else:
                if self._re_is_domain.match(target):
                    target = target.lower()
                    in_scope = target in self.__domains or any(target.endswith('.' + domain) for domain in self.__roots)
                else:
                    warn("Can't determine if this is out of scope or not: %r" % original, stacklevel=2)
                    return False
                if in_scope:
                    if parsed_url is not None and parsed_url.scheme in ('http', 'https',
                                                                        'ftp'):
                        path = parsed_url.path
                        for base_url in self.__web_pages:
                            parsed_url = ParsedURL(base_url)
                            if path.startswith(parsed_url.path) and parsed_url.scheme in ('http',
                                                                                          'https',
                                                                                          'ftp'):
                                return True

                        return False
                    return True
            return False


class DummyScope(AbstractScope):
    """
    Dummy scope tells you everything is in scope, all the time.
    """

    def __init__(self):
        pass

    @property
    def has_scope(self):
        return False

    @property
    def addresses(self):
        return []

    @property
    def domains(self):
        return []

    @property
    def roots(self):
        return []

    @property
    def web_pages(self):
        return []

    def get_targets(self):
        return []

    def __contains__(self, target):
        return True

    def __str__(self):
        return 'Audit scope:\n\nIP addresses:\n    *\n\nDomains:\n    *\n\nWeb pages:\n    *\n'