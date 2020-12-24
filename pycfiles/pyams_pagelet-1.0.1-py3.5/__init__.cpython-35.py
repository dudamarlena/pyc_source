# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/__init__.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 866 bytes
"""PyAMS_pagelet package

PyAMS pagelets management package
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_pagelet')

def includeme(config):
    """pyams_pagelet features include"""
    from .include import include_package
    include_package(config)