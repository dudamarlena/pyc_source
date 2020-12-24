# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/demo/views.py
# Compiled at: 2017-02-17 15:31:58
# Size of source mod 2**32: 2708 bytes
from __future__ import unicode_literals
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import ContactForm, FilesForm, ContactFormSet

class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context


class DefaultFormsetView(FormView):
    template_name = 'formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {'file4': fieldfile}


class PaginationView(TemplateView):
    template_name = 'pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append('Line %s' % (i + 1))

        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            show_lines = paginator.page(1)
        except EmptyPage:
            show_lines = paginator.page(paginator.num_pages)

        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'misc.html'