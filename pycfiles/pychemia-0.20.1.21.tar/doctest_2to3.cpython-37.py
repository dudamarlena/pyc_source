# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/PyChemia/tests/doctest_2to3.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 566 bytes
import re, sys, doctest

class DocTestChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        if sys.version_info[0] > 2:
            want = re.sub("u'(.*?)'", "'\\1'", want)
            want = re.sub('u"(.*?)"', '"\\1"', want)
        else:
            want = re.sub("b'(.*?)'", "'\\1'", want)
            want = re.sub('b"(.*?)"', '"\\1"', want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def doctest_suite(mod):
    return doctest.DocTestSuite(mod, checker=(DocTestChecker()))