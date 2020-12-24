# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ojarva/src/flask-url-generator/dev/lib/python3.5/site-packages/flask_restful_url_generator/urls.py
# Compiled at: 2016-02-18 04:09:48
# Size of source mod 2**32: 1241 bytes


class UrlList(Resource):
    __doc__ = ' Lists all registered URLs along with docstrings for classes and methods '

    def __init__(self, **kwargs):
        self.api = kwargs['api']

    def get(self):
        urls = self.api.app.url_map
        data = []
        for url in urls.iter_rules():
            methods = set(url.methods)
            methods.discard('HEAD')
            methods.discard('OPTIONS')
            item = {'methods': list(methods), 
             'url': url.rule}
            endpoint = url.endpoint
            if endpoint in self.api.app.view_functions:
                try:
                    endpoint_class = self.api.app.view_functions.get(endpoint).view_class
                    doc = endpoint_class.__doc__
                    if doc:
                        item['doc'] = doc.strip()
                    for method in item['methods']:
                        method_func = getattr(endpoint_class, method.lower())
                        doc = method_func.__doc__
                        if doc:
                            item['doc_for_%s' % method] = doc.strip()

                except AttributeError:
                    pass

                data.append(item)

        return data