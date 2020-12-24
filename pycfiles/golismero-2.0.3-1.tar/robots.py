# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/robots.py
# Compiled at: 2013-12-09 06:41:16
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.data import discard_data
from golismero.api.config import Config
from golismero.api.data.resource.url import BaseUrl, Url
from golismero.api.logger import Logger
from golismero.api.net import NetworkException, NetworkOutOfScope
from golismero.api.net.http import HTTP
from golismero.api.net.web_utils import download, generate_error_page_url, fix_url, urljoin
from golismero.api.plugin import TestingPlugin
from golismero.api.text.matching_analyzer import MatchingAnalyzer
from golismero.api.data.vulnerability.suspicious.url import SuspiciousURL
import codecs

class Robots(TestingPlugin):
    """
    This plugin analyzes robots.txt files looking for private pages.
    """

    def get_accepted_info(self):
        return [
         BaseUrl]

    def check_download(self, url, name, content_length, content_type):
        return content_type and content_type.strip().lower().split(';')[0] == 'text/plain'

    def check_response(self, request, url, status_code, content_length, content_type):
        return content_type and content_type.strip().lower().startswith('text/')

    def recv_info(self, info):
        m_return = []
        m_url = info.url
        m_hostname = info.hostname
        m_url_robots_txt = urljoin(m_url, 'robots.txt')
        p = None
        try:
            msg = 'Looking for robots.txt in: %s' % m_hostname
            Logger.log_more_verbose(msg)
            p = download(m_url_robots_txt, self.check_download)
        except NetworkOutOfScope:
            Logger.log_more_verbose('URL out of scope: %s' % m_url_robots_txt)
            return
        except Exception as e:
            Logger.log_more_verbose('Error while processing %r: %s' % (m_url_robots_txt, str(e)))
            return

        if not p:
            Logger.log_more_verbose('No robots.txt found.')
            return
        else:
            u = Url(m_url_robots_txt, referer=m_url)
            p.add_resource(u)
            m_return.append(u)
            m_return.append(p)
            m_robots_text = p.raw_data
            try:
                if m_robots_text.startswith(codecs.BOM_UTF8):
                    m_robots_text = m_robots_text.decode('utf-8').lstrip(unicode(codecs.BOM_UTF8, 'utf-8'))
                elif m_robots_text.startswith(codecs.BOM_UTF16):
                    m_robots_text = m_robots_text.decode('utf-16')
            except UnicodeDecodeError:
                Logger.log_error_verbose('Error while parsing robots.txt: Unicode format error.')
                return

            m_discovered_suspicious = []
            m_discovered_urls = []
            m_discovered_urls_append = m_discovered_urls.append
            tmp_discovered = None
            m_lines = m_robots_text.splitlines()
            m_lines_count = len(m_lines)
            m_total = float(m_lines_count)
            for m_step, m_line in enumerate(m_lines):
                m_octothorpe = m_line.find('#')
                if m_octothorpe >= 0:
                    m_line = m_line[:m_octothorpe]
                m_line = m_line.rstrip()
                if not m_line or ':' not in m_line:
                    continue
                try:
                    m_key, m_value = m_line.split(':', 1)
                    m_key = m_key.strip().lower()
                    m_value = m_value.strip()
                    if '*' in m_value:
                        continue
                    if m_key in ('disallow', 'allow', 'sitemap') and m_value:
                        tmp_discovered = urljoin(m_url, m_value)
                        m_discovered_urls_append(tmp_discovered)
                        if m_key.lower() == 'disallow':
                            m_discovered_suspicious.append(tmp_discovered)
                except Exception as e:
                    continue

            m_discovered_urls = set(m_discovered_urls)
            m_error_page = generate_error_page_url(m_url_robots_txt)
            m_response_error_page = HTTP.get_url(m_error_page, callback=self.check_response)
            if m_response_error_page:
                m_return.append(m_response_error_page)
                match = {}
                m_analyzer = MatchingAnalyzer(m_response_error_page.data)
                m_total = len(m_discovered_urls)
                for m_step, l_url in enumerate(m_discovered_urls):
                    if m_step % 2:
                        progress = float(m_step * 100) / m_total
                        self.update_status(progress=progress)
                    l_url = fix_url(l_url, m_url)
                    if l_url in Config.audit_scope:
                        l_p = None
                        try:
                            l_p = HTTP.get_url(l_url, callback=self.check_response)
                        except:
                            if l_p:
                                discard_data(l_p)
                            continue

                        if l_p:
                            if m_analyzer.analyze(l_p.data, url=l_url):
                                match[l_url] = l_p
                            else:
                                discard_data(l_p)

                for i in m_analyzer.unique_texts:
                    l_url = i.url
                    l_p = match.pop(l_url)
                    m_result = Url(l_url, referer=m_url)
                    m_result.add_information(l_p)
                    m_return.append(m_result)
                    m_return.append(l_p)
                    if l_url in m_discovered_suspicious:
                        v = SuspiciousURL(m_result, title='Suspicious URL found un robots.txt', risk=1, severity=0, level='low', description='An URLs was found in Disallow tag of robots.txt. It can contain confidential content or some information leak.', tool_id='robots')
                        v.add_resource(info)
                        m_return.append(v)

                map(discard_data, match.values())
            else:
                m_total = len(m_discovered_urls)
                for m_step, l_url in enumerate(m_discovered_urls):
                    if m_step % 2:
                        progress = float(m_step * 100) / m_total
                        self.update_status(progress=progress)
                    l_url = fix_url(l_url, m_url)
                    try:
                        l_p = HTTP.get_url(l_url, callback=self.check_response)
                    except NetworkOutOfScope:
                        continue
                    except NetworkException:
                        continue

                    if l_p:
                        m_result = Url(l_url, referer=m_url)
                        m_result.add_information(l_p)
                        m_return.append(m_result)
                        m_return.append(l_p)

            if m_return:
                Logger.log_more_verbose('Discovered %s URLs.' % len(m_return))
            else:
                Logger.log_more_verbose('No URLs discovered.')
            return m_return