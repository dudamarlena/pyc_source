# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ssi/templatetags/nginxssi_tags.py
# Compiled at: 2011-01-25 14:23:58
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django import template
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.db.models import Model
from django.conf import settings
from ssi.utils import generate_ssi_cache_key
register = Library()

class NginxSSINode(Node):

    def __init__(self, cache_key):
        self.cache_key = cache_key

    def render(self, context):
        cache.set('%s:context' % self.cache_key, context)
        return '<!--# include virtual="/nginxssi/%s/" -->' % self.cache_key


@register.tag
def nginxssi(parser, token):
    tokens = token.split_contents()
    template_string = render_raw_template(parser, token, 'endnginxssi')
    cache_key = generate_ssi_cache_key(template_string)
    if cache_key not in cache:
        cache.set(cache_key, template_string)
    return NginxSSINode(cache_key)


def render_raw_template(parser, token, parse_until):
    text = []
    tag_mapping = {template.TOKEN_TEXT: ('', ''), 
       template.TOKEN_VAR: ('{{', '}}'), 
       template.TOKEN_BLOCK: ('{%', '%}'), 
       template.TOKEN_COMMENT: ('{#', '#}')}
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == template.TOKEN_BLOCK and token.contents == parse_until:
            return ('').join(text)
        (start, end) = tag_mapping[token.token_type]
        text.append('%s%s%s' % (start, token.contents, end))

    parser.unclosed_block_tag(parse_until)