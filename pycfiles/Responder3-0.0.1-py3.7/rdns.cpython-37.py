# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\core\rdns.py
# Compiled at: 2019-06-20 05:39:07
# Size of source mod 2**32: 2218 bytes
import ipaddress
from responder3.protocols.DNS import *
from responder3.core.udpwrapper import UDPClient
import os

class RDNS:

    def __init__(self, server, server6):
        self.server = server
        self.server6 = server6

    async def resolve(self, ip):
        try:
            ip = ipaddress.ip_address(ip).reverse_pointer
            tid = os.urandom(2)
            question = DNSQuestion.construct(ip, (DNSType.PTR), (DNSClass.IN), qu=False)
            if self.server[0]['proto'].upper() == 'TCP':
                packet = DNSPacket.construct(TID=tid,
                  flags=(DNSFlags.RD),
                  response=(DNSResponse.REQUEST),
                  opcode=(DNSOpcode.QUERY),
                  rcode=(DNSResponseCode.NOERR),
                  questions=[
                 question],
                  proto=(socket.SOCK_STREAM))
                reader, writer = await asyncio.open_connection(self.server[0]['ip'], self.server[0]['port'])
                writer.write(packet.to_bytes())
                await writer.drain()
                data = await DNSPacket.from_streamreader(reader, proto=(socket.SOCK_STREAM))
                if data.Rcode == DNSResponseCode.NOERR:
                    if len(data.Answers) > 0:
                        return str(data.Answers[0].domainname)
                return 'NA'
                return str(data.Answers[0].domainname)
            cli = UDPClient((self.server[0]['ip'], self.server[0]['port']))
            packet = DNSPacket.construct(TID=tid,
              flags=(DNSFlags.RD),
              response=(DNSResponse.REQUEST),
              opcode=(DNSOpcode.QUERY),
              rcode=(DNSResponseCode.NOERR),
              questions=[
             question],
              proto=(socket.SOCK_DGRAM))
            reader, writer = await cli.run(packet.to_bytes())
            data = await DNSPacket.from_streamreader(reader)
            if data.Rcode == DNSResponseCode.NOERR:
                if len(data.Answers) > 0:
                    return str(data.Answers[0].domainname)
            return 'NA'
        except Exception as e:
            try:
                import traceback
                traceback.print_exc()
                return
            finally:
                e = None
                del e