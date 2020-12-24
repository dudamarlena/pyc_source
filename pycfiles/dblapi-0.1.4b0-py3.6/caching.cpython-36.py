# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dblapi\caching.py
# Compiled at: 2018-03-18 13:07:26
# Size of source mod 2**32: 3431 bytes
import datetime

class Cacher:

    def __init__(self, client, update_function, store_for: int=10, is_dict: bool=True, **kwargs):
        self.client = client
        self.store = {} if is_dict else []
        self.store_for = datetime.timedelta(seconds=store_for)
        self.expiry = datetime.datetime.utcnow()
        self.kwargs = kwargs
        self.update_cache = update_function

    def set_expiry(self):
        self.expiry = datetime.datetime.utcnow() + self.store_for

    @property
    async def get(self):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        return self.store

    def __set__(self, instance, value):
        self.store.clear()
        self.store = value
        self.set_expiry()

    async def get_val(self, key):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        return self.store[key]

    async def remove_val(self, key):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        del self.store[key]

    async def append(self, value):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        self.store.append(value)

    async def update(self, key, value):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        self.store.update({key: value})

    async def is_in(self, key):
        if datetime.datetime.utcnow() > self.expiry:
            self.store.clear()
            self.store = await self.update_cache(self.client, self.kwargs)
            self.set_expiry()
        if key in self.store:
            return True
        else:
            return False