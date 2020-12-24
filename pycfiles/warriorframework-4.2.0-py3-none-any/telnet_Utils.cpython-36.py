# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/Framework/Utils/telnet_Utils.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 3698 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import telnetlib, socket, time, re
from datetime import datetime
from .print_Utils import print_info, print_warning, print_error, print_debug

class Tnet_Comm(object):
    __doc__ = ' Does communication with the NE/Server using Telnet protocol\n    Write/Read commands to and from the NE/Server'

    def __init__(self, target, port='', uid='', pid='', logfile='telnet_log', cmd_rsp=None):
        """Creates Comms objects"""
        self.target = target
        self.port = port
        self.uid = uid
        self.pid = pid
        self.logfile = logfile
        self.cmd_rsp = cmd_rsp
        self.ne_prompt = re.compile('\\r\\nM.*\\r\\n;\\r\\n> ', re.DOTALL)
        self.tnet = telnetlib.Telnet()

    def open_target(self):
        """ Connects to a NE using telnet protocol with provided
        login credentials"""
        print_info('telnet Target open')
        host = self.target
        port = self.port
        print_info('OPENING TELNET Connection...\n')
        print_info('HOST: {0} PORT: {1}'.format(host, port))
        try:
            self.tnet.open(host, port)
            self.log = open(self.logfile, 'w')
        except socket.error as err:
            print_warning('Login failed {0}'.format(str(err)))
            return False
        else:
            return True

    def close(self):
        """Calls the telnetlib close and terminates the telnet session"""
        try:
            self.tnet.close()
            print_debug('TELNET CONNECTION CLOSING...')
        except Exception:
            print_error('Error occured while closing telnet session')
            return False

    def write(self, cmd_string):
        """ Writes the commands to the terminal"""
        self.tnet.write(cmd_string + '\r\n')
        time.sleep(3)

    def read(self, prompt='', timeout=60):
        """ Reads the output till the prompt and returns the result and
        reports Failure on mismatch of response"""
        if not prompt:
            prompt = self.ne_prompt
        res = self.tnet.expect([prompt], timeout)
        self.cmd_rsp = res[2]
        try:
            if res:
                self.log.write(res[2])
                self.log.flush()
            else:
                self.log.write('Expected Prompt Not found.', res)
                self.log.flush()
        except re.error:
            print_debug('Expected Response:{0}'.format(prompt))
            print_debug('Received Response:{0}'.format(self.cmd_rsp))

        return self.cmd_rsp

    def get_response(self, cmd_string, prompt, timeout=120):
        """ Reads the output till the prompt and returns the result and
        reports Failure on mismatch of response"""
        self.write(cmd_string)
        try:
            self.cmd_resp = self.read(prompt, timeout)
        except re.error:
            print_debug('Expected Response:{0}'.format(prompt))
            print_debug('Received Response:{0}'.format(self.cmd_rsp))

        return self.cmd_resp