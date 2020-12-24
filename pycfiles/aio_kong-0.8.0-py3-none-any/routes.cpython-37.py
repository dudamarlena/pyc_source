# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/routes.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 1201 bytes
from itertools import zip_longest
from .components import CrudComponent
from .plugins import KongEntityWithPlugins
from .utils import as_list

class Routes(CrudComponent):
    """Routes"""
    Entity = KongEntityWithPlugins

    async def delete(self, id_):
        route = self.wrap({'id': id_})
        await route.plugins.delete_all()
        return await super().delete(id_)

    async def apply_json(self, data):
        if not isinstance(data, list):
            data = [
             data]
        routes = await self.get_list()
        result = []
        for d, route in zip_longest(data, routes):
            if not d:
                if route:
                    await self.delete(route.id)
                    continue
                plugins = d.pop('plugins', [])
                as_list('hosts', d)
                as_list('paths', d)
                as_list('methods', d)
                if not route:
                    route = await (self.create)(**d)
                else:
                    route = await (self.update)((route.id), **d)
                route.data['plugins'] = await route.plugins.apply_json(plugins)
                result.append(route.data)

        return result