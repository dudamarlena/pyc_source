# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/vpn/openvpn.py
# Compiled at: 2015-09-30 11:20:13
import subprocess, threading, time

class OpenVPN:

    def __init__(self, config_file=None, auth_file=None, crt_file=None, timeout=60):
        self.started = False
        self.stopped = False
        self.error = False
        self.notifications = ''
        self.auth_file = auth_file
        self.crt_file = crt_file
        self.config_file = config_file
        self.thread = threading.Thread(target=self._invoke_openvpn)
        self.thread.setDaemon(1)
        self.timeout = timeout

    def _invoke_openvpn(self):
        if self.auth_file is None:
            cmd = [
             'sudo', 'openvpn', '--script-security', '2',
             '--config', self.config_file]
        else:
            if self.crt_file is None:
                cmd = [
                 'sudo', 'openvpn', '--script-security', '2',
                 '--config', self.config_file,
                 '--auth-user-pass', self.auth_file]
            else:
                cmd = [
                 'sudo', 'openvpn', '--script-security', '2',
                 '--config', self.config_file,
                 '--auth-user-pass', self.auth_file,
                 '--ca', self.crt_file]
            self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.kill_switch = self.process.terminate
            self.starting = True
            while True:
                line = self.process.stdout.readline().strip()
                if not line:
                    break
                self.output_callback(line, self.process.terminate)

        return

    def output_callback(self, line, kill_switch):
        """Set status of openvpn according to what we process"""
        self.notifications += line + '\n'
        if 'Initialization Sequence Completed' in line:
            self.started = True
        if 'ERROR:' in line or 'Cannot resolve host address:' in line:
            self.error = True
        if 'process exiting' in line:
            self.stopped = True

    def start(self, timeout=None):
        """Start openvpn and block until the connection is opened or there is
        an error

        """
        if not timeout:
            timeout = self.timeout
        self.thread.start()
        start_time = time.time()
        while start_time + timeout > time.time():
            self.thread.join(1)
            if self.error or self.started:
                break

        if self.started:
            print 'openvpn started'
        else:
            print 'openvpn not started'
            print self.notifications

    def stop(self, timeout=None):
        """Stop openvpn"""
        if not timeout:
            timeout = self.timeout
        self.kill_switch()
        self.thread.join(timeout)
        if self.stopped:
            print 'stopped'
        else:
            print 'not stopped'
            print self.notifications