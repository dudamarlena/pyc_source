# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/codecs.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 382 bytes


class BaseParser(object):
    media_type = None

    def parse(self, stream, media_type=None, parser_context=None):
        raise NotImplementedError('.parse() must be overridden.')


class JSONParser(BaseParser):
    media_type = 'application/json'

    async def parse(self, request):
        data = await request.json()
        return data


PARSER_MEDIA_TYPE = (
 JSONParser(),)