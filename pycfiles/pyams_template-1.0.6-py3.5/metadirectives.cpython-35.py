# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_template/metadirectives.py
# Compiled at: 2020-02-18 19:35:21
# Size of source mod 2**32: 3628 bytes
"""PyAMS_template.metadirectives module

This module provides ZCML directives interfaces
"""
from pyramid.interfaces import IRequest
from zope.configuration.fields import GlobalInterface, GlobalObject, Path
from zope.interface import Interface
from zope.schema import ASCIILine, TextLine
from pyams_template.interfaces import IContentTemplate, ILayoutTemplate
__docformat__ = 'restructuredtext'

class ITemplateDirective(Interface):
    __doc__ = 'Parameters for the template directive.'
    template = Path(title='Layout template.', description='Refers to a file containing a page template (should end in extension ``.pt`` or ``.html``).', required=True)
    name = TextLine(title='The name of the template.', description='The name is used to look up the template.', default='', required=False)
    macro = TextLine(title='Macro', description='The macro to be used. This allows us to define different macros in one template. The template designer can now create a whole site, the ViewTemplate can then extract the macros for single viewlets or views. If no macro is given the whole template is used for rendering.', default='', required=False)
    for_ = GlobalObject(title='View', description='The view for which the template should be available', default=Interface, required=False)
    layer = GlobalObject(title='Layer', description='The layer for which the template should be available', required=False, default=IRequest)
    context = GlobalObject(title='Context', description='The context for which the template should be available', required=False)
    provides = GlobalInterface(title='Interface the template provides', description='This attribute specifies the interface the template instance will provide.', default=IContentTemplate, required=False)
    content_type = ASCIILine(title='Content Type', description='The content type identifies the type of data.', default='text/html', required=False)


class ILayoutTemplateDirective(ITemplateDirective):
    __doc__ = 'Parameters for the layout template directive.'
    provides = GlobalInterface(title='Interface the template provides', description='This attribute specifies the interface the template instance will provide.', default=ILayoutTemplate, required=False)