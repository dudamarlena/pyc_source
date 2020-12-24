# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/output/generic/pm_json.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 2573 bytes
from __future__ import unicode_literals, absolute_import
import json, os
from datetime import datetime
from phishme_intelligence.output.generic.generic_integration import GenericIntegration

class PmJson(GenericIntegration):
    __doc__ = '\n    Class for generic processing of JSON formatted PhishMe Intelligence data\n    '

    def _file_append(self, mrti):
        """
        Append JSON formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in JSON format
        :return: None
        """
        with open(self.config.get(self.product, 'append_file_location'), 'a+') as (file_handle):
            file_handle.write(json.dumps((mrti.json), indent=4, sort_keys=True) + '\n')

    def _file_write(self, mrti, threat_id):
        """
        Write JSON formatted PhishMe Intelligence Threat ID information to a file.

        :param str mrti: PhishMe Intelligence in JSON format
        :return: None
        """
        year_month_day = datetime.fromtimestamp(mrti.first_published / 1000.0).strftime('%Y-%m-%d')
        if self.config.getboolean(self.product, 'multiple_file_split_by_date'):
            current_path = os.path.join(self.config.get(self.product, 'multiple_file_location'), year_month_day)
        else:
            current_path = self.config.get(self.product, 'multiple_file_location')
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        cur_file = os.path.join(current_path, str(threat_id) + '.json')
        with open(cur_file, 'w+') as (file_handle):
            file_handle.write(json.dumps((mrti.json), indent=4, sort_keys=True) + '\n')