# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/__init__.py
# Compiled at: 2019-12-04 09:15:40
# Size of source mod 2**32: 854 bytes
"""PyAMS_file package

PyAMS files management package
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_file')

def includeme(config):
    """pyams_file features include"""
    from .include import include_package
    include_package(config)