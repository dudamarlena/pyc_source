# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/attack/sqlmap.py
# Compiled at: 2014-02-10 15:24:09
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
import shlex, re
from os.path import join
from time import time
from traceback import format_exc
from golismero.api.config import Config
from golismero.api.data.resource.url import Url
from golismero.api.data.vulnerability.injection.sql import SQLInjection
from golismero.api.external import run_external_tool, find_binary_in_path, tempdir, get_tools_folder
from golismero.api.logger import Logger
from golismero.api.net import ConnectionSlot
from golismero.api.net.web_utils import WEB_SERVERS_VARS
from golismero.api.plugin import TestingPlugin

class SQLMapTestingPlugin(TestingPlugin):

    def check_params(self):
        if not find_binary_in_path('sqlmap.py'):
            raise RuntimeError('SQLMap not found! You can download it from: http://sqlmap.org/')

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        if not info.has_url_params and not info.has_post_params:
            return
        results = []
        user_args = shlex.split(Config.plugin_args['args'])
        with tempdir() as (output_dir):
            args = [
             '-u',
             info.url,
             '--batch',
             '--output-dir',
             output_dir]
            args.extend(user_args)
            if info.has_url_params:
                args.extend([
                 '-p',
                 (',').join([ x for x in info.url_params if x not in WEB_SERVERS_VARS ])])
                r = self.make_injection(info.url, args)
                if r:
                    results.extend(self.parse_sqlmap_results(info, output_dir))
            if info.has_post_params:
                args.extend([
                 '--data',
                 ('&').join([ '%s=%s' % (k, v) for k, v in info.post_params.iteritems() if k not in WEB_SERVERS_VARS ])])
                r = self.make_injection(info.url, args)
                if r:
                    results.extend(self.parse_sqlmap_results(info, output_dir))
        if results:
            Logger.log('Found %s SQL injection vulnerabilities.' % len(results))
        else:
            Logger.log('No SQL injection vulnerabilities found.')
        return results

    def make_injection(self, target, args):
        """
        Run SQLMap against the given target.

        :param target: URL to scan.
        :type target: Url

        :param args: Arguments to pass to SQLMap.
        :type args: list(str)

        :return: True on success, False on failure.
        :rtype: bool
        """
        Logger.log('Launching SQLMap against: %s' % target)
        Logger.log_more_verbose('SQLMap arguments: %s' % (' ').join(args))
        sqlmap_script = join(get_tools_folder(), 'sqlmap', 'sqlmap.py')
        with ConnectionSlot(target):
            t1 = time()
            code = run_external_tool(sqlmap_script, args, callback=Logger.log_verbose)
            t2 = time()
        if code:
            Logger.log_error('SQLMap execution failed, status code: %d' % code)
            return False
        Logger.log('SQLMap scan finished in %s seconds for target: %s' % (
         t2 - t1, target))
        return True

    @staticmethod
    def parse_sqlmap_results(info, output_dir):
        """
        Convert the output of a SQLMap scan to the GoLismero data model.

        :param info: Data object to link all results to (optional).
        :type info: Url

        :param output_filename: Path to the output filename.
            The format should always be XML.
        :type output_filename:

        :returns: Results from the SQLMap scan.
        :rtype: list(Data)
        """
        results = []
        log_file = join(output_dir, info.parsed_url.host, 'log')
        try:
            with open(log_file, 'rU') as (f):
                text = f.read()
                m_banner = None
                m_backend = None
                m_technology = None
                tmp = []
                for t in text.split('---'):
                    l_injectable_place = re.search('(Place: )([a-zA-Z]+)', t)
                    if l_injectable_place:
                        l_inject_place = l_injectable_place.group(2)
                        l_inject_param = re.search('(Parameter: )([\\w\\_\\-]+)', t).group(2)
                        l_inject_type = re.search('(Type: )([\\w\\- ]+)', t).group(2)
                        l_inject_title = re.search('(Title: )([\\w\\- ]+)', t).group(2)
                        l_inject_payload = re.search('(Payload: )([\\w\\- =\\\'\\"\\%\\&\\$\\)\\(\\?\\¿\\*\\@\\!\\|\\/\\\\\\{\\}\\[\\]\\<\\>\\_\\:,;\\.]+)', t).group(2)
                        url = Url(info.url, method=l_inject_place, post_params=info.post_params, referer=info.referer)
                        v = SQLInjection(url, title='SQL Injection Vulnerability - ' + l_inject_title, vulnerable_params={l_inject_param: l_inject_payload}, injection_point=SQLInjection.str2injection_point(l_inject_place), injection_type=l_inject_type)
                        tmp.append(v)
                    if not m_banner:
                        m_banner = re.search('(banner:[\\s]*)(\')([\\w\\- =\'"\\%\\&\\$\\)\\(\\?\\¿\\*\\@\\!\\|\\/\\\\{\\}\\[\\]\\<\\>\\_\\.\\:,;]*)(\')', t)
                        if m_banner:
                            m_banner = m_banner.group(3)
                            m_backend = re.search('(back-end DBMS:[\\s]*)([\\w\\- =\'"\\%\\&\\$\\)\\(\\?\\¿\\*\\@\\!\\|\\/\\\\{\\}\\[\\]\\<\\>\\_\\.\\:,;]+)', t).group(2)
                            m_technology = re.search('(web application technology:[\\s]*)([\\w\\- =\'"\\%\\&\\$\\)\\(\\?\\¿\\*\\@\\!\\|\\/\\\\{\\}\\[\\]\\<\\>\\_\\.\\:,;]+)', t).group(2)

                for v in tmp:
                    if m_banner:
                        v.description = 'Banner: %s\n\n%s\n%s' % (m_backend, m_backend, m_technology)
                    results.append(v)

        except Exception as e:
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(format_exc())

        return results