# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/metadirectives.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 4838 bytes
"""PyAMS_viewlet.metadirectives module

This template provides definition of ZCML directives.
"""
from zope.configuration.fields import GlobalInterface, GlobalObject
from zope.interface import Interface
from zope.schema import TextLine
from pyams_viewlet.interfaces import IViewletManager
__docformat__ = 'restructuredtext'

class IContentProvider(Interface):
    __doc__ = 'A directive to register a simple content provider.\n\n    Content providers are registered by their context (`for` attribute), the\n    request (`layer` attribute) and the view (`view` attribute). They also\n    must provide a name, so that they can be found using the TALES\n    ``provider`` namespace. Other than that, content providers are just like\n    any other views.\n    '
    view = GlobalObject(title='The view the content provider is registered for', description='The view can either be an interface or a class. By default the provider is registered for all views, the most common case.', required=False, default=Interface)
    name = TextLine(title='The name of the content provider', description='The name of the content provider is used in the TALES ``provider`` namespace to look up the content provider.', required=True)
    for_ = GlobalObject(title='The interface or class this view is for', required=False)
    permission = TextLine(title='Permission', description='The permission needed to use the view', required=False)
    class_ = GlobalObject(title='Class', description='A class that provides attributes used by the view', required=False)
    layer = GlobalInterface(title='The layer the view is in', description="A skin is composed of layers; layers are defined as interfaces, which are provided to the request when the skin is applied. It is common to put skin specific views in a layer named after the skin. If the 'layer' attribute is not supplied, it defaults to IRequest, which is the base interface of any request.", required=False)


class IViewletManagerDirective(IContentProvider):
    __doc__ = 'A directive to register a new viewlet manager.\n\n    Viewlet manager registrations are very similar to content provider\n    registrations, since they are just a simple extension of content\n    providers. However, viewlet managers commonly have a specific provided\n    interface, which is used to discriminate the viewlets they are providing.\n    '
    provides = GlobalInterface(title='The interface this viewlet manager provides', description='A viewlet manager can provide an interface, which is used to lookup its contained viewlets.', required=False, default=IViewletManager)


class IViewletDirective(IContentProvider):
    __doc__ = 'A directive to register a new viewlet.\n\n    Viewlets are content providers that can only be displayed inside a viewlet\n    manager. Thus they are additionally discriminated by the manager. Viewlets\n    can rely on the specified viewlet manager interface to provide their\n    content.\n\n    The viewlet directive also supports an undefined set of keyword arguments\n    that are set as attributes on the viewlet after creation. Those attributes\n    can then be used to implement sorting and filtering, for example.\n    '
    manager = GlobalObject(title='Manager', description='The interface or class of the viewlet manager', required=False, default=IViewletManager)


IViewletDirective.setTaggedValue('keyword_arguments', True)