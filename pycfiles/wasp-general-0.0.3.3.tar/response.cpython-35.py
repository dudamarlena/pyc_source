# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/response.py
# Compiled at: 2017-06-28 15:47:15
# Size of source mod 2**32: 2588 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type, verify_value
from wasp_general.network.web.proto import WWebResponseProto
from wasp_general.network.web.headers import WHTTPHeaders

class WWebResponse(WWebResponseProto):
    __doc__ = ' Simple :class:`.WWebResponseProto` implementation\n\t'

    @verify_type(status=(int, None), headers=(WHTTPHeaders, None), response_data=(bytes, None))
    @verify_value(status=lambda x: x is None or x > 0)
    def __init__(self, status=None, headers=None, response_data=None):
        """ Create new response

                :param status: response status code
                :param headers: response headers
                :param response_data: response data
                """
        WWebResponseProto.__init__(self)
        self._WWebResponse__status = status
        self._WWebResponse__headers = headers
        self._WWebResponse__response_data = response_data
        self._WWebResponse__pushed_responses = []

    def status(self):
        """ :meth:`.WWebResponseProto.status` method implementation
                """
        return self._WWebResponse__status

    def headers(self):
        """ :meth:`.WWebResponseProto.headers` method implementation
                """
        return self._WWebResponse__headers

    def response_data(self):
        """ :meth:`.WWebResponseProto.response_data` method implementation
                """
        return self._WWebResponse__response_data

    @verify_type(response=WWebResponseProto)
    def __push__(self, *responses):
        """ Save responses to push

                :param responses: responses to push
                :return:
                """
        self._WWebResponse__pushed_responses.extend(responses)

    def __pushed_responses__(self):
        """ :meth:`.WWebResponseProto.__pushed_responses__` method implementation
                """
        return tuple(self._WWebResponse__pushed_responses)