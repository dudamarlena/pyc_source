# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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