# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/__init__.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 866 bytes
__doc__ = 'PyAMS_viewlet package\n\nPyAMS viewlets management package\n'
__docformat__ = 'restructuredtext'
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('pyams_viewlet')

def includeme(config):
    """pyams_viewlet features include"""
    from .include import include_package
    include_package(config)