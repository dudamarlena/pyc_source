# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ventriloquist/wsgi_app.py
# Compiled at: 2010-02-28 21:56:12
import urllib, jinja2
from webob import Request, exc
from ventriloquist import loader

class VentriloquistApp(object):

    def __init__(self, template_env, document_root, setup_path='setup.json'):
        self.template_env = template_env
        self.pagemap = loader.recursive_page_load(setup_path, document_root, template_env, {})

    def __call__(self, environ, start_response):
        request = Request(environ)
        path_info = request.path_info
        page = self.pagemap.get(path_info)
        if not page:
            if not path_info.endswith('/') and request.method == 'GET' and self.pagemap.get(path_info + '/'):
                new_path_info = path_info + '/'
                if request.GET:
                    new_path_info = '%s?%s' % (
                     new_path_info, urllib.urlencode(request.GET))
                redirect = exc.HTTPTemporaryRedirect(location=new_path_info)
                return request.get_response(redirect)(environ, start_response)
            return exc.HTTPNotFound()(environ, start_response)
        return page(request)(environ, start_response)


def ventriloquist_app_factory(global_config, **kwargs):
    template_loader = jinja2.FileSystemLoader(kwargs['document_root'])
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    return VentriloquistApp(template_env, kwargs['document_root'], kwargs.get('setup_path', '/setup.json'))