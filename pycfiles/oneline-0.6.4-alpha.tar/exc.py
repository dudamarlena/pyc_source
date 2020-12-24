# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/exc.py
# Compiled at: 2014-09-06 21:58:19
"""Exceptions for marking tests as skipped or deprecated.

This module exists to provide backwards compatibility with previous
versions of nose where skipped and deprecated tests were core
functionality, rather than being provided by plugins. It may be
removed in a future release.
"""
from nose.plugins.skip import SkipTest
from nose.plugins.deprecated import DeprecatedTest