# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/remote_logging.py
# Compiled at: 2018-02-22 23:42:49
# Size of source mod 2**32: 1205 bytes
import logging
from mercury.common.exceptions import MercuryGeneralException
from mercury.common.clients.router_req_client import RouterReqClient
LOG = logging.getLogger('')

class MercuryLogHandler(logging.Handler):

    def __init__(self, service_url, mercury_id=None):
        super(MercuryLogHandler, self).__init__()
        self.service_url = service_url
        self._MercuryLogHandler__mercury_id = mercury_id
        self.client = RouterReqClient((self.service_url), linger=0, response_timeout=2)
        self.service_name = 'Logging Service'

    def emit(self, record):
        if not self._MercuryLogHandler__mercury_id:
            return
        data = record.__dict__
        data.update({'mercury_id': self._MercuryLogHandler__mercury_id})
        err_msg = 'There is a problem with the remote logging service!'
        try:
            try:
                response = self.client.transceiver(data)
            except Exception:
                logging.error(err_msg)
            else:
                if response.get('error'):
                    logging.error(err_msg)
        finally:
            self.client.close()

    def set_mercury_id(self, mercury_id):
        self._MercuryLogHandler__mercury_id = mercury_id