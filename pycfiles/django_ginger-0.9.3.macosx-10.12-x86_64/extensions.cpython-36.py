# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/template/builtins/extensions.py
# Compiled at: 2015-11-28 19:33:27
# Size of source mod 2**32: 8108 bytes
from __future__ import unicode_literals
import traceback
from django.conf import settings
from django.core.cache import cache
from django.utils import six
from jinja2.ext import Extension
from jinja2 import nodes
from jinja2 import Markup
from jinja2 import TemplateSyntaxError
try:
    from django.utils.encoding import force_text
    from django.utils.encoding import force_bytes
except ImportError:
    from django.utils.encoding import force_unicode as force_text
    from django.utils.encoding import smart_str as force_bytes

from django.core.cache.utils import make_template_fragment_key

class CsrfExtension(Extension):
    tags = set(['csrf_token'])

    def __init__(self, environment):
        self.environment = environment

    def parse(self, parser):
        try:
            token = next(parser.stream)
            call_res = self.call_method('_render', [nodes.Name('csrf_token', 'load')])
            return nodes.Output([call_res]).set_lineno(token.lineno)
        except Exception:
            traceback.print_exc()

    def _render(self, csrf_token):
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return Markup('')
            return Markup("<input type='hidden' name='csrfmiddlewaretoken' value='%s' />" % csrf_token)
        else:
            if settings.DEBUG:
                import warnings
                warnings.warn('A {% csrf_token %} was used in a template, but the contextdid not provide the value.  This is usually caused by not using RequestContext.')
            return ''


class CacheExtension(Extension):
    __doc__ = '\n    Exactly like Django\'s own tag, but supports full Jinja2\n    expressiveness for all arguments.\n\n        {% cache gettimeout()*2 "foo"+options.cachename  %}\n            ...\n        {% endcache %}\n\n    General Syntax:\n\n        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}\n            .. some expensive processing ..\n        {% endcache %}\n\n    Available by default (does not need to be loaded).\n\n    Partly based on the ``FragmentCacheExtension`` from the Jinja2 docs.\n    '
    tags = set(['cache'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        expire_time = parser.parse_expression()
        fragment_name = parser.parse_expression()
        vary_on = []
        while not parser.stream.current.test('block_end'):
            vary_on.append(parser.parse_expression())

        body = parser.parse_statements(['name:endcache'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_cache_support', [
         expire_time, fragment_name,
         nodes.List(vary_on), nodes.Const(lineno)]), [], [], body).set_lineno(lineno)

    def _cache_support(self, expire_time, fragm_name, vary_on, lineno, caller):
        try:
            expire_time = int(expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"%s" tag got a non-integer timeout value: %r' % (
             list(self.tags)[0], expire_time), lineno)

        cache_key = make_template_fragment_key(fragm_name, vary_on)
        value = cache.get(cache_key)
        if value is None:
            value = caller()
            cache.set(cache_key, force_text(value), expire_time)
        return value


class LoadExtension(Extension):
    tags = set(['load'])

    def parse(self, parser):
        while not parser.stream.current.type == 'block_end':
            six.next(parser.stream)

        return []


class URLExtension(Extension):
    __doc__ = 'Returns an absolute URL matching given view with its parameters.\n\nThis is a way to define links that aren\'t tied to a particular URL\nconfiguration::\n\n{% url path.to.some_view arg1,arg2,name1=value1 %}\n\nKnown differences to Django\'s url-Tag:\n\n- In Django, the view name may contain any non-space character.\nSince Jinja\'s lexer does not identify whitespace to us, only\ncharacters that make up valid identifers, plus dots and hyphens\nare allowed. Note that identifers in Jinja 2 may not contain\nnon-ascii characters.\n\nAs an alternative, you may specifify the view as a string,\nwhich bypasses all these restrictions. It further allows you\nto apply filters:\n\n{% url "ghg.some-view"|afilter %}\n'
    tags = set(['url'])

    def parse(self, parser):
        stream = parser.stream
        tag = six.next(stream)
        if stream.current.test('string'):
            if stream.look().test('string'):
                token = six.next(stream)
                viewname = nodes.Const((token.value), lineno=(token.lineno))
            else:
                viewname = parser.parse_expression()
        else:
            bits = []
            name_allowed = True
            while True:
                if stream.current.test_any('dot', 'sub', 'colon'):
                    bits.append(six.next(stream))
                    name_allowed = True
                elif stream.current.test('name') and name_allowed:
                    bits.append(six.next(stream))
                    name_allowed = False
                else:
                    break

            viewname = nodes.Const(''.join([b.value for b in bits]))
        if not bits:
            raise TemplateSyntaxError("'%s' requires path to view" % tag.value, tag.lineno)
        args = []
        kwargs = []
        while not stream.current.test_any('block_end', 'name:as'):
            if args or kwargs:
                stream.expect('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                key = nodes.Const(six.next(stream).value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=(key.lineno)))
            else:
                args.append(parser.parse_expression())

        def make_call_node(*kw):
            return self.call_method('_reverse', args=[
             viewname,
             nodes.List(args),
             nodes.Dict(kwargs),
             nodes.Name('_current_app', 'load')],
              kwargs=kw)

        if stream.next_if('name:as'):
            var = nodes.Name(stream.expect('name').value, 'store')
            call_node = make_call_node(nodes.Keyword('fail', nodes.Const(False)))
            return nodes.Assign(var, call_node)
        else:
            return nodes.Output([make_call_node()]).set_lineno(tag.lineno)

    @classmethod
    def _reverse(self, viewname, args, kwargs, current_app=None, fail=True):
        from django.core.urlresolvers import reverse, NoReverseMatch
        url = ''
        try:
            url = reverse(viewname, args=args, kwargs=kwargs, current_app=current_app)
        except NoReverseMatch:
            projectname = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse((projectname + '.' + viewname), args=args,
                  kwargs=kwargs)
            except NoReverseMatch:
                if fail:
                    raise
                else:
                    return ''

        return url