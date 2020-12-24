# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\image_type.py
# Compiled at: 2018-03-17 16:25:23
# Size of source mod 2**32: 738 bytes


class ImageType(object):

    def __init__(self, name: str, client):
        """
        WIP
        :param name:
        :param client:
        """
        self.name = name
        self.client = client

    def __str__(self):
        return self.name

    def __get__(self, instance, owner):
        return self.name

    @property
    async def get_preview(self):
        g = await self.client.request.get((str(self.client.route.types)), params={'nsfw':'true', 
         'preview':'true'})
        for p in g['preview']:
            if p['type'] == self.name:
                return Preview.parse(p, self.client)

        raise FileNotFoundError