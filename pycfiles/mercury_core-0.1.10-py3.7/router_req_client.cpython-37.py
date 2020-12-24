# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/clients/router_req_client.py
# Compiled at: 2018-06-15 15:32:47
# Size of source mod 2**32: 3961 bytes
import logging, msgpack, zmq
from mercury.common.exceptions import parse_exception, fancy_traceback_short, MercuryTransportError
log = logging.getLogger(__name__)

class RouterReqClient(object):
    service_name = 'Generic Service'

    def __init__(self, zmq_url, linger=-1, response_timeout=-1, rcv_retry=0, raise_on_timeout=False):
        """

        :param zmq_url:
        :param linger:
        :param response_timeout:
        :param rcv_retry: The number of times to retry
        """
        self.zmq_url = zmq_url
        self.linger = linger
        self.response_timeout = response_timeout
        self.rcv_retry = rcv_retry
        self.raise_on_timeout = raise_on_timeout
        self.context = zmq.Context()
        self.socket = None
        log.debug('[{}] Creating connection to {}'.format(self.service_name, self.zmq_url))
        self.refresh_socket()

    def refresh_socket(self):
        """
        Creates a new socket if socket is None or the socket is closed
        :return:
        """
        if not self.socket or self.socket.closed:
            self.socket = self.context.socket(zmq.REQ)
            if self.response_timeout < 0:
                timeout = -1
            else:
                timeout = self.response_timeout * 1000
            self.socket.setsockopt(zmq.LINGER, self.linger)
            self.socket.setsockopt(zmq.RCVTIMEO, timeout)
            self.socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
            self.socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 120)
            self.socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 3)
            self.socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 10)
            self.socket.connect(self.zmq_url)

    def safe_send(self, data):
        """
        Ensures that the socket is alive by calling refresh_socket
        :return:
        """
        self.refresh_socket()
        packed = msgpack.packb(data)
        self.socket.send_multipart([packed])

    def safe_receive(self):
        """
        Receive server reply.
        :return: The unpacked message
        """
        retry_count = self.rcv_retry and self.rcv_retry + 1 or 1
        while retry_count:
            try:
                return msgpack.unpackb((self.socket.recv()), encoding='utf-8')
            except zmq.Again:
                retry_count -= 1
                log.error(f"[{self.service_name}] Receive timeout Retries remaining: {retry_count}")
            except Exception:
                log.error(f"An unhandled exception occurred while receiving <{fancy_traceback_short(parse_exception())}>")
                break

        error_message = f"[{self.service_name}] Failure receiving server reply. Closing socket to reset state."
        log.error(error_message)
        self.close()
        if self.raise_on_timeout:
            raise MercuryTransportError(error_message)
        return {'error':True,  'message':error_message}

    def transceiver(self, payload):
        """
        Convenience method
        :param payload:
        :return:
        """
        self.safe_send(payload)
        return self.safe_receive()

    def close(self):
        """ close the socket """
        self.socket.close()