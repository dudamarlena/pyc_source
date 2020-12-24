# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webbridge\server.py
# Compiled at: 2016-09-02 12:59:33
import shlex, subprocess

class Server:

    def __init__(self, cmd):
        self.cmd = shlex.split(cmd)
        self.process = None
        return

    def run(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.process = subprocess.Popen(self.cmd, startupinfo=startupinfo)

    def kill(self):
        if self.process != None:
            self.process.kill()
        return