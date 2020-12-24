# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/base/mixins.py
# Compiled at: 2015-03-02 10:21:03
"""
reusable restframework mixins for API views
"""
import reversion
from rest_framework.response import Response

class ACLMixin(object):
    """ implements ACL in views """

    def get_queryset(self):
        """
        Returns only objects which are accessible to the current user.
        If user is not authenticated all public objects will be returned.

        Model must implement AccessLevelManager!
        """
        return self.queryset.accessible_to(user=self.request.user)


class CustomDataMixin(object):
    """
    Implements custom data in views

    Must implement:
        * self.serializer_custom_class: a custom serializer
        * self.get_custom_data(): method that specifies the custom data to pass to the custom serializer
    """

    def get_custom_data(self):
        """ automatically determine user on creation """
        raise NotImplementedError('CustomDataMixin needs a get_custom_data method')

    def get_custom_serializer(self, **kwargs):
        """ returns the custom serializer class """
        try:
            serializer_class = self.serializer_custom_class
        except AttributeError:
            serializer_class = self.get_serializer

        return serializer_class(**kwargs)

    def create(self, request, *args, **kwargs):
        """ custom create method """
        data = request.DATA.copy()
        additional_data = self.get_custom_data()
        custom_data = dict(data.items() + additional_data.items())
        serializer = self.get_custom_serializer(data=custom_data, files=request.FILES, context=self.get_serializer_context())
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        return Response(serializer.errors, status=400)


class RevisionUpdate(object):
    """
    Mixin that adds compatibility with django reversion for PUT and PATCH requests
    """

    def put(self, request, *args, **kwargs):
        """ custom put method to support django-reversion """
        with reversion.create_revision():
            reversion.set_user(request.user)
            reversion.set_comment('changed through the RESTful API from ip %s' % request.META['REMOTE_ADDR'])
            return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ custom patch method to support django-reversion """
        with reversion.create_revision():
            reversion.set_user(request.user)
            reversion.set_comment('changed through the RESTful API from ip %s' % request.META['REMOTE_ADDR'])
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)


class RevisionCreate(object):
    """
    Mixin that adds compatibility with django reversion for POST requests
    """

    def post(self, request, *args, **kwargs):
        """ custom put method to support django-reversion """
        with reversion.create_revision():
            reversion.set_user(request.user)
            reversion.set_comment('created through the RESTful API from ip %s' % request.META['REMOTE_ADDR'])
            return self.create(request, *args, **kwargs)