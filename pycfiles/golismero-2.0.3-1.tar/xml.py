# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/report/xml.py
# Compiled at: 2014-01-09 06:32:52
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'XMLOutput']
from golismero.api.audit import get_audit_times, parse_audit_times
from golismero.api.config import Config
from golismero.api.data import Data
from golismero.api.data.db import Database
from golismero.api.logger import Logger
from golismero.api.plugin import ReportPlugin
from datetime import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

try:
    from cPickle import dumps
except ImportError:
    from pickle import dumps

class XMLOutput(ReportPlugin):
    """
    Dumps the output in XML format.
    """
    EXTENSION = '.xml'

    def generate_report(self, output_file):
        Logger.log_verbose('Writing audit results to file: %s' % output_file)
        self.__full_report = not Config.audit_config.only_vulns
        report_time = '%s UTC' % datetime.utcnow()
        start_time, stop_time = get_audit_times()
        start_time, stop_time, run_time = parse_audit_times(start_time, stop_time)
        xml = ET.Element('golismero')
        xml.set('audit_name', Config.audit_name)
        if start_time:
            xml.set('start_time', start_time)
        if stop_time:
            xml.set('stop_time', stop_time)
        if run_time:
            xml.set('run_time', run_time)
        xml.set('report_time', report_time)
        xml.set('report_type', 'full' if self.__full_report else 'brief')
        xml_scope = ET.SubElement(xml, 'audit_scope')
        for address in Config.audit_scope.addresses:
            xml_ip = ET.SubElement(xml_scope, 'address')
            xml_ip.text = address

        for root_domain in Config.audit_scope.roots:
            xml_root = ET.SubElement(xml_scope, 'root_domain')
            xml_root.text = root_domain

        for domain in Config.audit_scope.domains:
            xml_domain = ET.SubElement(xml_scope, 'domain')
            xml_domain.text = domain

        for web_page in Config.audit_scope.web_pages:
            xml_web = ET.SubElement(xml_scope, 'web_page')
            xml_web.text = web_page

        datas = self.__collect_vulns(False)
        if datas or self.__full_report:
            fp = self.__collect_vulns(True)
            self.__fp = set(fp)
            try:
                if datas:
                    xml_vulns = ET.SubElement(xml, 'vulnerabilities')
                    self.__add_to_xml(xml_vulns, datas, Data.TYPE_VULNERABILITY, 'vulnerability')
                self.__vulnerable = set()
                try:
                    datas = self.__collect_data(Data.TYPE_RESOURCE)
                    if datas:
                        xml_res = ET.SubElement(xml, 'resources')
                        self.__add_to_xml(xml_res, datas, Data.TYPE_RESOURCE, 'resource')
                    datas = self.__collect_data(Data.TYPE_INFORMATION)
                    if datas:
                        xml_info = ET.SubElement(xml, 'informations')
                        self.__add_to_xml(xml_info, datas, Data.TYPE_INFORMATION, 'information')
                finally:
                    self.__vulnerable.clear()

            finally:
                self.__fp.clear()

            if self.__full_report and fp:
                xml_fp = ET.SubElement(xml, 'false_positives')
                self.__add_to_xml(xml_fp, fp, Data.TYPE_VULNERABILITY, 'vulnerability')
        tree = ET.ElementTree(xml)
        tree.write(output_file, encoding='utf-8')
        self.launch_command(output_file)

    def __iterate_data(self, identities=None, data_type=None, data_subtype=None):
        if identities is None:
            identities = list(Database.keys(data_type))
        if identities:
            for page in xrange(0, len(identities), 100):
                for data in Database.get_many(identities[page:page + 100], data_type):
                    yield data

        return

    def __collect_data(self, data_type):
        if self.__full_report:
            datas = [ data.identity for data in self.__iterate_data(data_type=data_type)
                    ]
        else:
            datas = [ data.identity for data in self.__iterate_data(data_type=data_type) if data.identity in self.__vulnerable
                    ]
        datas.sort()
        return datas

    def __collect_vulns(self, fp_filter):
        vulns = [ vuln.identity for vuln in self.__iterate_data(data_type=Data.TYPE_VULNERABILITY) if bool(vuln.false_positive) == fp_filter
                ]
        vulns.sort()
        return vulns

    def __add_to_xml(self, parent, datas, data_type, tag):
        for data in self.__iterate_data(datas, data_type):
            elem = ET.SubElement(parent, tag)
            for name, value in data.to_dict().iteritems():
                if value is None:
                    continue
                if isinstance(value, unicode):
                    if name.startswith('raw_'):
                        value = value.encode('utf-8').encode('base64')
                    else:
                        try:
                            value = value.encode('ascii')
                        except Exception:
                            value = value.encode('utf-8').encode('base64')

                elif isinstance(value, str):
                    if name.startswith('raw_'):
                        value = value.encode('base64')
                    else:
                        try:
                            value = str(value.decode('ascii'))
                        except Exception:
                            value = value.encode('base64')

                elif type(value) in (bool, int, float):
                    value = str(value)
                else:
                    value = dumps(value, protocol=0).encode('base64')
                elem.set(name, value)

        return