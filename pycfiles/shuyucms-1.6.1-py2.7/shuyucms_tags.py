# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/core/templatetags/shuyucms_tags.py
# Compiled at: 2016-05-25 04:38:14
from __future__ import absolute_import, division, unicode_literals
import os
from hashlib import md5
from future.builtins import int, open, str
try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote

from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse, resolve, NoReverseMatch
from django.db.models import Model, get_model
from django.template import Context, Node, TextNode, Template, TemplateSyntaxError, TOKEN_TEXT, TOKEN_VAR, TOKEN_COMMENT, TOKEN_BLOCK
from django.template.defaultfilters import escape
from django.template.loader import get_template
from django.utils import translation
from django.utils.html import strip_tags
from django.utils.text import capfirst
from shuyucms.conf import settings
from shuyucms.core.fields import RichTextField
from shuyucms.core.forms import get_edit_form
from shuyucms.utils.cache import nevercache_token, cache_installed
from shuyucms.utils.html import decode_entities
from shuyucms.utils.importing import import_dotted_path
from shuyucms.utils.urls import admin_url
from shuyucms.utils.views import is_editable
from shuyucms import template
from wlapps.utils.common import get_theme
register = template.Library()

@register.to_end_tag
def compress(parsed, context, token):
    """
    Dummy tag for fallback when django-compressor isn't installed.
    """
    return parsed


if cache_installed():

    @register.tag
    def nevercache(parser, token):
        """
        Tag for two phased rendering. Converts enclosed template
        code and content into text, which gets rendered separately
        in ``shuyucms.core.middleware.UpdateCacheMiddleware``.
        This is to bypass caching for the enclosed code and content.
        """
        text = []
        end_tag = b'endnevercache'
        tag_mapping = {TOKEN_TEXT: ('', ''), 
           TOKEN_VAR: ('{{', '}}'), 
           TOKEN_BLOCK: ('{%', '%}'), 
           TOKEN_COMMENT: ('{#', '#}')}
        delimiter = nevercache_token()
        while parser.tokens:
            token = parser.next_token()
            if token.token_type == TOKEN_BLOCK and token.contents == end_tag:
                return TextNode(delimiter + (b'').join(text) + delimiter)
            start, end = tag_mapping[token.token_type]
            text.append(b'%s%s%s' % (start, token.contents, end))

        parser.unclosed_block_tag(end_tag)


else:

    @register.to_end_tag
    def nevercache(parsed, context, token):
        """
        Dummy fallback ``nevercache`` for when caching is not
        configured.
        """
        return parsed


@register.inclusion_tag(get_theme() + b'/includes/form_fields.html', takes_context=True)
def fields_for(context, form):
    """
    Renders fields for a form.
    """
    context[b'form_for_fields'] = form
    return context


@register.inclusion_tag(get_theme() + b'/includes/form_errors.html', takes_context=True)
def errors_for(context, form):
    """
    Renders an alert if the form has any errors.
    """
    context[b'form'] = form
    return context


@register.filter
def sort_by(items, attr):
    """
    General sort filter - sorts by either attribute or key.
    """

    def key_func(item):
        try:
            return getattr(item, attr)
        except AttributeError:
            try:
                return item[attr]
            except TypeError:
                getattr(item, attr)

    return sorted(items, key=key_func)


@register.filter
def is_installed(app_name):
    """
    Returns ``True`` if the given app name is in the
    ``INSTALLED_APPS`` setting.
    """
    from warnings import warn
    warn(b'The is_installed filter is deprecated. Please use the tag {% ifinstalled appname %}{% endifinstalled %}')
    return app_name in settings.INSTALLED_APPS


@register.tag
def ifinstalled(parser, token):
    """
    Old-style ``if`` tag that renders contents if the given app is
    installed. The main use case is:

    {% ifinstalled app_name %}
    {% include "app_name/template.html" %}
    {% endifinstalled %}

    so we need to manually pull out all tokens if the app isn't
    installed, since if we used a normal ``if`` tag with a False arg,
    the include tag will still try and find the template to include.
    """
    try:
        tag, app = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(b'ifinstalled should be in the form: {% ifinstalled app_name %}{% endifinstalled %}')

    end_tag = b'end' + tag
    if app.strip(b'"\'') not in settings.INSTALLED_APPS:
        while True:
            token = parser.tokens.pop(0)
            if token.token_type == TOKEN_BLOCK and token.contents == end_tag:
                parser.tokens.insert(0, token)
                break

    nodelist = parser.parse((end_tag,))
    parser.delete_first_token()

    class IfInstalledNode(Node):

        def render(self, context):
            return nodelist.render(context)

    return IfInstalledNode()


@register.simple_tag
def gravatar_url(email, size=32):
    """
    Return the full URL for a Gravatar given an email hash.
    """
    bits = (
     md5(email.lower().encode(b'utf-8')).hexdigest(), size)
    return b'//www.gravatar.com/avatar/%s?s=%s&d=identicon&r=PG' % bits


@register.to_end_tag
def metablock(parsed):
    """
    Remove HTML tags, entities and superfluous characters from
    meta blocks.
    """
    parsed = (b' ').join(parsed.replace(b'\n', b'').split()).replace(b' ,', b',')
    return escape(strip_tags(decode_entities(parsed)))


@register.inclusion_tag(get_theme() + b'/includes/pagination.html', takes_context=True)
def pagination_for(context, current_page, page_var=b'page', exclude_vars=b''):
    """
    Include the pagination template and data for persisting querystring
    in pagination links. Can also contain a comma separated string of
    var names in the current querystring to exclude from the pagination
    links, via the ``exclude_vars`` arg.
    """
    querystring = context[b'request'].GET.copy()
    exclude_vars = [ v for v in exclude_vars.split(b',') if v ] + [page_var]
    for exclude_var in exclude_vars:
        if exclude_var in querystring:
            del querystring[exclude_var]

    querystring = querystring.urlencode()
    return {b'current_page': current_page, 
       b'querystring': querystring, 
       b'page_var': page_var}


@register.inclusion_tag(get_theme() + b'/includes/search_form.html', takes_context=True)
def search_form(context, search_model_names=None):
    """
    Includes the search form with a list of models to use as choices
    for filtering the search by. Models should be a string with models
    in the format ``app_label.model_name`` separated by spaces. The
    string ``all`` can also be used, in which case the models defined
    by the ``SEARCH_MODEL_CHOICES`` setting will be used.
    """
    if not search_model_names or not settings.SEARCH_MODEL_CHOICES:
        search_model_names = []
    else:
        if search_model_names == b'all':
            search_model_names = list(settings.SEARCH_MODEL_CHOICES)
        else:
            search_model_names = search_model_names.split(b' ')
        search_model_choices = []
        for model_name in search_model_names:
            try:
                model = get_model(*model_name.split(b'.', 1))
            except LookupError:
                pass
            else:
                verbose_name = model._meta.verbose_name_plural.capitalize()
                search_model_choices.append((verbose_name, model_name))

    context[b'search_model_choices'] = sorted(search_model_choices)
    return context


@register.simple_tag
def thumbnail(image_url, width, height, quality=95, left=0.5, top=0.5, padding=False, padding_color=b'#fff'):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image. if width or height are zero then original ratio is
    maintained.
    """
    if not image_url:
        return b''
    try:
        from PIL import Image, ImageFile, ImageOps
    except ImportError:
        return b''

    image_url = unquote(str(image_url)).split(b'?')[0]
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, b'', 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {b'.png': b'PNG', b'.gif': b'GIF'}.get(image_ext, b'JPEG')
    thumb_name = b'%s-%sx%s' % (image_prefix, width, height)
    if left != 0.5 or top != 0.5:
        left = min(1, max(0, left))
        top = min(1, max(0, top))
        thumb_name = b'%s-%sx%s' % (thumb_name, left, top)
    thumb_name += b'-padded-%s' % padding_color if padding else b''
    thumb_name = b'%s%s' % (thumb_name, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir, settings.THUMBNAILS_DIR_NAME, image_name)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = b'%s/%s/%s' % (settings.THUMBNAILS_DIR_NAME,
     quote(image_name.encode(b'utf-8')),
     quote(thumb_name.encode(b'utf-8')))
    image_url_path = os.path.dirname(image_url)
    if image_url_path:
        thumb_url = b'%s/%s' % (image_url_path, thumb_url)
    try:
        thumb_exists = os.path.exists(thumb_path)
    except UnicodeEncodeError:
        from shuyucms.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()

    if thumb_exists:
        return thumb_url
    else:
        if not default_storage.exists(image_url):
            return image_url
        f = default_storage.open(image_url)
        try:
            image = Image.open(f)
        except:
            return image_url

        image_info = image.info
        to_width = int(width)
        to_height = int(height)
        from_width = image.size[0]
        from_height = image.size[1]
        if to_width == 0:
            to_width = from_width * to_height // from_height
        else:
            if to_height == 0:
                to_height = from_height * to_width // from_width
            if image.mode not in ('P', 'L', 'RGBA'):
                try:
                    image = image.convert(b'RGBA')
                except:
                    return image_url

            ImageFile.MAXBLOCK = 2 * max(image.size) ** 2
            if padding and to_width and to_height:
                from_ratio = float(from_width) / from_height
                to_ratio = float(to_width) / to_height
                pad_size = None
                if to_ratio < from_ratio:
                    pad_height = int(to_height * (float(from_width) / to_width))
                    pad_size = (from_width, pad_height)
                    pad_top = (pad_height - from_height) // 2
                    pad_left = 0
                elif to_ratio > from_ratio:
                    pad_width = int(to_width * (float(from_height) / to_height))
                    pad_size = (pad_width, from_height)
                    pad_top = 0
                    pad_left = (pad_width - from_width) // 2
                if pad_size is not None:
                    pad_container = Image.new(b'RGBA', pad_size, padding_color)
                    pad_container.paste(image, (pad_left, pad_top))
                    image = pad_container
            to_size = (to_width, to_height)
            to_pos = (left, top)
            try:
                image = ImageOps.fit(image, to_size, Image.ANTIALIAS, 0, to_pos)
                image = image.save(thumb_path, filetype, quality=quality, **image_info)
                if b'://' in settings.MEDIA_URL:
                    with open(thumb_path, b'rb') as (f):
                        default_storage.save(thumb_url, File(f))
            except Exception:
                try:
                    os.remove(thumb_path)
                except Exception:
                    pass

                return image_url

        return thumb_url


@register.inclusion_tag(get_theme() + b'/includes/editable_loader.html', takes_context=True)
def editable_loader(context):
    """
    Set up the required JS/CSS for the in-line editing toolbar and controls.
    """
    user = context[b'request'].user
    if settings.INLINE_EDITING_ENABLED:
        t = get_template(b'includes/editable_toolbar.html')
        context[b'REDIRECT_FIELD_NAME'] = REDIRECT_FIELD_NAME
        try:
            context[b'editable_obj']
        except KeyError:
            context[b'editable_obj'] = context.get(b'page', None)

        context[b'toolbar'] = t.render(Context(context))
        context[b'richtext_media'] = RichTextField().formfield().widget.media
    return context


@register.filter
def richtext_filters(content):
    """
    Takes a value edited via the WYSIWYG editor, and passes it through
    each of the functions specified by the RICHTEXT_FILTERS setting.
    """
    filter_names = settings.RICHTEXT_FILTERS
    if not filter_names:
        try:
            filter_names = [
             settings.RICHTEXT_FILTER]
        except AttributeError:
            pass
        else:
            from warnings import warn
            warn(b'The `RICHTEXT_FILTER` setting is deprecated in favor of the new plural setting `RICHTEXT_FILTERS`.')

    for filter_name in filter_names:
        filter_func = import_dotted_path(filter_name)
        content = filter_func(content)

    return content


@register.filter
def richtext_filter(content):
    """
    Deprecated version of richtext_filters above.
    """
    from warnings import warn
    warn(b'The `richtext_filter` template tag is deprecated in favor of the new plural tag `richtext_filters`.')
    return richtext_filters(content)


@register.to_end_tag
def editable(parsed, context, token):
    """
    Add the required HTML to the parsed content for in-line editing,
    such as the icon and edit form if the object is deemed to be
    editable - either it has an ``editable`` method which returns
    ``True``, or the logged in user has change permissions for the
    model.
    """

    def parse_field(field):
        field = field.split(b'.')
        obj = context.get(field.pop(0), None)
        attr = field.pop()
        while field:
            obj = getattr(obj, field.pop(0))
            if callable(obj):
                obj = obj()

        return (
         obj, attr)

    fields = [ parse_field(f) for f in token.split_contents()[1:] ]
    if fields:
        fields = [ f for f in fields if len(f) == 2 and f[0] is fields[0][0] ]
    if not parsed.strip():
        try:
            parsed = (b'').join([ str(getattr(*field)) for field in fields ])
        except AttributeError:
            pass

    if settings.INLINE_EDITING_ENABLED and fields and b'request' in context:
        obj = fields[0][0]
        if isinstance(obj, Model) and is_editable(obj, context[b'request']):
            field_names = (b',').join([ f[1] for f in fields ])
            context[b'editable_form'] = get_edit_form(obj, field_names)
            context[b'original'] = parsed
            t = get_template(b'includes/editable_form.html')
            return t.render(Context(context))
    return parsed


@register.simple_tag
def try_url(url_name):
    """
    Mimics Django's ``url`` template tag but fails silently. Used for
    url names in admin templates as these won't resolve when admin
    tests are running.
    """
    from warnings import warn
    warn(b"try_url is deprecated, use the url tag with the 'as' arg instead.")
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        return b''

    return url


def admin_app_list(request):
    """
    Adopted from ``django.contrib.admin.sites.AdminSite.index``.
    Returns a list of lists of models grouped and ordered according to
    ``shuyucms.conf.ADMIN_MENU_ORDER``. Called from the
    ``admin_dropdown_menu`` template tag as well as the ``app_list``
    dashboard widget.
    """
    app_dict = {}
    menu_order = {}
    for group_index, group in enumerate(settings.ADMIN_MENU_ORDER):
        group_title, items = group
        group_title = group_title.title()
        for item_index, item in enumerate(items):
            if isinstance(item, (tuple, list)):
                item_title, item = item
            else:
                item_title = None
            menu_order[item] = (
             group_index, group_title,
             item_index, item_title)

    for model, model_admin in admin.site._registry.items():
        opts = model._meta
        in_menu = not hasattr(model_admin, b'in_menu') or model_admin.in_menu()
        if in_menu and request.user.has_module_perms(opts.app_label):
            perms = model_admin.get_model_perms(request)
            admin_url_name = b''
            if perms[b'change']:
                admin_url_name = b'changelist'
                change_url = admin_url(model, admin_url_name)
            else:
                change_url = None
            if perms[b'add']:
                admin_url_name = b'add'
                add_url = admin_url(model, admin_url_name)
            else:
                add_url = None
            if admin_url_name:
                model_label = b'%s.%s' % (opts.app_label, opts.object_name)
                try:
                    app_index, app_title, model_index, model_title = menu_order[model_label]
                except KeyError:
                    app_index = None
                    app_title = opts.app_label.title()
                    model_index = None
                    model_title = None
                else:
                    del menu_order[model_label]

                if not model_title:
                    model_title = capfirst(model._meta.verbose_name_plural)
                if app_title not in app_dict:
                    app_dict[app_title] = {b'index': app_index, b'name': app_title, 
                       b'models': []}
                app_dict[app_title][b'models'].append({b'index': model_index, 
                   b'perms': model_admin.get_model_perms(request), 
                   b'name': model_title, 
                   b'admin_url': change_url, 
                   b'add_url': add_url})

    for item_url, item in menu_order.items():
        app_index, app_title, item_index, item_title = item
        try:
            item_url = reverse(item_url)
        except NoReverseMatch:
            continue

        if app_title not in app_dict:
            app_dict[app_title] = {b'index': app_index, b'name': app_title, 
               b'models': []}
        app_dict[app_title][b'models'].append({b'index': item_index, 
           b'perms': {b'custom': True}, b'name': item_title, 
           b'admin_url': item_url})

    app_list = list(app_dict.values())
    sort = lambda x: (x[b'index'] if x[b'index'] is not None else 999, x[b'name'])
    for app in app_list:
        app[b'models'].sort(key=sort)

    app_list.sort(key=sort)
    return app_list


@register.inclusion_tag(b'admin/includes/dropdown_menu.html', takes_context=True)
def admin_dropdown_menu(context):
    """
    Renders the app list for the admin dropdown menu navigation.
    """
    context[b'dropdown_menu_app_list'] = admin_app_list(context[b'request'])
    user = context[b'request'].user
    context[b'dropdown_menu_selected_site_id'] = b'1'
    return context


@register.inclusion_tag(b'admin/includes/app_list.html', takes_context=True)
def app_list(context):
    """
    Renders the app list for the admin dashboard widget.
    """
    context[b'dashboard_app_list'] = admin_app_list(context[b'request'])
    return context


@register.inclusion_tag(b'admin/includes/recent_actions.html', takes_context=True)
def recent_actions(context):
    """
    Renders the recent actions list for the admin dashboard widget.
    """
    return context


@register.render_tag
def dashboard_column(context, token):
    """
    Takes an index for retrieving the sequence of template tags from
    ``shuyucms.conf.DASHBOARD_TAGS`` to render into the admin
    dashboard.
    """
    column_index = int(token.split_contents()[1])
    output = []
    for tag in settings.DASHBOARD_TAGS[column_index]:
        t = Template(b'{%% load %s %%}{%% %s %%}' % tuple(tag.split(b'.')))
        output.append(t.render(Context(context)))

    return (b'').join(output)


@register.simple_tag(takes_context=True)
def translate_url(context, language):
    """
    Translates the current URL for the given language code, eg:

        {% translate_url de %}
    """
    try:
        request = context[b'request']
    except KeyError:
        return b''

    view = resolve(request.path)
    current_language = translation.get_language()
    translation.activate(language)
    try:
        url = reverse(view.func, args=view.args, kwargs=view.kwargs)
    except NoReverseMatch:
        try:
            url_name = (view.namespace or view).url_name if 1 else b'%s:%s' % (view.namespace, view.url_name)
            url = reverse(url_name, args=view.args, kwargs=view.kwargs)
        except NoReverseMatch:
            url_name = b'admin:' + view.url_name
            url = reverse(url_name, args=view.args, kwargs=view.kwargs)

    translation.activate(current_language)
    if context[b'request'].META[b'QUERY_STRING']:
        url += b'?' + context[b'request'].META[b'QUERY_STRING']
    return url