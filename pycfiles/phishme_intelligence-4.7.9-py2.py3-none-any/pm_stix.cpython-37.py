# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/output/generic/pm_stix.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 2986 bytes
from __future__ import unicode_literals, absolute_import
import os, re, sys
import defusedxml.ElementTree as etree
from phishme_intelligence.output.generic.generic_integration import GenericIntegration

class PmStix(GenericIntegration):
    __doc__ = '\n    Class for generic processing of STIX 1.1.1 formatted PhishMe Intelligence data\n    '

    def _file_append(self, mrti):
        """
        Append STIX 1.1.1 formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in STIX 1.1.1 format
        :return: None
        """
        try:
            stix_xml = etree.fromstring(mrti.encode('utf-8'))
        except etree.XMLSyntaxError:
            self.logger.error('XML parse error of STIX package')
        else:
            with open(self.config.get(self.product, 'append_file_location'), 'ab+') as (file_handle):
                file_handle.write(mrti.encode('utf-8') + b'\n')

    def _file_write(self, mrti, threat_id):
        """
        Write STIX 1.1.1 formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in STIX 1.1.1 format
        :return: None
        """
        year_month_day = re.search('<indicator:Start_Time precision="second">(\\d{4}-\\d{2}-\\d{2})T', mrti).group(1)
        if self.config.getboolean(self.product, 'multiple_file_split_by_date'):
            current_path = os.path.join(self.config.get(self.product, 'multiple_file_location'), year_month_day)
        else:
            current_path = self.config.get(self.product, 'multiple_file_location')
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        cur_file = os.path.join(current_path, str(threat_id) + '.xml')
        try:
            stix_xml = etree.fromstring(mrti.encode('utf-8'))
        except etree.XMLSyntaxError:
            self.logger.error('XML parse error of STIX package for Threat ID: ' + threat_id + '.')
        else:
            with open(cur_file, 'wb+') as (file_handle):
                file_handle.write(mrti.encode('utf-8') + b'\n')