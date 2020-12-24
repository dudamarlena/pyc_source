# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/Base.py
# Compiled at: 2013-12-09 06:41:17
"""
$Id: Base.py,v 1.12.2.4 2007/05/22 20:28:31 customdesigned Exp $

This file is part of the pydns project.
Homepage: http://pydns.sourceforge.net

This code is covered by the standard Python License.

    Base functionality. Request and Response classes, that sort of thing.
"""
import socket, string, types, time, Type, Class, Opcode, asyncore

class DNSError(Exception):
    pass


defaults = {'protocol': 'udp', 'port': 53, 'opcode': Opcode.QUERY, 'qtype': Type.A, 
   'rd': 1, 'timing': 1, 'timeout': 30}
defaults['server'] = []

def ParseResolvConf(resolv_path):
    global defaults
    try:
        lines = open(resolv_path).readlines()
    except:
        print 'error in path' + resolv_path

    for line in lines:
        line = string.strip(line)
        if not line or line[0] == ';' or line[0] == '#':
            continue
        fields = string.split(line)
        if len(fields) < 2:
            continue
        if fields[0] == 'domain' and len(fields) > 1:
            defaults['domain'] = fields[1]
        if fields[0] == 'search':
            pass
        if fields[0] == 'options':
            pass
        if fields[0] == 'sortlist':
            pass
        if fields[0] == 'nameserver':
            defaults['server'].append(fields[1])


def DiscoverNameServers():
    import sys
    if sys.platform in ('win32', 'nt'):
        import win32dns
        defaults['server'] = win32dns.RegistryResolve()
    else:
        return ParseResolvConf()


class DnsRequest:
    """ high level Request object """

    def __init__(self, *name, **args):
        self.donefunc = None
        self.async = None
        self.defaults = {}
        self.argparse(name, args)
        self.defaults = self.args
        return

    def argparse(self, name, args):
        if not name and self.defaults.has_key('name'):
            args['name'] = self.defaults['name']
        if type(name) is types.StringType:
            args['name'] = name
        else:
            if len(name) == 1:
                if name[0]:
                    args['name'] = name[0]
            for i in defaults.keys():
                if not args.has_key(i):
                    if self.defaults.has_key(i):
                        args[i] = self.defaults[i]
                    else:
                        args[i] = defaults[i]

        if type(args['server']) == types.StringType:
            args['server'] = [
             args['server']]
        self.args = args

    def socketInit(self, a, b):
        self.s = socket.socket(a, b)

    def processUDPReply(self):
        import time, select
        if self.args['timeout'] > 0:
            r, w, e = select.select([self.s], [], [], self.args['timeout'])
            if not len(r):
                raise DNSError, 'Timeout'
        self.reply = self.s.recv(1024)
        self.time_finish = time.time()
        self.args['server'] = self.ns
        return self.processReply()

    def processTCPReply(self):
        import time, Lib
        self.f = self.s.makefile('r')
        header = self.f.read(2)
        if len(header) < 2:
            raise DNSError, 'EOF'
        count = Lib.unpack16bit(header)
        self.reply = self.f.read(count)
        if len(self.reply) != count:
            raise DNSError, 'incomplete reply'
        self.time_finish = time.time()
        self.args['server'] = self.ns
        return self.processReply()

    def processReply(self):
        import Lib
        self.args['elapsed'] = (self.time_finish - self.time_start) * 1000
        u = Lib.Munpacker(self.reply)
        r = Lib.DnsResult(u, self.args)
        r.args = self.args
        return r

    def conn(self):
        self.s.connect((self.ns, self.port))

    def req(self, *name, **args):
        """ needs a refactoring """
        import time, Lib
        self.argparse(name, args)
        protocol = self.args['protocol']
        self.port = self.args['port']
        opcode = self.args['opcode']
        rd = self.args['rd']
        server = self.args['server']
        if type(self.args['qtype']) == types.StringType:
            try:
                qtype = getattr(Type, string.upper(self.args['qtype']))
            except AttributeError:
                raise DNSError, 'unknown query type'

        else:
            qtype = self.args['qtype']
        if not self.args.has_key('name'):
            print self.args
            raise DNSError, 'nothing to lookup'
        qname = self.args['name']
        if qtype == Type.AXFR:
            print 'Query type AXFR, protocol forced to TCP'
            protocol = 'tcp'
        m = Lib.Mpacker()
        m.addHeader(0, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
        m.addQuestion(qname, qtype, Class.IN)
        self.request = m.getbuf()
        try:
            if protocol == 'udp':
                self.sendUDPRequest(server)
            else:
                self.sendTCPRequest(server)
        except socket.error as reason:
            raise DNSError, reason

        if self.async:
            return
        else:
            return self.response
            return

    def sendUDPRequest(self, server):
        """refactor me"""
        self.response = None
        self.socketInit(socket.AF_INET, socket.SOCK_DGRAM)
        for self.ns in server:
            try:
                self.conn()
                self.time_start = time.time()
                if not self.async:
                    self.s.send(self.request)
                    self.response = self.processUDPReply()
            except None:
                continue

            break

        if not self.response:
            if not self.async:
                raise DNSError, 'no working nameservers found'
        return

    def sendTCPRequest(self, server):
        """ do the work of sending a TCP request """
        import time, Lib
        self.response = None
        for self.ns in server:
            try:
                self.socketInit(socket.AF_INET, socket.SOCK_STREAM)
                self.time_start = time.time()
                self.conn()
                self.s.send(Lib.pack16bit(len(self.request)) + self.request)
                self.s.shutdown(1)
                self.response = self.processTCPReply()
            except socket.error:
                continue

            break

        if not self.response:
            raise DNSError, 'no working nameservers found'
        return


class DnsAsyncRequest(DnsRequest, asyncore.dispatcher_with_send):
    """ an asynchronous request object. out of date, probably broken """

    def __init__(self, *name, **args):
        DnsRequest.__init__(self, *name, **args)
        if args.has_key('done') and args['done']:
            self.donefunc = args['done']
        else:
            self.donefunc = self.showResult
        self.async = 1

    def conn(self):
        import time
        self.connect((self.ns, self.port))
        self.time_start = time.time()
        if self.args.has_key('start') and self.args['start']:
            asyncore.dispatcher.go(self)

    def socketInit(self, a, b):
        self.create_socket(a, b)
        asyncore.dispatcher.__init__(self)
        self.s = self

    def handle_read(self):
        if self.args['protocol'] == 'udp':
            self.response = self.processUDPReply()
            if self.donefunc:
                apply(self.donefunc, (self,))

    def handle_connect(self):
        self.send(self.request)

    def handle_write(self):
        pass

    def showResult(self, *s):
        self.response.show()