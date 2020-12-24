# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/base.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 1776 bytes
import json, asyncio, aiohttp, logging
logger = logging.getLogger(__name__)

class DiscordObject:
    __doc__ = 'Base class for discord objects.'

    @classmethod
    async def from_api_res(cls, coro_or_json_or_str):
        """Parses a discord API response"""
        if coro_or_json_or_str is None:
            return
        json_obj = coro_or_json_or_str
        if isinstance(coro_or_json_or_str, str):
            json_obj = json.loads(coro_or_json_or_str)
        else:
            if asyncio.iscoroutine(coro_or_json_or_str):
                json_obj = await coro_or_json_or_str()
            elif isinstance(coro_or_json_or_str, aiohttp.ClientResponse):
                json_obj = await coro_or_json_or_str.json()
        if isinstance(json_obj, list):
            lst = []
            for item in json_obj:
                result = cls()
                for key, value in item.items():
                    if hasattr(result, key):
                        await result._from_api_ext(key, value)

                lst.append(result)

            return lst
        if isinstance(json_obj, dict):
            result = cls()
            for key, value in json_obj.items():
                if hasattr(result, key):
                    await result._from_api_ext(key, value)

            return result
        raise ValueError('it must be a dictionary or a list.')

    async def _from_api_ext(self, key, value):
        """Api response decoding extensions, called automatically by DiscordObject.from_api_res().
        Used if the class contains a attribute that it's a class and must be initialized with info,
        also used if the class contains an array of classes as attribute."""
        setattr(self, key, value)


__all__ = [
 'DiscordObject']