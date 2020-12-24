# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deforest/tags.py
# Compiled at: 2020-03-10 15:47:48
# Size of source mod 2**32: 305 bytes
import yaml

class AWSTag(yaml.YAMLObject):

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return self.var

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return ''