# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/__init__.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 854 bytes
"""PyAMS_form package

PyAMS forms management package
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_form')

def includeme(config):
    """pyams_form features include"""
    from .include import include_package
    include_package(config)