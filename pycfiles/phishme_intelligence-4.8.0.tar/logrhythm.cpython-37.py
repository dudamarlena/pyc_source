# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/logrhythm/logrhythm.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 2536 bytes
import logging, os
from phishme_intelligence.output.base_integration import BaseIntegration

class LogRhythm(BaseIntegration):

    def __init__(self, config, product):
        super(LogRhythm, self).__init__(config=config, product=product)
        self.logger = logging.getLogger(__name__)
        self.output_dir = self.config.get(self.product, 'output_dir')
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    @staticmethod
    def _file_write(ioc, file_path):
        """

        :param ioc:
        :param file_path:
        :return:
        """
        with open(file_path, 'ab+') as (file_handle):
            file_handle.write(ioc.encode('utf8') + '\n'.encode('utf8'))

    def process(self, mrti, threat_id):
        """

        :param mrti:
        :param threat_id:
        :return:
        """
        for item in mrti.block_set:
            file_name = 'phishme_intelligence_' + item.block_type + '_' + item.impact + '.txt'
            file_name = file_name.replace(' ', '').lower()
            destination_dir = os.path.join(self.output_dir, file_name)
            self._file_write(ioc=(item.watchlist_ioc), file_path=destination_dir)

        for item in mrti.subject_set:
            file_name = 'phishme_intelligence_subjects_none.txt'
            destination_dir = os.path.join(self.output_dir, file_name)
            self._file_write(ioc=(item.subject), file_path=destination_dir)

        for item in mrti.executable_set:
            file_name = 'phishme_intelligence_md5.txt'
            destination_dir = os.path.join(self.output_dir, file_name)
            self._file_write(ioc=(item.md5), file_path=destination_dir)