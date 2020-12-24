# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/danielwatkins/dev/django-rest-test-data/rest_test_data/views.py
# Compiled at: 2013-11-25 08:41:21
# Size of source mod 2**32: 4002 bytes
import json, logging
from django.core import serializers
from django.db.models import get_model
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import six
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from model_mommy import mommy
logger = logging.getLogger(__name__)

class BaseTestDataRestView(View):

    @property
    def serializer(self):
        return serializers.get_serializer('json')()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.model = get_model(kwargs['app'], kwargs['model'])
        if self.model is None:
            return HttpResponseNotFound()
        else:
            if 'pk' in kwargs:
                try:
                    self.object = self.get_object(int(kwargs['pk']), model=self.model)
                except:
                    logger.exception('Error fetching object')
                    return HttpResponseNotFound()

            self.data = None
            if request.body:
                body = request.body.decode('utf-8')
                self.data = json.loads(body)
            result = super(BaseTestDataRestView, self).dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            else:
                if isinstance(result, six.string_types):
                    return HttpResponse(result, content_type='application/json')
                return HttpResponse(json.dumps(result), content_type='application/json')
            return

    @staticmethod
    def get_object(value, model=None):
        if model is None:
            model, value = value.split(':')
            model = get_model(*model.split('.'))
            value = int(value)
        return model.objects.get(pk=value)

    @classmethod
    def get_data(cls, data):
        kwargs = data.get('data', {}).copy()
        for key, value in six.iteritems(data.get('objects', {})):
            if isinstance(value, list):
                kwargs[key] = [cls.get_object(i) for i in value]
            else:
                kwargs[key] = cls.get_object(value)

        return kwargs


class TestDataModelRestView(BaseTestDataRestView):

    def get(self, request, *args, **kwargs):
        return self.serializer.serialize(self.model.objects.all())

    def delete(self, request, *args, **kwargs):
        try:
            qs = self.model.objects.all()
            count = qs.count()
            qs.delete()
        except:
            logger.exception('Error deleting objects')
            return False
        else:
            return count

    def post(self, request, *args, **kwargs):
        if self.data is None:
            data = {}
        else:
            data = self.get_data(self.data)
        obj = mommy.make(self.model, **data)
        return self.serializer.serialize([
         self.model.objects.get(pk=obj.pk)])


class TestDataDetailRestView(BaseTestDataRestView):

    def get(self, request, *args, **kwargs):
        return self.serializer.serialize([self.object])

    def delete(self, request, *args, **kwargs):
        try:
            self.object.delete()
        except:
            logger.exception('Error deleting object')
            return False
        else:
            return True


class TestDataSearchRestView(BaseTestDataRestView):

    def post(self, request, *args, **kwargs):
        if self.data is None:
            data = {}
        else:
            data = self.get_data(self.data)
        return self.serializer.serialize(self.model.objects.filter(**data))