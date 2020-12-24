# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/templatetags/djangocms_misc_tags.py
# Compiled at: 2020-01-30 09:18:11
from __future__ import unicode_literals
from cms.models import Page, Placeholder
from django.conf import settings
from django import template
from djangocms_misc.utils.edit_mode import is_edit_mode
register = template.Library()

@register.filter()
def djangocms_misc_placeholder_empty(page_placeholder, slot=None):
    """
    for page/slot, pass a page object, and a slot name:
    {% if request.current_page|djangocms_misc_placeholder_empty:"content" %}

    for a outside page placeholder, just the placeholder object:
    {% if object.placeholderfield|djangocms_misc_placeholder_empty %}

    also, with:
    {% with ph_empty=object.placeholderfield|djangocms_misc_placeholder_empty %}
    """
    placeholder = None
    if isinstance(page_placeholder, Placeholder):
        placeholder = page_placeholder
    elif isinstance(page_placeholder, Page):
        page = page_placeholder
        try:
            placeholder = page.placeholders.get(slot=slot)
        except Placeholder.DoesNotExist:
            pass

    if placeholder:
        return not placeholder.cmsplugin_set.exists()
    else:
        return False


@register.inclusion_tag(b'djangocms_misc/tags/page_link.html', takes_context=True)
def djangocms_misc_page_link(context, lookup, css_class=b'', link_text=b'', link_text_attr=b''):
    """
    link_text_attr is not working (yet)
    """
    if not link_text_attr:
        link_text_attr = b'title'
    context.update({b'lookup': lookup, 
       b'css_class': css_class, 
       b'link_text': link_text, 
       b'link_text_attr': link_text_attr})
    return context


@register.simple_tag(takes_context=True)
def djangocms_misc_get_from_page_content(context, config_name, page_lookup=None):
    config = settings.DJANGOCMS_MISC_GET_FROM_PAGE_CONTENT.get(config_name, None)
    request = context[b'request']
    page = None
    if isinstance(page_lookup, Page):
        page = page_lookup
    else:
        try:
            page_id = int(page_lookup)
            page = Page.objects.get(pk=page_id)
        except (TypeError, ValueError, Page.DoesNotExist):
            pass

        try:
            page_reverse_id = str(page_lookup)
            qs = Page.objects.all()
            if is_edit_mode(request.toolbar):
                qs = qs.drafts()
            else:
                qs = qs.public()
            page = qs.get(reverse_id=page_reverse_id)
        except (ValueError, Page.DoesNotExist):
            pass

    if not page:
        page = getattr(request, b'current_page', None)
    if page and config:
        content = get_from_page_content(request, config, page)
        return content
    else:
        return b''


def get_from_page_content(request, config, page):
    placeholders = page.get_placeholders()
    to_scan_placeholders = config.get(b'placeholders')
    to_scan_plugins = config.get(b'plugins')
    for slot_name in to_scan_placeholders:
        placeholder = placeholders.filter(slot=slot_name)
        if placeholder.count():
            language = request.LANGUAGE_CODE
            if b'djangocms_misc.global_untranslated_placeholder' in settings.INSTALLED_APPS and settings.DJANGOCMS_MISC_UNTRANSLATED_PLACEHOLDERS:
                from djangocms_misc.global_untranslated_placeholder.utils import get_untranslated_default_language
                language = get_untranslated_default_language()
            plugins = placeholder[0].get_plugins(language).order_by(b'position')
            for plugin in plugins:
                if plugin.plugin_type in to_scan_plugins:
                    instance, plugin_cls = plugin.get_plugin_instance()
                    to_scan_fields = to_scan_plugins[plugin.plugin_type]
                    if len(to_scan_fields):
                        for field in to_scan_fields:
                            if instance and getattr(instance, field, None):
                                content = getattr(instance, field)
                                return content

                    else:
                        return instance

    return b''