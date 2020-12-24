# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_batching/__init__.py
# Compiled at: 2019-12-05 08:43:35
# Size of source mod 2**32: 864 bytes
"""PyAMS_batching package

PyAMS table batching package
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_batching')

def includeme(config):
    """pyams_batching features include"""
    from .include import include_package
    include_package(config)