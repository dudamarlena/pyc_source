# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/services/cmd.py
# Compiled at: 2017-01-04 05:56:19
# Size of source mod 2**32: 495 bytes
import os, signal, subprocess

class Cmd:

    def __init__(self):
        self.process = None

    def run(self, cmd):
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        return self.process

    def kill(self):
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        self.process = None