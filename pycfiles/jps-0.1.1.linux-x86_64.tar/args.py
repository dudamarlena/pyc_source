# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/args.py
# Compiled at: 2016-06-11 06:32:43
import argparse
from .env import get_master_host
from .common import DEFAULT_PUB_PORT
from .common import DEFAULT_SUB_PORT
from .common import DEFAULT_RES_PORT
from .common import DEFAULT_REQ_PORT

class ArgumentParser(argparse.ArgumentParser):
    """
    Create ArgumentParser with args (host/subscriber_port/publisher_port)

    Example:

    >>> parser = jps.ArgumentParser(description='my program')
    >>> args = parser.parse_args()
    >>> args.host
    'localhost'
    >>> args.subscriber_port
    54321
    >>> args.publisher_port
    54320

    :param subscriber add subscriber_port (default: True)
    :param publisher add publisher_port (default: True)

    """

    def __init__(self, subscriber=True, publisher=True, service=False, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.add_argument('--host', type=str, help='fowarder host', default=get_master_host())
        self.add_argument('--prefix', type=str, help='add prefix for topics', default='')
        if subscriber:
            self.add_argument('--subscriber_port', type=int, help='subscriber port', default=DEFAULT_SUB_PORT)
        if publisher:
            self.add_argument('--publisher_port', type=int, help='publisher port', default=DEFAULT_PUB_PORT)
        if service:
            self.add_argument('--request_port', type=int, help='request port', default=DEFAULT_REQ_PORT)
            self.add_argument('--response_port', type=int, help='response port', default=DEFAULT_RES_PORT)