# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/VALDYS/MANAGER/app/templatetags/app.py
# Compiled at: 2017-12-20 04:43:12
# Size of source mod 2**32: 8090 bytes
import json, re, os
from urllib.parse import urlparse, urlencode, parse_qs, urlsplit, urlunsplit
from django.conf import settings
from django import template, forms
from django.templatetags.static import static
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.templatetags.static import StaticNode, static as original_static, do_static as original_do_static
from django.core.files.storage import get_storage_class, FileSystemStorage
from django import forms
import app.utils
register = template.Library()

@register.filter()
def currency(value):
    return app.utils.currency(value if value else 0)


@register.filter()
def pluralize(value):
    if value:
        return 's'
    else:
        return ''


@register.filter()
def typeof(obj):
    return type(obj)


@register.filter
def jsonify(obj):
    if obj is None:
        return '{}'
    else:
        if isinstance(obj, dict):
            return json.dumps(obj)
        if isinstance(obj, list):
            return json.dumps(obj)
        if type(obj) == type({}.keys()):
            return json.dumps(list(obj))
    obj = re.sub('([\\w\\d_]+)\\:', '"\\1":', obj)
    obj = re.sub("\\'", '"', obj)
    obj = re.sub('\\/\\/\\s*[\\w\\s\\d]+', '', obj)
    obj = re.sub('Date\\.UTC\\(.+\\)', '""', obj)
    try:
        return json.dumps(json.loads(obj))
    except:
        return json.loads(json.dumps(obj))


@register.simple_tag
def field(field, **kwargs):
    return render_field(field, **kwargs)


@register.simple_tag
def form(form, **kwargs):
    return render_form(form, **kwargs)


def add_input_classes(field, **kwargs):
    widget_classes = f"field field_{field.name} {kwargs.pop('classes', '')}"
    if not is_checkbox(field):
        if not is_multiple_checkbox(field):
            if not is_radio(field):
                if not is_file(field):
                    classes = ''
                    if is_textarea(field):
                        classes = 'materialize-textarea'
                    field_classes = field.field.widget.attrs.get('class', classes)
                    if field.errors:
                        field_classes += ' invalid'
                    field.field.widget.attrs['class'] = field_classes
                    if hasattr(field.field, 'max_length'):
                        field.field.widget.attrs['data-length'] = field.field.max_length
    if hasattr(field.field.widget, 'clear_checkbox_label'):
        field.checkbox_name = field.field.widget.clear_checkbox_name(field.name)
        field.checkbox_id = field.field.widget.clear_checkbox_id(field.checkbox_name)
    if is_select(field):
        field.field.widget.attrs['data-select'] = '-'
    field.label = kwargs.get('label', field.label)
    placeholder = kwargs.pop('placeholder', None)
    if placeholder:
        if not field.label:
            field.field.widget.attrs['placeholder'] = placeholder
    for name, value in kwargs.items():
        field.field.widget.attrs[name] = value

    field.real_value = field.value()
    field.classes = widget_classes
    field.error_classes = 'field-error'
    field.help_classes = 'field-help'
    field.label_classes = 'active' if field.real_value else ''
    template_name = f"forms/fields/_{field.field.widget.__class__.__name__.lower()}.html"
    try:
        field.template = get_template(template_name)
        print(f" {template_name} form widget template")
    except:
        print(f"Unknow {template_name} form widget template")
        field.template = get_template('forms/fields/_unknow.html')


def render_field(field, **kwargs):
    element_type = field.__class__.__name__.lower()
    if element_type == 'boundfield':
        add_input_classes(field, **kwargs)
        kwargs['field'] = field
        return field.template.render(kwargs)


def render_form(form, **kwargs):
    html = ''
    for field in form:
        html += render_field(field)

    return html


def form_as_app(self):
    return render_form(self)


forms.Form.as_app = form_as_app

@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_date_input(field):
    return isinstance(field.field.widget, forms.DateInput)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput) or isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkbox_select_multiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.inclusion_tag('javascripts.html')
def javascripts(*names, **kwargs):
    global_async = kwargs.get('async', False)
    internals = ''
    paths = []
    for name in names:
        if 'valdys' in name:
            paths += [
             'js/vendors/jquery.js',
             'js/vendors/jquery-migrate.js',
             'js/vendors/jquery-ui.js',
             'js/vendors/moment.min.js']
            for path in os.listdir(os.path.join(settings.BASE_DIR, 'assets/js')):
                if path.endswith('.js'):
                    paths.append(f"js/{path}")

        else:
            paths.append(name)

    for path in paths:
        internals += f'<script type="text/javascript" src="{static(path)}"></script>'

    return {'internals': mark_safe(internals)}


PACKAGES_CSS = {'materialize-icons': [
                       'https://fonts.googleapis.com/icon?family=Material+Icons']}

@register.inclusion_tag('stylesheets.html')
def stylesheets(*names):
    internals = ''
    externals = ''
    if not names:
        names = PACKAGES_CSS.keys()
    packages = []
    for name in names:
        paths = PACKAGES_CSS.get(name)
        if paths:
            if isinstance(paths, list):
                packages += paths
            else:
                packages.append(paths)
        else:
            packages.append(name)

    for path in packages:
        if path.startswith('http') or path.startswith('//'):
            externals += f'<link type="text/css" rel="stylesheet"  href="{path}" media="screen,projection" />'
        else:
            internals += f'<link type="text/css" rel="stylesheet"  href="{static(path)}" media="screen,projection" />'

    return {'externals':mark_safe(externals), 
     'internals':mark_safe(internals)}


@register.inclusion_tag('messages.html')
def messages(messages):
    return {'messages': messages}


@register.filter
def absolute_url(url):
    return app.utils.canonical_url(url)


@register.filter
def static(url):
    return original_static(url)


@register.filter
def external_url(url):
    return app.utils.append_protocol(url)


@register.filter
def absolute_static(url):
    return absolute_url(original_static(url))


class AbsoluteStaticNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        return absolute_url(self.handle_simple(path))


@register.tag('absolute_static')
def absolute_static_tag(parser, token):
    return AbsoluteStaticNode.handle_token(parser, token)


@register.filter
def static_image(url):
    storage_class = get_storage_class(settings.STATICFILES_STORAGE)
    storage = storage_class()
    image = ImageFile(storage.open(url))
    image.storage = storage
    return (image, image.url)


@register.filter
def replace_urls_to_href(text):
    return mark_safe(app.utils.replace_urls_to_href(text))


@register.simple_tag()
def url_replace_param(url, param_name, param_value):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    query_params[param_name] = [
     param_value]
    new_query_string = urlencode(query_params, doseq=True)
    return mark_safe(urlunsplit((scheme, netloc, path, new_query_string, fragment)))