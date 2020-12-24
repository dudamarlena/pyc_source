# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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