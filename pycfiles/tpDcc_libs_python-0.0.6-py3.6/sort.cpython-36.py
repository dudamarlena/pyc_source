# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/sort.py
# Compiled at: 2020-05-02 23:38:35
# Size of source mod 2**32: 2826 bytes
"""
Utility methods related to sort algorithms
"""
from __future__ import print_function, division, absolute_import

class QuickNumbersListSort(object):
    __doc__ = '\n    Fast method to sort lists of numbers\n    '

    def __init__(self, list_of_numbers):
        self.list_of_numbers = list_of_numbers
        self.follower_list = list()

    def _sort(self, list_of_numbers, follower_list=[]):
        less = list()
        equal = list()
        greater = list()
        if follower_list:
            less_follow = list()
            equal_follow = list()
            greater_follow = list()
        else:
            count = len(list_of_numbers)
            if count > 1:
                pivot = list_of_numbers[0]
                for i in range(count):
                    value = list_of_numbers[i]
                    if follower_list:
                        follower_value = follower_list[i]
                    if value < pivot:
                        less.append(value)
                        if follower_list:
                            less_follow.append(follower_value)
                    if value == pivot:
                        equal.append(value)
                        if follower_list:
                            equal_follow.append(follower_value)
                        if value > pivot:
                            greater.append(value)
                            if follower_list:
                                greater_follow.append(follower_value)

                if not self.follower_list:
                    return self._sort(less) + equal + self._sort(greater)
                else:
                    less_list_of_numbers, less_follower_list = self._sort(less, less_follow)
                    greater_list_of_numbers, greater_follower_list = self._sort(greater, greater_follow)
                    list_of_numbers = less_list_of_numbers + equal + greater_list_of_numbers
                    follower_list = less_follower_list + equal_follow + greater_follower_list
                    return (
                     list_of_numbers, follower_list)
            else:
                if not self.follower_list:
                    return list_of_numbers
                else:
                    return (
                     list_of_numbers, follower_list)

    def set_follower_list(self, list_of_anything):
        """
        This list must match the length of the list given when the class was initialized
        :param list_of_anything: list
        """
        self.follower_list = list_of_anything

    def run(self):
        """
        If not follower list is supplied, return number list sorted else return number list and follower list
        :return:  variant, list || list, list
        """
        if not self.list_of_numbers:
            return
        else:
            if self.follower_list:
                if len(self.follower_list) != len(self.list_of_numbers):
                    return
            return self._sort(self.list_of_numbers, self.follower_list)