# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/scan/brute_dns.py
# Compiled at: 2014-01-14 18:58:51
"""
This plugin tries to find hidden subdomains.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data.resource.domain import Domain
from golismero.api.text.text_utils import generate_random_string
from golismero.api.logger import Logger
from golismero.api.net.dns import DNS
from golismero.api.plugin import TestingPlugin
from golismero.api.text.wordlist import WordListLoader, WordlistNotFound
from golismero.api.data.vulnerability.information_disclosure.domain_disclosure import DomainDisclosure

class DNSBruteforcer(TestingPlugin):

    def get_accepted_info(self):
        return [
         Domain]

    def recv_info(self, info):
        root = info.root
        if root == 'localhost':
            return
        else:
            if self.state.put(root, True):
                return
            try:
                wordlist = WordListLoader.get_advanced_wordlist_as_list(Config.plugin_args['wordlist'])
            except WordlistNotFound:
                Logger.log_error_verbose("Wordlist '%s' not found.." % Config.plugin_args['wordlist'])
                return
            except TypeError:
                Logger.log_error_verbose("Wordlist '%s' is not a file." % Config.plugin_args['wordlist'])
                return

            try:
                whitelist = WordListLoader.get_advanced_wordlist_as_list(Config.plugin_config['wordlist'])
            except WordlistNotFound:
                Logger.log_error_verbose("Wordlist '%s' not found.." % Config.plugin_config['wordlist'])
                return
            except TypeError:
                Logger.log_error_verbose("Wordlist '%s' is not a file." % Config.plugin_config['wordlist'])
                return

            m_virtual_domains = []
            for v in (generate_random_string(40) for x in xrange(3)):
                l_subdomain = ('.').join((v, root))
                records = DNS.get_a(l_subdomain, also_CNAME=True)
                for rec in records:
                    if rec.type == 'CNAME':
                        m_virtual_domains.append(rec.target)

            m_base_domain = None
            if len(set(m_virtual_domains)) == 1:
                m_base_domain = m_virtual_domains[0]
            self.progress.set_total(len(wordlist))
            self.progress.min_delta = 1
            found = 0
            results = []
            visited = set()
            for prefix in wordlist:
                self.progress.add_completed()
                name = ('.').join((prefix, root))
                if name not in Config.audit_scope:
                    continue
                records = DNS.get_a(name, also_CNAME=True)
                records.extend(DNS.get_aaaa(name, also_CNAME=True))
                if not records:
                    continue
                chk = [ True for x in records if x.type == 'CNAME' and x.target == m_base_domain ]
                if len(chk) > 0 and all(chk):
                    continue
                found += 1
                Logger.log_more_verbose('Subdomain found: %s' % name)
                domain = Domain(name)
                results.append(domain)
                if prefix not in whitelist:
                    d = DomainDisclosure(name, risk=0, level='low', title='Possible subdomain leak', description='A subdomain was discovered which may be an unwanted information disclosure.')
                    d.add_resource(domain)
                    results.append(d)
                for rec in records:
                    if rec.type == 'CNAME':
                        location = rec.target
                    elif rec.type in ('A', 'AAAA'):
                        location = rec.address
                    else:
                        results.append(rec)
                        domain.add_information(rec)
                        continue
                    if location not in visited:
                        visited.add(location)
                        results.append(rec)
                        domain.add_information(rec)

            if found:
                Logger.log('Found %d subdomains for root domain: %s' % (
                 found, root))
            else:
                Logger.log_verbose('No subdomains found for root domain: %s' % root)
            return results