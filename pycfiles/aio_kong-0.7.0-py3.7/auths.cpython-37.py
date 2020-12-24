# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/auths.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 2051 bytes
from .components import CrudComponent

def auth_factory(consumer, auth_type):
    known_types = {'basic-auth':BasicAuth, 
     'key-auth':KeyAuth}
    constructor = known_types.get(auth_type, ConsumerAuth)
    return constructor(consumer, auth_type)


class ConsumerAuth(CrudComponent):
    unique_field = None

    @property
    def url(self) -> str:
        return f"{self.root.url}/{self.name}"

    async def get_existing_id(self, creds_config):
        if not self.unique_field:
            raise NotImplementedError('Existence check not implemented for this type of                 authentication')
        cur_unique = creds_config[self.unique_field]
        try:
            return next((cred for cred in await self.get_list() if cred[self.unique_field] == cur_unique))['id']
        except StopIteration:
            return

    async def create_or_update_credentials(self, creds_config):
        existing_id = await self.get_existing_id(creds_config)
        if existing_id:
            await self.update_credentials(id_=existing_id, data=creds_config)
        else:
            await self.create_credentials(data=creds_config)

    async def update_credentials(self, id_, **kw):
        url = f"{self.url}/{id_}"
        return await (self.cli.execute)(
 url,
 'patch', headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
         wrap=self.wrap, **kw)

    async def create_credentials(self, **kw):
        return await (self.cli.execute)(
 self.url,
 'post', headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
         wrap=self.wrap, **kw)

    async def get_or_create(self):
        secrets = await self.get_list(limit=1)
        if secrets:
            return secrets[0]
        return await self.create()


class BasicAuth(ConsumerAuth):
    unique_field = 'username'


class KeyAuth(ConsumerAuth):
    unique_field = 'key'