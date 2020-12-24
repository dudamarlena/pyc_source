# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-crispy-forms/django-crispy-forms-ng/crispy_forms/tests/test_tags.py
# Compiled at: 2015-04-08 09:53:39
from django.conf import settings
from django.forms.forms import BoundField
from django.forms.models import formset_factory
from django.template import Context
from .base import CrispyTestCase
from .forms import TestForm
from crispy_forms.templatetags.crispy_forms_field import crispy_addon
from crispy_forms.tests.utils import get_template_from_string

class TestBasicFunctionalityTags(CrispyTestCase):

    def test_as_crispy_errors_form_without_non_field_errors(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {{ form|as_crispy_errors }}\n        ')
        form = TestForm({'password1': 'god', 'password2': 'god'})
        form.is_valid()
        c = Context({'form': form})
        html = template.render(c)
        self.assertFalse('errorMsg' in html or 'alert' in html)

    def test_as_crispy_errors_form_with_non_field_errors(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {{ form|as_crispy_errors }}\n        ')
        form = TestForm({'password1': 'god', 'password2': 'wargame'})
        form.is_valid()
        c = Context({'form': form})
        html = template.render(c)
        self.assertTrue('errorMsg' in html or 'alert' in html)
        self.assertTrue('<li>Passwords dont match</li>' in html)
        self.assertFalse('<h3>' in html)

    def test_crispy_filter_with_form(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {{ form|crispy }}\n        ')
        c = Context({'form': TestForm()})
        html = template.render(c)
        self.assertTrue('<td>' not in html)
        self.assertTrue('id_is_company' in html)
        self.assertEqual(html.count('<label'), 7)

    def test_crispy_filter_with_formset(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {{ testFormset|crispy }}\n        ')
        TestFormset = formset_factory(TestForm, extra=4)
        testFormset = TestFormset()
        c = Context({'testFormset': testFormset})
        html = template.render(c)
        self.assertEqual(html.count('<form'), 0)
        self.assertTrue('form-TOTAL_FORMS' in html)
        self.assertTrue('form-INITIAL_FORMS' in html)
        self.assertTrue('form-MAX_NUM_FORMS' in html)

    def test_classes_filter(self):
        template = get_template_from_string('\n            {% load crispy_forms_field %}\n            {{ testField|classes }}\n        ')
        test_form = TestForm()
        test_form.fields['email'].widget.attrs.update({'class': 'email-fields'})
        c = Context({'testField': test_form.fields['email']})
        html = template.render(c)
        self.assertTrue('email-fields' in html)

    def test_crispy_field_and_class_converters(self):
        if hasattr(settings, 'CRISPY_CLASS_CONVERTERS'):
            template = get_template_from_string("\n                {% load crispy_forms_field %}\n                {% crispy_field testField 'class' 'error' %}\n            ")
            test_form = TestForm()
            field_instance = test_form.fields['email']
            bound_field = BoundField(test_form, field_instance, 'email')
            c = Context({'testField': bound_field})
            html = template.render(c)
            self.assertTrue('error' in html)
            self.assertTrue('inputtext' in html)

    def test_crispy_addon(self):
        test_form = TestForm()
        field_instance = test_form.fields['email']
        bound_field = BoundField(test_form, field_instance, 'email')
        if self.current_template_pack == 'bootstrap':
            self.assertIn('input-prepend', crispy_addon(bound_field, prepend='Work'))
            self.assertNotIn('input-append', crispy_addon(bound_field, prepend='Work'))
            self.assertNotIn('input-prepend', crispy_addon(bound_field, append='Primary'))
            self.assertIn('input-append', crispy_addon(bound_field, append='Secondary'))
            self.assertIn('input-append', crispy_addon(bound_field, prepend='Work', append='Primary'))
            self.assertIn('input-prepend', crispy_addon(bound_field, prepend='Work', append='Secondary'))
        elif self.current_template_pack == 'bootsrap3':
            self.assertIn('input-group-addon', crispy_addon(bound_field, prepend='Work', append='Primary'))
            self.assertIn('input-group-addon', crispy_addon(bound_field, prepend='Work', append='Secondary'))
        with self.assertRaises(TypeError):
            crispy_addon()
            crispy_addon(bound_field)