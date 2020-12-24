# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parterre/loader.py
# Compiled at: 2009-08-29 20:18:24
"""Parterre variant loader
    Copyright (C) 2008-2009  Eric Wald
    
    This module provides the entry point for exporting variants to Parlance.
    
    This package may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this package for
    commercial purposes without permission from the authors is prohibited.
"""
from parlance.config import VerboseObject
from parlance.gameboard import Variant

class Loader(VerboseObject):

    def __getattr__(self, name):
        resource = 'resource://%s/data/%s.cfg' % (__name__, name)
        self.log_debug(11, 'Loading %s', resource)
        variant = Variant(name, filename=resource)
        setattr(self, name, variant)
        return variant


loader = Loader()