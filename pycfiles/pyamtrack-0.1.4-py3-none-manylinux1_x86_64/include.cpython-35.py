# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/include.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 927 bytes
__doc__ = 'PyAMS_viewlet.include module\n\nThis module is used for Pyramid integration\n'
from chameleon import PageTemplateFile
from pyams_viewlet.provider import ProviderExpr
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_viewlet:locales')
    config.scan()
    PageTemplateFile.expression_types['provider'] = ProviderExpr