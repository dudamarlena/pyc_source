# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/motion_detection.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 2191 bytes
from amcrest.utils import str2bool

class MotionDetection(object):

    def __get_config(self, config_name):
        ret = self.command('configManager.cgi?action=getConfig&name={0}'.format(config_name))
        return ret.content.decode('utf-8')

    @property
    def motion_detection(self):
        return self._MotionDetection__get_config('MotionDetect')

    def is_motion_detector_on(self):
        ret = self.motion_detection
        status = [s for s in ret.split() if '.Enable=' in s][0].split('=')[(-1)]
        return str2bool(status)

    def is_record_on_motion_detection(self):
        ret = self.motion_detection
        status = [s for s in ret.split() if '.RecordEnable=' in s][0].split('=')[(-1)]
        return str2bool(status)

    @motion_detection.setter
    def motion_detection(self, opt):
        if opt.lower() == 'true' or opt.lower() == 'false':
            ret = self.command('configManager.cgi?action=setConfig&MotionDetect[0].Enable={0}'.format(opt.lower()))
            if 'ok' in ret.content.decode('utf-8').lower():
                return True
        return False

    @motion_detection.setter
    def motion_recording(self, opt):
        if opt.lower() == 'true' or opt.lower() == 'false':
            ret = self.command('configManager.cgi?action=setConfig&MotionDetect[0].EventHandler.RecordEnable={0}'.format(opt.lower()))
            if 'ok' in ret.content.decode('utf-8').lower():
                return True
        return False