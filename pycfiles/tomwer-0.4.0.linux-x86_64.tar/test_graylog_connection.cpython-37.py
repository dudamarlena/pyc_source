# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/web/test/test_graylog_connection.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2123 bytes
""" Not a unit test but send a simple test message error to gray log"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
from tomwer.web.client import OWClient
import logging
logger = logging.getLogger(__name__)

class TestGrayLog(OWClient):

    def __init__(self):
        OWClient.__init__(self, logger)

    def sendErrorMessage(self):
        logger.error('test error message')

    def sendwarningMessage(self):
        logger.warning('test warning message')

    def sendInfoMessage(self):
        logger.info('test info message')

    def sendProcessEndedMessage(self):
        logger.processEnded('test processEnded message')


if __name__ == '__main__':
    c = TestGrayLog()
    c.sendErrorMessage()
    c.sendwarningMessage()
    c.sendInfoMessage()
    c.sendProcessEndedMessage()