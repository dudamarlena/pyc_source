# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\preview.py
# Compiled at: 2018-03-17 15:28:43
# Size of source mod 2**32: 982 bytes
from weebapi.image_type import ImageType
from weebapi.errors import *

class Preview(object):

    def __init__(self, snowflake: str, url: str, file_type: str, base_type: str, image_type: str, client):
        self.client = client
        self.snowflake = snowflake
        self.url = url
        self.image_type = ImageType(image_type, self.client)
        self.base_type = base_type
        self.file_type = file_type

    def __str__(self):
        return self.url

    @classmethod
    def parse(cls, response, client):
        status = response.get('status', 200)
        if status != 200:
            raise FileNotFoundError('This resource does not exist or you are not allowed to access.')
        try:
            data = cls(response['id'], response['url'], response['fileType'], response['baseType'], response['type'], client)
        except KeyError:
            raise WeirdResponse
        else:
            return data