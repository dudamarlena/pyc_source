# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/clonable.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 228 bytes


class Clonable(object):

    def clone(self):
        cloned_obj = self.__class__()
        cloned_obj._on_clone_creation(self)
        return cloned_obj

    def _on_clone_creation(self, original):
        raise NotImplemented