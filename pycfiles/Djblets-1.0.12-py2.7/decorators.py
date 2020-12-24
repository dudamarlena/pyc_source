# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/testing/decorators.py
# Compiled at: 2019-06-12 01:17:17
"""Decorators to help with API test suites."""
from __future__ import unicode_literals
from djblets.util.decorators import simple_decorator

@simple_decorator
def webapi_test_template(test_func):
    """Mark a test function as a template for tests.

    This adds a flag to the test function hinting that it should be processed
    differently. :py:class:`WebAPITestCaseMixin` will replace the docstring to
    match that of the active test suite.
    """

    def _call(*args, **kwargs):
        return test_func(*args, **kwargs)

    _call.is_test_template = True
    return _call