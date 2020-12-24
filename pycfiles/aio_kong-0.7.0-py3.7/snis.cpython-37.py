# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/snis.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 578 bytes
from .components import CrudComponent

class Snis(CrudComponent):
    __doc__ = 'Kong SNI API component'

    async def apply_json(self, data):
        """Apply a JSON data object for a service
        """
        if not isinstance(data, list):
            data = [
             data]
        result = []
        for entry in data:
            name = entry.pop('name')
            if await self.has(name):
                sni = await (self.update)(name, **entry)
            else:
                sni = await (self.create)(name=name, **entry)
            result.append(sni.data)

        return result