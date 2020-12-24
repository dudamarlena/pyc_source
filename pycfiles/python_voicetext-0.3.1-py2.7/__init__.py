# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/voicetext/__init__.py
# Compiled at: 2015-03-14 01:15:24
from __future__ import absolute_import, division, print_function, unicode_literals
import wave, logging, json, os, os.path, requests
from requests.auth import HTTPBasicAuth
import pyaudio

class VoiceTextException(Exception):
    pass


class VoiceText(object):
    """
    Speech synthesizer by VoiceText Web API
    """
    URL = b'https://api.voicetext.jp/v1/tts'
    CHUNK = 1024
    _audio = pyaudio.PyAudio()

    def __init__(self, user_name=b'', password=b'', speaker=b'hikari'):
        """
        :param user_name: Auth user name of VoiceText Web API
        :type user_name: str
        :param password: Auth password of VoiceText Web API
        :type password: str
        :param speaker: Speaker name
        :type speaker: str
        """
        self._auth = HTTPBasicAuth(user_name, password)
        self._default_speaker = speaker
        self._data = {b'speaker': self._default_speaker}
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)
        try:
            self.to_wave(b'test')
        except VoiceTextException as e:
            raise VoiceTextException(b'HTTP basic auth error')

    def set_logger(self, logger):
        """
        Set user-specific logger.
        :type logger: Logger
        :rtype: VoiceText
        """
        self._logger = logger
        return self

    def restore_default(self):
        """
        Restore default parameters.
        :rtype: VoiceText
        """
        self._data = {b'speaker': self._default_speaker}
        return self

    def speaker(self, speaker):
        """
        Change speaker.
        :param speaker: Speaker name
        :type speaker: str
        :rtype: VoiceText
        """
        if speaker in ('show', 'haruka', 'hikari', 'takeru', 'santa', 'bear'):
            self._data[b'speaker'] = speaker
        else:
            self._logger.warning(b'Unknown speaker: %s' % str(speaker))
        return self

    def emotion(self, emotion, level=1):
        """
        Change emotion and its level.
        :param emotion: Emotion type
        :type emotion: str
        :param level: Level of emotion
        :type level: int
        :rtype: VoiceText
        """
        if emotion in ('happiness', 'anger', 'sadness'):
            self._data[b'emotion'] = emotion
            if isinstance(level, int) and 1 <= level <= 2:
                self._data[b'emotion_level'] = level
        else:
            self._logger.warning(b'Unknown emotion: %s' % str(emotion))
        return self

    def pitch(self, pitch):
        """
        Change pitch.
        :param pitch: Amount of pitch
        :type pitch: int
        :rtype: VoiceText
        """
        if isinstance(pitch, int):
            if pitch < 50:
                pitch = 50
            elif 200 < pitch:
                pitch = 200
            self._data[b'pitch'] = pitch
        return self

    def speed(self, speed):
        """
        Change speed.
        :param speed: Amount of speed
        :type speed: int
        :rtype: VoiceText
        """
        if isinstance(speed, int):
            if speed < 50:
                speed = 50
            elif 400 < speed:
                speed = 400
            self._data[b'speed'] = speed
        return self

    def volume(self, volume):
        """
        Change volume.
        :param volume: Amount of volume
        :type volume: int
        :rtype: VoiceText
        """
        if isinstance(volume, int):
            if volume < 50:
                volume = 50
            elif 200 < volume:
                volume = 200
            self._data[b'volume'] = volume
        return self

    def to_wave(self, text):
        """
        Convert text to wave binary.
        :param text: Text to synthesize
        :type text: str
        :return: bytearray
        """
        self._data[b'text'] = text
        self._logger.debug(b'Post: %s' % str(self._data))
        request = requests.post(self.URL, self._data, auth=self._auth)
        self._logger.debug(b'Status: %d' % request.status_code)
        if request.status_code != requests.codes.ok:
            raise VoiceTextException(b'Invalid status code: %d' % request.status_code)
        return request.content

    def speak(self, text):
        """
        Speak text.
        :param text: Text to synthesize
        :type text: str
        """
        self._data[b'text'] = text
        path = b'/tmp/voicetext_%s.wav' % hash(json.dumps(self._data))
        if not os.path.exists(path):
            w = self.to_wave(text)
            with open(path, b'wb') as (temp):
                temp.write(w)
        temp = wave.open(path)
        stream = self._audio.open(format=self._audio.get_format_from_width(temp.getsampwidth()), channels=temp.getnchannels(), rate=temp.getframerate(), output=True)
        data = temp.readframes(self.CHUNK)
        while data:
            stream.write(data)
            data = temp.readframes(min(data, self.CHUNK))

        stream.close()
        temp.close()


if __name__ == b'__main__':
    import argparse
    parser = argparse.ArgumentParser(description=VoiceText.__name__)
    parser.add_argument(b'--user', type=str, default=b'', help=b'user name')
    args, unknown = parser.parse_known_args()
    vt = VoiceText(user_name=args.user)