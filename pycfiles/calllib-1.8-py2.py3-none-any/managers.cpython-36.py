# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/managers.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1773 bytes
import logging
from django.contrib.sites.models import Site
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from . import forms, mocks, models
logger = logging.getLogger(__name__)

class FormManager(object):

    @classmethod
    def get_serialized_forms(cls, site_id=1):
        return [form.serialized for form in cls.get_form_models(site_id=site_id)]

    @classmethod
    def get_form_models(cls, form_data={}, answer_data={}, site_id=1):
        self = cls()
        self.site_id = site_id
        self.answer_data = answer_data
        self.form_data = form_data
        if not form_data:
            self.form_data = self._get_form_data_from_db()
        return self._create_forms_via_data()

    def _get_form_data_from_db(self):
        return [[question.serialized for question in page.site_questions(self.site_id)] for page in models.Page.objects.on_site(self.site_id)]

    def _create_forms_via_data(self):
        return [forms.PageForm.setup(page, self.answer_data) for page in self._pages_via_form_data()]

    def _pages_via_form_data(self):
        pages = []
        for page_questions in self.form_data:
            page = mocks.MockPage(page_questions)
            pages.append(page)

        return pages


class PageQuerySet(QuerySet):

    def on_site(self, site_id=None):
        try:
            site_id = site_id or Site.objects.get_current().id
        except Site.DoesNotExist:
            site_id = 1

        return self.filter(formquestion__sites__id__in=[site_id]).distinct()


class PageManager(Manager):
    _queryset_class = PageQuerySet

    def on_site(self, site_id=None):
        return self.get_queryset().on_site(site_id)