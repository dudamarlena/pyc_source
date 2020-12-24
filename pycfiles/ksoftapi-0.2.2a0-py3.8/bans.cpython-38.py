# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\apis\bans.py
# Compiled at: 2020-04-19 14:32:46
# Size of source mod 2**32: 4472 bytes
import logging
from asyncio import CancelledError, sleep
from itertools import count
from time import time
from ..errors import APIError, NoResults
from ..events import BanUpdateEvent
from ..models import BanInfo, PaginatorListing
logger = logging.getLogger('ksoft/bans')

class Bans:

    def __init__(self, client):
        self._client = client
        self._hooks = []
        self._last_update = time() - 600
        self._listener_task = None

    async def __aiter__(self):
        for page in count(start=1):
            r = await self._client.http.get('/bans/list', params={'page': page})
            for ban in r['data']:
                yield BanInfo(ban)

            if r['next_page'] is None:
                break

    async def _ban_checker(self):
        while self._hooks:
            try:
                try:
                    r = await self._client.http.get('/bans/updates', params={'timestamp': self._last_update})
                except APIError as exc:
                    try:
                        logger.error('The API responded with an error while fetching ban updates.', exc_info=exc)
                    finally:
                        exc = None
                        del exc

                else:
                    self._last_update = r['current_timestamp']
                    for b in r['data']:
                        await self._dispatch_ban_event(BanUpdateEvent(b))

            finally:
                await sleep(300)

        try:
            self._listener_task.cancel()
        except CancelledError:
            pass
        else:
            self._listener_task = None

    async def _dispatch_ban_event(self, event):
        logger.debug('Dispatching event of type %s to %d hooks', event.__class__.__name__, len(self._hooks))
        for hook in self._hooks:
            try:
                await hook(event)
            except Exception as exc:
                try:
                    logger.warning('Event hook "%s" encountered an exception', (hook.__name__), exc_info=exc)
                finally:
                    exc = None
                    del exc

    def subscribe(self, hook):
        if hook not in self._hooks:
            logger.debug('Registered ban event hook with name %s', hook.__name__)
            self._hooks.append(hook)
        if len(self._hooks) > 0:
            if self._listener_task is None:
                self._listener_task = self._client._loop.create_task(self._ban_checker)

    def unsubscribe(self, hook):
        if hook in self._hooks:
            logger.debug('Unregistered ban event hook with name %s', hook.__name__)
            self._hooks.remove(hook)

    async def count(self) -> int:
        r = await self._client.http.get('/bans/list', params={'per_page': 1})
        return r['ban_count']

    async def paginator(self, page: int=1, per_page: int=20):
        r = await self._client.http.get('/bans/list', params={'per_page':per_page,  'page':page})
        return PaginatorListing(r)

    async def add(self, user_id: int, reason: str, proof: str, mod=None, user_name=None, user_discriminator=None, appeal_possible=None) -> bool:
        payload = {'user':user_id, 
         'reason':reason, 
         'proof':proof}
        if mod is not None:
            payload['mod'] = mod
        if user_name is not None:
            payload['user_name'] = user_name
        if user_discriminator is not None:
            payload['user_discriminator'] = user_discriminator
        if appeal_possible is not None:
            payload['appeal_possible'] = appeal_possible
        r = await self._client.http.post('/bans/add', data=payload)
        return r['success']

    async def check(self, user_id: int) -> bool:
        r = await self._client.http.get('/bans/check', params={'user': user_id})
        return r['is_banned']

    async def info(self, user_id: int) -> BanInfo:
        """|coro|

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to get ban information for.

        Returns
        -------
        :class:`BanInfo`

        Raises
        ------
        :class:`NoResults`
        """
        r = await self._client.http.get('/bans/info', params={'user': user_id})
        if 'code' in r:
            if r['code'] == 404:
                raise NoResults
        return BanInfo(r)

    async def delete(self, user_id: int, force: bool=False) -> bool:
        r = await self._client.http.delete('/bans/delete', params={'user':user_id,  'force':force})
        return r['done']