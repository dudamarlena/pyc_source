# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtp/client.py
# Compiled at: 2013-02-13 13:37:18
"""client routines for LDTP"""
import os, re, sys, time, signal, platform, traceback, xmlrpclib, subprocess
from socket import error as SocketError
from client_exception import LdtpExecutionError, ERROR_CODE
from log import logger
_python26 = False
if sys.version_info[:2] <= (2, 6):
    _python26 = True
_ldtp_windows_env = False
if 'LDTP_DEBUG' in os.environ:
    _ldtp_debug = os.environ['LDTP_DEBUG']
else:
    _ldtp_debug = None
if 'LDTP_XML_DEBUG' in os.environ:
    verbose = 1
else:
    verbose = 0
if 'LDTP_SERVER_ADDR' in os.environ:
    _ldtp_server_addr = os.environ['LDTP_SERVER_ADDR']
else:
    _ldtp_server_addr = 'localhost'
if 'LDTP_SERVER_PORT' in os.environ:
    _ldtp_server_port = os.environ['LDTP_SERVER_PORT']
else:
    _ldtp_server_port = '4118'
if 'LDTP_WINDOWS' in os.environ or sys.platform.find('darwin') == -1 and sys.platform.find('win') != -1:
    if 'LDTP_LINUX' in os.environ:
        _ldtp_windows_env = False
    else:
        _ldtp_windows_env = True
else:
    _ldtp_windows_env = False

class _Method(xmlrpclib._Method):

    def __call__(self, *args, **kwargs):
        if _ldtp_debug:
            logger.debug('%s(%s)' % (self.__name,
             (', ').join(map(repr, args) + [ '%s=%s' % (k, repr(v)) for k, v in kwargs.items()
                              ])))
        return self.__send(self.__name, args)


class Transport(xmlrpclib.Transport):

    def _handle_signal(self, signum, frame):
        if _ldtp_debug:
            if signum == signal.SIGCHLD:
                print 'ldtpd exited!'
            elif signum == signal.SIGUSR1:
                print 'SIGUSR1 received. ldtpd ready for requests.'
            elif signum == signal.SIGALRM:
                print 'SIGALRM received. Timeout waiting for SIGUSR1.'

    def _spawn_daemon(self):
        pid = os.getpid()
        if _ldtp_windows_env:
            if _ldtp_debug:
                cmd = 'start cmd /K CobraWinLDTP.exe'
            else:
                cmd = 'CobraWinLDTP.exe'
            subprocess.Popen(cmd, shell=True)
            self._daemon = True
        elif platform.mac_ver()[0] != '':
            pycmd = 'import atomac.ldtpd; atomac.ldtpd.main(parentpid=%s)' % pid
            self._daemon = os.spawnlp(os.P_NOWAIT, 'python', 'python', '-c', pycmd)
        else:
            pycmd = 'import ldtpd; ldtpd.main(parentpid=%s)' % pid
            self._daemon = os.spawnlp(os.P_NOWAIT, 'python', 'python', '-c', pycmd)

    if not _python26:

        def make_connection(self, host):
            import httplib
            host, extra_headers, x509 = self.get_host_info(host)
            return httplib.HTTPConnection(host)

    def request(self, host, handler, request_body, verbose=0):
        retry_count = 1
        while True:
            try:
                if _python26:
                    return xmlrpclib.Transport.request(self, host, handler, request_body, verbose=verbose)
                else:
                    h = self.make_connection(host)
                    if verbose:
                        h.set_debuglevel(1)
                    self.send_request(h, handler, request_body)
                    self.send_host(h, host)
                    self.send_user_agent(h)
                    self.send_content(h, request_body)
                    response = h.getresponse()
                    if response.status != 200:
                        raise xmlrpclib.ProtocolError(host + handler, response.status, response.reason, response.msg.headers)
                    payload = response.read()
                    parser, unmarshaller = self.getparser()
                    parser.feed(payload)
                    parser.close()
                    return unmarshaller.close()

            except SocketError as e:
                if (_ldtp_windows_env and e[0] == 10061 or not _ldtp_windows_env and (e.errno == 111 or e.errno == 61 or e.errno == 146)) and 'localhost' in host:
                    if hasattr(self, 'close'):
                        self.close()
                    if retry_count == 1:
                        retry_count += 1
                        if not _ldtp_windows_env:
                            sigusr1 = signal.signal(signal.SIGUSR1, self._handle_signal)
                            sigalrm = signal.signal(signal.SIGALRM, self._handle_signal)
                            sigchld = signal.signal(signal.SIGCHLD, self._handle_signal)
                        self._spawn_daemon()
                        if _ldtp_windows_env:
                            time.sleep(5)
                        else:
                            signal.alarm(15)
                            signal.pause()
                            signal.alarm(0)
                            signal.signal(signal.SIGUSR1, sigusr1)
                            signal.signal(signal.SIGALRM, sigalrm)
                            signal.signal(signal.SIGCHLD, sigchld)
                        continue
                    else:
                        raise
                raise
            except xmlrpclib.Fault as e:
                if hasattr(self, 'close'):
                    self.close()
                if e.faultCode == ERROR_CODE:
                    raise LdtpExecutionError(e.faultString.encode('utf-8'))
                else:
                    raise e

    def __del__(self):
        self.kill_daemon()

    def kill_daemon(self):
        try:
            if _ldtp_windows_env and self._daemon:
                subprocess.Popen('taskkill /F /IM CobraWinLDTP.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            else:
                os.kill(self._daemon, signal.SIGKILL)
        except AttributeError:
            pass


class LdtpClient(xmlrpclib.ServerProxy):

    def __init__(self, uri, encoding=None, verbose=0, use_datetime=0):
        xmlrpclib.ServerProxy.__init__(self, uri, Transport(), encoding, verbose, 1, use_datetime)

    def __getattr__(self, name):
        return _Method(self._ServerProxy__request, name)

    def kill_daemon(self):
        self._ServerProxy__transport.kill_daemon()

    def setHost(self, host):
        setattr(self, '_ServerProxy__host', host)


_client = LdtpClient('http://%s:%s' % (_ldtp_server_addr, _ldtp_server_port), verbose=verbose)