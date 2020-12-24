# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/examples/nameko/services.py
# Compiled at: 2018-12-16 19:40:16
# Size of source mod 2**32: 999 bytes
from dis import dis
from io import StringIO
from nameko.web.handlers import http

class IntrospectiveService:
    name = 'introspective_service'

    @http('GET', '/introspective')
    def do_a_thing(self, _):
        with StringIO() as (output):
            dis((self.do_a_thing), file=output)
            return str(output.getvalue())


class HotdogService:
    name = 'hotdog_service'

    @http('POST', '/hotdog')
    def order_a_hotdog(self, _):
        return "One hotdog, comin' up!"