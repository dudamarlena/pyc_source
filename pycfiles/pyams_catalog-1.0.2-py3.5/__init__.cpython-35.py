# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/__init__.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 869 bytes
"""PyAMS_catalog package

PyAMS extensions for Hypatia catalog
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_catalog')

def includeme(config):
    """pyams_catalog features include"""
    from .include import include_package
    include_package(config)