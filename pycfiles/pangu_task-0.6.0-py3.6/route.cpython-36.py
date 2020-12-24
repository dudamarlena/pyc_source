# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pangu_task/route.py
# Compiled at: 2019-12-04 22:33:10
# Size of source mod 2**32: 2789 bytes
import json, threading
from django import urls
from django.http import HttpResponse

class R(HttpResponse):

    def __init__(self, code=10000, message='', description='', *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.code = code
        self.message = message
        self.description = description
        self.content_type = 'application/json'
        self.content = self.__str__()

    def __str__(self):
        result = {'code':self.code, 
         'message':self.message, 
         'description':self.description}
        return json.dumps(result)

    @classmethod
    def success(cls):
        return R(message='success')

    @classmethod
    def fail(cls, code=9999, description=None):
        return R(message='fail', code=code, description=description)


class Proxy:

    def __init__(self, method, *args, **kwargs):
        assert callable(method), 'method must be a function'
        self.original_method = method
        self.init = kwargs.get('init')
        self.callback = kwargs.get('callback')

    def __new_method(self, *args, **kwargs):
        if self.init:
            self.init()
        self.original_method()
        if self.callback:
            self.callback()

    def delay(self, *args, **kwargs):
        try:
            t = threading.Thread(target=(self._Proxy__new_method), args=args, kwargs=kwargs)
            t.start()
        except Exception as e:
            return R.fail(description=(str(e)))

        return R.success()

    def execute(self, *args, **kwargs):
        try:
            (self._Proxy__new_method)(*args, **kwargs)
        except Exception as e:
            return R.fail(description=(str(e)))

        return R.success()


class Route:

    def __init__(self, url_prefix='', name_prefix=''):
        self.url_prefix = url_prefix.strip('/')
        self.name_prefix = name_prefix
        self.routes = {}

    def __call__(self, path=None, name=None, *args, **kwargs):

        def wrapper(method):
            url_name = self.name_prefix + (name or method.__name__)
            url_path = path or method.__name__
            url_path = self.url_prefix + '/' + url_path.lstrip('/')
            self.routes[url_name] = (url_path, Proxy(method, *args, **kwargs).delay)
            return Proxy(method, *args, **kwargs).delay

        if callable(path):
            method = path
            path = None
            return wrapper(method)
        else:
            return wrapper

    @property
    def patterns(self):
        return [urls.path((path.lstrip('/')), handler, name=name) for name, (path, handler) in self.routes.items()]

    @property
    def names(self):
        return {name:'/' + path.lstrip('/') for name, (path, _) in self.routes.items()}