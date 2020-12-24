# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-crispy-forms/django-crispy-forms-ng/crispy_forms/tests/test_form_helper.py
# Compiled at: 2015-04-08 10:03:36
# Size of source mod 2**32: 22437 bytes
import re, django
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory
from django.middleware.csrf import _get_new_csrf_key
from django.template import TemplateSyntaxError, Context
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .base import CrispyTestCase
from .forms import TestForm
from crispy_forms.bootstrap import FieldWithButtons, PrependedAppendedText, AppendedText, PrependedText, StrictButton
from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import Layout, Submit, Reset, Hidden, Button, MultiField, Field
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode
from crispy_forms.tests.utils import get_template_from_string

class TestFormHelper(CrispyTestCase):
    urls = 'crispy_forms.tests.urls'

    def test_inputs(self):
        form_helper = FormHelper()
        form_helper.add_input(Submit('my-submit', 'Submit', css_class='button white'))
        form_helper.add_input(Reset('my-reset', 'Reset'))
        form_helper.add_input(Hidden('my-hidden', 'Hidden'))
        form_helper.add_input(Button('my-button', 'Button'))
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy form form_helper %}\n        ')
        c = Context({'form': TestForm(),  'form_helper': form_helper})
        html = template.render(c)
        self.assertTrue('button white' in html)
        self.assertTrue('id="submit-id-my-submit"' in html)
        self.assertTrue('id="reset-id-my-reset"' in html)
        self.assertTrue('name="my-hidden"' in html)
        self.assertTrue('id="button-id-my-button"' in html)
        if self.current_template_pack == 'uni_form':
            self.assertTrue('submit submitButton' in html)
            self.assertTrue('reset resetButton' in html)
            self.assertTrue('class="button"' in html)
        else:
            self.assertTrue('class="btn"' in html)
            self.assertTrue('btn btn-primary' in html)
            self.assertTrue('btn btn-inverse' in html)
            self.assertEqual(len(re.findall('<input[^>]+> <', html)), 8)

    def test_invalid_form_method(self):
        form_helper = FormHelper()
        try:
            form_helper.form_method = 'superPost'
            self.fail('Setting an invalid form_method within the helper should raise an Exception')
        except FormHelpersException:
            pass

    def test_form_with_helper_without_layout(self):
        form_helper = FormHelper()
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
        form_helper.form_action = 'simpleAction'
        form_helper.form_error_title = 'ERRORS'
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy testForm form_helper %}\n        ')
        form = TestForm({'password1': 'wargame',  'password2': 'god'})
        form.is_valid()
        c = Context({'testForm': form,  'form_helper': form_helper})
        html = template.render(c)
        self.assertTrue(html.count('<form'), 1)
        self.assertTrue('forms-that-rock' in html)
        self.assertTrue('method="get"' in html)
        self.assertTrue('id="this-form-rocks"' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)
        if self.current_template_pack == 'uni_form':
            self.assertTrue('class="uniForm' in html)
        self.assertTrue('ERRORS' in html)
        self.assertTrue('<li>Passwords dont match</li>' in html)
        form_helper.form_tag = False
        html = template.render(c)
        self.assertFalse('<form' in html)
        self.assertFalse('forms-that-rock' in html)
        self.assertFalse('method="get"' in html)
        self.assertFalse('id="this-form-rocks"' in html)

    def test_form_show_errors_non_field_errors(self):
        form = TestForm({'password1': 'wargame',  'password2': 'god'})
        form.helper = FormHelper()
        form.helper.form_show_errors = True
        form.is_valid()
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy testForm %}\n        ')
        c = Context({'testForm': form})
        html = template.render(c)
        self.assertTrue('<li>Passwords dont match</li>' in html)
        self.assertTrue(six.text_type(_('This field is required.')) in html)
        self.assertTrue('error' in html)
        form.helper.form_show_errors = False
        c = Context({'testForm': form})
        html = template.render(c)
        self.assertFalse('<li>Passwords dont match</li>' in html)
        self.assertFalse(six.text_type(_('This field is required.')) in html)
        self.assertFalse('error' in html)

    def test_html5_required(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.html5_required = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('required="required"'), 7)
        form = TestForm()
        form.helper = FormHelper()
        form.helper.html5_required = False
        html = render_crispy_form(form)

    def test_attrs(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.attrs = {'id': 'TestIdForm',  'autocomplete': 'off'}
        html = render_crispy_form(form)
        self.assertTrue('autocomplete="off"' in html)
        self.assertTrue('id="TestIdForm"' in html)

    def test_template_context(self):
        helper = FormHelper()
        helper.attrs = {'id': 'test-form', 
         'class': 'test-forms', 
         'action': 'submit/test/form', 
         'autocomplete': 'off'}
        node = CrispyFormNode('form', 'helper')
        context = node.get_response_dict(helper, {}, False)
        self.assertEqual(context['form_id'], 'test-form')
        self.assertEqual(context['form_attrs']['id'], 'test-form')
        self.assertTrue('test-forms' in context['form_class'])
        self.assertTrue('test-forms' in context['form_attrs']['class'])
        self.assertEqual(context['form_action'], 'submit/test/form')
        self.assertEqual(context['form_attrs']['action'], 'submit/test/form')
        self.assertEqual(context['form_attrs']['autocomplete'], 'off')

    def test_template_context_using_form_attrs(self):
        helper = FormHelper()
        helper.form_id = 'test-form'
        helper.form_class = 'test-forms'
        helper.form_action = 'submit/test/form'
        node = CrispyFormNode('form', 'helper')
        context = node.get_response_dict(helper, {}, False)
        self.assertEqual(context['form_id'], 'test-form')
        self.assertEqual(context['form_attrs']['id'], 'test-form')
        self.assertTrue('test-forms' in context['form_class'])
        self.assertTrue('test-forms' in context['form_attrs']['class'])
        self.assertEqual(context['form_action'], 'submit/test/form')
        self.assertEqual(context['form_attrs']['action'], 'submit/test/form')

    def test_template_helper_access(self):
        helper = FormHelper()
        helper.form_id = 'test-form'
        self.assertEqual(helper['form_id'], 'test-form')

    def test_without_helper(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy form %}\n        ')
        c = Context({'form': TestForm()})
        html = template.render(c)
        self.assertTrue('<form' in html)
        self.assertTrue('method="post"' in html)
        self.assertFalse('action' in html)
        if self.current_template_pack == 'uni_form':
            self.assertTrue('uniForm' in html)

    def test_template_pack_override_compact(self):
        current_pack = self.current_template_pack
        override_pack = current_pack == 'uni_form' and 'bootstrap' or 'uni_form'
        template = get_template_from_string('\n            {%% load crispy_forms_tags %%}\n            {%% crispy form "%s" %%}\n        ' % override_pack)
        c = Context({'form': TestForm()})
        html = template.render(c)
        if current_pack == 'uni_form':
            self.assertTrue('control-group' in html)
        else:
            self.assertTrue('uniForm' in html)

    def test_template_pack_override_verbose(self):
        current_pack = self.current_template_pack
        override_pack = current_pack == 'uni_form' and 'bootstrap' or 'uni_form'
        template = get_template_from_string('\n            {%% load crispy_forms_tags %%}\n            {%% crispy form form_helper "%s" %%}\n        ' % override_pack)
        c = Context({'form': TestForm(),  'form_helper': FormHelper()})
        html = template.render(c)
        if current_pack == 'uni_form':
            self.assertTrue('control-group' in html)
        else:
            self.assertTrue('uniForm' in html)

    def test_template_pack_override_wrong(self):
        try:
            get_template_from_string("\n                {% load crispy_forms_tags %}\n                {% crispy form 'foo' %}\n            ")
        except TemplateSyntaxError:
            pass

    def test_invalid_helper(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy form form_helper %}\n        ')
        c = Context({'form': TestForm(),  'form_helper': 'invalid'})
        settings.CRISPY_FAIL_SILENTLY = False
        if settings.TEMPLATE_DEBUG and django.VERSION < (1, 4):
            self.assertRaises(TemplateSyntaxError, lambda : template.render(c))
        else:
            self.assertRaises(TypeError, lambda : template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_formset_with_helper_without_layout(self):
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy testFormSet formset_helper %}\n        ')
        form_helper = FormHelper()
        form_helper.form_id = 'thisFormsetRocks'
        form_helper.form_class = 'formsets-that-rock'
        form_helper.form_method = 'POST'
        form_helper.form_action = 'simpleAction'
        TestFormSet = formset_factory(TestForm, extra=3)
        testFormSet = TestFormSet()
        c = Context({'testFormSet': testFormSet,  'formset_helper': form_helper,  'csrf_token': _get_new_csrf_key()})
        html = template.render(c)
        self.assertEqual(html.count('<form'), 1)
        self.assertEqual(html.count("<input type='hidden' name='csrfmiddlewaretoken'"), 1)
        self.assertTrue('form-TOTAL_FORMS' in html)
        self.assertTrue('form-INITIAL_FORMS' in html)
        self.assertTrue('form-MAX_NUM_FORMS' in html)
        self.assertTrue('formsets-that-rock' in html)
        self.assertTrue('method="post"' in html)
        self.assertTrue('id="thisFormsetRocks"' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)
        if self.current_template_pack == 'uni_form':
            self.assertTrue('class="uniForm' in html)

    def test_CSRF_token_POST_form(self):
        form_helper = FormHelper()
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy form form_helper %}\n        ')
        c = Context({'form': TestForm(),  'form_helper': form_helper,  'csrf_token': _get_new_csrf_key()})
        html = template.render(c)
        self.assertTrue("<input type='hidden' name='csrfmiddlewaretoken'" in html)

    def test_CSRF_token_GET_form(self):
        form_helper = FormHelper()
        form_helper.form_method = 'GET'
        template = get_template_from_string('\n            {% load crispy_forms_tags %}\n            {% crispy form form_helper %}\n        ')
        c = Context({'form': TestForm(),  'form_helper': form_helper,  'csrf_token': _get_new_csrf_key()})
        html = template.render(c)
        self.assertFalse("<input type='hidden' name='csrfmiddlewaretoken'" in html)

    def test_disable_csrf(self):
        form = TestForm()
        helper = FormHelper()
        helper.disable_csrf = True
        html = render_crispy_form(form, helper, {'csrf_token': _get_new_csrf_key()})
        self.assertFalse('csrf' in html)

    def test_render_hidden_fields(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout('email')
        test_form.helper.render_hidden_fields = True
        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 1)
        for field in ('password1', 'password2'):
            test_form.fields[field].widget = forms.HiddenInput()

        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 3)
        self.assertEqual(html.count('hidden'), 2)
        self.assertInHTML('<input type="hidden" name="password1" id="id_password1" />', html, count=1)
        self.assertInHTML('<input type="hidden" name="password2" id="id_password2" />', html, count=1)

    def test_render_required_fields(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout('email')
        test_form.helper.render_required_fields = True
        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 7)

    def test_helper_custom_template(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.template = 'custom_form_template.html'
        html = render_crispy_form(form)
        self.assertTrue('<h1>Special custom form</h1>' in html)

    def test_helper_custom_field_template(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.layout = Layout('password1', 'password2')
        form.helper.field_template = 'custom_field_template.html'
        html = render_crispy_form(form)
        self.assertEqual(html.count('<h1>Special custom field</h1>'), 2)


class TestUniformFormHelper(TestFormHelper):

    def test_form_show_errors(self):
        form = TestForm({'email': 'invalidemail', 
         'first_name': 'first_name_too_long', 
         'last_name': 'last_name_too_long', 
         'password1': 'yes', 
         'password2': 'yes'})
        form.helper = FormHelper()
        form.helper.layout = Layout(Field('email'), Field('first_name'), Field('last_name'), Field('password1'), Field('password2'))
        form.is_valid()
        form.helper.form_show_errors = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 9)
        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)

    def test_multifield_errors(self):
        form = TestForm({'email': 'invalidemail', 
         'password1': 'yes', 
         'password2': 'yes'})
        form.helper = FormHelper()
        form.helper.layout = Layout(MultiField('legend', 'email'))
        form.is_valid()
        form.helper.form_show_errors = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 3)
        form.helper.layout = Layout(MultiField('legend', 'email'))
        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)


class TestBootstrapFormHelper(TestFormHelper):

    def test_form_show_errors(self):
        form = TestForm({'email': 'invalidemail', 
         'first_name': 'first_name_too_long', 
         'last_name': 'last_name_too_long', 
         'password1': 'yes', 
         'password2': 'yes'})
        form.helper = FormHelper()
        form.helper.layout = Layout(AppendedText('email', 'whatever'), PrependedText('first_name', 'blabla'), PrependedAppendedText('last_name', 'foo', 'bar'), AppendedText('password1', 'whatever'), PrependedText('password2', 'blabla'))
        form.is_valid()
        form.helper.form_show_errors = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 6)
        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)

    def test_error_text_inline(self):
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        layout = Layout(AppendedText('first_name', 'wat'), PrependedText('email', '@'), PrependedAppendedText('last_name', '@', 'wat'))
        form.helper.layout = layout
        form.is_valid()
        html = render_crispy_form(form)
        help_class = 'help-inline'
        if self.current_template_pack == 'bootstrap3':
            help_class = 'help-block'
        matches = re.findall('<span id="error_\\d_\\w*" class="%s"' % help_class, html, re.MULTILINE)
        self.assertEqual(len(matches), 3)
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.layout = layout
        form.helper.error_text_inline = False
        html = render_crispy_form(form)
        matches = re.findall('<p id="error_\\d_\\w*" class="help-block"', html, re.MULTILINE)
        self.assertEqual(len(matches), 3)

    def test_error_and_help_inline(self):
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.error_text_inline = False
        form.helper.help_text_inline = True
        form.helper.layout = Layout('email')
        form.is_valid()
        html = render_crispy_form(form)
        help_position = html.find('<span id="hint_id_email" class="help-inline">')
        error_position = html.find('<p id="error_1_id_email" class="help-block">')
        self.assertTrue(help_position < error_position)
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.error_text_inline = True
        form.helper.help_text_inline = False
        form.helper.layout = Layout('email')
        form.is_valid()
        html = render_crispy_form(form)
        error_position = html.find('<span id="error_1_id_email" class="help-inline">')
        help_position = html.find('<p id="hint_id_email" class="help-block">')
        self.assertTrue(error_position < help_position)

    def test_form_show_labels(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.layout = Layout('password1', FieldWithButtons('password2', StrictButton('Confirm')), PrependedText('first_name', 'Mr.'), AppendedText('last_name', '@'), PrependedAppendedText('datetime_field', 'on', 'secs'))
        form.helper.form_show_labels = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('<label'), 0)


class TestBootstrap3FormHelper(TestFormHelper):

    def test_label_class_and_field_class(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.label_class = 'col-lg-2'
        form.helper.field_class = 'col-lg-8'
        html = render_crispy_form(form)
        self.assertTrue('<div class="form-group"> <div class="controls col-lg-offset-2 col-lg-8"> <div id="div_id_is_company" class="checkbox"> <label for="id_is_company" class=""> <input class="checkboxinput checkbox" id="id_is_company" name="is_company" type="checkbox" />')
        self.assertEqual(html.count('col-lg-8'), 7)
        form.helper.label_class = 'col-sm-3'
        form.helper.field_class = 'col-sm-8'
        html = render_crispy_form(form)
        self.assertTrue('<div class="form-group"> <div class="controls col-sm-offset-3 col-sm-8"> <div id="div_id_is_company" class="checkbox"> <label for="id_is_company" class=""> <input class="checkboxinput checkbox" id="id_is_company" name="is_company" type="checkbox" />')
        self.assertEqual(html.count('col-sm-8'), 7)

    def test_template_pack(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.template_pack = 'uni_form'
        html = render_crispy_form(form)
        self.assertFalse('form-control' in html)
        self.assertTrue('ctrlHolder' in html)