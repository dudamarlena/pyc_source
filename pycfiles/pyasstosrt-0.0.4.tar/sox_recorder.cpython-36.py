# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/record/sox_recorder.py
# Compiled at: 2018-01-07 13:00:15
# Size of source mod 2**32: 981 bytes
import assistant.util.package as package, subprocess, tempfile, assistant.util.alsa as alsa, logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')

class SoxRecorder:

    def __init__(self):
        package.install('sox', 'sudo apt-get install -y sox')
        self.threshold = 50
        self.start_second = 0.3
        self.end_seond = 1
        self.default_mic, self.default_speaker = alsa.get_default()

    def record(self):
        temp = tempfile.NamedTemporaryFile()
        temp.close()
        file = temp.name + '.wav'
        thres_str = str(self.threshold) + '%'
        start_sec = '00:00:' + str(self.start_second)
        end_sec = '00:00:' + str(self.end_seond)
        cmd = 'sox -c 1 -t alsa plughw:%s,%s %s silence 1 %s %s 1 %s %s' % (self.default_mic['card_id'], self.default_mic['device_id'], file, start_sec, thres_str, end_sec, thres_str)
        logger.info(cmd)
        subprocess.call(cmd.split(' '))
        return file