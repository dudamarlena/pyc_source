# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/audio.py
# Compiled at: 2019-05-16 15:27:13
# Size of source mod 2**32: 4226 bytes
import shutil
from urllib3.exceptions import HTTPError
from . import utils
from .exceptions import CommError

class Audio(object):

    @property
    def audio_input_channels_numbers(self):
        ret = self.command('devAudioInput.cgi?action=getCollect')
        return ret.content.decode('utf-8')

    @property
    def audio_output_channels_numbers(self):
        ret = self.command('devAudioOutput.cgi?action=getCollect')
        return ret.content.decode('utf-8')

    def play_wav(self, httptype=None, channel=None, path_file=None):
        if httptype is None:
            httptype = 'singlepart'
        else:
            if channel is None:
                channel = '1'
            if path_file is None:
                raise RuntimeError('filename is required')
        self.audio_send_stream(httptype, channel, path_file, 'G.711A')

    def audio_send_stream(self, httptype=None, channel=None, path_file=None, encode=None):
        """
        Params:

            path_file - path to audio file
            channel: - integer
            httptype - type string (singlepart or multipart)

                singlepart: HTTP content is a continuos flow of audio packets
                multipart: HTTP content type is multipart/x-mixed-replace, and
                           each audio packet ends with a boundary string

            Supported audio encode type according with documentation:
                PCM
                ADPCM
                G.711A
                G.711.Mu
                G.726
                G.729
                MPEG2
                AMR
                AAC

        """
        if httptype is None or channel is None:
            raise RuntimeError('Requires htttype and channel')
        file_audio = {'file': open(path_file, 'rb')}
        header = {'content-type':'Audio/' + encode, 
         'content-length':'9999999'}
        self.command_audio(('audio.cgi?action=postAudio&httptype={0}&channel={1}'.format(httptype, channel)),
          file_content=file_audio,
          http_header=header)

    def audio_stream_capture(self, httptype=None, channel=None, path_file=None):
        """
        Params:

            path_file - path to output file
            channel: - integer
            httptype - type string (singlepart or multipart)

                singlepart: HTTP content is a continuos flow of audio packets
                multipart: HTTP content type is multipart/x-mixed-replace, and
                           each audio packet ends with a boundary string

        """
        if httptype is None:
            if channel is None:
                raise RuntimeError('Requires htttype and channel')
        ret = self.command(('audio.cgi?action=getAudio&httptype={0}&channel={1}'.format(httptype, channel)),
          stream=True)
        if path_file:
            try:
                with open(path_file, 'wb') as (out_file):
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug('%s Audio stream capture to file failed due to error: %s', self, repr(error))
                raise CommError(error)

        return ret.raw

    @property
    def audio_enabled(self):
        """Return if any audio stream enabled."""
        return utils.extract_audio_video_enabled('Audio', self.encode_media)

    @audio_enabled.setter
    def audio_enabled(self, enable):
        """Enable/disable all audio streams."""
        self.command(utils.enable_audio_video_cmd('Audio', enable))