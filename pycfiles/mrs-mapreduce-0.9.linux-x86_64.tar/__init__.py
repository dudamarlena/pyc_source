# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/__init__.py
# Compiled at: 2012-10-25 19:11:40
"""Mrs: MapReduce - a Simple implementation

Your Mrs MapReduce program might look something like this:

import mrs

class Mrs_Program(mrs.MapReduce):
    def map(key, value):
        yield newkey, newvalue

    def reduce(key, values):
        yield newvalue

if __name__ == '__main__':
    mrs.main(Mrs_Program)
"""
import logging, sys
logger = logging.getLogger('mrs')
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stderr)
format = '%(asctime)s: %(levelname)s: %(message)s'
formatter = logging.Formatter(format)
handler.setFormatter(formatter)
logger.addHandler(handler)
from . import registry
from . import version
from .fileformats import HexWriter, TextWriter, BinWriter, ZipWriter
from .main import main
from .mapreduce import MapReduce, IterativeMR
from .serializers import Serializer, output_serializers, raw_serializer, str_serializer, int_serializer, make_struct_serializer, make_primitive_serializer, make_protobuf_serializer
__version__ = version.__version__
__all__ = [
 'MapReduce', 'main', 'logger', 'BinWriter', 'HexWriter',
 'TextWriter', 'Serializer', 'output_serializers', 'raw_serializer',
 'str_serializer', 'int_serializer', 'make_struct_serializer',
 'make_primitive_serializer', 'make_protobuf_serializer']