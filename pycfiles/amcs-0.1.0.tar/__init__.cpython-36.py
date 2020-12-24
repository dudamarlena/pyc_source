# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/__init__.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 1174 bytes
from .exceptions import AmcrestError, CommError, LoginError
from .http import Http

class AmcrestCamera(object):
    """AmcrestCamera"""

    def __init__(self, host, port, user, password, verbose=True, protocol='http', retries_connection=None, timeout_protocol=None):
        super(AmcrestCamera, self).__init__()
        self.camera = Http(host=host,
          port=port,
          user=user,
          password=password,
          verbose=verbose,
          protocol=protocol,
          retries_connection=retries_connection,
          timeout_protocol=timeout_protocol)