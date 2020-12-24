# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_layer/__init__.py
# Compiled at: 2020-02-21 07:39:56
# Size of source mod 2**32: 866 bytes
"""PyAMS_layer package

PyAMS base layers and skins management.
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_layer')

def includeme(config):
    """pyams_layer features include"""
    from .include import include_package
    include_package(config)