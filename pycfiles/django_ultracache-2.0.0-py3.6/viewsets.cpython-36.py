# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/viewsets.py
# Compiled at: 2018-09-10 07:18:30
# Size of source mod 2**32: 420 bytes
import django
from rest_framework import viewsets, serializers
from ultracache.tests.models import DummyModel

class DummySerializer(serializers.ModelSerializer):

    class Meta:
        model = DummyModel
        if not django.get_version().startswith('1.6'):
            fields = '__all__'


class DummyViewSet(viewsets.ModelViewSet):
    queryset = DummyModel.objects.all()
    serializer_class = DummySerializer