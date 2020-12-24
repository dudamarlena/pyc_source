# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/io/NestedYAMLLoader.py
# Compiled at: 2019-09-09 00:13:27
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

    def include(self, node):
        """
        Load from another YAML file, the additional YAML file path must be
        relative to the original YAML file.

        .. warning::

            Tested to work with loading a ``list``, and **not** work with
            loading a ``dict``.
        """
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as (f):
            return yaml.load(f, NestedYAMLLoader)


NestedYAMLLoader.add_constructor('!include', NestedYAMLLoader.include)