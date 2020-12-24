# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/output/generic/pm_cef.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 2695 bytes
from __future__ import unicode_literals, absolute_import
import os, re
from datetime import datetime
from phishme_intelligence.output.generic.generic_integration import GenericIntegration

class PmCef(GenericIntegration):
    __doc__ = '\n    Class for generic processing of CEF formatted PhishMe Intelligence data\n    '

    def _file_append(self, mrti):
        """
        Append CEF formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in CEF format
        :return: None
        """
        temp_mrti = mrti.encode('utf-8')
        with open(self.config.get(self.product, 'append_file_location'), 'ab+') as (file_handle):
            file_handle.write(temp_mrti + b'\n')

    def _file_write(self, mrti, threat_id):
        """
        Write CEF formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in CEF format
        :return: None
        """
        first_published = re.search('deviceCustomDate1=(\\d+)', mrti).group(1)
        year_month_day = datetime.fromtimestamp(int(first_published) / 1000.0).strftime('%Y-%m-%d')
        if self.config.getboolean(self.product, 'multiple_file_split_by_date'):
            current_path = os.path.join(self.config.get(self.product, 'multiple_file_location'), year_month_day)
        else:
            current_path = self.config.get(self.product, 'multiple_file_location')
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        cur_file = os.path.join(current_path, str(threat_id) + '.cef')
        temp_mrti = mrti.encode('utf-8')
        with open(cur_file, 'wb+') as (file_handle):
            file_handle.write(temp_mrti + b'\n')