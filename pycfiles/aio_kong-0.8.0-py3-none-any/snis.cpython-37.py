# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/snis.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 578 bytes
from .components import CrudComponent

class Snis(CrudComponent):
    """Snis"""

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