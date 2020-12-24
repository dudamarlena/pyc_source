# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/output/base_integration.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 1817 bytes
import logging

class BaseIntegration(object):
    __doc__ = '\n    Base Class of all PhishMe Integration classes\n    '

    def __init__(self, config, product):
        """
        Initialize BaseIntegration class

        :param ConfigParser config: PhishMe Intelligence integration configuration
        :param str product: Name of integration (section name from configuration e.g. integration_mcafee_siem)
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.product = product
        self.logger.info('Initialized %s integration' % self.product)

    def process(self, mrti, threat_id):
        """
        Method stub for process; this will be overridden by child integration classes

        :param str mrti: PhishMe Intelligence Threat ID data
        :param int threat_id: PhishMe Intelligence threat id
        :return: None
        """
        pass

    def post_run(self, config_file_location):
        """
        Method stub for post_run; this will be overridden by child integration classes as needed

        :param str config_file_location: Path to configuration file
        :return: None
        """
        pass