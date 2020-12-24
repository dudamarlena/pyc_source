# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/demo/cps/CPS340DocTest.py
# Compiled at: 2015-05-06 05:03:08
"""Doctest support for CPS340TestCase

$Id$
"""
from CPS340TestCase import CPSTestCase
from FunkLoadDocTest import FunkLoadDocTest

class CPSDocTest(FunkLoadDocTest, CPSTestCase):
    """Class to use to doctest a CPS portal

    >>> from CPS340DocTest import CPSDocTest
    >>> cps_url = 'http://localhost:8080/cps'
    >>> fl = CPSDocTest(cps_url)
    >>> fl.cps_test_case_version
    (3, 4, 0)
    >>> fl.server_url == cps_url
    True

    Then you can use the CPS340TestCase API like fl.cpsLogin('manager', 'pwd').
    """

    def __init__(self, server_url, debug=False, debug_level=1):
        """init CPSDocTest

        server_url is the CPS server url."""
        FunkLoadDocTest.__init__(self, debug=debug, debug_level=debug_level)
        self.server_url = server_url


def _test():
    import doctest, CPS340DocTest
    return doctest.testmod(CPS340DocTest)


if __name__ == '__main__':
    _test()