# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/core/Compression/base.py
# Compiled at: 2014-08-28 11:28:54


class CompressionEngine(object):
    """Base class for Compression Engines"""

    def __init__(self, compress_type='Non-defined'):
        self.type = compress_type
        self.compressor = None
        self.decompressor = None
        return

    def __repr__(self):
        return 'Compresser of type %s.' % str(self.type)

    def setup(self, compressor, decompressor):
        """ Setup the compression functionality based on the compression type """
        self.compressor = compressor
        self.decompressor = decompressor

    def compress(self, data):
        """ Apply the compression """
        if self.compressor is None:
            raise ValueError('No compression defined.')
        else:
            return self.compressor(data)
        return

    def decompress(self, compressed_data):
        """ Apply the decompression """
        if self.decompressor is None:
            raise ValueError('No compression defined.')
        else:
            return self.decompressor(compressed_data)
        return


class Compressor(object):
    """Base class for Compressors"""

    def __init__(self):
        super(Compressor, self).__init__()

    def compress(self, data):
        return data

    def __call__(self, data):
        return self.compress(data)


class Decompressor(object):
    """Base class for Decompressor"""

    def __init__(self):
        super(Decompressor, self).__init__()

    def decompress(self, data):
        return data

    def __call__(self, data):
        return self.decompress(data)