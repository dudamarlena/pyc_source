# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/__init__.py
# Compiled at: 2020-01-12 12:29:08
# Size of source mod 2**32: 1226 bytes
from .exceptions import AmcrestError, CommError, LoginError
from .http import Http

class AmcrestCamera(object):
    __doc__ = 'Amcrest camera object implementation.'

    def __init__(self, host, port, user, password, verbose=True, protocol='http', ssl_verify=True, retries_connection=None, timeout_protocol=None):
        super(AmcrestCamera, self).__init__()
        self.camera = Http(host=host,
          port=port,
          user=user,
          password=password,
          verbose=verbose,
          protocol=protocol,
          ssl_verify=ssl_verify,
          retries_connection=retries_connection,
          timeout_protocol=timeout_protocol)