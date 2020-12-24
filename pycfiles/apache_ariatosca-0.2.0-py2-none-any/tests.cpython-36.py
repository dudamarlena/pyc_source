# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/tests.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1342 bytes
import re, unittest

def skipUnlessImported(module, obj):
    import importlib
    try:
        m = importlib.import_module(module)
    except ImportError:
        m = None

    return unittest.skipUnless(obj in dir(m), 'Skipping test because {} could not be imported from {}'.format(obj, module))


def assertEqualIgnoreMultipleSpaces(case, first, second, msg=None):

    def _trim(s):
        return re.sub('\\s+', ' ', s.strip())

    return case.assertEqual(_trim(first), _trim(second), msg)