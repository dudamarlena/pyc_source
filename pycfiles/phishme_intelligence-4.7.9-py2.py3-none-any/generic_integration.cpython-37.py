# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/output/generic/generic_integration.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 1546 bytes
from __future__ import unicode_literals, absolute_import
from phishme_intelligence.output.base_integration import BaseIntegration

class GenericIntegration(BaseIntegration):
    __doc__ = '\n    Parent class for "generic" PhishMe Intelligence integrations; extends :class:`phishme_intelligence.output.base_integration.BaseIntegration`\n    '

    def process(self, mrti, threat_id):
        """
        Processing method for all generic integrations to handle either appending to a single file or writing multiple files

        :param str mrti: PhishMe Intelligence data used by
        :param int threat_id: Threat ID of PhishMe Intelligence being processed
        :return: None
        """
        if self.config.getboolean(self.product, 'append_file_use'):
            self._file_append(mrti)
        if self.config.getboolean(self.product, 'multiple_file_use'):
            self._file_write(mrti, threat_id)