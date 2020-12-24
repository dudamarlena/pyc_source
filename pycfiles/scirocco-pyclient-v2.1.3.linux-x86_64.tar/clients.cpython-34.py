# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/sciroccoclient/clients.py
# Compiled at: 2016-11-22 16:46:46
# Size of source mod 2**32: 655 bytes
from sciroccoclient.clientfactory import ClientFactory
from sciroccoclient.exceptions import SciroccoInitParamsError

class HTTPClient:
    __doc__ = '\n        :param api_url: string\n            scirocco instance to connect to.\n        :param node_id: string\n            identify this instance as a node of the system.\n        :param auth_token: string\n            Token that authorizes this node to access the server.\n        :return: Client intance.\n    '

    def __new__(cls, *args, **kwargs):
        try:
            return ClientFactory().get_http_client(args[0], args[1], args[2])
        except IndexError:
            raise SciroccoInitParamsError