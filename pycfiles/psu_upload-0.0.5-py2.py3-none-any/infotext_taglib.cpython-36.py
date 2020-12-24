# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mjg/git/django/psu/psu-infotext/psu_infotext/templatetags/infotext_taglib.py
# Compiled at: 2019-09-09 17:37:46
# Size of source mod 2**32: 4023 bytes
from django import template
from psu_infotext.models import Infotext
from ast import literal_eval
from psu_base.classes.Log import Log
from psu_base.templatetags.tag_processing import supporting_functions as support
from psu_base.services import utility_service
from django.utils.html import format_html
from django.template import TemplateSyntaxError
register = template.Library()
log = Log()

@register.simple_tag(takes_context=True)
def infotext(context, code, alt, replacements=None, auto_prefix=True):
    """
    Render user-editable text content
    """
    log.trace()
    attrs = {'code':code,  'alt':alt,  'auto_prefix':str(auto_prefix)}
    if replacements:
        attrs['replacements'] = replacements
    return prepare_infotext(attrs, alt, context)


@register.tag()
def infotext_block(parser, token):
    """
    Render user-editable text content
    """
    log.trace()
    tokens = token.split_contents()
    try:
        nodelist = parser.parse((f"end_{tokens[0]}",))
        parser.delete_first_token()
    except TemplateSyntaxError:
        nodelist = None

    return InfotextNode(nodelist, tokens)


class InfotextNode(template.Node):

    def __init__(self, nodelist, tokens):
        self.nodelist = nodelist
        self.tokens = tokens

    def render(self, context):
        log.trace()
        attrs, body = support.get_tag_params(self.nodelist, self.tokens, context)
        return prepare_infotext(attrs, body, context)


def prepare_infotext(attrs, alt_text, context):
    """
    Prepare infotext for both tags (inline and block)
    """
    log.trace(attrs)
    app = utility_service.get_app_code()
    path = context['request'].get_full_path().replace('/', '.').strip('.').lower()
    if not path.startswith(app):
        prefix = '{0}.{1}'.format(app, path)
    else:
        prefix = path
    if attrs.get('auto_prefix', 'True').lower() not in ('false', 'no', 'n'):
        infotext_code = f"{prefix}.{attrs['code']}".strip().lower()
    else:
        infotext_code = attrs['code'].strip().lower()
    log.debug(f"Infotext Code: {infotext_code}")
    result = Infotext.objects.filter(app_code=(app.upper())).filter(text_code=infotext_code)
    if not result:
        instance = Infotext(app_code=(app.upper()),
          text_code=infotext_code,
          content=alt_text)
        instance.save()
    else:
        instance = result[0]
    if instance.user_edited == 'N' and instance.content != alt_text:
        instance.content = alt_text
        instance.save()
    else:
        if instance.user_edited == 'Y':
            if instance.content == alt_text:
                instance.user_edited = 'N'
                instance.save()
    if instance.user_edited == 'Y':
        if utility_service.get_environment() == 'DEV':
            log.warn(f"{infotext_code} has been updated to: '{instance.content}'")
    content = instance.content
    if 'replacements' in attrs:
        replacements = attrs['replacements']
        if type(replacements) is str:
            for key, val in literal_eval(replacements).items():
                content = content.replace(key, val)

        elif type(replacements) is dict:
            for key, val in replacements.items():
                content = content.replace(key, val)

    log.end()
    return format_html(content)