# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/unit/filesys/abstract_test.py
# Compiled at: 2015-11-06 23:45:35
from nose.tools import istest
from tests.util import ensure_except
from salve.filesys import abstract

@istest
def filesys_is_abstract():
    """
    Unit: Filesys Base Class Is Abstract
    Ensures that a Filesys cannot be instantiated.
    """
    ensure_except(TypeError, abstract.Filesys)