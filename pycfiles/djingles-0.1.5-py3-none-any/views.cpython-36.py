# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/djingles/src/djingles/bootstrap4/views.py
# Compiled at: 2018-04-18 07:49:33
# Size of source mod 2**32: 595 bytes
from djingles.bootstrap4 import forms, models
from django.views import generic

class VerticalFormView(generic.FormView):
    template_name = 'bootstrap4/form.html'
    form_class = forms.VerticalForm


class InlineFormView(generic.FormView):
    template_name = 'bootstrap4/inline_form.html'
    form_class = forms.InlineForm


class ObjectTable(generic.ListView):
    pass


class ObjectDetailView(generic.DetailView):
    pass


class ObjectEditView(generic.UpdateView):
    pass


class ObjectDeleteView(generic.DeleteView):
    pass


class ObjectCreateView(generic.CreateView):
    pass