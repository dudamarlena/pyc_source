# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_template/metaconfigure.py
# Compiled at: 2020-02-18 19:35:21
# Size of source mod 2**32: 2348 bytes
"""PyAMS_template.metadirectives module

Is module allows to handle <template /> and <layout > directives in ZCML files.
"""
import os
from pyramid.exceptions import ConfigurationError
from pyramid.interfaces import IRequest
from zope.component import zcml
from zope.interface import Interface, directlyProvides
from pyams_template.interfaces import IContentTemplate, ILayoutTemplate
from pyams_template.template import TemplateFactory
__docformat__ = 'restructuredtext'

def template_directive(_context, template, name='', for_=Interface, layer=IRequest, provides=IContentTemplate, content_type='text/html', macro=None, context=None):
    """ZCML <template /> directive handler"""
    template = os.path.abspath(str(_context.path(template)))
    if not os.path.isfile(template):
        raise ConfigurationError('No such file', template)
    factory = TemplateFactory(template, content_type, macro)
    directlyProvides(factory, provides)
    for_ = (
     context, layer, for_)
    zcml.adapter(_context, (factory,), provides, for_, name=name)


def layout_template_directive(_context, template, name='', for_=Interface, layer=IRequest, provides=ILayoutTemplate, content_type='text/html', macro=None, context=None):
    """ZCML <layout /> directive handler"""
    template_directive(_context, template, name, for_, layer, provides, content_type, macro, context)