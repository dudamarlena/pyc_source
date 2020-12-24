# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/__init__.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 1174 bytes
from .exceptions import AmcrestError, CommError, LoginError
from .http import Http

class AmcrestCamera(object):
    __doc__ = 'Amcrest camera object implementation.'

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