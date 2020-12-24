# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycluster/ssh.py
# Compiled at: 2019-04-18 17:28:18
"""SSH tunneling for EasyCluster"""
from __future__ import print_function
import subprocess, os, fcntl, easycluster as _core, socket

class PipeSocket(object):

    def __init__(self, proc, rfd=None, wfd=None, peername=None):
        self._proc = proc
        if rfd is None:
            rfd = proc.stdout.fileno()
            wfd = proc.stdin.fileno()
        self._rfd = rfd
        self._wfd = wfd
        self._peername = peername
        return

    def fileno(self):
        return self._rfd

    def write_fileno(self):
        return self._wfd

    def recv(self, amt):
        return os.read(self._rfd, amt)

    def send(self, data):
        return os.write(self._wfd, data)

    def sendall(self, data):
        while data:
            w = os.write(self._wfd, data)
            data = data[w:]

    def close(self):
        try:
            if self._rfd is not None:
                os.close(self._rfd)
                os.close(self._wfd)
                self._rfd = self._wfd = None
        except EnvironmentError:
            pass

        try:
            if self._proc is not None:
                self._proc.terminate()
                self._proc.wait()
                self._proc = None
        except EnvironmentError:
            pass

        return

    def shutdown(self, type):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def setblocking(self, block):
        for fd in (self._rfd, self._wfd):
            flags = fcntl.fcntl(fcntl.F_GETFL, fd) & ~os.O_NONBLOCK
            if not block:
                flags |= os.O_NONBLOCK
            fcntl.fcntl(fcntl.F_SETFL, fd, flags)

    def getpeername(self):
        return self._peername


def _ss(key):
    from easycluster import server
    peer = (':').join(os.getenv('SSH_CONNECTION').split()[:2])
    sock = PipeSocket(None, 0, 1)
    svr = server.Server(key, sock, peer)
    while svr:
        svr = svr.run()

    return


if _core.PYTHON3:
    python_cmd = "python3 -c 'exec(eval(input()))'"
else:
    python_cmd = "python -c 'exec input()'"
_bootstrap = "\nimport sys,os,zlib,types\ndef r(n,a):\n sys.modules[n]=m=types.ModuleType(n)\n m._compcode=r=bytearray()\n while a > 0:\n  t = os.read(0, a)\n  if not t:\n   break\n  a -= len(t)\n  r.extend(t)\n eval(compile(zlib.decompress(r),n,'exec'),m.__dict__)\n return m\nos.write(1,%r)\nr('easycluster',%d)\nr('easycluster.server',%d)\nr('easycluster.ssh',%d)._ss(%r)\n"

def prepare_ssh(ssh_args):
    key = _core.generate_key()
    sig = os.urandom(8)
    coredata, svrdata, sshdata = _core._get_upgrade_data()
    bootstrap = repr(_bootstrap % (sig, len(coredata), len(svrdata), len(sshdata), key)) + '\n'
    proc = subprocess.Popen(ssh_args + [python_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sock = PipeSocket(proc)
    sock.sendall(core._str_to_bytes(bootstrap))
    data = bytearray()
    while not data.endswith(sig):
        data.extend(sock.read(8))

    sock.sendall(coredata)
    sock.sendall(svrdata)
    sock.sendall(sshdata)
    return (sock, key)


def connect_ssh(host, port=None, user=None, ssh='ssh', extra_args=(), client_class=None):
    args = [ssh]
    if port is not None:
        args.append('-p', str(port))
    userhost = host
    if user is not None:
        userhost = '%s@%s' % (user, host)
    peer = host
    if port is not None:
        peer = '%s:%d' % (host, port)
    args.append(userhost)
    args.extend(extra_args)
    sock, key = prepare_ssh(args)
    if client_class is None:
        client_class = _core.Client
    ret = client_class(key)
    ret.set_socket(sock, peer)
    return