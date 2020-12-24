# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/routes.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 1201 bytes
from itertools import zip_longest
from .components import CrudComponent
from .plugins import KongEntityWithPlugins
from .utils import as_list

class Routes(CrudComponent):
    __doc__ = 'Kong Routes\n\n    Routes are always associated with a Service\n    '
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