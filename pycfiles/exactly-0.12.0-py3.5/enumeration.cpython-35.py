# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/enumeration.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 787 bytes
from typing import List
from exactly_lib.test_suite.structure import TestSuiteHierarchy

class SuiteEnumerator:
    __doc__ = '\n    Determines in what order the suites should be executed.\n    '

    def apply(self, suite: TestSuiteHierarchy) -> List[TestSuiteHierarchy]:
        """
        Enumerates all suites contained in the argument.
        :param suite: Root of suites to be enumerated.
        :return: All suites in the given suite hierarchy.
        """
        raise NotImplementedError()


class DepthFirstEnumerator(SuiteEnumerator):

    def apply(self, suite: TestSuiteHierarchy) -> List[TestSuiteHierarchy]:
        ret_val = []
        for sub_suite in suite.sub_test_suites:
            ret_val += self.apply(sub_suite)

        ret_val.append(suite)
        return ret_val