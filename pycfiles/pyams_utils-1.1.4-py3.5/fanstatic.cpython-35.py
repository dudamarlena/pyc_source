# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/fanstatic.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4520 bytes
"""PyAMS_utils.fanstatic module

This module is a helper module to handle Fanstatic resources.

It includes several TALES extensions which can be used to include resources from a Chameleon
template, or to get path of a given resources from a template.
"""
from fanstatic import Resource
from fanstatic.core import NeededResources, render_css, set_resource_file_existence_checking
from pyramid.path import DottedNameResolver
from zope.interface import Interface
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

def render_js(url, defer=False):
    """Render tag to include Javascript resource"""
    return '<script type="text/javascript" src="%s" %s></script>' % (url, 'defer' if defer else '')


class ExternalResource(Resource):
    __doc__ = 'Fanstatic external resource'
    dependency_nr = 0

    def __init__(self, library, path, defer=False, resource_type=None, **kwargs):
        set_resource_file_existence_checking(False)
        try:
            if 'renderer' in kwargs:
                del kwargs['renderer']
            if 'bottom' not in kwargs:
                kwargs['bottom'] = path.endswith('.js')
            Resource.__init__(self, library, path, renderer=self.render, **kwargs)
        finally:
            set_resource_file_existence_checking(True)

        self.defer = defer
        if resource_type:
            self.resource_type = resource_type
        else:
            self.resource_type = path.rsplit('.', 1)[1].lower()

    def render(self, library_url):
        """Render resource tag"""
        if self.resource_type == 'css':
            return render_css(self.relpath)
        if self.resource_type == 'js':
            return render_js(self.relpath, self.defer)
        return ''


def get_resource_path(resource, signature='--static--', versioning=True):
    """Get path for given resource"""
    res = NeededResources(publisher_signature=signature, versioning=versioning)
    return '{0}/{1}'.format(res.library_url(resource.library), resource.relpath)


@adapter_config(name='resource_path', context=(Interface, Interface, Interface), provides=ITALESExtension)
class FanstaticTalesExtension(ContextRequestViewAdapter):
    __doc__ = 'tales:resource_path() TALES extension\n\n    This TALES extension generates an URL matching a given Fanstatic resource.\n    Resource is given as a string made of package name (in dotted form) followed by a colon and\n    by the resource name.\n\n    For example:\n\n    .. code-block:: html\n\n        <div tal:attributes="data-ams-plugin-pyams_content-src\n                             extension:resource_path(\'pyams_content.zmi:pyams_content\')" />\n    '

    @staticmethod
    def render(resource):
        """TALES extension rendering method"""
        library, resource_name = resource.split(':')
        resolver = DottedNameResolver()
        module = resolver.maybe_resolve(library)
        resource = getattr(module, resource_name)
        return get_resource_path(resource)


@adapter_config(name='need_resource', context=(Interface, Interface, Interface), provides=ITALESExtension)
class FanstaticNeededResourceTalesExtension(ContextRequestViewAdapter):
    __doc__ = 'tales:need_resource() TALES extension\n\n    This extension generates a call to Fanstatic resource.need() function to include given resource\n    into generated HTML code.\n    Resource is given as a string made of package name (in dotted form) followed by a colon and by\n    the resource name.\n\n    For example:\n\n    .. code-block:: html\n\n        <tal:var define="tales:need_resource(\'pyams_content.zmi:pyams_content\')" />\n    '

    @staticmethod
    def render(resource):
        """TALES extension rendering method"""
        library, resource_name = resource.split(':')
        resolver = DottedNameResolver()
        module = resolver.maybe_resolve(library)
        resource = getattr(module, resource_name)
        resource.need()
        return ''