# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/__init__.py
# Compiled at: 2019-12-05 08:40:48
# Size of source mod 2**32: 867 bytes
"""PyAMS_table package

PyAMS management package for HTML tables
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_table')

def includeme(config):
    """pyams_table features include"""
    from .include import include_package
    include_package(config)