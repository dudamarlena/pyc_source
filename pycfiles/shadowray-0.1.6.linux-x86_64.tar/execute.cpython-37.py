# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/core/execute.py
# Compiled at: 2019-03-24 13:21:40
# Size of source mod 2**32: 1233 bytes
import subprocess
from shadowray.config.v2ray import EXECUTE_ARGS, V2RAY_PID_FILE, CONFIG_STREAM_FILE
from shadowray.common.utils import write_to_file
import multiprocessing, time, os, sys

class Execute:

    def __init__(self, binary):
        self.v2ray_binary = binary
        self.config = None

    def __exec(self):
        s = subprocess.Popen([self.v2ray_binary, EXECUTE_ARGS], stdin=(subprocess.PIPE))
        write_to_file(V2RAY_PID_FILE, 'w', str(s.pid))
        s.communicate(self.config)

    def exec(self, config: str, daemon=False):
        self.config = bytes(config, encoding='utf8')
        process = multiprocessing.Process(target=(self._Execute__exec), daemon=daemon)
        process.start()
        if daemon is True:
            time.sleep(1)

    def stop(self):
        if self.v2_process is not None:
            self.v2_process.kill()
            self.v2_process = None

    def restart(self, config=None):
        if self.v2_process is not None:
            self.v2_process.kill()
        elif config is not None:
            self.v2_process = self.exec(config)
        else:
            if self.config is not None:
                self.v2_process = self.exec(self.config)
            else:
                print('No config!!!')