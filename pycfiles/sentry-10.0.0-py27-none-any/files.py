# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/files.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import zlib
from sentry import features, options
from sentry.models import MAX_FILE_SIZE

def compress_file(fp, level=6):
    compressor = zlib.compressobj(level)
    z_chunks = []
    chunks = []
    for chunk in fp.chunks():
        chunks.append(chunk)
        z_chunks.append(compressor.compress(chunk))

    return (
     ('').join(z_chunks) + compressor.flush(), ('').join(chunks))


def get_max_file_size(organization):
    """Returns the maximum allowed debug file size for this organization."""
    if features.has('organizations:large-debug-files', organization):
        return MAX_FILE_SIZE
    else:
        return options.get('system.maximum-file-size')