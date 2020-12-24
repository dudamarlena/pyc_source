# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/qradar_siem/qradar_siem.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 4559 bytes
from __future__ import unicode_literals
import sys, json
from phishme_intelligence.output.base_integration import BaseIntegration
PYTHON_MAJOR_VERSION = sys.version_info[0]

class QRadarSiem(BaseIntegration):

    def write_file(self, indicator_json, indicator_type):
        output_dir = self.config.get(self.product, 'json_output_dir')
        try:
            with open(output_dir + '%s.json' % indicator_type, 'a') as (indicator_file):
                indicator_file.write(json.dumps(indicator_json) + '\n')
        except OSError as e:
            try:
                self.logger.error('Could not write indicator file to %s: %s' % (output_dir, e))
            finally:
                e = None
                del e

    def process(self, mrti, threat_id):
        """

        :param mrti:
        :param threat_id:
        :return:
        """
        self.logger.info('Processing Threat ID: %s' % threat_id)
        self.logger.info('Building Collection Data for %s' % threat_id)
        threathq_url = mrti.threathq_url
        active_threat_report_url = mrti.active_threat_report
        brand = mrti.brand
        first_published = mrti.first_published
        last_published = mrti.last_published
        self.logger.info('Writing %s indicators to JSON files' % threat_id)
        for artifact in mrti.executable_set:
            md5 = {artifact.md5: {'Identifier':threat_id,  'First Seen Date':first_published, 
                            'Last Seen Date':last_published, 
                            'Malware Family':artifact.malware_family, 
                            'Threat Details':threathq_url, 
                            'Active Threat Report':active_threat_report_url, 
                            'Brand':brand, 
                            'Infrastructure Type':artifact.type, 
                            'Provider':'Cofense Intelligence'}}
            sha256 = {artifact.sha256: {'Identifier':threat_id,  'First Seen Date':first_published, 
                               'Last Seen Date':last_published, 
                               'Malware Family':artifact.malware_family, 
                               'Threat Details':threathq_url, 
                               'Active Threat Report':active_threat_report_url, 
                               'Brand':brand, 
                               'Infrastructure Type':artifact.type, 
                               'Provider':'Cofense Intelligence'}}
            self.write_file(md5, 'MD5')
            self.write_file(sha256, 'SHA256')

        for ioc in mrti.block_set:
            indicator = {ioc.watchlist_ioc: {'Identifier':threat_id,  'Impact Rating':ioc.impact, 
                                 'First Seen Date':first_published, 
                                 'Last Seen Date':last_published, 
                                 'Malware Family':ioc.malware_family, 
                                 'Threat Details':threathq_url, 
                                 'Active Threat Report':active_threat_report_url, 
                                 'Brand':brand, 
                                 'Infrastructure Type':ioc.role, 
                                 'Provider':'Cofense Intelligence'}}
            if ioc.block_type == 'URL':
                self.write_file(indicator, 'URL')
            if ioc.block_type == 'IPv4 Address':
                self.write_file(indicator, 'IPv4')
            if ioc.block_type == 'Domain Name':
                self.write_file(indicator, 'Hostname')