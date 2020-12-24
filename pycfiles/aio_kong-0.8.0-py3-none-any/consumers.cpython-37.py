# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/consumers.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 2456 bytes
from .auths import auth_factory
from .components import CrudComponent, KongError
from .plugins import KongEntityWithPlugins

class Consumers(CrudComponent):

    def wrap(self, data):
        return Consumer(self, data)

    async def apply_credentials(self, auths, consumer):
        for auth_data in auths:
            auth = auth_factory(consumer, auth_data['type'])
            await auth.create_or_update_credentials(auth_data['config'])

    async def apply_json(self, data):
        if not isinstance(data, list):
            data = [
             data]
        result = []
        for entry in data:
            if not isinstance(entry, dict):
                raise KongError('dictionary required')
            groups = entry.pop('groups', [])
            auths = entry.pop('auths', [])
            udata = entry.copy()
            id_ = udata.pop('id', None)
            username = None
            if not id_:
                username = udata.pop('username', None)
                if not username:
                    raise KongError('Consumer username or id is required')
                else:
                    uid = id_ or 
                    try:
                        consumer = await self.get(uid)
                    except KongError as exc:
                        try:
                            if exc.status == 404:
                                consumer = await (self.create)(**entry)
                            else:
                                raise
                        finally:
                            exc = None
                            del exc

                    else:
                        if entry:
                            consumer = await (self.update)(uid, **udata)
                acls = await consumer.acls.get_list()
                current_groups = dict(((a['group'], a) for a in acls))
                for group in groups:
                    if group not in current_groups:
                        await consumer.acls.create(group=group)
                    else:
                        current_groups.pop(group)

                for acl in current_groups.values():
                    await consumer.acls.delete(acl['id'])

                await self.apply_credentials(auths, consumer)
                result.append(consumer.data)

        return result


class Consumer(KongEntityWithPlugins):

    @property
    def username(self):
        return self.data.get('username')

    @property
    def acls(self):
        return CrudComponent(self, 'acls')

    @property
    def jwts(self):
        return auth_factory(self, 'jwt')

    @property
    def keyauths(self):
        return auth_factory(self, 'key-auth')

    @property
    def basicauths(self):
        return auth_factory(self, 'basic-auth')