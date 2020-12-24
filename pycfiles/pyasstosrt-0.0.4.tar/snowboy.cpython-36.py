# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/hwd/snowboy.py
# Compiled at: 2018-01-05 12:56:39
# Size of source mod 2**32: 3518 bytes
import os, subprocess, sys, logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')
logger.setLevel(logging.INFO)
dir_path = os.path.abspath(os.path.dirname(__file__))
resource = os.path.join(dir_path, 'common.res')
setup = os.path.join(dir_path, 'setup.sh')
if sys.platform.startswith('linux'):
    if not os.path.exists(resource):
        subprocess.call(setup)
    from . import snowboydetect
else:
    logger.warning('snowboy can support only linux platform')
import pyaudio, time, wave, collections

class RingBuffer(object):
    """RingBuffer"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


class Snowboy:

    def __init__(self, decoder_model=os.path.join(dir_path, 'helloraspi.pmdl'), sensitivity=[], audio_gain=1):
        tm = type(decoder_model)
        ts = type(sensitivity)
        if tm is not list:
            decoder_model = [
             decoder_model]
        if ts is not list:
            sensitivity = [
             sensitivity]
        model_str = ','.join(decoder_model)
        self.detector = snowboydetect.SnowboyDetect(resource.encode(), model_str.encode())
        self.detector.SetAudioGain(audio_gain)
        self.num_hotwords = self.detector.NumHotwords()
        if len(decoder_model) > 1:
            if len(sensitivity) == 1:
                sensitivity = sensitivity * self.num_hotwords
        if len(sensitivity) != 0:
            if not self.num_hotwords == len(sensitivity):
                raise AssertionError('number of hotwords in decoder_model (%d) and sensitivity (%d) does not match' % (
                 self.num_hotwords, len(sensitivity)))
        sensitivity_str = ','.join([str(t) for t in sensitivity])
        if len(sensitivity) != 0:
            self.detector.SetSensitivity(sensitivity_str.encode())
        self.ring_buffer = RingBuffer(self.detector.NumChannels() * self.detector.SampleRate() * 5)

    def start(self, stop_callback, mute_callback, sleep_time=0.03):

        def audio_callback(in_data, frame_count, time_info, status):
            self.ring_buffer.extend(in_data)
            play_data = chr(0) * len(in_data)
            return (
             play_data, pyaudio.paContinue)

        self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(input=True,
          output=False,
          format=(self.audio.get_format_from_width(self.detector.BitsPerSample() / 8)),
          channels=(self.detector.NumChannels()),
          rate=(self.detector.SampleRate()),
          frames_per_buffer=2048,
          stream_callback=audio_callback)
        self.hotword = None
        while stop_callback():
            data = self.ring_buffer.get()
            if len(data) == 0:
                time.sleep(sleep_time)
            ans = mute_callback() or self.detector.RunDetection(data)
            if ans == -1:
                raise 'Error initializing streams or reading audio data'
                break
            elif ans > 0:
                self.hotword = ans
                break

        self.stream_in.stop_stream()
        self.stream_in.close()
        self.audio.terminate()
        return self.hotword