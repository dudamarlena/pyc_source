# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/services.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 2142 bytes
from .components import CrudComponent, KongError
from .plugins import KongEntityWithPlugins
from .routes import Routes
from .utils import local_ip
REMOVE = frozenset(('absent', 'remove'))
LOCAL_HOST = frozenset(('localhost', '127.0.0.1'))

class Service(KongEntityWithPlugins):
    __doc__ = 'Object representing a Kong service\n    '

    @property
    def routes(self):
        return Routes(self)

    @property
    def host(self):
        return self.data.get('host')


class Services(CrudComponent):
    __doc__ = 'Kong Services\n    '
    Entity = Service

    async def delete(self, id_):
        srv = self.wrap({'id': id_})
        await srv.routes.delete_all()
        await srv.plugins.delete_all()
        return await super().delete(id_)

    async def apply_json(self, data):
        """Apply a JSON data object for a service
        """
        if not isinstance(data, list):
            data = [
             data]
        result = []
        for entry in data:
            if not isinstance(entry, dict):
                raise KongError('dictionary required')
            else:
                ensure = entry.pop('ensure', None)
                name = entry.pop('name', None)
                routes = entry.pop('routes', [])
                plugins = entry.pop('plugins', [])
                host = entry.pop('host', None)
                if host in LOCAL_HOST:
                    host = local_ip()
                assert name, 'Service name is required'
            if ensure in REMOVE:
                if await self.has(name):
                    await self.delete(name)
                    continue
                config = entry.pop('config', None)
                if isinstance(config, dict):
                    entry.update(config)
                elif await self.has(name):
                    srv = await (self.update)(name, host=host, **entry)
                else:
                    srv = await (self.create)(name=name, host=host, **entry)
                srv.data['routes'] = await srv.routes.apply_json(routes)
                srv.data['plugins'] = await srv.plugins.apply_json(plugins)
                result.append(srv.data)

        return result