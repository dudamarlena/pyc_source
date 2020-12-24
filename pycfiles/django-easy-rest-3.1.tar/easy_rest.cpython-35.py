# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jonatan/myprojects/django-easy-rest/easy_rest/templatetags/easy_rest.py
# Compiled at: 2018-06-14 16:33:48
# Size of source mod 2**32: 3634 bytes
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
register = template.Library()
load_message = ''
root = '/easy_rest/static'
if hasattr(settings, 'EASY_REST_ROOT_URL'):
    root = '/' + settings.EASY_REST_ROOT_URL + '/static'
else:
    load_message = '<!--{0}-->\n<script>console.warn("{0}")</script>'.format('EASY_REST_ROOT_URL not specified in settings defaulting with easy_rest ')
js_base = '<script src="' + root + '/{}"></script>'
css_base = '<link rel="stylesheet" href="' + root + '/{}">'

@register.simple_tag(takes_context=True)
def load_rest_scripts(context):
    """
    loads only easy rest scripts
    :return: html with the scripts
    """
    data = _get_rest_scripts(context)
    if load_message:
        data = load_message + '\n' + data
    return mark_safe(data)


@register.simple_tag(takes_context=True)
def load_rest_all(context):
    """
    load rest scripts along with bootstrap
    :return: html including bootstrap and rest scripts
    """
    data = _get_rest_scripts(context) + _get_bootstrap()
    if load_message:
        data = load_message + '\n' + data
    return mark_safe(data)


def _load_debug_scripts():
    data = [
     js_base.format('jquery-3.2.1.min.js')]
    for script in [
     'bootstrap.js',
     'highlight.js',
     'json.js']:
        data.append(js_base.format('/highlight/{}'.format(script)))

    for script in ['default.css',
     'bootstrap.css']:
        data.append(css_base.format('/highlight/{}'.format(script)))

    return mark_safe('\n'.join(data))


@register.simple_tag(takes_context=True)
def load_debug_scripts(context):
    return _load_debug_scripts() + load_rest_all(context)


def _get_rest_scripts(context=None):
    """
    :return: html scripts
    """
    files = []
    if settings.DEBUG:
        files.append('debugger.js')
    files += [
     'jquery-3.2.1.min.js',
     'restConsts.js',
     'Request.js',
     'PostHandler.js',
     'Submit.js',
     'fetch/restFetch.js']
    if context and context.get('js_context'):
        files.append('context.js')
    return '<!--start of easy rest scripts-->\n{}\n<!--end of easy rest scripts-->'.format('\n'.join([js_base.format(file) for file in files]))


def _get_bootstrap():
    """
    :return: html scripts
    """
    files = [
     'bootstrap.css',
     'bootstrap-grid.css',
     'bootstrap-reboot.css']
    data = '\n'.join([css_base.format('bootstrap-4.0.0-alpha.6-dist/css/{}'.format(file)) for file in files])
    data += '\n' + css_base.format('bootstrap-4.0.0-alpha.6-dist/js/{}'.format('bootstrap.js'))
    return '<!--start bootstrap-->\n{}\n<!--end of bootstrap-->'.format(data)


@register.tag('livecontext')
def live_context(parser, token):
    bits = token.split_contents()[1:]
    url = None
    if bits:
        url = bits[0]
    nodelist = parser.parse(('endlivecontext', ))
    parser.delete_first_token()
    return LiveContext(nodelist, url)


class LiveContext(template.Node):

    def __init__(self, nodelist, url):
        self.nodelist = nodelist
        self.url = url

    def render(self, context):
        output = self.nodelist.render(context)
        if self.url:
            return '<div class="fetch-context" data-fetch-url="{}">\n{}\n</div>'.format(self.url, output)
        else:
            return '<div class="fetch-context">\n{}\n</div>'.format(output)