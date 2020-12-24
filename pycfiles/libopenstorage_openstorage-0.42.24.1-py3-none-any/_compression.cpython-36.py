# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/_compression.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 1695 bytes
from grpc._cython import cygrpc
NoCompression = cygrpc.CompressionAlgorithm.none
Deflate = cygrpc.CompressionAlgorithm.deflate
Gzip = cygrpc.CompressionAlgorithm.gzip
_METADATA_STRING_MAPPING = {NoCompression: 'identity', 
 Deflate: 'deflate', 
 Gzip: 'gzip'}

def _compression_algorithm_to_metadata_value(compression):
    return _METADATA_STRING_MAPPING[compression]


def compression_algorithm_to_metadata(compression):
    return (
     cygrpc.GRPC_COMPRESSION_REQUEST_ALGORITHM_MD_KEY,
     _compression_algorithm_to_metadata_value(compression))


def create_channel_option(compression):
    if compression:
        return ((cygrpc.GRPC_COMPRESSION_CHANNEL_DEFAULT_ALGORITHM, int(compression)),)
    else:
        return ()


def augment_metadata(metadata, compression):
    if not metadata:
        if not compression:
            return
    base_metadata = tuple(metadata) if metadata else ()
    compression_metadata = (compression_algorithm_to_metadata(compression),) if compression else ()
    return base_metadata + compression_metadata


__all__ = ('NoCompression', 'Deflate', 'Gzip')