# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vxi11/rpc.py
# Compiled at: 2017-01-18 12:58:14
"""
Sun RPC version 2 -- RFC1057

This file is drawn from Python's RPC demo, updated for python 3.  There
doesn't seem to be an original author or license associated the original
file.

XXX There should be separate exceptions for the various reasons why
XXX an RPC can fail, rather than using RuntimeError for everything

XXX Need to use class based exceptions rather than string exceptions

XXX The UDP version of the protocol resends requests when it does
XXX not receive a timely reply -- use only for idempotent calls!

XXX There is no provision for call timeout on TCP connections

Original source: http://svn.python.org/projects/python/trunk/Demo/rpc/rpc.py

"""
import xdrlib, socket, os, struct
RPCVERSION = 2
CALL = 0
REPLY = 1
AUTH_NULL = 0
AUTH_UNIX = 1
AUTH_SHORT = 2
AUTH_DES = 3
MSG_ACCEPTED = 0
MSG_DENIED = 1
SUCCESS = 0
PROG_UNAVAIL = 1
PROG_MISMATCH = 2
PROC_UNAVAIL = 3
GARBAGE_ARGS = 4
RPC_MISMATCH = 0
AUTH_ERROR = 1
AUTH_BADCRED = 1
AUTH_REJECTEDCRED = 2
AUTH_BADVERF = 3
AUTH_REJECTEDVERF = 4
AUTH_TOOWEAK = 5

class RPCError(Exception):
    pass


class RPCBadFormat(RPCError):
    pass


class RPCBadVersion(RPCError):
    pass


class RPCGarbageArgs(RPCError):
    pass


class RPCUnpackError(RPCError):
    pass


def make_auth_null():
    return ''


class Packer(xdrlib.Packer):

    def pack_auth(self, auth):
        flavor, stuff = auth
        self.pack_enum(flavor)
        self.pack_opaque(stuff)

    def pack_auth_unix(self, stamp, machinename, uid, gid, gids):
        self.pack_uint(stamp)
        self.pack_string(machinename)
        self.pack_uint(uid)
        self.pack_uint(gid)
        self.pack_uint(len(gids))
        for i in gids:
            self.pack_uint(i)

    def pack_callheader(self, xid, prog, vers, proc, cred, verf):
        self.pack_uint(xid)
        self.pack_enum(CALL)
        self.pack_uint(RPCVERSION)
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(proc)
        self.pack_auth(cred)
        self.pack_auth(verf)

    def pack_replyheader(self, xid, verf):
        self.pack_uint(xid)
        self.pack_enum(REPLY)
        self.pack_uint(MSG_ACCEPTED)
        self.pack_auth(verf)
        self.pack_enum(SUCCESS)


class Unpacker(xdrlib.Unpacker):

    def unpack_auth(self):
        flavor = self.unpack_enum()
        stuff = self.unpack_opaque()
        return (flavor, stuff)

    def unpack_callheader(self):
        xid = self.unpack_uint()
        temp = self.unpack_enum()
        if temp != CALL:
            raise RPCBadFormat('no CALL but %r' % (temp,))
        temp = self.unpack_uint()
        if temp != RPCVERSION:
            raise RPCBadVersion('bad RPC version %r' % (temp,))
        prog = self.unpack_uint()
        vers = self.unpack_uint()
        proc = self.unpack_uint()
        cred = self.unpack_auth()
        verf = self.unpack_auth()
        return (xid, prog, vers, proc, cred, verf)

    def unpack_replyheader(self):
        xid = self.unpack_uint()
        mtype = self.unpack_enum()
        if mtype != REPLY:
            raise RPCUnpackError('no REPLY but %r' % (mtype,))
        stat = self.unpack_enum()
        if stat == MSG_DENIED:
            stat = self.unpack_enum()
            if stat == RPC_MISMATCH:
                low = self.unpack_uint()
                high = self.unpack_uint()
                raise RPCUnpackError('MSG_DENIED: RPC_MISMATCH: %r' % ((low, high),))
            if stat == AUTH_ERROR:
                stat = self.unpack_uint()
                raise RPCUnpackError('MSG_DENIED: AUTH_ERROR: %r' % (stat,))
            raise RPCUnpackError('MSG_DENIED: %r' % (stat,))
        if stat != MSG_ACCEPTED:
            raise RPCUnpackError('Neither MSG_DENIED nor MSG_ACCEPTED: %r' % (stat,))
        verf = self.unpack_auth()
        stat = self.unpack_enum()
        if stat == PROG_UNAVAIL:
            raise RPCUnpackError('call failed: PROG_UNAVAIL')
        if stat == PROG_MISMATCH:
            low = self.unpack_uint()
            high = self.unpack_uint()
            raise RPCUnpackError('call failed: PROG_MISMATCH: %r' % ((low, high),))
        if stat == PROC_UNAVAIL:
            raise RPCUnpackError('call failed: PROC_UNAVAIL')
        if stat == GARBAGE_ARGS:
            raise RPCGarbageArgs
        if stat != SUCCESS:
            raise RPCUnpackError('call failed: %r' % (stat,))
        return (
         xid, verf)


class Client:

    def __init__(self, host, prog, vers, port):
        self.host = host
        self.prog = prog
        self.vers = vers
        self.port = port
        self.lastxid = 0
        self.cred = None
        self.verf = None
        return

    def make_call(self, proc, args, pack_func, unpack_func):
        if pack_func is None and args is not None:
            raise TypeError('non-null args with null pack_func')
        self.start_call(proc)
        if pack_func:
            pack_func(args)
        self.do_call()
        if unpack_func:
            result = unpack_func()
        else:
            result = None
        self.unpacker.done()
        return result

    def start_call(self, proc):
        self.lastxid = xid = self.lastxid + 1
        cred = self.mkcred()
        verf = self.mkverf()
        p = self.packer
        p.reset()
        p.pack_callheader(xid, self.prog, self.vers, proc, cred, verf)

    def do_call(self):
        raise RPCError('do_call not defined')

    def mkcred(self):
        if self.cred is None:
            self.cred = (
             AUTH_NULL, make_auth_null())
        return self.cred

    def mkverf(self):
        if self.verf is None:
            self.verf = (
             AUTH_NULL, make_auth_null())
        return self.verf

    def call_0(self):
        return self.make_call(0, None, None, None)


def sendfrag(sock, last, frag):
    x = len(frag)
    if last:
        x = x | 2147483648
    header = struct.pack('>I', x)
    sock.sendall(header + frag)


def sendrecord(sock, record):
    if len(record) > 0:
        sendfrag(sock, 1, record)


def recvfrag(sock):
    header = sock.recv(4)
    if len(header) < 4:
        raise EOFError
    x = struct.unpack('>I', header[0:4])[0]
    last = x & 2147483648 != 0
    n = int(x & 2147483647)
    frag = ''
    while n > 0:
        buf = sock.recv(n)
        if not buf:
            raise EOFError
        n = n - len(buf)
        frag = frag + buf

    return (
     last, frag)


def recvrecord(sock):
    record = ''
    last = 0
    while not last:
        last, frag = recvfrag(sock)
        record = record + frag

    return record


class RawTCPClient(Client):

    def __init__(self, host, prog, vers, port):
        Client.__init__(self, host, prog, vers, port)
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        self.sock.close()

    def do_call(self):
        call = self.packer.get_buf()
        sendrecord(self.sock, call)
        while True:
            reply = recvrecord(self.sock)
            u = self.unpacker
            u.reset(reply)
            xid, verf = u.unpack_replyheader()
            if xid == self.lastxid:
                return
            if xid < self.lastxid:
                continue
            else:
                raise RPCError('wrong xid in reply %r instead of %r' % (xid, self.lastxid))


class RawUDPClient(Client):

    def __init__(self, host, prog, vers, port):
        Client.__init__(self, host, prog, vers, port)
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        self.sock.close()

    def do_call(self):
        call = self.packer.get_buf()
        self.sock.send(call)
        try:
            from select import select
        except ImportError:
            print 'WARNING: select not found, RPC may hang'
            select = None

        BUFSIZE = 8192
        timeout = 1
        count = 5
        while 1:
            r, w, x = [
             self.sock], [], []
            if select:
                r, w, x = select(r, w, x, timeout)
            if self.sock not in r:
                count = count - 1
                if count < 0:
                    raise RPCError('timeout')
                if timeout < 25:
                    timeout = timeout * 2
                self.sock.send(call)
                continue
            reply = self.sock.recv(BUFSIZE)
            u = self.unpacker
            u.reset(reply)
            xid, verf = u.unpack_replyheader()
            if xid != self.lastxid:
                continue
            break

        return


class RawBroadcastUDPClient(RawUDPClient):

    def __init__(self, bcastaddr, prog, vers, port):
        RawUDPClient.__init__(self, bcastaddr, prog, vers, port)
        self.reply_handler = None
        self.timeout = 30
        return

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def set_reply_handler(self, reply_handler):
        self.reply_handler = reply_handler

    def set_timeout(self, timeout):
        self.timeout = timeout

    def make_call(self, proc, args, pack_func, unpack_func):
        if pack_func is None and args is not None:
            raise TypeError('non-null args with null pack_func')
        self.start_call(proc)
        if pack_func:
            pack_func(args)
        call = self.packer.get_buf()
        self.sock.sendto(call, (self.host, self.port))
        try:
            from select import select
        except ImportError:
            print 'WARNING: select not found, broadcast will hang'
            select = None

        BUFSIZE = 8192
        replies = []
        if unpack_func is None:

            def dummy():
                pass

            unpack_func = dummy
        while 1:
            r, w, x = [
             self.sock], [], []
            if select:
                if self.timeout is None:
                    r, w, x = select(r, w, x)
                else:
                    r, w, x = select(r, w, x, self.timeout)
            if self.sock not in r:
                break
            reply, fromaddr = self.sock.recvfrom(BUFSIZE)
            u = self.unpacker
            u.reset(reply)
            xid, verf = u.unpack_replyheader()
            if xid != self.lastxid:
                continue
            reply = unpack_func()
            self.unpacker.done()
            replies.append((reply, fromaddr))
            if self.reply_handler:
                self.reply_handler(reply, fromaddr)

        return replies


PMAP_PROG = 100000
PMAP_VERS = 2
PMAP_PORT = 111
PMAPPROC_NULL = 0
PMAPPROC_SET = 1
PMAPPROC_UNSET = 2
PMAPPROC_GETPORT = 3
PMAPPROC_DUMP = 4
PMAPPROC_CALLIT = 5
IPPROTO_TCP = 6
IPPROTO_UDP = 17

class PortMapperPacker(Packer):

    def pack_mapping(self, mapping):
        prog, vers, prot, port = mapping
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(prot)
        self.pack_uint(port)

    def pack_pmaplist(self, list):
        self.pack_list(list, self.pack_mapping)

    def pack_call_args(self, ca):
        prog, vers, proc, args = ca
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(proc)
        self.pack_opaque(args)


class PortMapperUnpacker(Unpacker):

    def unpack_mapping(self):
        prog = self.unpack_uint()
        vers = self.unpack_uint()
        prot = self.unpack_uint()
        port = self.unpack_uint()
        return (prog, vers, prot, port)

    def unpack_pmaplist(self):
        return self.unpack_list(self.unpack_mapping)

    def unpack_call_result(self):
        port = self.unpack_uint()
        res = self.unpack_opaque()
        return (port, res)


class PartialPortMapperClient:

    def __init__(self):
        self.packer = PortMapperPacker()
        self.unpacker = PortMapperUnpacker('')

    def set(self, mapping):
        return self.make_call(PMAPPROC_SET, mapping, self.packer.pack_mapping, self.unpacker.unpack_uint)

    def unset(self, mapping):
        return self.make_call(PMAPPROC_UNSET, mapping, self.packer.pack_mapping, self.unpacker.unpack_uint)

    def get_port(self, mapping):
        return self.make_call(PMAPPROC_GETPORT, mapping, self.packer.pack_mapping, self.unpacker.unpack_uint)

    def dump(self):
        return self.make_call(PMAPPROC_DUMP, None, None, self.unpacker.unpack_pmaplist)

    def callit(self, ca):
        return self.make_call(PMAPPROC_CALLIT, ca, self.packer.pack_call_args, self.unpacker.unpack_call_result)


class TCPPortMapperClient(PartialPortMapperClient, RawTCPClient):

    def __init__(self, host):
        RawTCPClient.__init__(self, host, PMAP_PROG, PMAP_VERS, PMAP_PORT)
        PartialPortMapperClient.__init__(self)


class UDPPortMapperClient(PartialPortMapperClient, RawUDPClient):

    def __init__(self, host):
        RawUDPClient.__init__(self, host, PMAP_PROG, PMAP_VERS, PMAP_PORT)
        PartialPortMapperClient.__init__(self)


class BroadcastUDPPortMapperClient(PartialPortMapperClient, RawBroadcastUDPClient):

    def __init__(self, bcastaddr):
        RawBroadcastUDPClient.__init__(self, bcastaddr, PMAP_PROG, PMAP_VERS, PMAP_PORT)
        PartialPortMapperClient.__init__(self)


class TCPClient(RawTCPClient):

    def __init__(self, host, prog, vers, port=0):
        if port == 0:
            pmap = TCPPortMapperClient(host)
            port = pmap.get_port((prog, vers, IPPROTO_TCP, 0))
            pmap.close()
        if port == 0:
            raise RPCError('program not registered')
        RawTCPClient.__init__(self, host, prog, vers, port)


class UDPClient(RawUDPClient):

    def __init__(self, host, prog, vers, port=0):
        if port == 0:
            pmap = UDPPortMapperClient(host)
            port = pmap.get_port((prog, vers, IPPROTO_UDP, 0))
            pmap.close()
        if port == 0:
            raise RPCError('program not registered')
        RawUDPClient.__init__(self, host, prog, vers, port)


class BroadcastUDPClient(Client):

    def __init__(self, bcastaddr, prog, vers):
        self.pmap = BroadcastUDPPortMapperClient(bcastaddr)
        self.pmap.set_reply_handler(self.my_reply_handler)
        self.prog = prog
        self.vers = vers
        self.user_reply_handler = None
        self.addpackers()
        return

    def close(self):
        self.pmap.close()

    def set_reply_handler(self, reply_handler):
        self.user_reply_handler = reply_handler

    def set_timeout(self, timeout):
        self.pmap.set_timeout(timeout)

    def my_reply_handler(self, reply, fromaddr):
        port, res = reply
        self.unpacker.reset(res)
        result = self.unpack_func()
        self.unpacker.done()
        self.replies.append((result, fromaddr))
        if self.user_reply_handler is not None:
            self.user_reply_handler(result, fromaddr)
        return

    def make_call(self, proc, args, pack_func, unpack_func):
        self.packer.reset()
        if pack_func:
            pack_func(args)
        if unpack_func is None:

            def dummy():
                pass

            self.unpack_func = dummy
        else:
            self.unpack_func = unpack_func
        self.replies = []
        packed_args = self.packer.get_buf()
        dummy_replies = self.pmap.Callit((
         self.prog, self.vers, proc, packed_args))
        return self.replies


class Server:

    def __init__(self, host, prog, vers, port):
        self.host = host
        self.prog = prog
        self.vers = vers
        self.port = port
        self.registered = False
        self.addpackers()

    def __del__(self):
        if self.registered:
            self.unregister()

    def register(self):
        mapping = (self.prog, self.vers, self.prot, self.port)
        p = TCPPortMapperClient(self.host)
        if not p.set(mapping):
            raise RPCError('register failed')
        self.registered = True

    def unregister(self):
        mapping = (
         self.prog, self.vers, self.prot, self.port)
        p = TCPPortMapperClient(self.host)
        if not p.unset(mapping):
            raise RPCError('unregister failed')
        self.registered = False

    def handle(self, call):
        self.unpacker.reset(call)
        self.packer.reset()
        xid = self.unpacker.unpack_uint()
        self.packer.pack_uint(xid)
        temp = self.unpacker.unpack_enum()
        if temp != CALL:
            return None
        else:
            self.packer.pack_uint(REPLY)
            temp = self.unpacker.unpack_uint()
            if temp != RPCVERSION:
                self.packer.pack_uint(MSG_DENIED)
                self.packer.pack_uint(RPC_MISMATCH)
                self.packer.pack_uint(RPCVERSION)
                self.packer.pack_uint(RPCVERSION)
                return self.packer.get_buf()
            self.packer.pack_uint(MSG_ACCEPTED)
            self.packer.pack_auth((AUTH_NULL, make_auth_null()))
            prog = self.unpacker.unpack_uint()
            if prog != self.prog:
                self.packer.pack_uint(PROG_UNAVAIL)
                return self.packer.get_buf()
            vers = self.unpacker.unpack_uint()
            if vers != self.vers:
                self.packer.pack_uint(PROG_MISMATCH)
                self.packer.pack_uint(self.vers)
                self.packer.pack_uint(self.vers)
                return self.packer.get_buf()
            proc = self.unpacker.unpack_uint()
            methname = 'handle_' + repr(proc)
            try:
                meth = getattr(self, methname)
            except AttributeError:
                self.packer.pack_uint(PROC_UNAVAIL)
                return self.packer.get_buf()

            cred = self.unpacker.unpack_auth()
            verf = self.unpacker.unpack_auth()
            try:
                meth()
            except (EOFError, RPCGarbageArgs):
                self.packer.reset()
                self.packer.pack_uint(xid)
                self.packer.pack_uint(REPLY)
                self.packer.pack_uint(MSG_ACCEPTED)
                self.packer.pack_auth((AUTH_NULL, make_auth_null()))
                self.packer.pack_uint(GARBAGE_ARGS)

            return self.packer.get_buf()

    def turn_around(self):
        try:
            self.unpacker.done()
        except RuntimeError:
            raise RPCGarbageArgs

        self.packer.pack_uint(SUCCESS)

    def handle_0(self):
        self.turn_around()

    def addpackers(self):
        self.packer = Packer()
        self.unpacker = Unpacker('')


class TCPServer(Server):

    def __init__(self, host, prog, vers, port):
        Server.__init__(self, host, prog, vers, port)
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.prot = IPPROTO_TCP
        self.sock.bind((self.host, self.port))
        self.host, self.port = self.sock.getsockname()

    def loop(self):
        self.sock.listen(0)
        while 1:
            self.session(self.sock.accept())

    def session(self, connection):
        sock, (host, port) = connection
        while 1:
            try:
                call = recvrecord(sock)
            except EOFError:
                break
            except socket.error:
                print (
                 'socket error:', sys.exc_info()[0])
                break

            reply = self.handle(call)
            if reply is not None:
                sendrecord(sock, reply)

        return

    def forkingloop(self):
        self.sock.listen(0)
        while 1:
            self.forksession(self.sock.accept())

    def forksession(self, connection):
        import os
        try:
            while 1:
                pid, sts = os.waitpid(0, os.WNOHANG)

        except os.error:
            pass

        pid = None
        try:
            pid = os.fork()
            if pid:
                connection[0].close()
                return
            self.session(connection)
        finally:
            if pid == 0:
                os._exit(0)

        return


class UDPServer(Server):

    def __init__(self, host, prog, vers, port):
        Server.__init__(self, host, prog, vers, port)
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.prot = IPPROTO_UDP
        self.sock.bind((self.host, self.port))
        self.host, self.port = self.sock.getsockname()

    def loop(self):
        while 1:
            self.session()

    def session(self):
        call, host_port = self.sock.recvfrom(8192)
        reply = self.handle(call)
        if reply is not None:
            self.sock.sendto(reply, host_port)
        return


def test(host=''):
    pmap = UDPPortMapperClient(host)
    list = pmap.dump()
    list.sort()
    for prog, vers, prot, port in list:
        st = '%d %d ' % (prog, vers)
        if prot == IPPROTO_TCP:
            st += 'tcp '
        elif prot == IPPROTO_UDP:
            st += 'udp '
        else:
            st += '%d ' % prot
        st += '%d' % port
        print st