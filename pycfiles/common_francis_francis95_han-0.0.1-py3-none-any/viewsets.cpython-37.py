# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/api/viewsets.py
# Compiled at: 2019-07-09 16:57:41
# Size of source mod 2**32: 18660 bytes
from django.core.exceptions import FieldDoesNotExist
from django.db import ProgrammingError
from django.db.models.query import F, EmptyResultSet, Prefetch, QuerySet
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.compat import coreapi
from rest_framework.exceptions import ValidationError
from rest_framework.schemas import AutoSchema
from common.api.utils import AGGREGATES, CACHE_PREFIX, CACHE_TIMEOUT, RESERVED_QUERY_PARAMS, url_value, parse_filters
from common.api.fields import ChoiceDisplayField, ReadOnlyObjectField
from common.models import Entity, MetaData
import common.settings as settings
from common.utils import get_field_by_path, str_to_bool

class CommonModelViewSet(viewsets.ModelViewSet):
    """CommonModelViewSet"""
    url_params = {}
    if coreapi:
        schema = AutoSchema()

    def get_serializer_class(self):
        default_serializer = getattr(self, 'default_serializer', None)
        if default_serializer:
            if self.action not in ('list', 'retrieve', 'update', 'partial_update'):
                return default_serializer
        query_params = getattr(self.request, 'query_params', None)
        url_params = self.url_params or 
        if default_serializer:

            def add_field_to_serializer(fields, field_name):
                if not field_name:
                    return
                field_name = field_name.strip()
                source = field_name.replace('.', '__')
                choices = getattr(get_field_by_path(self.queryset.model, field_name), 'flatchoices', None)
                if choices:
                    if str_to_bool(url_params.get('display')):
                        fields[field_name + '_display'] = ChoiceDisplayField(choices=choices, source=source)
                fields[field_name] = ReadOnlyObjectField(source=(source if '.' in field_name else None))

            aggregations = {}
            for aggregate in AGGREGATES.keys():
                for field in url_params.get(aggregate, '').split(','):
                    if not field:
                        continue
                    field_name = field.strip() + '_' + aggregate
                    source = field_name.replace('.', '__') if '.' in field else None
                    aggregations[field_name] = serializers.ReadOnlyField(source=source)

            if 'group_by' in url_params or aggregations:
                fields = {}
                for field in url_params.get('group_by', '').split(','):
                    add_field_to_serializer(fields, field)

                fields.update(aggregations)
                return type(default_serializer.__name__, (serializers.Serializer,), fields)
            if 'fields' in url_params:
                fields = {}
                for field in url_params.get('fields').split(','):
                    add_field_to_serializer(fields, field)

                return type(default_serializer.__name__, (serializers.Serializer,), fields)
            if str_to_bool(url_params.get('simple')):
                return getattr(self, 'simple_serializer', default_serializer)
            if self.action in ('update', 'partial_update'):
                return default_serializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if issubclass(serializer.Meta.model, Entity):
            return serializer.save(_current_user=(self.request.user))
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        if issubclass(serializer.Meta.model, Entity):
            return serializer.save(_current_user=(self.request.user))
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if isinstance(instance, Entity):
            return instance.delete(_current_user=(self.request.user))
        return super().perform_destroy(instance)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not isinstance(queryset, QuerySet):
            from rest_framework.response import Response
            return Response(queryset)
        try:
            return (super().list)(request, *args, **kwargs)
        except (AttributeError, FieldDoesNotExist) as error:
            try:
                self.queryset_error = error
                raise ValidationError('fields: {}'.format(error))
            finally:
                error = None
                del error

    def paginate_queryset(self, queryset):
        if not isinstance(queryset, QuerySet) or str_to_bool(self.request.query_params.get('all', None)):
            return
        try:
            return super().paginate_queryset(queryset)
        except ProgrammingError as error:
            try:
                raise ValidationError(str(error).split('\n'))
            finally:
                error = None
                del error

    def get_queryset(self):
        if getattr(self, 'queryset_error', False):
            return
        try:
            queryset = super().get_queryset()
            if not isinstance(queryset, QuerySet):
                return queryset
            else:
                options = dict(aggregates=None, distinct=None, filters=None, order_by=None)
                self.url_params = url_params = self.request.query_params.dict()

                def get_from_url_params(name):
                    return url_params.get(name, '').replace('.', '__')

                default_reserved_query_params = [
                 'format'] + ([self.paginator.page_query_param, self.paginator.page_size_query_param] if self.paginator else [])
                reserved_query_params = default_reserved_query_params + RESERVED_QUERY_PARAMS
                cache_key = url_params.pop('cache', None)
                if cache_key:
                    import django.core.cache as cache
                    cache_params = cache.get(CACHE_PREFIX + cache_key, {})
                    new_url_params = {}
                    (new_url_params.update)(**cache_params)
                    (new_url_params.update)(**url_params)
                    self.url_params = url_params = new_url_params
                    new_cache_params = {key:value for key, value in url_params.items() if key not in default_reserved_query_params}
                    if new_cache_params:
                        from django.utils.timezone import now
                        from datetime import timedelta
                        cache_timeout = int(url_params.pop('timeout', CACHE_TIMEOUT)) or 
                        cache.set((CACHE_PREFIX + cache_key), new_cache_params, timeout=cache_timeout)
                        options['cache_expires'] = now() + timedelta(seconds=cache_timeout)
                    cache_url = '{}?cache={}'.format(self.request.build_absolute_uri(self.request.path), cache_key)
                    plain_url = cache_url
                    for key, value in url_params.items():
                        url_param = '&{}={}'.format(key, value)
                        if key in default_reserved_query_params:
                            cache_url += url_param
                        plain_url += url_param

                    options['cache_data'] = new_cache_params
                    options['cache_url'] = cache_url
                    options['raw_url'] = plain_url
                silent = str_to_bool(get_from_url_params('silent'))
                fields = get_from_url_params('fields')
                if str_to_bool(get_from_url_params('simple')) or fields:
                    if queryset.query.select_related:
                        queryset = queryset.select_related(None).prefetch_related(None)
                    try:
                        relateds = set()
                        field_names = set()
                        for field in fields.split(','):
                            if not field:
                                continue
                            field_names.add(field)
                            *related, field_name = field.split('__')
                            if related:
                                relateds.add('__'.join(related))

                        if relateds:
                            queryset = (queryset.select_related)(*relateds)
                        if field_names:
                            queryset = (queryset.values)(*field_names)
                    except Exception as error:
                        try:
                            if not silent:
                                raise ValidationError('fields: {}'.format(error))
                        finally:
                            error = None
                            del error

            metadata = str_to_bool(get_from_url_params('meta'))
            if metadata:
                if hasattr(self, 'metadata'):
                    viewset_lookups = [prefetch if isinstance(prefetch, str) else prefetch.prefetch_through for prefetch in queryset._prefetch_related_lookups]
                    lookups_metadata = []
                    for lookup in self.metadata or :
                        if isinstance(lookup, str):
                            lookup = Prefetch(lookup)
                        if lookup.prefetch_through not in viewset_lookups:
                            lookups_metadata.append(lookup)
                        lookup.queryset = MetaData.objects.select_valid()

                    if lookups_metadata:
                        queryset = (queryset.prefetch_related)(*lookups_metadata)

            def do_filter(queryset):
                try:
                    filters, excludes = {}, {}
                    for key, value in url_params.items():
                        key = key.replace('.', '__')
                        if value.startswith('('):
                            if value.endswith(')'):
                                value = F(value[1:-1])
                        if key in reserved_query_params:
                            continue
                        if key.startswith('-'):
                            key = key[1:].strip()
                            excludes[key] = url_value(key, value)
                        else:
                            key = key.strip()
                            filters[key] = url_value(key, value)

                    if filters:
                        queryset = (queryset.filter)(**filters)
                    if excludes:
                        queryset = (queryset.exclude)(**excludes)
                    others = get_from_url_params('filters')
                    if others:
                        queryset = queryset.filter(parse_filters(others))
                    if filters or others:
                        options['filters'] = True
                except Exception as error:
                    try:
                        if not silent:
                            raise ValidationError('filters: {}'.format(error))
                        options['filters'] = False
                        if settings.DEBUG:
                            options['filters_error'] = str(error)
                    finally:
                        error = None
                        del error

                return queryset

            if self.action == 'list':
                try:
                    aggregations = {}
                    for aggregate, function in AGGREGATES.items():
                        for field in get_from_url_params(aggregate).split(','):
                            if not field:
                                continue
                            distinct = field.startswith(' ')
                            field = field.strip().replace('.', '__')
                            aggregations[field + '_' + aggregate] = function(field, distinct=distinct)

                    group_by = get_from_url_params('group_by')
                    if group_by:
                        _queryset = (queryset.values)(*group_by.split(','))
                        if aggregations:
                            _queryset = (_queryset.annotate)(**aggregations)
                        else:
                            _queryset = _queryset.distinct()
                        queryset = _queryset
                        options['aggregates'] = True
                    elif aggregations:
                        queryset = do_filter(queryset)
                        return (queryset.aggregate)(**aggregations)
                except Exception as error:
                    try:
                        if not silent:
                            raise ValidationError('aggregates: {}'.format(error))
                        options['aggregates'] = False
                        if settings.DEBUG:
                            options['aggregates_error'] = str(error)
                    finally:
                        error = None
                        del error

            queryset = do_filter(queryset)
            try:
                order_by = get_from_url_params('order_by')
                if order_by:
                    _queryset = (queryset.order_by)(*order_by.split(','))
                    str(_queryset.query)
                    queryset = _queryset
                    options['order_by'] = True
            except EmptyResultSet:
                pass
            except Exception as error:
                try:
                    if not silent:
                        raise ValidationError('order_by: {}'.format(error))
                    options['order_by'] = False
                    if settings.DEBUG:
                        options['order_by_error'] = str(error)
                finally:
                    error = None
                    del error

            distincts = []
            try:
                distinct = get_from_url_params('distinct')
                if distinct:
                    distincts = distinct.split(',')
                    if str_to_bool(distinct) is not None:
                        distincts = []
                    queryset = (queryset.distinct)(*distincts)
                    options['distinct'] = True
            except EmptyResultSet:
                pass
            except Exception as error:
                try:
                    if not silent:
                        raise ValidationError('distinct: {}'.format(error))
                    options['distinct'] = False
                    if settings.DEBUG:
                        options['distinct_error'] = str(error)
                finally:
                    error = None
                    del error

            if self.paginator:
                if hasattr(self.paginator, 'additional_data'):
                    if hasattr(queryset, 'ordered'):
                        if not queryset.ordered:
                            queryset = (queryset.order_by)(*getattr(queryset, '_fields', None) or )
                    self.paginator.additional_data = dict(options=options)
            return queryset
        except ValidationError as error:
            try:
                self.queryset_error = error
                raise error
            finally:
                error = None
                del error


class UserViewSet(CommonModelViewSet):
    """UserViewSet"""

    def check_permissions(self, request):
        current_user = request.user
        if current_user.is_superuser:
            return True
        if self.action in ('create', ):
            return True
        if self.action in ('update', 'partial_update'):
            self.kwargs.update({self.lookup_field: self.kwargs.get(self.lookup_url_kwarg or , None)})
            user = self.get_object()
            if not current_user == user:
                if current_user.is_staff:
                    if not user.is_staff:
                        if not user.is_superuser:
                            return True
        return super().check_permissions(request)

    def check_data(self, data):
        user = self.request.user
        if user and not user.is_staff:
            if not user.is_superuser:
                data['is_active'] = True
        if not (user and user.is_staff):
            data['is_staff'] = False
        if not (user and user.is_superuser):
            data['is_superuser'] = False
        if 'groups' in data and data.get('groups'):
            if not user:
                data['groups'] = []
        elif not user.is_superuser:
            groups = user.groups.all()
            data['groups'] = list(set(groups) & set(data.get('groups', [])))
        elif 'user_permissions' in data:
            if data.get('user_permissions'):
                if not user:
                    data['user_permissions'] = []
                else:
                    user_permissions = user.is_superuser or user.user_permissions.all()
                    data['user_permissions'] = list(set(user_permissions) & set(data.get('user_permissions', [])))

    def perform_create(self, serializer):
        self.check_data(serializer.validated_data)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        self.check_data(serializer.validated_data)
        super().perform_update(serializer)