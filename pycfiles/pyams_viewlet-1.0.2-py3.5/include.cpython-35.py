# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/include.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 927 bytes
"""PyAMS_viewlet.include module

This module is used for Pyramid integration
"""
from chameleon import PageTemplateFile
from pyams_viewlet.provider import ProviderExpr
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_viewlet:locales')
    config.scan()
    PageTemplateFile.expression_types['provider'] = ProviderExpr