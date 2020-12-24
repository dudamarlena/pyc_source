# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/s3iotools-project/s3iotools/compat.py
# Compiled at: 2019-05-19 22:48:53
"""
For Python2/3 compatible.

- The ``gzip.compress``, ``gzip.decompress`` function are not implemented in Python2.7.
"""
import gzip
from six import PY2, PY3, StringIO
if PY2:

    def gzip_compress(data, compresslevel=9):
        """Compress data in one shot and return the compressed string.
        Optional argument is the compression level, in range of 0-9.
        """
        buf = StringIO()
        with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=compresslevel) as (f):
            f.write(data)
        return buf.getvalue()


    def gzip_decompress(data):
        """Decompress a gzip compressed string in one shot.
        Return the decompressed string.
        """
        with gzip.GzipFile(fileobj=StringIO(data)) as (f):
            return f.read()


elif PY3:
    gzip_compress = gzip.compress
    gzip_decompress = gzip.decompress
else:
    raise EnvironmentError