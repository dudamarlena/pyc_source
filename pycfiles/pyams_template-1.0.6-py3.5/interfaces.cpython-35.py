# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_template/interfaces.py
# Compiled at: 2020-02-18 19:35:21
# Size of source mod 2**32: 897 bytes
"""PyAMS_template.interfaces module

Templates marker interfaces definitions
"""
from zope.interface import Interface
__docformat__ = 'restructuredtext'

class IPageTemplate(Interface):
    __doc__ = 'Base page template interface'


class ILayoutTemplate(IPageTemplate):
    __doc__ = 'A template used for render the layout.'


class IContentTemplate(IPageTemplate):
    __doc__ = 'A template used for render the content.'