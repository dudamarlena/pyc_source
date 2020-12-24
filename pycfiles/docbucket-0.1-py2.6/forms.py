# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/docbucket/forms.py
# Compiled at: 2010-12-14 14:28:05
from django import forms
from helpers import list_document_classes, list_incomings
from itertools import chain
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.datastructures import MultiValueDict, MergeDict
from django.core.urlresolvers import reverse

class PageSelector(forms.Widget):

    def __init__(self, attrs=None, choices=()):
        super(PageSelector, self).__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs)
        output = []
        output.append('<div id="pages"%s>' % forms.widgets.flatatt(final_attrs))
        output.append('<a class="action select" href="#">Select all</a>')
        output.append('<a class="action deselect" href="#">Deselect all</a>')
        output.append('<ul>')
        pages = self.render_pages(name, choices, value)
        if pages:
            output.append(pages)
        output.append('</ul></div>')
        return mark_safe(('\n').join(output))

    def render_pages(self, name, choices, selected_pages):
        selected_pages = tuple([ force_unicode(v) for v in selected_pages ])
        output = []
        choices = self._reorder_choices_from_selected(selected_pages, chain(self.choices, choices))
        for (i, (page_filename, page_name)) in enumerate(choices):
            output.append(self.render_page(i, name, selected_pages, page_filename, page_name))

        return ('\n').join(output)

    def render_page(self, idx, name, selected_pages, page_filename, page_name):
        page_filename = force_unicode(page_filename)
        checked = page_filename in selected_pages and ' checked="checked"' or ''
        opts = (reverse('thumb', args=(page_filename,)), name, idx, name, checked,
         escape(page_filename), name, idx, conditional_escape(force_unicode(page_name)))
        return '<li><img src="%s" /><p><input id="id_%s_%s" name="%s"%s value="%s" type="checkbox" /><label for="id_%s_%s">%s</label></p></li>' % opts

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        else:
            return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        else:
            for (value1, value2) in zip(initial, data):
                if force_unicode(value1) != force_unicode(value2):
                    return True

            return False

    def _reorder_choices_from_selected(self, selected, choices):
        choices = dict(choices)
        ordered_choices = list(selected)
        for c in choices:
            if c not in ordered_choices:
                ordered_choices.append(c)

        real_choices = []
        for c in ordered_choices:
            real_choices.append((c, choices[c]))

        return real_choices


class CreateDocumentForm(forms.Form):
    name = forms.CharField(max_length=200)
    document_class = forms.ChoiceField(choices=())
    pages = forms.MultipleChoiceField(choices=(), widget=PageSelector)

    def __init__(self, *args, **kwargs):
        super(CreateDocumentForm, self).__init__(*args, **kwargs)
        self.fields['pages'].choices = list_incomings()
        self.fields['document_class'].choices = list_document_classes()


class CreateDocumentClassForm(forms.Form):
    name = forms.CharField(max_length=200)
    slug = forms.CharField(max_length=20)