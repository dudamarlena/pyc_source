# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/templatetags/ultracache_tags.py
# Compiled at: 2019-05-31 04:25:01
from django import template
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.utils.functional import Promise
from django.templatetags.cache import CacheNode
from django.template.base import VariableDoesNotExist
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.conf import settings
from ultracache import _thread_locals
from ultracache.utils import cache_meta, get_current_site_pk
register = template.Library()

class UltraCacheNode(CacheNode):
    """Based on Django's default cache template tag. Add SITE_ID as implicit
    vary on parameter is sites product is installed. Allow unresolvable
    variables. Allow translated strings."""

    def __init__(self, *args):
        try:
            super(UltraCacheNode, self).__init__(cache_name=None, *args)
        except TypeError:
            super(UltraCacheNode, self).__init__(*args)

        return

    def render(self, context):
        try:
            expire_time = self.expire_time_var.resolve(context)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('ultracache tag got an unknown variable: %r' % self.expire_time_var.var)

        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('ultracache tag got a non-integer timeout value: %r' % expire_time)

        request = context['request']
        if request.method.lower() not in ('get', 'head'):
            return self.nodelist.render(context)
        else:
            if not hasattr(_thread_locals, 'ultracache_recorder'):
                setattr(_thread_locals, 'ultracache_recorder', [])
                start_index = 0
            else:
                start_index = len(_thread_locals.ultracache_recorder)
            vary_on = []
            if 'django.contrib.sites' in settings.INSTALLED_APPS:
                vary_on.append(str(get_current_site_pk(request)))
            for var in self.vary_on:
                try:
                    r = var.resolve(context)
                except VariableDoesNotExist:
                    pass

                if isinstance(r, Promise):
                    r = force_text(r)
                vary_on.append(r)

            cache_key = make_template_fragment_key(self.fragment_name, vary_on)
            value = cache.get(cache_key)
            if value is None:
                value = self.nodelist.render(context)
                cache.set(cache_key, value, expire_time)
                cache_meta(_thread_locals.ultracache_recorder, cache_key, start_index, request=request)
            else:
                for tu in cache.get(cache_key + '-objs', []):
                    _thread_locals.ultracache_recorder.append(tu)

            return value


@register.tag('ultracache')
def do_ultracache(parser, token):
    """Based on Django's default cache template tag"""
    nodelist = parser.parse(('endultracache', ))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError('' % ' tag requires at least 2 arguments.' % tokens[0])
    return UltraCacheNode(nodelist, parser.compile_filter(tokens[1]), tokens[2], [ parser.compile_filter(token) for token in tokens[3:] ])