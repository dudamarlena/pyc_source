# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/io/NestedYAMLLoader.py
# Compiled at: 2020-05-01 05:18:06
# Size of source mod 2**32: 1110 bytes
"""
This module provides a YAML loader with ``!include`` directive so that other
YAML files can be included in the input YAML file.
"""
import yaml, os

class NestedYAMLLoader(yaml.SafeLoader):
    __doc__ = '\n    An extension to the standard ``SafeLoader`` to allow the inclusion of\n    another YAML file.\n    '

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def include--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _root
               10  LOAD_FAST                'self'
               12  LOAD_METHOD              construct_scalar
               14  LOAD_FAST                'node'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'filename'

 L.  36        22  LOAD_GLOBAL              open
               24  LOAD_FAST                'filename'
               26  LOAD_STR                 'r'
               28  CALL_FUNCTION_2       2  ''
               30  SETUP_WITH           58  'to 58'
               32  STORE_FAST               'f'

 L.  37        34  LOAD_GLOBAL              yaml
               36  LOAD_METHOD              load
               38  LOAD_FAST                'f'
               40  LOAD_GLOBAL              NestedYAMLLoader
               42  CALL_METHOD_2         2  ''
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH       30  '30'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 46


NestedYAMLLoader.add_constructor('!include', NestedYAMLLoader.include)