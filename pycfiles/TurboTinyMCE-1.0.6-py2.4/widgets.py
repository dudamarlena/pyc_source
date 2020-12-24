# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/tinymce/widgets.py
# Compiled at: 2006-10-07 09:18:42
__all__ = [
 'TinyMCE']
import logging, pkg_resources
from turbojson.jsonify import encode
from turbogears.widgets import JSSource, JSLink, TextArea, WidgetDescription, register_static_directory
from turbogears.i18n.utils import get_locale
from tinymce import utils
log = logging.getLogger('tinymce')
js_dir = pkg_resources.resource_filename('tinymce', 'static/javascript')
register_static_directory('tinymce', js_dir)

class TinyMCE(TextArea):
    """WYSIWYG editor for textareas. You can pass options directly to TinyMCE
    at consruction or display time via the 'mce_options' dict parameter.
    """
    __module__ = __name__
    template = '\n    <span xmlns:py="http://purl.org/kid/ns#">\n        <textarea\n            name="${name}"\n            class="${field_class}"\n            id="${field_id}"\n            rows="${rows}"\n            cols="${cols}"\n            py:attrs="attrs"\n            py:content="value"\n        />\n        <script type="text/javascript">${TinyMCEInit}</script>\n    </span>\n    '
    langs = utils.get_available_languages()
    params = ['mce_options', 'new_options']
    params_doc = {'mce_options': _("Options to initialize TinyMCE's javascript. This dict will override the defaults"), 'new_options': _("Options to initialize TinyMCE's javascript. This dict will update the defaults")}
    rows = 25
    mce_options = dict(mode='exact', theme='advanced', plugins='advimage', theme_advanced_toolbar_location='top', theme_advanced_toolbar_align='center', theme_advanced_statusbar_location='bottom', extended_valid_elements='a[href|target|name]', theme_advanced_resizing=True, paste_use_dialog=False, paste_auto_cleanup_on_paste=True, paste_convert_headers_to_strong=False, paste_strip_class_attributes='all')
    new_options = {}
    validator = utils.HTMLCleaner()
    javascript = [JSLink('tinymce', 'tiny_mce_src.js')]

    def _get_locale(self):
        locale = get_locale().lower()
        if locale in self.langs:
            log.debug('Locale %s is available' % locale)
            return locale
        else:
            log.debug('Locale %s is not available' % locale)
            locale = locale.split('_')[0]
            if locale in self.langs:
                log.debug('Locale %s is available' % locale)
                return locale
        log.debug('Locale %s is not available, resorting to default locale' % locale)
        return

    _get_locale = utils.cache_for_request('_get_locale')(_get_locale)

    def update_params(self, d):
        super(TinyMCE, self).update_params(d)
        d['mce_options'].update(d['new_options'])
        locale = self._get_locale()
        if locale:
            d['mce_options'].setdefault('language', locale)
        if d['mce_options'].get('mode', 'textareas') == 'exact':
            d['mce_options']['elements'] = d['field_id']
        d['TinyMCEInit'] = 'tinyMCE.init(%s);' % encode(d['mce_options'])


class TinyMCEDesc(WidgetDescription):
    __module__ = __name__
    name = 'TinyMCE'
    for_widget = TinyMCE('mce_sample')
    value = '<h1>This is some sample text.</h1>Edit me as you please.'