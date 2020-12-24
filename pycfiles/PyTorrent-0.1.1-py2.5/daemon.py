# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pytorrent/daemon.py
# Compiled at: 2008-09-26 21:08:50
import subprocess, os, signal, time

class Daemon(object):
    term = signal.SIGTERM
    kill = signal.SIGKILL

    def __init__(self, executable):
        self.executable = executable
        self.pid = None
        self.process = None
        return

    def start(self):
        self.process = subprocess.Popen(self.executable)
        self.pid = self.process.pid

    def stop(self):
        if self.process:
            pid = self.process.pid
            for i in range(0, 10):
                if self.process.poll() is not None:
                    return
                os.kill(pid, self.term)
                time.sleep(0.1)

            for i in range(0, 10):
                if self.process.poll() is not None:
                    return
                os.kill(pid, self.kill)
                time.sleep(0.1)

        return