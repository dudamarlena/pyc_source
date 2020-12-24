# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/special.py
# Compiled at: 2019-05-16 15:28:40
# Size of source mod 2**32: 5009 bytes
import shutil
from urllib3.exceptions import HTTPError
from .exceptions import CommError

class Special(object):

    def realtime_stream(self, channel=1, typeno=0, path_file=None):
        """
        If the stream is redirect to a file, use mplayer tool to
        visualize the video record

        camera.realtime_stream(path_file="/home/user/Desktop/myvideo)
        $ mplayer /home/user/Desktop/myvideo
        """
        ret = self.command(('realmonitor.cgi?action=getStream&channel={0}&subtype={1}'.format(channel, typeno)),
          stream=True)
        if path_file:
            try:
                with open(path_file, 'wb') as (out_file):
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug('%s Realtime stream capture to file failed due to error: %s', self, repr(error))
                raise CommError(error)

        return ret.raw

    def rtsp_url(self, channelno=None, typeno=None):
        """
        Return RTSP streaming url

        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        if channelno is None:
            channelno = 1
        else:
            if typeno is None:
                typeno = 0
            cmd = 'cam/realmonitor?channel={0}&subtype={1}'.format(channelno, typeno)
            try:
                port = ':' + [x.split('=')[1] for x in self.rtsp_config.split() if x.startswith('table.RTSP.Port=')][0]
            except IndexError:
                port = ''

        return 'rtsp://{}:{}@{}{}/{}'.format(self._user, self._password, self._host, port, cmd)

    def mjpeg_url(self, channelno=None, typeno=None):
        """
        Return MJPEG streaming url

        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        if channelno is None:
            channelno = 0
        if typeno is None:
            typeno = 1
        cmd = 'mjpg/video.cgi?channel={0}&subtype={1}'.format(channelno, typeno)
        return '{0}{1}'.format(self._base_url, cmd)

    def mjpg_stream(self, channelno=None, typeno=None, path_file=None):
        """
        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        cmd = self.mjpeg_url(channelno=channelno, typeno=typeno)
        ret = self.command(cmd, stream=True)
        if path_file:
            try:
                with open(path_file, 'wb') as (out_file):
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug('%s MJPEG stream capture to file failed due to error: %s', self, repr(error))
                raise CommError(error)

        return ret.raw