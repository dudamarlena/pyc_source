# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/__init__.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 872 bytes
"""PyAMS_apm package

PyAMS extension package for Elastic APM integration
"""
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_apm')

def includeme(config):
    """pyams_apm features include"""
    from .include import include_package
    include_package(config)