# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/resource/base.py
# Compiled at: 2017-11-03 05:35:30
# Size of source mod 2**32: 4142 bytes
import six
from flask import jsonify
from flask.globals import request
from flask.views import View
from werkzeug.exceptions import MethodNotAllowed
from flask_restframework.decorators import auth_backends
ALL_METHODS = [
 'GET',
 'POST',
 'PUT',
 'PATCH',
 'DELETE',
 'HEAD',
 'OPTIONS']

class BaseResourceMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name != 'BaseResource':
            allowedMethods = []
            allowedObjectMethods = []
            for base in bases:
                if hasattr(base, '_allowed_methods') and base._allowed_methods:
                    allowedMethods += base._allowed_methods
                if hasattr(base, '_allowed_object_methods') and base._allowed_object_methods:
                    allowedObjectMethods += base._allowed_object_methods

            for key, value in six.iteritems(attrs):
                if key.upper() in ALL_METHODS:
                    allowedMethods.append(key)
                if key.endswith('_object'):
                    objectMethod = key.replace('_object', '')
                    if objectMethod.upper() in ALL_METHODS:
                        allowedObjectMethods.append(objectMethod)

            attrs['_allowed_methods'] = allowedMethods
            attrs['_allowed_object_methods'] = allowedObjectMethods
        return type.__new__(cls, name, bases, attrs)


@six.add_metaclass(BaseResourceMetaClass)
class BaseResource(object):
    _allowed_methods = None
    _allowed_object_methods = None
    request = None
    authentication_backends = None

    def __init__(self, request):
        self.request = request

    @classmethod
    def get_allowed_methods(cls):
        """
        Returns list of allowed methods (NOT object)
        for example if you define get, post, put methods
        this method returns ["get", "post", "put"]
        And you will be able to make

            GET <url>
            POST <url>
            PUT <url>

        """
        return cls._allowed_methods

    @classmethod
    def get_allowed_object_methods(cls):
        """
        Returls list of allowed PER OBJECT methods
        You can define <method name>_object function
        than this method returns ["method_name"]
        and you will be able to make request

            <METHOD_NAME> <url>/<id>

        """
        return cls._allowed_object_methods

    @classmethod
    def as_view(cls, funcName, suffix=''):
        """
        Returns dispatcher function
        :param funcName: url basename
        :param suffix: For dispathing is used <resuest method name>+suffix. Need for dispatching object requests,
            for example GET <url>/<id> will be registered with suffix "_object" and will be dispatched on get_object
            method
        :return:
        """

        def view_func(**params):
            return cls(request).dispatch_request(suffix=suffix, **params)

        view_func.__name__ = funcName
        if cls.authentication_backends:
            view_func = auth_backends(*cls.authentication_backends)(view_func)
        return view_func

    def dispatch_request(self, suffix='', **params):
        return self._dispatch(request, request.method.lower() + suffix, params)

    def _dispatch(self, request, callback_name, params):
        if hasattr(self, callback_name):
            return getattr(self, callback_name)(request, **params)
        raise MethodNotAllowed('Method {} is not allowed'.format(callback_name))

    def validate_request(self, serializerClass):
        """
        :returns: tuple (errorResponse, cleanedData)
        """
        serializer = serializerClass(data=request.json)
        serializer.validate()
        if serializer.errors:
            resp = jsonify(serializer.errors)
            resp.status_code = 400
            return (
             resp, None)
        return ({}, serializer.cleaned_data)


class Test(BaseResource):
    pass