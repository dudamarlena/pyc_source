# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scriptaculous/widgets.py
# Compiled at: 2008-05-13 09:22:56
import pkg_resources
from turbogears import expose
from turbogears.widgets import JSLink, CSSLink, Widget, WidgetDescription, TextField, register_static_directory
from turbogears.widgets.base import CoreWD
js_dir = pkg_resources.resource_filename('scriptaculous', 'static')
register_static_directory('scriptaculous', js_dir)
prototype = JSLink('scriptaculous', 'javascript/prototype.js')
prototype_js = JSLink('scriptaculous', 'javascript/prototype.js')
scriptaculous_js = JSLink('scriptaculous', 'javascript/scriptaculous.js')
builder_js = JSLink('scriptaculous', 'javascript/builder.js')
controls_js = JSLink('scriptaculous', 'javascript/controls.js')
dragdrop_js = JSLink('scriptaculous', 'javascript/dragdrop.js')
effects_js = JSLink('scriptaculous', 'javascript/effects.js')
slider_js = JSLink('scriptaculous', 'javascript/slider.js')
sound_js = JSLink('scriptaculous', 'javascript/sound.js')
unittest_js = JSLink('scriptaculous', 'javascript/unittest.js')
autocompletefield_css = CSSLink('scriptaculous', 'css/autocomplete.css')

class Scriptaculous(Widget):
    """Provides an easy way to use Scriptaculous in your own packages.
    from scriptaculous import scriptaculous, and then just return
    that scriptaculous widget in the output dictionary from your
    controller."""
    javascript = [
     prototype_js, scriptaculous_js]


scriptaculous = Scriptaculous()

class ScriptaculousDesc(WidgetDescription):
    for_widget = scriptaculous
    template = '<div onclick="new Effect.BlindUp(this)">\n      Click here to watch this disappear!\n    </div>\n    '
    show_separately = True


class AutoCompleteField(TextField):
    """A standard, single-line text field with Scriptaculous AutoComplete enhancements."""
    template = 'scriptaculous.templates.autocomplete'
    css = [autocompletefield_css]
    params = ['attrs', 'id', 'search_controller', 'search_param', 'min_chars']
    params_doc = {'attrs': 'Dictionary containing extra (X)HTML attributes for the input tag', 'id': 'ID for the entire AutoComplete construct.'}
    attrs = {}
    id = 'noid'
    search_param = 'input'
    min_chars = 2
    javascript = [prototype_js, scriptaculous_js]


class AutoCompleteFieldDesc(CoreWD):
    name = 'Scriptaculous Auto Complete'
    show_separately = True
    template = '\n    <div>\n        Please choose a country:<br/>\n        ${for_widget.display()}\n    </div>\n    '
    full_class_name = 'scriptaculous.widgets.AutoCompleteField'

    def __init__(self, *args, **kw):
        super(AutoCompleteFieldDesc, self).__init__(*args, **kw)
        self.for_widget = AutoCompleteField(name='country', id='country', search_controller='%s/search_for_country' % self.full_class_name, search_param='input')

    def ret_as_ul(self, lst):
        if len(lst) == 0:
            return '<ul></ul>'
        else:
            tmp = ('</li><li>').join(lst)
            return '<ul><li>' + tmp + '</li></ul>'

    @expose()
    def search_for_country(self, input):
        from turbogears.i18n import format as tgformat
        input = input.lower()
        found = [ country for (code, country) in tgformat.get_countries() if input in country.lower()
                ]
        return self.ret_as_ul(found)