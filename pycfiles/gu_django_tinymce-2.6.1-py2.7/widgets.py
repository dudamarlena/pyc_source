# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/additional/projects/tinymce/gu-django-tinymce/tinymce/widgets.py
# Compiled at: 2016-06-08 06:42:02
"""
This TinyMCE widget was copied and extended from this code by John D'Agostino:
http://code.djangoproject.com/wiki/CustomWidgetsTinyMCE
"""
from __future__ import unicode_literals
import filebrowser, tinymce.settings
from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.core.urlresolvers import reverse
from django.forms.widgets import flatatt
from django.utils.html import escape
try:
    from collections import OrderedDict as SortedDict
except ImportError:
    from django.utils.datastructures import SortedDict

from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext as _
import json
try:
    from django.utils.encoding import smart_text as smart_unicode
except ImportError:
    try:
        from django.utils.encoding import smart_unicode
    except ImportError:
        from django.forms.util import smart_unicode

class TinyMCE(forms.Textarea):
    """
    TinyMCE widget. Set settings.TINYMCE_JS_URL to set the location of the
    javascript file. Default is "MEDIA_URL + 'js/tiny_mce/tiny_mce.js'".
    You can customize the configuration with the mce_attrs argument to the
    constructor.

    In addition to the standard configuration you can set the
    'content_language' parameter. It takes the value of the 'language'
    parameter by default.

    In addition to the default settings from settings.TINYMCE_DEFAULT_CONFIG,
    this widget sets the 'language', 'directionality' and
    'spellchecker_languages' parameters by default. The first is derived from
    the current Django language, the others from the 'content_language'
    parameter.
    """

    def __init__(self, content_language=None, attrs=None, mce_attrs=None):
        super(TinyMCE, self).__init__(attrs)
        mce_attrs = mce_attrs or {}
        self.mce_attrs = mce_attrs
        if b'mode' not in self.mce_attrs:
            self.mce_attrs[b'mode'] = b'exact'
        self.mce_attrs[b'strict_loading_mode'] = 1
        if content_language is None:
            content_language = mce_attrs.get(b'language', None)
        self.content_language = content_language
        return

    def get_mce_config(self, attrs):
        mce_config = tinymce.settings.DEFAULT_CONFIG.copy()
        mce_config.update(get_language_config(self.content_language))
        if tinymce.settings.USE_FILEBROWSER:
            mce_config[b'file_browser_callback'] = b'djangoFileBrowser'
        mce_config.update(self.mce_attrs)
        if mce_config[b'mode'] == b'exact':
            mce_config[b'elements'] = attrs[b'id']
        return mce_config

    def get_mce_json(self, mce_config):
        js_functions = {}
        for k in ('paste_preprocess', 'paste_postprocess'):
            if k in mce_config:
                js_functions[k] = mce_config[k]
                del mce_config[k]

        mce_json = json.dumps(mce_config)
        for k in js_functions:
            index = mce_json.rfind(b'}')
            mce_json = mce_json[:index] + b', ' + k + b':' + js_functions[k].strip() + mce_json[index:]

        return mce_json

    def render(self, name, value, attrs=None):
        if value is None:
            value = b''
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs)
        final_attrs[b'name'] = name
        final_attrs[b'class'] = b'tinymce'
        assert b'id' in final_attrs, b"TinyMCE widget attributes must contain 'id'"
        mce_config = self.get_mce_config(final_attrs)
        mce_json = self.get_mce_json(mce_config)
        if tinymce.settings.USE_COMPRESSOR:
            compressor_config = {b'plugins': mce_config.get(b'plugins', b''), b'themes': mce_config.get(b'theme', b'advanced'), 
               b'languages': mce_config.get(b'language', b''), 
               b'diskcache': True, 
               b'debug': False}
            final_attrs[b'data-mce-gz-conf'] = json.dumps(compressor_config)
        final_attrs[b'data-mce-conf'] = mce_json
        html = [(b'<textarea{!s}>{!s}</textarea>').format(flatatt(final_attrs), escape(value))]
        return mark_safe((b'\n').join(html))

    def _media(self):
        if tinymce.settings.USE_COMPRESSOR:
            js = [
             reverse(b'tinymce-compressor')]
        else:
            js = [
             tinymce.settings.JS_URL]
        if tinymce.settings.USE_FILEBROWSER:
            js.append(reverse(b'tinymce-filebrowser'))
            filebrowser_dir_url = reverse(b'tinymce-filebrowser-path')
            if filebrowser.get_default_dir():
                filebrowser_dir_url += (b'?url={}').format(filebrowser.get_default_dir())
            js.append(filebrowser_dir_url)
        js.append(b'django_tinymce/init_tinymce.js')
        return forms.Media(js=js)

    media = property(_media)


class AdminTinyMCE(TinyMCE, admin_widgets.AdminTextareaWidget):
    pass


def get_language_config(content_language=None):
    language = get_language()[:2]
    if content_language:
        content_language = content_language[:2]
    else:
        content_language = language
    config = {}
    config[b'language'] = language
    lang_names = SortedDict()
    for lang, name in settings.LANGUAGES:
        if lang[:2] not in lang_names:
            lang_names[lang[:2]] = []
        lang_names[lang[:2]].append(_(name))

    sp_langs = []
    for lang, names in lang_names.items():
        if lang == content_language:
            default = b'+'
        else:
            default = b''
        sp_langs.append((b'{!s}{!s}={!s}').format(default, (b' / ').join(names), lang))

    config[b'spellchecker_languages'] = (b',').join(sp_langs)
    if content_language in settings.LANGUAGES_BIDI:
        config[b'directionality'] = b'rtl'
    else:
        config[b'directionality'] = b'ltr'
    if tinymce.settings.USE_SPELLCHECKER:
        config[b'spellchecker_rpc_url'] = reverse(b'tinymce.views.spell_check')
    return config