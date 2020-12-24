# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/serializers.py
# Compiled at: 2020-04-30 08:35:11
# Size of source mod 2**32: 4780 bytes
import os.path
from django.shortcuts import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from tom_targets.models import Target
from tom_dataproducts.models import DataProduct
from tom_education.models import AsyncProcess, PipelineProcess

class TimestampField(serializers.Field):

    def to_representation(self, dt):
        return dt.timestamp()


class AsyncProcessSerializer(serializers.ModelSerializer):
    created = TimestampField()
    terminal_timestamp = TimestampField()
    failure_message = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = AsyncProcess
        fields = [
         'identifier', 'created', 'status', 'terminal_timestamp', 'failure_message', 'view_url',
         'process_type']

    def get_view_url(self, obj):
        """
        Special case for PipelineProcess objects: provide link to detail view
        """
        if hasattr(obj, 'pipelineprocess'):
            return reverse('tom_education:pipeline_detail', kwargs={'pk': obj.pk})

    def get_failure_message(self, obj):
        return obj.failure_message or None


class PipelineProcessSerializer(AsyncProcessSerializer):
    group_name = serializers.SerializerMethodField()
    group_url = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    class Meta:
        model = PipelineProcess
        fields = [
         'identifier', 'created', 'status', 'terminal_timestamp', 'failure_message', 'view_url',
         'logs', 'group_name', 'group_url']

    def get_group_name(self, obj):
        if obj.group:
            return obj.group.name

    def get_group_url(self, obj):
        if obj.group:
            return reverse('tom_dataproducts:group-detail', kwargs={'pk': obj.group.pk})

    def get_logs(self, obj):
        """
        Make sure logs is always a string
        """
        return obj.logs or ''


class TargetSerializer(serializers.ModelSerializer):
    __doc__ = '\n    Serialize a subset of the Target fields, plus any extra fields\n    '

    class Meta:
        model = Target
        fields = ['name', 'extra_fields']


class PhotometrySerializer(serializers.Serializer):
    __doc__ = '\n    Serializer for photometry data file URL and image\n    '
    csv = serializers.SerializerMethodField()
    plot = serializers.SerializerMethodField()

    def get_csv(self, obj):
        url = reverse('tom_education:photometry_download', kwargs={'pk': obj.id})
        connection_type = 'https'
        if settings.DEBUG:
            connection_type = 'http'
        request = self.context.get('request')
        full_url = f"{connection_type}://{get_current_site(request)}{url}"
        return full_url

    def get_plot(self, obj):
        try:
            dp = DataProduct.objects.filter(target=obj, data_product_type='plot').latest('created')
            return dp.data.url
        except ObjectDoesNotExist:
            return


class TimelapsePipelineSerializer(serializers.Serializer):
    __doc__ = '\n    Serialize basic info for a timelapse from a TimelapsePipeline object,\n    including the (relative) URL to the actual timelapse file\n    '
    name = serializers.SerializerMethodField()
    format = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    frames = serializers.SerializerMethodField()

    def _get_dataproduct(self, obj):
        return obj.group.dataproduct_set.first()

    def get_name(self, obj):
        return os.path.basename(self._get_dataproduct(obj).data.name)

    def get_format(self, obj):
        filename = self.get_name(obj)
        return filename.split('.')[(-1)]

    def get_url(self, obj):
        return self._get_dataproduct(obj).data.url

    def get_created(self, obj):
        return TimestampField().to_representation(obj.terminal_timestamp)

    def get_frames(self, obj):
        return obj.input_files.count()


class TargetDetailSerializer(serializers.Serializer):
    __doc__ = '\n    Response for target detail API: includes information about the target and\n    its timelapses\n    '
    target = TargetSerializer()
    timelapses = serializers.ListSerializer(child=(TimelapsePipelineSerializer()))
    data = PhotometrySerializer()


class ObservationAlertSerializer(serializers.Serializer):
    target = serializers.IntegerField(min_value=1)
    template_name = serializers.CharField()
    facility = serializers.CharField()
    overrides = serializers.DictField(required=False)
    email = serializers.EmailField()