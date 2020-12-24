# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/extensions.py
# Compiled at: 2014-03-31 04:42:18
# Size of source mod 2**32: 4645 bytes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError
from jinja2 import nodes
from django.conf import settings

class URLExtension(Extension):
    __doc__ = 'Returns an absolute URL matching given view with its parameters.\n\nThis is a way to define links that aren\'t tied to a particular URL\nconfiguration::\n\n{% url path.to.some_view arg1,arg2,name1=value1 %}\n\nKnown differences to Django\'s url-Tag:\n\n- In Django, the view name may contain any non-space character.\nSince Jinja\'s lexer does not identify whitespace to us, only\ncharacters that make up valid identifers, plus dots and hyphens\nare allowed. Note that identifers in Jinja 2 may not contain\nnon-ascii characters.\n\nAs an alternative, you may specifify the view as a string,\nwhich bypasses all these restrictions. It further allows you\nto apply filters:\n\n{% url "ghg.some-view"|afilter %}\n'
    tags = set(['url'])

    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()
        if stream.current.test('string'):
            if stream.look().test('string'):
                token = stream.next()
                viewname = nodes.Const(token.value, lineno=token.lineno)
            else:
                viewname = parser.parse_expression()
        else:
            bits = []
            name_allowed = True
            while True:
                if stream.current.test_any('dot', 'sub', 'colon'):
                    bits.append(stream.next())
                    name_allowed = True
                elif stream.current.test('name') and name_allowed:
                    bits.append(stream.next())
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
                key = nodes.Const(stream.next().value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))
            else:
                args.append(parser.parse_expression())

        def make_call_node(*kw):
            return self.call_method('_reverse', args=[
             viewname,
             nodes.List(args),
             nodes.Dict(kwargs),
             nodes.Name('_current_app', 'load')], kwargs=kw)

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
                url = reverse(projectname + '.' + viewname, args=args, kwargs=kwargs)
            except NoReverseMatch:
                if fail:
                    raise
                else:
                    return ''

        return url