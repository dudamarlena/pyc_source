# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/model_resource.py
# Compiled at: 2017-10-27 10:49:50
# Size of source mod 2**32: 7208 bytes
import copy, six
from flask import jsonify
from flask.globals import current_app
from flask.wrappers import Request
from mongoengine.errors import DoesNotExist
from flask_restframework.queryset_wrapper import QuerysetWrapper, InstanceWrapper
from flask_restframework.serializer.base_serializer import BaseSerializer
from flask_restframework.exceptions import NotFound
from flask_restframework.filter_backends import BaseBackend
from flask_restframework.resource import BaseResource, BaseResourceMetaClass
from flask_restframework.serializer.model_serializer import ModelSerializer

class GenericResource(BaseResource):
    __metaclass__ = BaseResourceMetaClass
    serializer_class = None
    queryset = None
    pagination_class = None
    filter_backends = None

    def __init__(self, request):
        super(GenericResource, self).__init__(request)
        if not self.serializer_class:
            raise ValueError('serializer_class is required')
        if self.get_queryset() is None:
            raise ValueError('queryset is required')

    def get_pagination_class(self):
        """
        Returns pagination class

        You can use pagination_class attribute or set config variable:

            FLASK_REST = {
                "PAGINATION_CLASS": <Your pagination class>
            }
        """
        return self.pagination_class or current_app.config.get('FLASK_REST', {}).get('PAGINATION_CLASS')

    def get_queryset(self):
        return self.queryset

    def get_adaptated_queryset(self):
        qs = self.get_queryset()
        return QuerysetWrapper.from_queryset(qs)

    def get_instance(self, pk):
        """returns one instance from queryset by its PK"""
        try:
            return self.get_adaptated_queryset().get(id=pk)
        except DoesNotExist:
            raise NotFound('Object not found')

    def get_backend_classes(self):
        """Returns backend classes"""
        return self.filter_backends or current_app.config.get('FLASK_REST', {}).get('FILTER_BACKENDS')

    def filter_qs(self, qs):
        """Perform filtration of queryset base on filter_backends"""
        backend_classes = self.get_backend_classes()
        if backend_classes:
            for backendCls in backend_classes:
                backend = backendCls(qs, self.request, resource=self)
                assert isinstance(backend, BaseBackend)
                qs = backend.filter()

        return qs

    def get_data(self, request):
        """Returns json body data from request"""
        return request.json


class ListObjectsMixin:
    __doc__ = '\n    Allows you to add GET endpoint for resource:\n\n        GET /yourresource\n\n    Returns array of (paginated if set pagination_class) elements\n    '

    def get(self, request):
        assert isinstance(self, ModelResource)
        qs = self.get_adaptated_queryset()
        qs = self.filter_qs(qs)
        assert isinstance(qs, QuerysetWrapper)
        paginationCls = self.get_pagination_class()
        if paginationCls:
            pagination = paginationCls(qs)
            pagination.paginate(request)
            data = self.serializer_class.from_queryset(pagination.qs).serialize()
            data = pagination.update_response(data)
        else:
            data = self.serializer_class(qs).serialize()
        return jsonify(data)


class CreateMixin:

    def after_create(self, instance, validated_data):
        """Will be create after creating new instance"""
        pass

    def post(self, request):
        data = self.get_data(request)
        serializer = self.serializer_class(data)
        if not serializer.validate():
            out = jsonify(serializer.errors)
            out.status_code = 400
            return out
        instance = serializer.create(serializer.cleaned_data)
        assert isinstance(instance, InstanceWrapper)
        self.after_create(instance, serializer.cleaned_data)
        return jsonify(self.serializer_class(instance).serialize())


class RetrieveMixin:

    def get_object(self, request, pk):
        assert isinstance(self, GenericResource)
        obj = self.get_instance(pk)
        assert isinstance(obj, InstanceWrapper)
        return jsonify(self.serializer_class(obj).serialize())


class UpdateMixin:

    def after_update(self, oldInstance, updatedInstance, validated_data):
        """Will be called after updating existed instance"""
        pass

    def put_object(self, request, pk):
        return self._perform_update(pk, request)

    def _perform_update(self, pk, request, part=False):
        data = self.get_data(request)
        instance = self.get_instance(pk)
        assert isinstance(instance, InstanceWrapper)
        serializer = self.serializer_class(data, context={'instance': instance})
        assert isinstance(serializer, ModelSerializer)
        if not serializer.validate(part=part):
            out = jsonify(serializer.errors)
            out.status_code = 400
            return out
        oldInstance = copy.deepcopy(instance)
        validated_data = {key:value for key, value in six.iteritems(serializer.cleaned_data) if key in data}
        updatedInstance = serializer.update(instance, validated_data=validated_data)
        self.after_update(oldInstance, updatedInstance, validated_data)
        return jsonify(self.serializer_class(updatedInstance).serialize())

    def patch_object(self, request, pk):
        return self._perform_update(pk, request, part=True)


class DeleteMixin:

    def delete_object(self, request, pk):
        instance = self.get_instance(pk)
        assert isinstance(instance, InstanceWrapper)
        id = instance.get_id()
        instance.delete()
        return jsonify({'id': str(id)})


class ModelResource(GenericResource, ListObjectsMixin, CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin):
    __doc__ = '\n    Generic resource for CRUD on mongoengine models.\n\n    Simple usage example::\n\n        >>> class Model(db.Document):\n        >>>\n        >>>     f1 = db.StringField()\n        >>>     f2 = db.BooleanField()\n        >>>     f3 = db.StringField()\n        >>>\n        >>> class S(ModelSerializer):\n        >>>     class Meta:\n        >>>         model = Model\n        >>>\n        >>> class ModelRes(ModelResource):\n        >>>     serializer_class = S\n        >>>     queryset = Model.objects.all()\n        >>>\n        >>> router = DefaultRouter(app)\n        >>> router.register("/test", ModelRes, "modelres")\n\n    In this configuration will be allowed next HTTP methods:\n\n        * GET /test returns::\n\n            [{\'f1\': \'1\', \'f2\': True, \'f3\': \'1\', \'id\': \'5864db5d32105b50fa02162b\'},\n             {\'f1\': \'2\', \'f2\': True, \'f3\': \'2\', \'id\': \'5864db5d32105b50fa02162c\'}]\n\n        * GET /test/5864db5d32105b50fa02162b returns::\n\n            {\'f1\': \'1\', \'f2\': True, \'f3\': \'1\', \'id\': \'5864e2a332105b5a350b99bc\'}\n\n    '
    __metaclass__ = BaseResourceMetaClass