# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/manifest/socket_msg.py
# Compiled at: 2016-06-13 14:11:03
"""
Use socket to transfer msg.
This file is never used. Instead by WSGI interfaces to add Agents.
"""
import socket, time, json
from vsm import flags
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

def _to_json_data(msg):
    """Check the message is already json format."""
    LOG.info('msg = %s' % msg)
    try:
        json.loads(msg)
        return msg
    except TypeError:
        return json.dumps(msg)


class SocketMessage(object):
    """This class is main used to send message."""

    def __init__(self, server_host, msg=None, socket_port=FLAGS.sockclient_port):
        self.port = socket_port
        self.protocol = socket.SOCK_STREAM
        self.family = socket.AF_INET
        self.data_size = 102400
        self.server_host = server_host
        self.send_data = _to_json_data(msg)

    def send(self, once=False):
        """Send the message until success."""
        LOG.info('Try to send the message = %s' % self.send_data)
        recive = None
        while recive is None and once == False:
            recive = self._send_and_rec_msg()
            time.sleep(1)

        LOG.info('Rec msg from vsm-api node, msg = %s' % recive)
        return recive

    def _send_and_rec_msg(self):
        """Try to connect and send the msg.

        If success, feed back the recived message.
        If failed, return None.

        If can not connect to server, we still try to
        connect and send the message.
        """
        try:
            sock = socket.socket(self.family, self.protocol)
        except socket.error:
            LOG.info('Failed to create socket!')
            return

        try:
            sock.connect((self.server_host, self.port))
            sock.send(self.send_data + '\n')
            res = sock.recv(self.data_size)
            sock.close()
            return res
        except socket.error:
            LOG.info('Can not to connect to socket!')
            return

        return