# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/server.py
# Compiled at: 2014-06-12 20:22:27
import subprocess

class Server(object):

    def __init__(self, port=8080):
        self.port = port
        self.server = None
        return

    def start(self):
        """ Start the web server
        """
        commands = 'python2 -m SimpleHTTPServer 8080 >& /dev/null'
        self.server = subprocess.Popen(commands, shell=True)

    def stop(self):
        """ Stop the server
        """
        if self.server:
            self.server.kill()
            self.server = None
        return