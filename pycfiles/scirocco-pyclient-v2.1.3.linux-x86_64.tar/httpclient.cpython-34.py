# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/httpclient.py
# Compiled at: 2016-11-19 16:40:57
# Size of source mod 2**32: 338 bytes
from sciroccoclient.clientfactory import ClientFactory
from sciroccoclient.exceptions import SciroccoInitParamsError

class HTTPClient:

    def __new__(cls, *args, **kwargs):
        try:
            return ClientFactory().get_http_client(args[0], args[1], args[2])
        except IndexError:
            raise SciroccoInitParamsError