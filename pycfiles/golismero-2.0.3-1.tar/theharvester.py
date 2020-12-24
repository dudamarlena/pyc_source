# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/theharvester.py
# Compiled at: 2014-01-14 18:58:51
"""
Integration with `theHarvester <https://code.google.com/p/theharvester/>`_.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data import discard_data
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.email import Email
from golismero.api.data.resource.ip import IP
from golismero.api.external import get_tools_folder
from golismero.api.logger import Logger
from golismero.api.plugin import TestingPlugin
import os, os.path, socket, StringIO, sys, traceback, warnings
cwd = os.path.abspath(get_tools_folder())
cwd = os.path.join(cwd, 'theHarvester')
sys.path.insert(0, cwd)
try:
    import discovery
    from discovery import *
finally:
    sys.path.remove(cwd)

del cwd

class HarvesterPlugin(TestingPlugin):
    """
    Integration with `theHarvester <https://code.google.com/p/theharvester/>`_.
    """
    SUPPORTED = ('google', 'bing', 'pgp')

    def get_accepted_info(self):
        return [
         Domain]

    def recv_info(self, info):
        word = info.hostname
        limit = 100
        try:
            limit = int(Config.plugin_config.get('limit', str(limit)), 0)
        except ValueError:
            pass

        total = float(len(self.SUPPORTED))
        all_emails, all_hosts = set(), set()
        for step, engine in enumerate(self.SUPPORTED):
            try:
                Logger.log_verbose('Searching keyword %r in %s' % (word, engine))
                self.update_status(progress=float(step * 80) / total)
                emails, hosts = self.search(engine, word, limit)
            except Exception as e:
                t = traceback.format_exc()
                Logger.log_error(str(e))
                Logger.log_error_more_verbose(t)
                continue

            all_emails.update(address.lower() for address in emails if address)
            all_hosts.update(name.lower() for name in hosts if name)

        self.update_status(progress=80)
        Logger.log_more_verbose('Search complete for keyword %r' % word)
        results = []
        emails_found = set()
        for address in all_emails:
            if '...' in address:
                continue
            while address and not address[0].isalnum():
                address = address[1:]

            while address and not address[(-1)].isalnum():
                address = address[:-1]

            if not address:
                continue
            if '@' not in address:
                continue
            if address in emails_found:
                continue
            emails_found.add(address)
            try:
                data = Email(address)
            except Exception as e:
                warnings.warn('Cannot parse email address: %r' % address)
                continue

            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                in_scope = data.is_in_scope()
            if in_scope:
                data.add_resource(info)
                results.append(data)
                all_hosts.add(data.hostname)
            else:
                Logger.log_more_verbose('Email address out of scope: %s' % address)
                discard_data(data)

        visited = set()
        total = float(len(all_hosts))
        for step, name in enumerate(all_hosts):
            while name and not name[0].isalnum():
                name = name[1:]

            while name and not name[(-1)].isalnum():
                name = name[:-1]

            if not name:
                continue
            visited.add(name)
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                in_scope = name in Config.audit_scope
            if not in_scope:
                Logger.log_more_verbose('Hostname out of scope: %s' % name)
                continue
            try:
                self.update_status(progress=float(step * 20) / total + 80.0)
                Logger.log_more_verbose('Checking hostname: %s' % name)
                real_name, aliaslist, addresslist = socket.gethostbyname_ex(name)
            except socket.error:
                continue

            all_names = set()
            all_names.add(name)
            all_names.add(real_name)
            all_names.update(aliaslist)
            for name in all_names:
                if name and name not in visited:
                    visited.add(name)
                    with warnings.catch_warnings():
                        warnings.filterwarnings('ignore')
                        in_scope = name in Config.audit_scope
                    if not in_scope:
                        Logger.log_more_verbose('Hostname out of scope: %s' % name)
                        continue
                    data = Domain(name)
                    data.add_resource(info)
                    results.append(data)
                    for ip in addresslist:
                        with warnings.catch_warnings():
                            warnings.filterwarnings('ignore')
                            in_scope = ip in Config.audit_scope
                        if not in_scope:
                            Logger.log_more_verbose('IP address out of scope: %s' % ip)
                            continue
                        d = IP(ip)
                        data.add_resource(d)
                        results.append(d)

        text = 'Found %d emails and %d hostnames for keyword %r'
        text = text % (len(all_emails), len(all_hosts), word)
        if len(all_emails) + len(all_hosts) > 0:
            Logger.log(text)
        else:
            Logger.log_verbose(text)
        return results

    @staticmethod
    def search(engine, word, limit=100):
        """
        Run a theHarvester search on the given engine.

        :param engine: Search engine.
        :type engine: str

        :param word: Word to search for.
        :type word: str

        :param limit: Maximum number of results.
            Its exact meaning may depend on the search engine.
        :type limit: int

        :returns: All email addresses, hostnames and usernames collected.
        :rtype: tuple(list(str), list(str), list(str))
        """
        Logger.log_more_verbose('Searching on: %s' % engine)
        if engine == 'pgp':

            def search_fn(word, limit, start):
                return discovery.pgpsearch.search_pgp(word)

        else:
            search_mod = getattr(discovery, '%ssearch' % engine)
            search_fn = getattr(search_mod, 'search_%s' % engine)
        fd = StringIO.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = fd, fd
            search = search_fn(word, limit, 0)
            if engine == 'bing':
                search.process('no')
            else:
                search.process()
        finally:
            sys.stdout, sys.stderr = old_out, old_err

        emails, hosts = [], []
        if hasattr(search, 'get_emails'):
            try:
                emails = search.get_emails()
            except Exception as e:
                t = traceback.format_exc()
                Logger.log_error(str(e))
                Logger.log_error_more_verbose(t)

        if hasattr(search, 'get_hostnames'):
            try:
                hosts = search.get_hostnames()
            except Exception as e:
                t = traceback.format_exc()
                Logger.log_error(str(e))
                Logger.log_error_more_verbose(t)

        Logger.log_verbose('Found %d emails and %d hostnames on %s for domain %s' % (
         len(emails), len(hosts), engine, word))
        return (
         emails, hosts)