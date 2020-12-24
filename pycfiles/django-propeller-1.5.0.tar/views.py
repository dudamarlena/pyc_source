# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller_demo/views.py
# Compiled at: 2017-03-24 13:36:01
from __future__ import unicode_literals
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django_propeller.views import NavBarMixin
from .navbars import MainNavBar, DemoNavBar1, DemoNavBar2
from .forms import ContactForm, FilesForm, ContactFormSet
from .cards import DemoCard1, DemoCard2, DemoCard3, DemoCard4

class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, b'dummy.txt')

class HomePageView(TemplateView, NavBarMixin):
    template_name = b'home.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, b'hello http://example.com')
        return context


class DefaultFormsetView(FormView, NavBarMixin):
    template_name = b'formset.html'
    form_class = ContactFormSet
    navbar_class = MainNavBar


class DefaultFormView(FormView, NavBarMixin):
    template_name = b'form.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class DefaultFormByFieldView(FormView, NavBarMixin):
    template_name = b'form_by_field.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormHorizontalView(FormView, NavBarMixin):
    template_name = b'form_horizontal.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormInlineView(FormView, NavBarMixin):
    template_name = b'form_inline.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormWithFilesView(FormView, NavBarMixin):
    template_name = b'form_with_files.html'
    form_class = FilesForm
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context[b'layout'] = self.request.GET.get(b'layout', b'vertical')
        return context

    def get_initial(self):
        return {b'file4': fieldfile}


class PaginationView(TemplateView, NavBarMixin):
    template_name = b'pagination.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append(b'Line %s' % (i + 1))

        paginator = Paginator(lines, 10)
        page = self.request.GET.get(b'page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            show_lines = paginator.page(1)
        except EmptyPage:
            show_lines = paginator.page(paginator.num_pages)

        context[b'lines'] = show_lines
        return context


class MiscView(TemplateView, NavBarMixin):
    template_name = b'misc.html'
    navbar_class = MainNavBar


class ButtonsView(TemplateView, NavBarMixin):
    template_name = b'buttons.html'
    navbar_class = MainNavBar


class FABsView(TemplateView, NavBarMixin):
    template_name = b'fabs.html'
    navbar_class = MainNavBar


class TypoView(TemplateView, NavBarMixin):
    template_name = b'typo.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(TypoView, self).get_context_data(**kwargs)
        context[b'text1'] = b'Propeller Heading'
        context[b'text2'] = b'with secondary heading'
        context[b'text3'] = b'Really large heading'
        context[b'text4'] = b'Larger heading'
        context[b'text5'] = b'Large heading'
        context[b'text6'] = b'Normal heading'
        context[b'text7'] = b'Heading'
        context[b'text8'] = b'Lead text...'
        context[b'text9'] = b'Normal text...'
        context[b'text10'] = b'With this filter you can '
        context[b'text11'] = b'highlight some text'
        context[b'text12'] = b'strikethrough some text'
        context[b'text13'] = b'underline some text'
        context[b'text14'] = b'show some bold text'
        context[b'text15'] = b'show some italic text'
        return context


class NavBarView(TemplateView, NavBarMixin):
    template_name = b'navbar.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(NavBarView, self).get_context_data(**kwargs)
        context[b'navbar1'] = DemoNavBar1
        context[b'navbar2'] = DemoNavBar2
        return context


class CardView(TemplateView, NavBarMixin):
    template_name = b'cards.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(CardView, self).get_context_data(**kwargs)
        context[b'card1'] = DemoCard1
        context[b'card2'] = DemoCard2
        context[b'card3'] = DemoCard3
        context[b'card4'] = DemoCard4
        return context