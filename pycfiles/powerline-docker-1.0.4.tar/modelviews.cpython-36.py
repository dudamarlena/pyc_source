# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cleber/.pyenv/versions/3.6.2/lib/python3.6/site-packages/powerlibs/django/restless/modelviews.py
# Compiled at: 2017-08-24 15:42:37
# Size of source mod 2**32: 8122 bytes
from django.forms.models import modelform_factory
from .views import Endpoint
from .http import HttpError, Http200, Http201
from .models import serialize
__all__ = [
 'ListEndpoint', 'DetailEndpoint', 'ActionEndpoint']

def _get_form(form, model):
    from django import VERSION
    if VERSION[:2] >= (1, 8):

        def mf(model):
            return modelform_factory(model, fields='__all__')

    else:
        mf = modelform_factory
    if form:
        return form
    if model:
        return mf(model)
    raise NotImplementedError('Form or Model class not specified')


class ListEndpoint(Endpoint):
    """ListEndpoint"""
    model = None
    form = None
    methods = ['GET', 'POST']

    def get_query_set(self, request, *args, **kwargs):
        """Return a QuerySet that this endpoint represents.

        If `model` class attribute is set, this method returns the `all()`
        queryset for the model. You can override the method to provide custom
        behaviour. The `args` and `kwargs` parameters are passed in directly
        from the URL pattern match.

        If the method raises a :py:class:`restless.http.HttpError` exception,
        the rest of the request processing is terminated and the error is
        immediately returned to the client.
        """
        if self.model:
            return self.model.objects.all()
        raise HttpError(404, 'Resource Not Found')

    def serialize(self, objs):
        """Serialize the objects in the response.

        By default, the method uses the :py:func:`restless.models.serialize`
        function to serialize the objects with default behaviour. Override the
        method to customize the serialization.
        """
        return serialize(objs)

    def get(self, request, *args, **kwargs):
        """Return a serialized list of objects in this endpoint."""
        if 'GET' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        qs = (self.get_query_set)(request, *args, **kwargs)
        return self.serialize(qs)

    def post(self, request, *args, **kwargs):
        """Create a new object."""
        if 'POST' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        Form = _get_form(self.form, self.model)
        form = Form(request.data or None, request.FILES)
        if form.is_valid():
            obj = form.save()
            return Http201(self.serialize(obj))
        raise HttpError(400, 'Invalid Data', errors=(form.errors))


class DetailEndpoint(Endpoint):
    """DetailEndpoint"""
    model = None
    form = None
    lookup_field = 'pk'
    methods = ['GET', 'PUT', 'PATCH', 'DELETE']

    def get_instance(self, request, *args, **kwargs):
        """Return a model instance represented by this endpoint.

        If `model` is set and the primary key keyword argument is present,
        the method attempts to get the model with the primary key equal
        to the url argument.

        By default, the primary key keyword argument name is `pk`. This can
        be overridden by setting the `lookup_field` class attribute.

        You can override the method to provide custom behaviour. The `args`
        and `kwargs` parameters are passed in directly from the URL pattern
        match.

        If the method raises a :py:class:`restless.http.HttpError` exception,
        the rest of the request processing is terminated and the error is
        immediately returned to the client.
        """
        if self.model:
            if self.lookup_field in kwargs:
                try:
                    return (self.model.objects.get)(**{self.lookup_field: kwargs.get(self.lookup_field)})
                except self.model.DoesNotExist:
                    raise HttpError(404, 'Resource Not Found')

        else:
            raise HttpError(404, 'Resource Not Found')

    def serialize(self, obj):
        """Serialize the object in the response.

        By default, the method uses the :py:func:`restless.models.serialize`
        function to serialize the object with default behaviour. Override the
        method to customize the serialization.
        """
        return serialize(obj)

    def get(self, request, *args, **kwargs):
        """Return the serialized object represented by this endpoint."""
        if 'GET' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        return self.serialize((self.get_instance)(request, *args, **kwargs))

    def patch(self, request, *args, **kwargs):
        """Update the object represented by this endpoint."""
        if 'PATCH' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        instance = (self.get_instance)(request, *args, **kwargs)
        for key, value in request.data.items():
            setattr(instance, key, value)

        instance.save()
        return Http200(self.serialize(instance))

    def put(self, request, *args, **kwargs):
        """Update the object represented by this endpoint."""
        if 'PUT' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        Form = _get_form(self.form, self.model)
        instance = (self.get_instance)(request, *args, **kwargs)
        form = Form((request.data or None), (request.FILES), instance=instance)
        if form.is_valid():
            obj = form.save()
            return Http200(self.serialize(obj))
        raise HttpError(400, 'Invalid data', errors=(form.errors))

    def delete(self, request, *args, **kwargs):
        """Delete the object represented by this endpoint."""
        if 'DELETE' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        instance = (self.get_instance)(request, *args, **kwargs)
        instance.delete()
        return {}


class ActionEndpoint(DetailEndpoint):
    """ActionEndpoint"""
    methods = [
     'POST']

    def post(self, request, *args, **kwargs):
        if 'POST' not in self.methods:
            raise HttpError(405, 'Method Not Allowed')
        instance = (self.get_instance)(request, *args, **kwargs)
        return (self.action)(request, instance, *args, **kwargs)

    def action(self, request, obj, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')