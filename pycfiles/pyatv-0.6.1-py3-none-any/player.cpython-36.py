# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/airplay/player.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 3001 bytes
"""Play media on a device by sending an URL."""
import logging, asyncio, plistlib
from pyatv import exceptions
_LOGGER = logging.getLogger(__name__)
AIRPLAY_PORT = 7000
TIMEOUT = 10

class AirPlayPlayer:
    __doc__ = 'This class helps with playing media from an URL.'

    def __init__(self, loop, session, address, port=7000):
        """Initialize a new AirPlay instance."""
        self.loop = loop
        self.address = address
        self.session = session
        self.port = port

    async def play_url(self, url, position=0):
        """Play media from an URL on the device."""
        headers = {'User-Agent':'MediaControl/1.0', 
         'Content-Type':'application/x-apple-binary-plist'}
        body = {'Content-Location':url,  'Start-Position':position}
        address = self._url(self.port, 'play')
        _LOGGER.debug('AirPlay %s to %s', url, address)
        resp = None
        try:
            resp = await self.session.post(address,
              headers=headers, data=plistlib.dumps(body, fmt=(plistlib.FMT_BINARY)),
              timeout=TIMEOUT)
            await self._wait_for_media_to_end()
        finally:
            if resp is not None:
                resp.close()

    def _url(self, port, command):
        return 'http://{0}:{1}/{2}'.format(self.address, port, command)

    async def _wait_for_media_to_end(self):
        address = self._url(self.port, 'playback-info')
        attempts = 5
        video_started = False
        while True:
            info = None
            try:
                info = await self.session.get(address)
                data = await info.content.read()
                if info.status == 403:
                    raise exceptions.NoCredentialsError('device authentication required')
                _LOGGER.debug('Playback-info (%d): %s', info.status, data)
                parsed = plistlib.loads(data)
                if 'duration' in parsed:
                    video_started = True
                    attempts = -1
                else:
                    video_started = False
                if attempts >= 0:
                    attempts -= 1
                if not video_started:
                    if attempts < 0:
                        _LOGGER.debug('media playback ended')
                        break
            finally:
                if info is not None:
                    info.close()

            await asyncio.sleep(1, loop=(self.loop))