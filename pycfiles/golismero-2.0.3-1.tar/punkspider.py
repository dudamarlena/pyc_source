# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/punkspider.py
# Compiled at: 2013-12-22 12:03:03
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.url import Url
from golismero.api.data.vulnerability.injection.sql import SQLInjection
from golismero.api.data.vulnerability.injection.xss import XSS
from golismero.api.logger import Logger
from golismero.api.plugin import TestingPlugin
from golismero.api.text.text_utils import to_utf8
from golismero.api.net.web_utils import parse_url
import requests, traceback

class PunkSPIDER(TestingPlugin):
    """
    This plugin tries to perform passive reconnaissance on a target using
    the PunkSPIDER vulnerability lookup engine.
    """

    def get_accepted_info(self):
        return [
         Domain]

    def recv_info(self, info):
        host_id = info.hostname
        host_id = parse_url(host_id).hostname
        host_id = ('.').join(reversed(host_id.split('.')))
        d = self.query_punkspider(host_id)
        if not d:
            Logger.log('No results found for host: %s' % info.hostname)
            return
        results = []
        for v in d['data']:
            try:
                if v['protocol'] not in ('http', 'https'):
                    Logger.log_more_verbose('Skipped non-web vulnerability: %s' % to_utf8(v['id']))
                    continue
                if v['bugType'] not in ('xss', 'sqli', 'bsqli'):
                    Logger.log_more_verbose('Skipped unknown vulnerability type: %s' % to_utf8(v['bugType']))
                    continue
                url = to_utf8(v['vulnerabilityUrl'])
                param = to_utf8(v['parameter'])
                parsed = parse_url(url)
                payload = parsed.query_params[param]
                level = to_utf8(v['level'])
                url_o = Url(url)
                results.append(url_o)
                if v['bugType'] == 'xss':
                    clazz = XSS
                else:
                    clazz = SQLInjection
                vuln = clazz(url=url_o, vulnerable_params={param: payload}, injection_point=clazz.INJECTION_POINT_URL, injection_type=to_utf8(v['bugType']), level=level, tool_id=to_utf8(v['id']))
                results.append(vuln)
            except Exception as e:
                tb = traceback.format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

        count = int(len(results) / 2)
        if count == 0:
            Logger.log('No vulnerabilities found for host: ' + info.hostname)
        elif count == 1:
            Logger.log('Found one vulnerability for host: ' + info.hostname)
        else:
            Logger.log('Found %d vulnerabilities for host: %s' % (
             count, info.hostname))
        return results

    URL = 'http://punkspider.hyperiongray.com/service/search/detail/%s'
    HEADERS = {'Accept': '*/*', 
       'Referer': 'http://punkspider.hyperiongray.com/', 
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
       'X-Requested-With': 'XMLHttpRequest'}

    def query_punkspider(self, host_id):
        try:
            r = requests.get(self.URL % host_id, headers=self.HEADERS)
            assert r.headers['Content-Type'].startswith('application/json'), 'Response from server is not a JSON encoded object'
            return r.json()
        except requests.RequestException as e:
            Logger.log_error('Query to PunkSPIDER failed, reason: %s' % str(e))