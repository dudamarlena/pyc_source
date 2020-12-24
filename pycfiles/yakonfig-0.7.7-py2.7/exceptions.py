# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yakonfig/exceptions.py
# Compiled at: 2015-07-07 22:00:14
"""Yakonfig exception types.

.. This software is released under an MIT/X11 open source license.
   Copyright 2014 Diffeo, Inc.

"""
from __future__ import absolute_import

class ConfigurationError(Exception):
    """Some part of the user-provided configuration is incomplete or
    incorrect."""
    pass


class ProgrammerError(Exception):
    """Some part of the actual code does not meet requirements."""
    pass