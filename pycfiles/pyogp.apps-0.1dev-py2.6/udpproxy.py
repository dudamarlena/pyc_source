# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/viewer_proxy/lib/udpproxy.py
# Compiled at: 2010-01-07 13:46:01
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
from logging import getLogger
import socket, traceback
from eventlet import api
from pyogp.lib.base.message.circuit import Host
from pyogp.lib.base.message.udpdispatcher import UDPDispatcher
from pyogp.lib.base.network.net import NetUDPClient
logger = getLogger('message.udpproxy')

class UDPProxy(UDPDispatcher):
    """ proxies a Second Life viewer's UDP connection to a region """

    def __init__(self, sim_ip, sim_port, viewer_facing_port, target_facing_port, udp_client=None, settings=None, message_handler=None, message_template=None, message_xml=None):
        """ initialize a UDP proxy, extending the UDPDispatcher """
        super(UDPProxy, self).__init__(udp_client, settings, message_handler, message_template, message_xml)
        self.settings.PROXY_LOGGING = True
        self.settings.ENABLE_DEFERRED_PACKET_PARSING = False
        self.target_host = Host((sim_ip, sim_port))
        self.local_host = None
        self.viewer_address = None
        self.target_udp_client = self.udp_client
        self.target_socket = self.socket
        self.target_socket.bind((socket.gethostname(), target_facing_port))
        self.target_socket.setblocking(0)
        self.proxy_udp_client = NetUDPClient()
        self.proxy_socket = self.proxy_udp_client.start_udp_connection()
        self.proxy_socket.bind((socket.gethostname(), viewer_facing_port))
        self.proxy_socket.setblocking(0)
        self.hostname = self.proxy_socket.getsockname()[0]
        self.local_host = Host((self.hostname, viewer_facing_port))
        logger.info('Initialized the UDPProxy for %s' % self.target_host)
        return

    def start_proxy(self):
        logger.debug('Starting proxies in UDPProxy')
        api.sleep(2)
        self._is_running = True
        api.spawn(self._send_viewer_to_sim)
        api.spawn(self._receive_sim_to_viewer)
        while self._is_running:
            api.sleep(0)

    def _send_viewer_to_sim(self):
        self.proxy_socket_is_locked = False
        while self._is_running:
            (msg_buf, msg_size) = self.proxy_udp_client.receive_packet(self.proxy_socket)
            if not self.viewer_address:
                self.viewer_address = self.proxy_udp_client.get_sender()
            if msg_size > 0:
                try:
                    recv_packet = self.receive_check(self.proxy_udp_client.get_sender(), msg_buf, msg_size)
                    logger.info('Sending message:%s ID:%s' % (recv_packet.name, recv_packet.packet_id))
                    logger.debug(recv_packet)
                except Exception, error:
                    logger.error('Problem handling viewer to sim proxy: %s.' % error)
                    traceback.print_exc()
                else:
                    self.target_udp_client.send_packet(self.target_socket, msg_buf, self.target_host)
            api.sleep(0)

    def _receive_sim_to_viewer(self):
        while self._is_running:
            (msg_buf, msg_size) = self.target_udp_client.receive_packet(self.target_socket)
            if msg_size > 0:
                try:
                    recv_packet = self.receive_check(self.target_udp_client.get_sender(), msg_buf, msg_size)
                    logger.info('Receiving message:%s ID:%s' % (recv_packet.name, recv_packet.packet_id))
                    logger.debug(recv_packet)
                except Exception, error:
                    logger.warning('Problem trying to handle sim to viewer proxy : %s' % error)
                    traceback.print_exc()
                else:
                    self.proxy_udp_client.send_packet(self.proxy_socket, msg_buf, self.viewer_address)
            api.sleep(0)