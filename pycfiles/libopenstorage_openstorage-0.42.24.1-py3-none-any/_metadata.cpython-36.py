# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/beta/_metadata.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 1606 bytes
"""API metadata conversion utilities."""
import collections
_Metadatum = collections.namedtuple('_Metadatum', ('key', 'value'))

def _beta_metadatum(key, value):
    beta_key = key if isinstance(key, (bytes,)) else key.encode('ascii')
    beta_value = value if isinstance(value, (bytes,)) else value.encode('ascii')
    return _Metadatum(beta_key, beta_value)


def _metadatum(beta_key, beta_value):
    key = beta_key if isinstance(beta_key, (str,)) else beta_key.decode('utf8')
    if isinstance(beta_value, (str,)) or key[-4:] == '-bin':
        value = beta_value
    else:
        value = beta_value.decode('utf8')
    return _Metadatum(key, value)


def beta(metadata):
    if metadata is None:
        return ()
    else:
        return tuple(_beta_metadatum(key, value) for key, value in metadata)


def unbeta(beta_metadata):
    if beta_metadata is None:
        return ()
    else:
        return tuple(_metadatum(beta_key, beta_value) for beta_key, beta_value in beta_metadata)