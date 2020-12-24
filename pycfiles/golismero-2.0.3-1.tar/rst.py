# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/report/rst.py
# Compiled at: 2014-01-09 06:32:52
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'RSTReport']
from golismero.api.audit import get_audit_times, parse_audit_times
from golismero.api.config import Config
from golismero.api.data import Data
from golismero.api.data.db import Database
from golismero.api.logger import Logger
from golismero.api.net.web_utils import parse_url
from golismero.api.plugin import ReportPlugin
from golismero.api.text.text_utils import hexdump, to_utf8
from collections import defaultdict
from datetime import datetime
from pprint import pformat
from textwrap import wrap
import re

class RSTReport(ReportPlugin):
    """
    Creates reports in reStructured Text format.
    """
    EXTENSION = '.rst'

    def generate_report(self, output_file):
        Logger.log_verbose('Writing reStructured text report to file: %s' % output_file)
        with open(output_file, 'w') as (f):
            self.write_report_to_open_file(f)
        self.launch_command(output_file)

    def write_report_to_open_file(self, f):
        """
        Write the report into the given open file.

        :param f: Open file.
        :type f: file
        """
        self.__full_report = not Config.audit_config.only_vulns
        print >> f, 'GoLismero Report'
        print >> f, '================'
        print >> f, ''
        print >> f, '.. title:: %s - GoLismero' % self.__format_rst(Config.audit_name)
        print >> f, ''
        print >> f, '.. footer:: Report generation date: %s UTC' % datetime.utcnow()
        print >> f, ''
        print >> f, '.. contents:: Table of Contents'
        print >> f, '   :depth: 3'
        print >> f, '   :backlinks: top'
        print >> f, ''
        start_time, stop_time, run_time = parse_audit_times(*get_audit_times())
        print >> f, 'Summary'
        print >> f, '-------'
        print >> f, ''
        print >> f, '- Audit name: ' + self.__format_rst(Config.audit_name)
        print >> f, '- Start date: ' + start_time
        print >> f, '- End date: ' + stop_time
        print >> f, '- Execution time: ' + run_time
        print >> f, '- Report type: ' + ('Full' if self.__full_report else 'Brief')
        print >> f, ''
        print >> f, 'Audit Scope'
        print >> f, '-----------'
        print >> f, ''
        print >> f, '- IP Addresses: '
        for address in Config.audit_scope.addresses:
            print >> f, '  + ' + self.__format_rst(address)

        print >> f, '- Domains:'
        scope_domains = [ '*.' + r for r in Config.audit_scope.roots ]
        scope_domains.extend(Config.audit_scope.domains)
        for domain in scope_domains:
            print >> f, '  + ' + self.__format_rst(domain)

        print >> f, '- Web Pages:'
        for url in Config.audit_scope.web_pages:
            print >> f, '  + ' + self.__format_rst(url)

        print >> f, ''
        datas = self.__collect_vulns(False)
        if not datas and not self.__full_report:
            print >> f, 'No vulnerabilities found.'
            print >> f, ''
            return
        fp = self.__collect_vulns(True)
        self.__fp = set()
        for ids in fp.itervalues():
            self.__fp.update(ids)

        try:
            self.__vulnerable = set()
            if datas:
                self.__write_rst(f, datas, Data.TYPE_VULNERABILITY, 'Vulnerabilities')
            try:
                datas = self.__collect_data(Data.TYPE_RESOURCE)
                if datas:
                    self.__write_rst(f, datas, Data.TYPE_RESOURCE, 'Resources' if self.__full_report else 'Assets')
                datas = self.__collect_data(Data.TYPE_INFORMATION)
                if datas:
                    self.__write_rst(f, datas, Data.TYPE_INFORMATION, 'Informations' if self.__full_report else 'Evidences')
            finally:
                self.__vulnerable.clear()

        finally:
            self.__fp.clear()

        if self.__full_report and fp:
            self.__write_rst(f, fp, Data.TYPE_VULNERABILITY, 'False Positives')

    def __iterate_data(self, identities=None, data_type=None, data_subtype=None):
        if identities is None:
            identities = list(Database.keys(data_type))
        if identities:
            for page in xrange(0, len(identities), 100):
                for data in Database.get_many(identities[page:page + 100], data_type):
                    yield data

        return

    __re_escape_rst = re.compile('(%s)' % ('|').join('\\' + x for x in '*:,."!-/\';~?@[]<>|+^=_\\'))
    __re_unindent = re.compile('^( +)', re.M)

    def __escape_rst(self, s):
        if not isinstance(s, basestring):
            s = str(s)
        s = s.replace('\t', '        ')
        s = s.replace('\r\n', '\n')
        s = s.replace('\r', '\n')
        s = self.__re_unindent.sub('', s)
        try:
            u = parse_url(s)
        except Exception:
            u = None

        if u is not None and u.scheme in ('http', 'https', 'ftp', 'mailto'):
            s = '`%s <%s>`_' % (self.__re_escape_rst.sub('\\\\\\1', s), u.url)
        else:
            s = self.__re_escape_rst.sub('\\\\\\1', s)
        return s

    def __format_rst(self, obj, hyperlinks=False, width=70):
        if hyperlinks:
            return ('\n').join('`ID: %s`_' % x for x in obj)
        if isinstance(obj, basestring):
            obj = str(obj)
            if any(ord(c) > 127 for c in obj):
                obj = hexdump(obj)
            elif width:
                obj = ('\n').join(wrap(obj, width, replace_whitespace=False, expand_tabs=False, drop_whitespace=False))
            return self.__escape_rst(obj)
        if (isinstance(obj, list) or isinstance(obj, tuple)) and all(isinstance(x, basestring) for x in obj):
            return ('\n').join('- ' + self.__escape_rst(to_utf8(x) if isinstance(x, basestring) else pformat(x)) for x in obj)
        if isinstance(obj, dict):
            return ('\n').join(self.__escape_rst('%s: %s' % (k, v)) for k, v in obj.iteritems())
        try:
            text = str(obj)
        except Exception:
            text = pformat(obj)

        return self.__escape_rst(text)

    def __collect_data(self, data_type):
        datas = defaultdict(list)
        if self.__full_report:
            for data in self.__iterate_data(data_type=data_type):
                datas[data.display_name].append(data.identity)

        else:
            for data in self.__iterate_data(data_type=data_type):
                if data.identity in self.__vulnerable:
                    datas[data.display_name].append(data.identity)

            for x in datas.itervalues():
                x.sort()

        return datas

    def __collect_vulns(self, fp_filter):
        vulns = defaultdict(list)
        for vuln in self.__iterate_data(data_type=Data.TYPE_VULNERABILITY):
            if bool(vuln.false_positive) == fp_filter:
                vulns[vuln.display_name].append(vuln.identity)

        for x in vulns.itervalues():
            x.sort()

        return vulns

    def __write_rst(self, f, datas, data_type, header):
        titles = datas.keys()
        titles.sort()
        if 'Uncategorized Vulnerability' in titles:
            titles.remove('Uncategorized Vulnerability')
            titles.append('Uncategorized Vulnerability')
        print >> f, header
        print >> f, '-' * len(header)
        print >> f, ''
        for title in titles:
            print >> f, title
            print >> f, '+' * len(title)
            print >> f, ''
            show_ruler = False
            for data in self.__iterate_data(datas[title], data_type):
                if show_ruler:
                    print >> f, '----'
                    print >> f, ''
                show_ruler = True
                data_title = 'ID: %s' % data.identity
                print >> f, data_title
                print >> f, '^' * len(data_title)
                print >> f, ''
                property_groups = defaultdict(dict)
                property_groups.update(data.display_properties)
                linked_info = data.get_links(Data.TYPE_INFORMATION)
                linked_res = data.get_links(Data.TYPE_RESOURCE)
                linked_vuln = data.get_links(Data.TYPE_VULNERABILITY)
                if self.__fp:
                    linked_fp = linked_vuln.intersection(self.__fp)
                    linked_vuln.difference_update(linked_fp)
                else:
                    linked_fp = set()
                if self.__full_report:
                    if linked_info:
                        property_groups['Graph Links']['Informations'] = sorted(linked_info)
                    if linked_res:
                        property_groups['Graph Links']['Resources'] = sorted(linked_res)
                    if linked_vuln:
                        property_groups['Graph Links']['Vulnerabilities'] = sorted(linked_vuln)
                    if linked_fp:
                        property_groups['Graph Links']['False Positives'] = sorted(linked_fp)
                else:
                    if data_type == Data.TYPE_VULNERABILITY:
                        if linked_info:
                            self.__vulnerable.update(linked_info)
                            property_groups['Graph Links']['Evidences'] = sorted(linked_info)
                        if linked_res:
                            self.__vulnerable.update(linked_res)
                            property_groups['Graph Links']['Assets'] = sorted(linked_res)
                        if linked_vuln:
                            property_groups['Graph Links']['Related'] = sorted(linked_vuln)
                    elif linked_vuln:
                        property_groups['Graph Links']['Vulnerabilities'] = sorted(linked_vuln)
                    groups = property_groups.keys()
                    groups.sort()
                    if '[DEFAULT]' in groups:
                        groups.remove('[DEFAULT]')
                        groups.insert(0, '[DEFAULT]')
                    for group in groups:
                        properties = property_groups[group]
                        hyperlinks = group == 'Graph Links'
                        properties = {key:self.__format_rst(value, hyperlinks).split('\n') for key, value in properties.iteritems() if value}
                        for key, value in properties.items():
                            if key.endswith(' ID') and len(value) == 1 and len(value[0]) == 32 and value[0].isalnum():
                                del properties[key]

                        if not properties:
                            continue
                        names = properties.keys()
                        names.sort()
                        if group == 'Description':
                            if 'References' in names:
                                names.remove('References')
                                names.append('References')
                            if 'Title' in names:
                                names.remove('Title')
                                names.insert(0, 'Title')
                        else:
                            if group == '[DEFAULT]':
                                if 'Category' in names:
                                    names.remove('Category')
                                    names.insert(0, 'Category')
                                if 'Level' in names:
                                    names.remove('Level')
                                    names.insert(0, 'Level')
                            h_names = 'Property name'
                            if names:
                                w_names = max(len(x) for x in names)
                                w_names = max(w_names, len(h_names))
                            else:
                                w_names = len(h_names)
                            h_values = 'Property value'
                            w_values = len(h_values)
                            for v in properties.itervalues():
                                for x in v:
                                    w_values = max(w_values, len(x))

                            if group != '[DEFAULT]':
                                print >> f, group
                                print >> f, '*' * len(group)
                                print >> f, ''
                            fmt = '| %%-%ds | %%-%ds |' % (w_names, w_values)
                            separator = '+-%s-+-%s-+' % ('-' * w_names, '-' * w_values)
                            print >> f, separator
                            print >> f, fmt % (h_names, h_values)
                            print >> f, separator.replace('-', '=')
                            for name in names:
                                lines = properties[name]
                                print >> f, fmt % (name, lines.pop(0))
                                for x in lines:
                                    print >> f, fmt % ('', x)

                                print >> f, separator

                        print >> f, ''