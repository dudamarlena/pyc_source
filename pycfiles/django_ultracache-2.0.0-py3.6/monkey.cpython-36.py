# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/monkey.py
# Compiled at: 2019-12-31 02:49:50
# Size of source mod 2**32: 9436 bytes
"""Monkey patch template variable resolution so we can recognize which objects
are covered within a containing caching template tag. The patch is based on
Django 1.11 but is backwards compatible with 1.9."""
import hashlib, inspect, pickle, types
from collections import OrderedDict
from django.core.cache import cache
from django.db.models import Model, Manager
from django.template.base import Variable, VariableDoesNotExist
from django.template.context import BaseContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from ultracache import _thread_locals
from ultracache.utils import cache_meta, get_current_site_pk
try:
    from django.template.base import logger
except ImportError:
    logger = None

def my_resolve_lookup(self, context):
    """
        Performs resolution of a real variable (i.e. not a literal) against the
        given context.

        As indicated by the method's name, this method is an implementation
        detail and shouldn"t be called by external code. Use Variable.resolve()
        instead.
        """
    current = context
    try:
        for bit in self.lookups:
            try:
                current = current[bit]
            except (TypeError, AttributeError, KeyError, ValueError, IndexError):
                try:
                    if isinstance(current, BaseContext):
                        if getattr(type(current), bit):
                            raise AttributeError
                    current = getattr(current, bit)
                except (TypeError, AttributeError) as e:
                    if isinstance(e, AttributeError):
                        if not isinstance(current, BaseContext):
                            if bit in dir(current):
                                raise
                    try:
                        current = current[int(bit)]
                    except (IndexError, ValueError,
                     KeyError,
                     TypeError):
                        raise VariableDoesNotExist('Failed lookup for key [%s] in %r', (
                         bit, current))

            if callable(current):
                if getattr(current, 'do_not_call_in_templates', False):
                    pass
                else:
                    if getattr(current, 'alters_data', False):
                        try:
                            current = context.template.engine.string_if_invalid
                        except AttributeError:
                            current = settings.TEMPLATE_STRING_IF_INVALID

                    else:
                        try:
                            current = current()
                        except TypeError:
                            try:
                                inspect.getcallargs(current)
                            except TypeError:
                                current = context.template.engine.string_if_invalid
                            else:
                                raise

            else:
                if isinstance(current, Model) and 'request' in context and hasattr(context['request'], '_ultracache'):
                    ct = ContentType.objects.get_for_model(current.__class__)
                    context['request']._ultracache.append((ct.id, current.pk))

    except Exception as e:
        template_name = getattr(context, 'template_name', None) or 'unknown'
        if logger is not None:
            logger.debug('Exception while resolving variable "%s" in template "%s".',
              bit,
              template_name,
              exc_info=True)
        if getattr(e, 'silent_variable_failure', False):
            current = context.template.engine.string_if_invalid
        else:
            raise

    return current


Variable._resolve_lookup = my_resolve_lookup
try:
    from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
    from rest_framework.response import Response
    from rest_framework.serializers import Serializer, ListSerializer
    HAS_DRF = True
except ImportError:
    HAS_DRF = False

def drf_cache(func):

    def wrapped(context, request, *args, **kwargs):
        viewsets = settings.ULTRACACHE.get('drf', {}).get('viewsets', {})
        dotted_name = context.__module__ + '.' + context.__class__.__name__
        do_cache = dotted_name in viewsets or context.__class__ in viewsets or '*' in viewsets
        if do_cache:
            li = [
             request.get_full_path()]
            viewset_settings = viewsets.get(dotted_name, {}) or viewsets.get(context.__class__, {}) or viewsets.get('*', {})
            evaluate = viewset_settings.get('evaluate', None)
            if evaluate is not None:
                if callable(evaluate):
                    li.append(evaluate(context, request))
                else:
                    li.append(eval(evaluate))
            if 'django.contrib.sites' in settings.INSTALLED_APPS:
                li.append(get_current_site_pk(request))
            s = ':'.join([str(l) for l in li])
            cache_key = hashlib.md5(s.encode('utf-8')).hexdigest()
            cached = cache.get(cache_key, None)
            if cached is not None:
                response = Response(pickle.loads(cached['content']))
                for k, v in cached['headers'].items():
                    response[v[0]] = v[1]

                return response
        if not hasattr(request, '_ultracache'):
            setattr(request, '_ultracache', [])
            setattr(request, '_ultracache_cache_key_range', [])
        response = func(context, request, *args, **kwargs)
        if do_cache:
            cache_meta((_thread_locals.ultracache_recorder), cache_key, request=request)
            response = (context.finalize_response)(request, response, *args, **kwargs)
            response.render()
            timeout = viewset_settings.get('timeout', 300)
            headers = getattr(response, '_headers', {})
            cache.set(cache_key, {'content':pickle.dumps(response.data), 
             'headers':headers}, timeout)
            return response
        else:
            return response

    return wrapped


def _serializer(func):

    def wrapped(context, instance):
        request = context.context['request']
        if hasattr(request, '_ultracache'):
            if isinstance(instance, Model):
                ct = ContentType.objects.get_for_model(instance.__class__)
                request._ultracache.append((ct.id, instance.pk))
        return func(context, instance)

    return wrapped


def _listserializer(func):

    def wrapped(context, data):
        request = context.context['request']
        if hasattr(request, '_ultracache'):
            iterable = data.all() if isinstance(data, Manager) else data
            for obj in iterable:
                if isinstance(obj, Model):
                    ct = ContentType.objects.get_for_model(obj.__class__)
                    request._ultracache.append((ct.id, obj.pk))

        return func(context, data)

    return wrapped


if HAS_DRF:
    ListModelMixin.list = drf_cache(ListModelMixin.list)
    RetrieveModelMixin.retrieve = drf_cache(RetrieveModelMixin.retrieve)
    Serializer.to_representation = _serializer(Serializer.to_representation)
    ListSerializer.to_representation = _listserializer(ListSerializer.to_representation)

def my__getattribute__(self, name):
    if hasattr(_thread_locals, 'ultracache_recorder'):
        if not hasattr(_thread_locals, '_ultracache_attr_marker'):
            setattr(_thread_locals, '_ultracache_attr_marker', 1)
            if hasattr(self, 'pk'):
                ct = ContentType.objects.get_for_model(self.__class__)
                _thread_locals.ultracache_recorder.append((ct.id, self.pk))
            delattr(_thread_locals, '_ultracache_attr_marker')
    return super(Model, self).__getattribute__(name)


Model.__getattribute__ = my__getattribute__