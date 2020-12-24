# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\portube.py
# Compiled at: 2019-04-08 02:56:18
# Size of source mod 2**32: 8511 bytes
import select, socket, argparse

class Portube(object):
    DATA_BLOCK = 4096

    def __init__(self, laddr, lport, raddr, rport):
        self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.l_connected = None
        self.r_connected = None
        self.laddr = laddr
        self.lport = lport
        self.raddr = raddr
        self.rport = rport

    def port2host(self):
        try:
            self.l_socket.bind((self.laddr, self.lport))
            self.l_socket.listen(1)
        except Exception as reason:
            print('Create Listen Port Failed!')
            exit(0)

        self.rlist = [
         self.l_socket]
        self.wlist = []
        self.elist = []
        tube = []
        while True:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                if sockfd == self.l_socket:
                    self.l_connected, addr = sockfd.accept()
                    self.rlist.append(self.l_connected)
                    print('[√] Local connected:laddr={},raddr={}'.format(self.l_connected.getsockname(), self.l_connected.getpeername()))
                    try:
                        self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.r_socket.connect((self.raddr, self.rport))
                    except Exception as reason:
                        print('Connect Source Port Failed!')
                        exit(0)

                    self.rlist.append(self.r_socket)
                    print('[√] Remote connected:laddr={},raddr={}'.format(self.r_socket.getsockname(), self.r_socket.getpeername()))
                    tube.append((self.l_connected, self.r_socket))
                    continue
                else:
                    for tb in tube:
                        if sockfd in tb:
                            r_i = tb.index(sockfd)
                            w_i = 0 if r_i == 1 else 1
                            rr = self.copy(sockfd, tb[w_i])
                            if rr < 0:
                                self.rlist.remove(tb[0])
                                self.rlist.remove(tb[1])
                                tube.remove(tb)
                                print('[x] connect close:laddr={},raddr={}'.format(tb[0].getsockname(), tb[0].getpeername()))
                                tb[0].close()
                                print('[x] connect close:laddr={},raddr={}'.format(tb[1].getsockname(), tb[1].getpeername()))
                                tb[1].close()

    def host2host(self):
        try:
            self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.l_socket.connect((self.laddr, self.lport))
            self.r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.r_socket.connect((self.raddr, self.rport))
        except Exception as reason:
            print('Connect Source Port Failed!')
            exit(0)

        self.rlist = [
         self.l_socket, self.r_socket]
        self.wlist = []
        self.elist = [self.l_socket, self.r_socket]
        loop_w = True
        while loop_w:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                for i, v in enumerate(self.rlist):
                    ret = 0
                    rev = None
                    if sockfd == v:
                        if i % 2 == 0:
                            rev = self.rlist[(i + 1)]
                            ret = self.copy(sockfd, rev)
                        if sockfd == v:
                            if i % 2 == 1:
                                rev = self.rlist[(i - 1)]
                                ret = self.copy(sockfd, rev)
                        elif ret < 0:
                            self.rlist.remove(sockfd)
                            self.rlist.remove(rev)
                            print('[x] connect close:laddr={},raddr={}'.format(sockfd.getsockname(), sockfd.getpeername()))
                            sockfd.close()
                            print('[x] connect close:laddr={},raddr={}'.format(rev.getsockname(), rev.getpeername()))
                            rev.close()
                            loop_w = False
                            break

        self.host2host()

    def port2port(self):
        try:
            self.l_socket.bind((self.laddr, self.lport))
            self.l_socket.listen(1)
            self.r_socket.bind((self.raddr, self.rport))
            self.r_socket.listen(1)
        except Exception as reason:
            print('Create Listen Port Failed!')
            exit(0)

        self.rlist = [
         self.l_socket, self.r_socket]
        self.wlist = []
        self.elist = []
        while True:
            rs, ws, es = select.select(self.rlist, self.wlist, self.elist)
            for sockfd in rs:
                if sockfd == self.l_socket:
                    self.l_connected, addr = sockfd.accept()
                    self.rlist.append(self.l_connected)
                    continue
                elif sockfd == self.r_socket:
                    self.r_connected, addr = sockfd.accept()
                    self.rlist.append(self.r_connected)
                    continue
                else:
                    tube = self.rlist[2:]
                    if not len(tube) < 2:
                        if len(tube) % 2 == 1:
                            continue
                        for i, v in enumerate(tube):
                            ret = 0
                            rev = None
                            if sockfd == v:
                                if i % 2 == 0:
                                    rev = tube[(i + 1)]
                                    ret = self.copy(sockfd, rev)
                                else:
                                    if sockfd == v:
                                        if i % 2 == 1:
                                            rev = tube[(i - 1)]
                                            ret = self.copy(sockfd, rev)
                                if ret < 0:
                                    self.rlist.remove(sockfd)
                                    self.rlist.remove(rev)
                                    print('[x] connect close:laddr={},raddr={}'.format(sockfd.getsockname(), sockfd.getpeername()))
                                    sockfd.close()
                                    print('[x] connect close:laddr={},raddr={}'.format(rev.getsockname(), rev.getpeername()))
                                    rev.close()

    def copy(self, reader, writer):
        data = reader.recv(self.DATA_BLOCK)
        if len(data) <= 0:
            return -1
        else:
            w = writer.send(data)
            if w <= 0:
                return -2
            print('[->] tran [{}] : from {} to {} '.format(len(data), reader.getsockname(), writer.getsockname()))
            return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='[listen] [slave] [tran] [l] [s] [t]')
    parser.add_argument('-l', '--laddr', dest='laddr', default='0.0.0.0', help='IP eg: 0.0.0.0')
    parser.add_argument('-p', '--lport', dest='lport', help='Port eg: 3306')
    parser.add_argument('-R', '--raddr', dest='raddr', default='0.0.0.0', help='IP eg: 0.0.0.0')
    parser.add_argument('-P', '--rport', dest='rport', help='Port eg: 3306')
    options = parser.parse_args()
    pt = Portube(options.laddr, int(options.lport), options.raddr, int(options.rport))
    if options.type in ('listen', 'l'):
        pt.port2port()
    else:
        if options.type in ('slave', 's'):
            pt.host2host()
        elif options.type in ('tran', 't'):
            pt.port2host()


if __name__ == '__main__':
    main()