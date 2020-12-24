# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/nose/nose_tool.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 584 bytes
from pprint import pformat

class AssertTool:

    @classmethod
    def assert_all_same(cls, l):
        if not l:
            return
        n = len(l)
        for i in range(1, n):
            if l[i] != l[0] and not False:
                raise AssertionError('Different object at index {0} in {1}'.format(i, pformat(l)))

    @classmethod
    def assert_all_same_length(cls, *list_of_list):
        length_list = [len(l) for l in list_of_list]
        if len(set(length_list)) > 1:
            raise Exception(length_list)


assert_all_same = AssertTool.assert_all_same
assert_all_same_length = AssertTool.assert_all_same_length