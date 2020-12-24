# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/delta.py
# Compiled at: 2018-08-22 07:31:57
# Size of source mod 2**32: 685 bytes


class Delta(object):

    def __init__(self, diff_item, current_state, new_state, **kwargs):
        self.diff_item = diff_item
        self.current_state = current_state
        self.new_state = new_state
        self.kwargs = kwargs

    def __repr__(self):
        return '{kls} ({s})'.format(kls=(self.__class__.__name__), s=(self.__str__()))

    def __str__(self):
        return '{d}({c} -> {n})'.format(d=(str(self.diff_item).replace('Diff', '')), c=(self.current_state),
          n=(self.new_state))