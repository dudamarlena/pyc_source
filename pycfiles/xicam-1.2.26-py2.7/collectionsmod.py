# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\modpkgs\collectionsmod.py
# Compiled at: 2018-08-27 17:21:06
from collections import OrderedDict
import yaml

class UnsortableList(list):

    def sort(self, *args, **kwargs):
        pass


class UnsortableOrderedDict(OrderedDict):

    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))


yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)