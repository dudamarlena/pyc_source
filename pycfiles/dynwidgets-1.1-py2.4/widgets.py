# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dynwidgets/widgets.py
# Compiled at: 2007-04-12 18:41:31
import pkg_resources
from cherrypy import request
from turbogears.widgets import RepeatingFormField
from turbogears.widgets import CompoundWidget
from turbogears.widgets.base import register_static_directory
from turbogears.widgets.base import JSLink, CSSLink
my_static = 'dyn_static'
directory = pkg_resources.resource_filename(__name__, 'static')
register_static_directory(my_static, directory)

class AppendableFormFieldList(RepeatingFormField):
    __module__ = __name__
    template = '\n    <div class="appendable_form_field_list" xmlns:py="http://purl.org/kid/ns#">\n    <ol id="${field_id}">\n        <li py:for="repetition in repetitions"\n            class="${field_class}"\n            id="${field_id}_${repetition}">\n            <div py:for="field in hidden_fields"\n                py:replace="field.display(value_for(field), **params_for(field))"\n            />\n            <ul>\n                <li py:for="field in fields">\n                    <label class="fieldlabel" for="${field.field_id}"\n                           py:content="field.label" />\n                    <span py:content="field.display(value_for(field),\n                          **params_for(field))" />\n                    <span py:if="error_for(field)" class="fielderror"\n                          py:content="error_for(field)" />\n                    <span py:if="field.help_text" class="fieldhelp"\n                          py:content="field_help_text" />\n                </li>\n                <li>\n                <a\n                href="javascript:AppendableFormFieldList.removeItem(\'${field_id}_${repetition}\')">\n                <img src=\'${tg.url([tg.widgets, "dyn_static/images/bin_empty.png"])}\'\n border="0"\n                     title="Remover item"\n                     alt="Remover item" />\n                </a></li>\n            </ul>\n        </li>\n    </ol>\n    <a id="doclink"\n       href="javascript:AppendableFormFieldList.addItem(\'${field_id}\');">\n       <img src="${tg.tg_static}/images/add.png" alt="Adicionar item"\n            title="Adicionar item" border="0" />\n       Adicionar\n    </a>\n    </div>\n    '
    javascript = [
     JSLink(my_static, 'javascript/appendable_form_field_list.js')]
    css = [CSSLink(my_static, 'css/appendable_form_field_list.css')]

    def display(self, value=None, **params):
        if value and isinstance(value, list) and len(value) > 1:
            params['repetitions'] = len(value)
        return super(AppendableFormFieldList, self).display(value, **params)