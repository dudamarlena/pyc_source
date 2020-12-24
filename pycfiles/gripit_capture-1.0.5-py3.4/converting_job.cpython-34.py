# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/jobs/converting_job.py
# Compiled at: 2017-02-08 05:29:00
# Size of source mod 2**32: 807 bytes
import getpass
from webcam.config import Config
from webcam.services.cmd import Cmd

class ConvertingJob:

    def __init__(self):
        self.job_running = False
        self.cmd = Cmd()

    def convert(self, file):
        print('START CONVERSION')
        self.job_running = True
        self.cmd.run(self._ConvertingJob__convert_command(file))

    def stop(self):
        print('STOP CONVERSION')
        self.cmd.kill()
        self.job_running = False

    def is_running(self):
        return self.job_running

    def __convert_command(self, file):
        user_name = getpass.getuser()
        return '/home/' + user_name + '/bin/ffmpeg -i ' + file + Config.OUTPUT_FILE_EXTENSION + ' -vcodec libx264 ' + file + '_h264' + Config.OUTPUT_FILE_EXTENSION + ' &'