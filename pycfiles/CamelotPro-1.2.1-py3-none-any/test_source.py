# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_source.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nTest the quality of the source code\n'
import os, unittest
source_code = os.path.join(os.path.dirname(__file__), '..', 'camelot')

class SourceQualityCase(unittest.TestCase):

    def test_deprecated(self):
        deprecated = [
         'setMargin']
        for dirpath, _dirnames, filenames in os.walk(source_code):
            for filename in filenames:
                if os.path.splitext(filename)[(-1)] == '.py':
                    code = open(os.path.join(dirpath, filename)).read()
                    for expr in deprecated:
                        if expr in code:
                            raise Exception('%s in %s/%s' % (expr,
                             dirpath,
                             filename))