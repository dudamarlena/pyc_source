# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/fanstatic.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4520 bytes
__doc__ = 'PyAMS_utils.fanstatic module\n\nThis module is a helper module to handle Fanstatic resources.\n\nIt includes several TALES extensions which can be used to include resources from a Chameleon\ntemplate, or to get path of a given resources from a template.\n'
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
    """ExternalResource"""
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
    """FanstaticTalesExtension"""

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
    """FanstaticNeededResourceTalesExtension"""

    @staticmethod
    def render(resource):
        """TALES extension rendering method"""
        library, resource_name = resource.split(':')
        resolver = DottedNameResolver()
        module = resolver.maybe_resolve(library)
        resource = getattr(module, resource_name)
        resource.need()
        return ''