# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cirdan/__init__.py
# Compiled at: 2015-07-06 16:01:24
# Size of source mod 2**32: 1374 bytes
from __future__ import absolute_import
import falcon, os.path
from cirdan.resource import DocsResource
from cirdan.registry import registry, METHODS_TO_VERBS
route_path = '/docs'
template_path = os.path.join(os.path.dirname(__file__), 'default.jinja2')
cache_template = True

def inject():
    falcon.API._wrapped_add_route = falcon.API.add_route
    falcon.API.add_route = register


def set_meta(api, name='Docs', intro_text='', **kwargs):
    """
    A quick aside here - this is a function in the cirdan module instead of a
    monkey-patch into falcon because falcon uses __slots__, and thus can't have
    new properties bound.
    """
    registry.set_api_meta(api, name=name, intro_text=intro_text, **kwargs)


def register(api, path, resource):
    api._wrapped_add_route(path, resource)
    add_docs_route(api)
    cls = resource.__class__
    wrapped_resource = registry.get(cls)
    wrapped_resource.path = path
    registry.bind_api(api, wrapped_resource)
    for method, verb in METHODS_TO_VERBS.items():
        if hasattr(cls, method):
            f = getattr(cls, method)
            if hasattr(f, '__func__'):
                f = f.__func__
            wrapped_resource.methods.append(registry.get(f))
            continue


def add_docs_route(api):
    if not registry.knows_about(api):
        api._wrapped_add_route(route_path, DocsResource(api))