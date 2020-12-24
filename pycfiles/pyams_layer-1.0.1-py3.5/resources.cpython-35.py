# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_layer/resources.py
# Compiled at: 2020-02-21 07:39:56
# Size of source mod 2**32: 4100 bytes
"""PyAMS_layer.resources module

This module provides adapters and TALES extensions used to manage static resources
which are associated with skins.
"""
from pyramid.interfaces import IRequest
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface
from pyams_layer.interfaces import IPyAMSUserLayer, IResources, ISkinnable
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.fanstatic import ExternalResource
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
__docformat__ = 'restructuredtext'

@adapter_config(name='custom-skin', context=(
 Interface, IPyAMSUserLayer, Interface), provides=IResources)
class CustomSkinResourcesAdapter(ContextRequestViewAdapter):
    __doc__ = 'Custom skin resources adapter'
    weight = 999

    @property
    def resources(self):
        """Get custom skin resources"""
        request = self.request
        main_resources = request.registry.queryMultiAdapter((
         self.context, request, self.view), IResources)
        if main_resources is not None:
            main_resource = main_resources.resources[(-1)]
            library = main_resource.library
            parent_resources = (main_resource,)
            skin_parent = get_parent(request.context, ISkinnable).skin_parent
            custom_css = skin_parent.custom_stylesheet
            if custom_css:
                modified = IZopeDublinCore(custom_css).modified
                custom_css_url = absolute_url(custom_css, request, query={'_': modified.timestamp()})
                resource = library.known_resources.get(custom_css_url)
                if resource is None:
                    resource = ExternalResource(library, custom_css_url, resource_type='css', depends=parent_resources)
                yield resource
            custom_js = skin_parent.custom_script
            if custom_js:
                modified = IZopeDublinCore(custom_js).modified
                custom_js_url = absolute_url(custom_js, request, query={'_': modified.timestamp()})
                resource = library.known_resources.get(custom_js_url)
                if resource is None:
                    resource = ExternalResource(library, custom_js_url, resource_type='js', depends=parent_resources, bottom=True)
                yield resource


@adapter_config(name='resources', context=(
 Interface, IRequest, Interface), provides=ITALESExtension)
class ResourcesTalesExtension(ContextRequestViewAdapter):
    __doc__ = 'extension:resources TALES extension'

    def render(self, context=None):
        """Render TALES extension by including needed resources"""
        if context is None:
            context = self.context
        for name, adapter in sorted(self.request.registry.getAdapters((
         context, self.request, self.view), IResources), key=lambda x: getattr(x[1], 'weight', 0)):
            for resource in adapter.resources:
                resource.need()

        return ''