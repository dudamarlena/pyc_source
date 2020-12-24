# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/downloader/forms.py
# Compiled at: 2010-04-22 10:40:35
from django import forms
from django.forms.forms import BoundField
from django.forms.widgets import Textarea
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.utils.datastructures import SortedDict
from models import Download

class SmartForm(object):
    """
    add new method that return
    """

    def _html_output_dict(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        top_errors = self.non_field_errors()
        output, hidden_fields = SortedDict(), SortedDict()
        for (name, field) in self.fields.items():
            html = []
            bf = BoundField(self, field, name)
            bf_errors = self.error_class([ conditional_escape(error) for error in bf.errors ])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([ '(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors ])
                hidden_fields[name] = unicode(bf)
            else:
                if errors_on_separate_row and bf_errors:
                    html.append(error_row % force_unicode(bf_errors))
                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    if self.label_suffix:
                        if label[(-1)] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''
                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = ''
                html.append(normal_row % {'errors': force_unicode(bf_errors), 'label': force_unicode(label), 'field': unicode(bf), 'help_text': help_text})
                output[name] = ('\n').join(html)

        if top_errors:
            output.insert(0, 'top_error', error_row % force_unicode(top_errors))
        if hidden_fields:
            str_hidden = ('').join(hidden_fields)
            if output:
                last_row = output[(-1)]
                if not last_row.endswith(row_ender):
                    last_row = normal_row % {'errors': '', 'label': '', 'field': '', 'help_text': ''}
                    output['last_row'] = last_row
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                output['hidden'] = str_hidden
        return output

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."""
        output = self._html_output_dict(normal_row, error_row, row_ender, help_text_html, errors_on_separate_row)
        output = output.values()
        return mark_safe(('\n').join(output))

    def _safe_dict(self, html_dict):
        safe = {}
        for (key, value) in html_dict.items():
            safe[key] = mark_safe(value)

        return safe

    def as_table_dict(self):
        """Returns this form rendered as HTML <tr>s -- excluding the <table></table>."""
        html_dict = self._html_output_dict('<tr><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>', '<tr><td colspan="2">%s</td></tr>', '</td></tr>', '<br />%s', False)
        return self._safe_dict(html_dict)

    def as_ul_dict(self):
        """Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."""
        html_dict = self._html_output_dict('<li>%(errors)s%(label)s %(field)s%(help_text)s</li>', '<li>%s</li>', '</li>', ' %s', False)
        return self._safe_dict(html_dict)

    def as_p_dict(self):
        """Returns this form rendered as HTML <p>s."""
        html_dict = self._html_output_dict('<p>%(label)s %(field)s%(help_text)s</p>', '%s', '</p>', ' %s', True)
        return self._safe_dict(html_dict)


class DownloadForm(SmartForm, forms.ModelForm):
    """
    Form for a Download
    """
    my_mail = forms.EmailField(label=_('Notify me'), required=False)
    notify1 = forms.EmailField(label=_('E-mail 1'), required=False)
    notify2 = forms.EmailField(label=_('E-mail 2'), required=False)
    notify3 = forms.EmailField(label=_('E-mail 3'), required=False)
    comment = forms.CharField(widget=Textarea, label=_('Add a comment'), required=False)

    class Meta:
        model = Download
        exclude = ['last_download', 'creation', 'slug']