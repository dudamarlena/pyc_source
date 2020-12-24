# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\client.py
# Compiled at: 2020-04-19 14:32:46
# Size of source mod 2**32: 1712 bytes
import asyncio
from asyncio import CancelledError
from .apis import bans, images, kumo, music
from .http import HttpClient

class Client:
    __doc__ = '\n    .. _aiohttp session: https://aiohttp.readthedocs.io/en/stable/client_reference.html#client-session\n\n    Client object for KSOFT.SI API.\n    Represents a client connection that connects to ksoft.si.\n\n    Parameters\n    -------------\n    api_key: :class:`str`\n        Your ksoft.si api token.\n        Specify different base url.\n    **loop: asyncio loop\n        Your asyncio loop.\n    '

    def __init__(self, api_key: str, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self.api_key = api_key
        self.http = HttpClient(authorization=(self.api_key), loop=(self._loop))
        self._bans_api = bans.Bans(self)
        self._images_api = images.Images(self)
        self._kumo_api = kumo.Kumo(self)
        self._music_api = music.Music(self)

    async def close(self):
        """
        Closes the client. This action will prevent
        the client from making any more requests to the API.
        """
        if self._bans_api._listener_task is not None:
            try:
                self._bans_api._listener_task.cancel()
            except CancelledError:
                pass

        await self.http.close()

    @property
    def bans(self) -> bans.Bans:
        return self._bans_api

    @property
    def images(self) -> images.Images:
        return self._images_api

    @property
    def kumo(self) -> kumo.Kumo:
        return self._kumo_api

    @property
    def music(self) -> music.Music:
        return self._music_api