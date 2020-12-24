# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/core/syslog.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 1798 bytes
from __future__ import unicode_literals, absolute_import
import logging, sys, socket
PYTHON_MAJOR_VERSION = sys.version_info[0]

class Syslog(object):

    def __init__(self, config, product):
        """
        Initialize a Syslog object

        :param ConfigParser config: PhishMe Intelligence configuration
        :param product: Name of integration (section name from configuration e.g. integration_mcafee_siem)
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.product = product

    def send(self, mrti):
        """
        Send syslog message to configured endpoint

        :param str mrti: PhishMe intelligence to send via syslog

        :return: None
        """
        level = 5
        facility = 3
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '<%d>%s' % (level + facility * 8, mrti)
        temp_mrti = data.encode('utf-8')
        sock.sendto(temp_mrti, (self.config.get(self.product, 'host_without_protocol'), self.config.getint(self.product, 'port')))
        sock.close()