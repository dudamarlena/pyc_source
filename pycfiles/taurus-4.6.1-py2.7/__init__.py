# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/__init__.py
# Compiled at: 2019-08-19 15:09:29
"""The main taurus module. It contains a reduced set of wrappers around the
real taurus model classes and information regarding the current release."""
from .core import release as __R

class Release:
    pass


for attr, value in __R.__dict__.items():
    setattr(Release, attr, value)

Release.__doc__ = __R.__doc__
from .core.taurushelper import *