# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/checks/urls.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from collections import Counter
from django.conf import settings
from django.utils import six
from . import Error, Tags, Warning, register

@register(Tags.urls)
def check_url_config(app_configs, **kwargs):
    if getattr(settings, b'ROOT_URLCONF', None):
        from django.urls import get_resolver
        resolver = get_resolver()
        return check_resolver(resolver)
    else:
        return []


def check_resolver(resolver):
    """
    Recursively check the resolver.
    """
    check_method = getattr(resolver, b'check', None)
    if check_method is not None:
        return check_method()
    else:
        if not hasattr(resolver, b'resolve'):
            return get_warning_for_invalid_pattern(resolver)
        else:
            return []

        return


@register(Tags.urls)
def check_url_namespaces_unique(app_configs, **kwargs):
    """
    Warn if URL namespaces used in applications aren't unique.
    """
    if not getattr(settings, b'ROOT_URLCONF', None):
        return []
    else:
        from django.urls import get_resolver
        resolver = get_resolver()
        all_namespaces = _load_all_namespaces(resolver)
        counter = Counter(all_namespaces)
        non_unique_namespaces = [ n for n, count in counter.items() if count > 1 ]
        errors = []
        for namespace in non_unique_namespaces:
            errors.append(Warning((b"URL namespace '{}' isn't unique. You may not be able to reverse all URLs in this namespace").format(namespace), id=b'urls.W005'))

        return errors


def _load_all_namespaces(resolver, parents=()):
    """
    Recursively load all namespaces from URL patterns.
    """
    url_patterns = getattr(resolver, b'url_patterns', [])
    namespaces = [ (b':').join(parents + (url.namespace,)) for url in url_patterns if getattr(url, b'namespace', None) is not None
                 ]
    for pattern in url_patterns:
        namespace = getattr(pattern, b'namespace', None)
        current = parents
        if namespace is not None:
            current += (namespace,)
        namespaces.extend(_load_all_namespaces(pattern, current))

    return namespaces


def get_warning_for_invalid_pattern(pattern):
    """
    Return a list containing a warning that the pattern is invalid.

    describe_pattern() cannot be used here, because we cannot rely on the
    urlpattern having regex or name attributes.
    """
    if isinstance(pattern, six.string_types):
        hint = (b"Try removing the string '{}'. The list of urlpatterns should not have a prefix string as the first element.").format(pattern)
    elif isinstance(pattern, tuple):
        hint = b'Try using url() instead of a tuple.'
    else:
        hint = None
    return [
     Error((b'Your URL pattern {!r} is invalid. Ensure that urlpatterns is a list of url() instances.').format(pattern), hint=hint, id=b'urls.E004')]


@register(Tags.urls)
def check_url_settings(app_configs, **kwargs):
    errors = []
    for name in ('STATIC_URL', 'MEDIA_URL'):
        value = getattr(settings, name)
        if value and not value.endswith(b'/'):
            errors.append(E006(name))

    return errors


def E006(name):
    return Error((b'The {} setting must end with a slash.').format(name), id=b'urls.E006')