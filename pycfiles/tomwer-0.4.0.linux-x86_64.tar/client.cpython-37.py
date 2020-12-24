# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/web/client.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 3416 bytes
"""module defining functions and class to communicate a status to the
orange-server.
The orange-server is used to display the advancement of the workflow.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '28/04/2017'
try:
    import graypy
    has_graypy = True
except:
    has_graypy = False

from .config import grayport_port, grayport_host
import os, socket, logging
_logger = logging.getLogger(__name__)
_INFO_UNKNOWN_HOST_NAME = False

class OWClient(object):
    __doc__ = 'Orange widget Client can emit information about his advancement\n    '
    WORKFLOW_INFO = 'workflow'
    SCAN_INFO = 'scan'

    def __init__(self, loggers):
        global _INFO_UNKNOWN_HOST_NAME
        assert loggers is not None
        if OWClient._knows_hostname(hostname=grayport_host) is False:
            if _INFO_UNKNOWN_HOST_NAME is False:
                _logger.warning('unknow host %s' % grayport_host)
                _INFO_UNKNOWN_HOST_NAME = True
            return
        if type(loggers) not in (list, tuple):
            loggers = (
             loggers,)
        for logger in loggers:
            if os.environ.get('ORANGE_WEB_LOG', 'True') is 'True':
                try:
                    self.graylogHandler = graypy.GELFHandler(grayport_host, grayport_port)
                except:
                    logger.error("Fail to create GELFHandler. Won't report log message")
                else:
                    logger.addHandler(self.graylogHandler)
                    logger.debug('- add graypy handler')
            else:
                info = 'No log will be send to graylog.'
                info += 'ORANGE_WEB_LOG variable is setted to False'
                logger.debug(info)

    @staticmethod
    def _knows_hostname(hostname):
        if hostname is None:
            return False
        try:
            socket.gethostbyname(hostname)
            return True
        except socket.error:
            return False