# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/guyskk/anyant/weirb/src/weirb/project-template/echo/services/echo.py
# Compiled at: 2018-06-30 10:51:08
# Size of source mod 2**32: 796 bytes
from validr import T
from weirb import require, route, raises
from weirb.error import HrpcError

class EchoError(HrpcError):
    __doc__ = 'Echo Error'
    status = 400
    code = 'Echo.Error'


class EchoService:
    echo_times = require('config.echo_times')

    @raises(EchoError)
    async def method_echo(self, text: T.str.default('')) -> T.dict(text=(T.str)):
        """A echo method"""
        if text == 'error':
            raise EchoError('I echo an error')
        text = text * self.echo_times
        return dict(text=text)

    @route.get('/echo')
    @route('/echo/echo', methods=['GET', 'POST'])
    async def get_echo(self):
        text = self.request.query.get('text') or ''
        self.response.json(dict(text=(text * self.echo_times)))