# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/widgets/forms.py
# Compiled at: 2006-11-21 20:30:39
import turbogears.widgets as w

class SubmitPreviewForm(w.Form):
    __module__ = __name__
    name = 'submit_preview_form'
    member_widgets = ['preview', 'reset']
    params = ['preview_text', 'reset_text']
    params_doc = {'preview_text': 'Text for the preview button', 'reset_text': 'Text for the reset button'}
    preview = w.SubmitButton(name='preview')
    reset = w.ResetButton()


class SubmitPreviewTableForm(SubmitPreviewForm):
    __module__ = __name__
    template = '\n    <form xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="tableform"\n        py:attrs="form_attrs"\n    >\n        <div py:for="field in hidden_fields"\n            py:replace="field.display(value_for(field), **params_for(field))"\n        />\n        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">\n            <tr py:for="i, field in enumerate(fields)"\n                class="${i%2 and \'odd\' or \'even\'}"\n            >\n                <th>\n                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />\n                </th>\n                <td>\n                    <span py:replace="field.display(value_for(field), **params_for(field))" />\n                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />\n                </td>\n            </tr>\n            <tr>\n                <td>&#160;</td>\n                <td>${submit.display(submit_text)} ${preview.display(preview_text)} ${reset.display(reset_text)}</td>\n            </tr>\n        </table>\n    </form>\n    '
    params = [
     'table_attrs']
    params_doc = {'table_attrs': 'Extra (X)HTML attributes for the Table tag'}
    table_attrs = {}