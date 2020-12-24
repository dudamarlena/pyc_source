# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/scan/zone_transfer.py
# Compiled at: 2013-12-02 13:49:15
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.ip import IP
from golismero.api.data.vulnerability.information_disclosure.dns_zone_transfer import DNSZoneTransfer
from golismero.api.logger import Logger
from golismero.api.net.dns import DNS
from golismero.api.plugin import TestingPlugin

class DNSZoneTransferPlugin(TestingPlugin):

    def get_accepted_info(self):
        return [
         Domain]

    def recv_info(self, info):
        root = info.root
        if root == 'localhost':
            return
        if root not in Config.audit_scope:
            return
        if self.state.put(root, True):
            return
        ns_servers, resolv = DNS.zone_transfer(root, ns_allowed_zone_transfer=True)
        if not resolv:
            Logger.log_verbose('DNS zone transfer failed, server %r not vulnerable' % root)
            return
        domain = Domain(root)
        for r in resolv:
            map(domain.add_information, r)

        results = []
        results.append(domain)
        msg = 'DNS zone transfer successful, '
        if len(ns_servers) > 1:
            msg += '%d nameservers for %r are vulnerable!'
            msg %= (len(ns_servers), root)
        else:
            msg += 'nameserver for %r is vulnerable!' % root
        Logger.log(msg)
        if not ns_servers:
            vulnerability = DNSZoneTransfer(root)
            vulnerability.add_resource(domain)
            results.append(vulnerability)
        else:
            for ns in ns_servers:
                vulnerability = DNSZoneTransfer(ns)
                try:
                    resource = IP(ns)
                except ValueError:
                    resource = Domain(ns)

                domain.add_resource(resource)
                vulnerability.add_resource(resource)
                results.append(resource)
                results.append(vulnerability)

        return results