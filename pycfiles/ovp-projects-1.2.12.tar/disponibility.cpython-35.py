# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/serializers/disponibility.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 2112 bytes
from ovp_projects import models
from ovp_projects.serializers.job import JobSerializer
from ovp_projects.serializers.work import WorkSerializer
from rest_framework import serializers
from collections import OrderedDict
from functools import wraps

def disponibility_validate(disponibility):
    if disponibility['type'] not in ('work', 'job'):
        raise serializers.ValidationError({'type': ["Must have either be 'work' or 'job'."]})
    else:
        disp_type = disponibility['type']
    disponibility_object_validate(disponibility, disp_type)


def disponibility_object_validate(d, k):
    if k not in d:
        raise serializers.ValidationError({k: ['This field is required if type="{}".'.format(k)]})
    if k == 'work':
        serializer = WorkSerializer(data=d[k])
    if k == 'job':
        serializer = JobSerializer(data=d[k])
    serializer.is_valid(raise_exception=True)


def add_disponibility_representation(func):

    @wraps(func)
    def _impl(self, instance):
        for i, field in enumerate(self._readable_fields):
            if field.field_name == 'disponibility':
                disponibility = self._readable_fields.pop(i)

        ret = func(self, instance)
        self._readable_fields.insert(i, disponibility)
        obj = None
        ret['disponibility'] = None
        try:
            type = 'job'
            obj = JobSerializer().to_representation(instance.job)
        except models.Job.DoesNotExist:
            try:
                type = 'work'
                obj = WorkSerializer().to_representation(instance.work)
            except models.Work.DoesNotExist:
                pass

        if obj:
            ret['disponibility'] = {'type': type, 
             type: obj}
        return ret

    return _impl


class DisponibilitySerializer(serializers.Serializer):
    type = serializers.CharField(max_length=4)
    work = WorkSerializer(required=False)
    job = JobSerializer(required=False)

    class Meta:
        validators = [
         disponibility_validate]