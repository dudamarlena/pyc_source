# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/metadirectives.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 4838 bytes
__doc__ = 'PyAMS_viewlet.metadirectives module\n\nThis template provides definition of ZCML directives.\n'
from zope.configuration.fields import GlobalInterface, GlobalObject
from zope.interface import Interface
from zope.schema import TextLine
from pyams_viewlet.interfaces import IViewletManager
__docformat__ = 'restructuredtext'

class IContentProvider(Interface):
    """IContentProvider"""
    view = GlobalObject(title='The view the content provider is registered for', description='The view can either be an interface or a class. By default the provider is registered for all views, the most common case.', required=False, default=Interface)
    name = TextLine(title='The name of the content provider', description='The name of the content provider is used in the TALES ``provider`` namespace to look up the content provider.', required=True)
    for_ = GlobalObject(title='The interface or class this view is for', required=False)
    permission = TextLine(title='Permission', description='The permission needed to use the view', required=False)
    class_ = GlobalObject(title='Class', description='A class that provides attributes used by the view', required=False)
    layer = GlobalInterface(title='The layer the view is in', description="A skin is composed of layers; layers are defined as interfaces, which are provided to the request when the skin is applied. It is common to put skin specific views in a layer named after the skin. If the 'layer' attribute is not supplied, it defaults to IRequest, which is the base interface of any request.", required=False)


class IViewletManagerDirective(IContentProvider):
    """IViewletManagerDirective"""
    provides = GlobalInterface(title='The interface this viewlet manager provides', description='A viewlet manager can provide an interface, which is used to lookup its contained viewlets.', required=False, default=IViewletManager)


class IViewletDirective(IContentProvider):
    """IViewletDirective"""
    manager = GlobalObject(title='Manager', description='The interface or class of the viewlet manager', required=False, default=IViewletManager)


IViewletDirective.setTaggedValue('keyword_arguments', True)