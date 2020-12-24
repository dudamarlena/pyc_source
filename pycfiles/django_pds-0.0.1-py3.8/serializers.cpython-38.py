# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/serializers.py
# Compiled at: 2020-05-11 13:43:42
# Size of source mod 2**32: 1759 bytes
from mongoengine import base
from mongoengine.queryset.queryset import QuerySet
from rest_framework_mongoengine import serializers

class GenericSerializerAlpha:
    _GenericSerializerAlpha__fields = ()
    _GenericSerializerAlpha__document = None

    def __init__(self, document_name=None, fields=None):
        if document_name:
            self._GenericSerializerAlpha__document = base.get_document(document_name)
        if fields:
            self._GenericSerializerAlpha__fields = fields

    def fields(self, fields='__all__'):
        self._GenericSerializerAlpha__fields = fields
        return self

    def document(self, document_name):
        self._GenericSerializerAlpha__document = base.get_document(document_name)
        return self

    def delete(self):
        self.__del__()

    def __del__(self):
        pass

    def select(self, field):
        if type(self._GenericSerializerAlpha__fields) == tuple:
            self._GenericSerializerAlpha__fields = self._GenericSerializerAlpha__fields + (field,)
        else:
            self._GenericSerializerAlpha__fields = (
             field,)
        return self

    def select_all(self):
        self._GenericSerializerAlpha__fields = '__all__'
        return self

    def serialize(self, data, many=True, allow_null=True):
        if type(data) is not QuerySet:
            many = False
        resp = self._GenSerializerAlpha(data, many=many, allow_null=allow_null, fields=(self._GenericSerializerAlpha__fields), document=(self._GenericSerializerAlpha__document))
        return resp

    class _GenSerializerAlpha(serializers.DocumentSerializer):

        def __init__(self, *args, **kwargs):
            _GenSerializerAlpha__fields = kwargs.pop('fields', '__all__')
            _GenSerializerAlpha__document = kwargs.pop('document', None)
            (super(GenericSerializerAlpha._GenSerializerAlpha, self).__init__)(*args, **kwargs)
            self.Meta.fields = _GenSerializerAlpha__fields
            self.Meta.model = _GenSerializerAlpha__document

        class Meta:
            model = None
            fields = '__all__'