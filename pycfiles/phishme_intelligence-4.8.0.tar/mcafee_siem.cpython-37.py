# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/mcafee_siem/mcafee_siem.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 1439 bytes
import logging, sys
from phishme_intelligence.output.base_integration import BaseIntegration
from phishme_intelligence.core.syslog import Syslog
PYTHON_MAJOR_VERSION = sys.version_info[0]

class McAfeeSiem(BaseIntegration):

    def __init__(self, config, product):
        super(McAfeeSiem, self).__init__(config=config, product=product)
        self.logger = logging.getLogger(__name__)
        self.syslog = Syslog(config=config, product=product)

    def process(self, mrti, threat_id):
        """

        :param mrti:
        :param threat_id:
        :return:
        """
        self.syslog.send(mrti=mrti)