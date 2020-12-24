# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/FunkLoadDocTest.py
# Compiled at: 2015-05-06 05:03:08
"""FunkLoad doc test

$Id$
"""
import os
from tempfile import gettempdir
from FunkLoadTestCase import FunkLoadTestCase
import PatchWebunit

class FunkLoadDocTest(FunkLoadTestCase):
    """Class to use in doctest.

    >>> from FunkLoadDocTest import FunkLoadDocTest
    >>> fl = FunkLoadDocTest()
    >>> ret = fl.get('http://localhost')
    >>> ret.code
    200
    >>> 'HTML' in ret.body
    True

    """

    def __init__(self, debug=False, debug_level=1):
        """Initialise the test case."""

        class Dummy:
            pass

        option = Dummy()
        option.ftest_sleep_time_max = 0.001
        option.ftest_sleep_time_min = 0.001
        if debug:
            option.ftest_log_to = 'console file'
            if debug_level:
                option.debug_level = debug_level
        else:
            option.ftest_log_to = 'file'
        tmp_path = gettempdir()
        option.ftest_log_path = os.path.join(tmp_path, 'fl-doc-test.log')
        option.ftest_result_path = os.path.join(tmp_path, 'fl-doc-test.xml')
        FunkLoadTestCase.__init__(self, 'runTest', option)

    def runTest(self):
        """FL doctest"""
        pass


def _test():
    import doctest, FunkLoadDocTest
    return doctest.testmod(FunkLoadDocTest)


if __name__ == '__main__':
    _test()