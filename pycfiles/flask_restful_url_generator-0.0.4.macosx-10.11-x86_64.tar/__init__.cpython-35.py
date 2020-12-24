# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ojarva/src/flask-url-generator/dev/lib/python3.5/site-packages/flask_restful_url_generator/__init__.py
# Compiled at: 2016-02-18 04:57:52
# Size of source mod 2**32: 1530 bytes
"""
Flask-restful URLs view generator
"""
from flask_restful import Resource
__all__ = [
 'UrlList']

def format_pydoc(doc):
    return doc.strip().replace('\n', '<br>')


class UrlList(Resource):
    __doc__ = ' Lists all registered URLs along with docstrings for classes\n        and methods '

    def __init__(self, **kwargs):
        self.api = kwargs['api']

    def get(self):
        """ Returns simple JSON for all registered endpoints """
        urls = self.api.app.url_map
        data = []
        view_funcs = self.api.app.view_functions
        for url in urls.iter_rules():
            methods = set(url.methods)
            methods.discard('HEAD')
            methods.discard('OPTIONS')
            item = {'methods': list(methods), 
             'url': url.rule}
            endpoint = url.endpoint
            if endpoint in self.api.app.view_functions:
                try:
                    endpoint_class = view_funcs.get(endpoint).view_class
                    doc = endpoint_class.__doc__
                    if doc:
                        item['doc'] = format_pydoc(doc)
                    for method in item['methods']:
                        method_func = getattr(endpoint_class, method.lower())
                        doc = method_func.__doc__
                        if doc:
                            item['doc_for_%s' % method] = format_pydoc(doc)

                except AttributeError:
                    pass

                data.append(item)

        return data