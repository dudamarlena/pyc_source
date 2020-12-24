# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/socialknife/__init__.py
# Compiled at: 2018-12-16 12:48:01
# Size of source mod 2**32: 1160 bytes
import asyncio, aiohttp, async_timeout
BASEURL = 'https://bastet.socialblade.com/{service}/lookup?query={query}'
HEADERS = {'authority':'bastet.socialblade.com', 
 'origin':'https://socialblade.com', 
 'accept':'*/*'}

class SocialKnife:

    def __init__(self, loop, session):
        self._loop = loop
        self._session = session

    async def get_count(self, service, query):
        url = BASEURL.format(service=service, query=query)
        data = ''
        try:
            async with async_timeout.timeout(5, loop=(self._loop)):
                header = HEADERS
                header['referer'] = self._generate_referer(service, query)
                response = await self._session.get(url, headers=header)
                data = await response.text()
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            try:
                print(error)
            finally:
                error = None
                del error

        return data.strip()

    def _generate_referer(self, service, query):
        if service is 'youtube':
            return 'https://socialblade.com/youtube/channel/{}'.format(query)
        return 'https://socialblade.com/{}/user/{}'.format(service, query)