# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/datapunt_api/rest.py
from rest_framework import viewsets
from rest_framework import renderers
from rest_framework_extensions.mixins import DetailSerializerMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework_xml.renderers import XMLRenderer
from .renderers import PaginatedCSVRenderer
from .pagination import HALPagination
from .serializers import DisplayField, DataSetSerializerMixin, get_links, HALSerializer, LinksField, RelatedSummaryField, SelfLinkSerializerMixin
DEFAULT_RENDERERS = [
 renderers.JSONRenderer,
 PaginatedCSVRenderer,
 renderers.BrowsableAPIRenderer,
 XMLRenderer]
if api_settings.DEFAULT_RENDERER_CLASSES:
    DEFAULT_RENDERERS = api_settings.DEFAULT_RENDERER_CLASSES

class _DisabledHTMLFilterBackend(DjangoFilterBackend):
    __doc__ = 'See https://github.com/tomchristie/django-rest-framework/issues/3766.\n\n    This prevents DRF from generating the filter dropdowns (which can be HUGE\n    in our case)\n    '

    def to_html(self, request, queryset, view):
        return ''


def _is_detailed_request(detailed_keyword, request):
    value = request.GET.get(detailed_keyword, False)
    if value:
        if value.lower() in (1, '1', True, 'true', 'yes'):
            return True


class DatapuntViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    __doc__ = 'ViewSet subclass for use in Datapunt APIs.\n\n    Note:\n    - this uses HAL JSON style pagination.\n    '
    renderer_classes = DEFAULT_RENDERERS
    pagination_class = HALPagination
    filter_backends = (_DisabledHTMLFilterBackend,)
    detailed_keyword = 'detailed'

    def list(self, request, *args, **kwargs):
        if _is_detailed_request(self.detailed_keyword, request):
            self.serializer_class = self.serializer_detail_class
        return (super().list)(request, *args, **kwargs)

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['header'] = self.request.GET['fields'].split(',') if 'fields' in self.request.GET else None
        return context


class DatapuntViewSetWritable(DetailSerializerMixin, viewsets.ModelViewSet):
    __doc__ = 'ViewSet subclass for use in Datapunt APIs.\n\n    Note:\n    - this uses HAL JSON style pagination.\n    '
    renderer_classes = DEFAULT_RENDERERS
    pagination_class = HALPagination
    filter_backends = (_DisabledHTMLFilterBackend,)
    detailed_keyword = 'detailed'

    def list(self, request, *args, **kwargs):
        if _is_detailed_request(self.detailed_keyword, request):
            self.serializer_class = self.serializer_detail_class
        return (super().list)(request, *args, **kwargs)