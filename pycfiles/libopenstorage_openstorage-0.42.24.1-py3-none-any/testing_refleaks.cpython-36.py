# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/internal/testing_refleaks.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 4659 bytes
"""A subclass of unittest.TestCase which checks for reference leaks.

To use:
- Use testing_refleak.BaseTestCase instead of unittest.TestCase
- Configure and compile Python with --with-pydebug

If sys.gettotalrefcount() is not available (because Python was built without
the Py_DEBUG option), then this module is a no-op and tests will run normally.
"""
import gc, sys
try:
    import copy_reg as copyreg
except ImportError:
    import copyreg

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class LocalTestResult(unittest.TestResult):
    __doc__ = 'A TestResult which forwards events to a parent object, except for Skips.'

    def __init__(self, parent_result):
        unittest.TestResult.__init__(self)
        self.parent_result = parent_result

    def addError(self, test, error):
        self.parent_result.addError(test, error)

    def addFailure(self, test, error):
        self.parent_result.addFailure(test, error)

    def addSkip(self, test, reason):
        pass


class ReferenceLeakCheckerMixin(object):
    __doc__ = 'A mixin class for TestCase, which checks reference counts.'
    NB_RUNS = 3

    def run(self, result=None):
        self._saved_pickle_registry = copyreg.dispatch_table.copy()
        super(ReferenceLeakCheckerMixin, self).run(result=result)
        super(ReferenceLeakCheckerMixin, self).run(result=result)
        oldrefcount = 0
        local_result = LocalTestResult(result)
        refcount_deltas = []
        for _ in range(self.NB_RUNS):
            oldrefcount = self._getRefcounts()
            super(ReferenceLeakCheckerMixin, self).run(result=local_result)
            newrefcount = self._getRefcounts()
            refcount_deltas.append(newrefcount - oldrefcount)

        print(refcount_deltas, self)
        try:
            self.assertEqual(refcount_deltas, [0] * self.NB_RUNS)
        except Exception:
            result.addError(self, sys.exc_info())

    def _getRefcounts(self):
        copyreg.dispatch_table.clear()
        copyreg.dispatch_table.update(self._saved_pickle_registry)
        gc.collect()
        gc.collect()
        gc.collect()
        return sys.gettotalrefcount()


if hasattr(sys, 'gettotalrefcount'):

    def TestCase(test_class):
        new_bases = (ReferenceLeakCheckerMixin,) + test_class.__bases__
        new_class = type(test_class)(test_class.__name__, new_bases, dict(test_class.__dict__))
        return new_class


    SkipReferenceLeakChecker = unittest.skip
else:

    def TestCase(test_class):
        return test_class


    def SkipReferenceLeakChecker(reason):
        del reason

        def Same(func):
            return func

        return Same