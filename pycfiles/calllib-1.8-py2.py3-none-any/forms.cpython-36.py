# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/forms.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1434 bytes
from django import forms
from django.contrib.auth import get_user_model
from . import widgets
User = get_user_model()

class PageForm(forms.Form):

    @classmethod
    def setup(cls, page, data):
        cls.base_fields = {question.field_id:question.make_field() for question in page.mock_questions}
        self = cls(data)
        self.page = page
        self.full_clean()
        return self

    @property
    def sections(self):
        from .models import Page
        return dict(Page.SECTION_CHOICES)

    @property
    def serialized(self):
        return [question.serialized for question in self.page.mock_questions]

    def _clean_fields(self):
        for name, field in self.fields.items():
            self.cleaned_data[name] = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))

        self._clean_conditional_fields()

    def _clean_conditional_fields(self):
        for question in self.page.mock_questions:
            for choice in question.choices:
                self._clean_if_choice_conditional(choice.data)

    def _clean_if_choice_conditional(self, choice):
        field = widgets.conditional_field_from_choice(choice)
        if field:
            name = widgets.conditional_id(choice)
            self.cleaned_data[name] = field.widget.value_from_datadict(self.data, self.files, name)