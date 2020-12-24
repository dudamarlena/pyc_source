# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/tests.py
# Compiled at: 2017-03-24 15:30:10
from __future__ import unicode_literals
import re
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.forms.formsets import formset_factory
from django.template import Context, Template
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch
from .propeller import PROPELLER_SET_REQUIRED_SET_DISABLED
from .exceptions import PropellerError
from .text import text_value, text_concat
from .utils import add_css_class, render_tag
from .test_data import DemoCard1, DemoCard2, DemoCard3, DemoCard4, TestNavbar1, TestNavbar2, TestNavbar3, NavBarLinkItem, NavBarDropDownDivider, NavBarDropDownItem, NavBar, TestNavbar4
from .test_results import RESULT_CARD1, RESULT_CARD2, RESULT_CARD3, RESULT_CARD4, RESULT_NAVBAR1, RESULT_NAVBAR2, RESULT_NAVBAR3
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class TemplateTestCase(TestCase):

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def render_template_with_propeller(self, string, context=None):
        return self.render_template(b'{% load propeller %}' + string, context)

    def render_template_with_form(self, text, context=None):
        """
        Create a template ``text`` that first loads bootstrap3.
        """
        if not context:
            context = {}
        if b'form' not in context:
            context[b'form'] = TestForm()
        return self.render_template_with_propeller(text, context)

    def render_formset(self, formset=None, context=None):
        """
        Create a template that renders a formset
        """
        if not context:
            context = {}
        context[b'formset'] = formset
        return self.render_template_with_form(b'{% propeller_formset formset %}', context)

    def render_form(self, form=None, context=None):
        """
        Create a template that renders a form
        """
        if not context:
            context = {}
        if form:
            context[b'form'] = form
        return self.render_template_with_form(b'{% propeller_form form %}', context)

    def render_form_field(self, field, context=None):
        """
        Create a template that renders a field
        """
        form_field = b'form.%s' % field
        return self.render_template_with_form(b'{% propeller_field ' + form_field + b' %}', context)

    def render_field(self, field, context=None):
        """
        Create a template that renders a field
        """
        if not context:
            context = {}
        context[b'field'] = field
        return self.render_template_with_form(b'{% propeller_field field %}', context)

    def get_title_from_html(self, html):

        class GetTitleParser(HTMLParser):

            def __init__(self):
                HTMLParser.__init__(self)
                self.title = None
                return

            def handle_starttag(self, tag, attrs):
                for attr, value in attrs:
                    if attr == b'title':
                        self.title = value

        parser = GetTitleParser()
        parser.feed(html)
        return parser.title


TestCase = TemplateTestCase
RADIO_CHOICES = (
 ('1', 'Radio 1'),
 ('2', 'Radio 2'))
MEDIA_CHOICES = (
 (
  b'Audio',
  (
   ('vinyl', 'Vinyl'),
   ('cd', 'CD'))),
 (
  b'Video',
  (
   ('vhs', 'VHS Tape'),
   ('dvd', 'DVD'))),
 ('unknown', 'Unknown'))

class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(max_length=100, help_text=b'my_help_text', required=True, widget=forms.TextInput(attrs={b'placeholder': b'placeholdertest'}))
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text=b'<i>my_help_text</i>')
    sender = forms.EmailField(label=b'Sender © unicode', help_text=b'E.g., "me@example.com"')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(required=False, help_text=b'cc stands for "carbon copy." You will get a copy in your mailbox.')
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(choices=RADIO_CHOICES, help_text=b'Check as many as you like.')
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(choices=MEDIA_CHOICES, help_text=b'Check as many as you like.')
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(choices=RADIO_CHOICES, widget=forms.CheckboxSelectMultiple, help_text=b'Check as many as you like.')
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(choices=MEDIA_CHOICES, widget=forms.CheckboxSelectMultiple, help_text=b'Check as many as you like.')
    addon = forms.CharField(widget=forms.TextInput(attrs={b'addon_before': b'before', b'addon_after': b'after'}))
    required_css_class = b'bootstrap3-req'
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(b'This error was added to show the non field errors styling.')


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = b''


class SettingsTest(TestCase):

    def test_settings(self):
        from .propeller import PROPELLER
        self.assertTrue(PROPELLER)

    def test_propeller_javascript_tag(self):
        res = self.render_template_with_form(b'{% propeller_javascript %}')
        self.assertEqual(res.strip(), b'<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>')

    def test_propeller_css_tag(self):
        res = self.render_template_with_form(b'{% propeller_css %}').strip()
        self.assertIn(b'<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">', res)

    def test_required_class(self):
        form = TestForm()
        res = self.render_template_with_form(b'{% propeller_form form %}', {b'form': form})
        self.assertIn(b'bootstrap3-req', res)


class TemplateTest(TestCase):

    def test_empty_template(self):
        res = self.render_template_with_form(b'')
        self.assertEqual(res.strip(), b'')

    def test_text_template(self):
        res = self.render_template_with_form(b'some text')
        self.assertEqual(res.strip(), b'some text')

    def test_propeller_template(self):
        res = self.render_template(b'{% extends "propeller/propeller.html" %}' + b'{% block propeller_content %}' + b'test_propeller_content' + b'{% endblock %}')
        self.assertIn(b'test_propeller_content', res)

    def test_javascript_without_jquery(self):
        res = self.render_template_with_form(b'{% propeller_javascript jquery=0 %}')
        self.assertIn(b'bootstrap', res)
        self.assertNotIn(b'jquery', res)

    def test_javascript_with_jquery(self):
        res = self.render_template_with_form(b'{% propeller_javascript jquery=1 %}')
        self.assertIn(b'bootstrap', res)
        self.assertIn(b'jquery', res)


class FormSetTest(TestCase):

    def test_illegal_formset(self):
        with self.assertRaises(PropellerError):
            self.render_formset(formset=b'illegal')


class FormTest(TestCase):

    def test_illegal_form(self):
        with self.assertRaises(PropellerError):
            self.render_form(form=b'illegal')

    def test_field_names(self):
        form = TestForm()
        res = self.render_form(form)
        for field in form:
            if field.name == b'datetime':
                self.assertIn(b'name="datetime_0"', res)
                self.assertIn(b'name="datetime_1"', res)
            else:
                self.assertIn(b'name="%s"' % field.name, res)

    def test_field_addons(self):
        form = TestForm()
        res = self.render_form(form)
        self.assertIn(b'<div class="input-group"><span class="input-group-addon">before</span><input', res)
        self.assertIn(b'/><span class="input-group-addon">after</span></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = self.render_template_with_form(b'{% propeller_form form exclude="cc_myself" %}', {b'form': form})
        self.assertNotIn(b'cc_myself', res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = self.render_template_with_form(b'{% propeller_form form layout="horizontal" %}', {b'form': form})
        self.assertIn(b'col-md-3', res)
        self.assertIn(b'col-md-9', res)
        res = self.render_template_with_form(b'{% propeller_form form layout="horizontal" ' + b'horizontal_label_class="hlabel" ' + b'horizontal_field_class="hfield" %}', {b'form': form})
        self.assertIn(b'hlabel', res)
        self.assertIn(b'hfield', res)

    def test_buttons_tag(self):
        form = TestForm()
        res = self.render_template_with_form(b'{% buttons layout="horizontal" %}{% endbuttons %}', {b'form': form})
        self.assertIn(b'col-md-3', res)
        self.assertIn(b'col-md-9', res)

    def test_required_class(self):
        form = TestForm({b'sender': b'sender'})
        res = self.render_template_with_form(b'{% propeller_form form %}', {b'form': form})
        self.assertIn(b'bootstrap3-req', res)
        res = self.render_template_with_form(b'{% propeller_form form required_css_class="successful-test" %}', {b'form': form})
        self.assertIn(b'successful-test', res)
        res = self.render_template_with_form(b'{% propeller_form form required_css_class="" %}', {b'form': form})
        self.assertNotIn(b'bootstrap3-req', res)


class FieldTest(TestCase):

    def test_illegal_field(self):
        with self.assertRaises(PropellerError):
            self.render_field(field=b'illegal')

    def test_show_help(self):
        res = self.render_form_field(b'subject')
        self.assertIn(b'my_help_text', res)
        self.assertNotIn(b'<i>my_help_text</i>', res)
        res = self.render_template_with_form(b'{% propeller_field form.subject show_help=0 %}')
        self.assertNotIn(b'my_help_text', res)

    def test_help_with_quotes(self):
        res = self.render_form_field(b'sender')
        self.assertEqual(self.get_title_from_html(res), TestForm.base_fields[b'sender'].help_text)
        res = self.render_form_field(b'cc_myself')
        self.assertEqual(self.get_title_from_html(res), TestForm.base_fields[b'cc_myself'].help_text)

    def test_subject(self):
        res = self.render_form_field(b'subject')
        self.assertIn(b'type="text"', res)
        self.assertIn(b'placeholder="placeholdertest"', res)

    def test_password(self):
        res = self.render_form_field(b'password')
        self.assertIn(b'type="password"', res)
        self.assertIn(b'placeholder="Password"', res)

    def test_required_field(self):
        if PROPELLER_SET_REQUIRED_SET_DISABLED:
            required_field = self.render_form_field(b'subject')
            self.assertIn(b'required', required_field)
            self.assertIn(b'bootstrap3-req', required_field)
            not_required_field = self.render_form_field(b'message')
            self.assertNotIn(b'required', not_required_field)
            form_field = b'form.subject'
            rendered = self.render_template_with_form(b'{% propeller_field ' + form_field + b' set_required=0 %}')
            self.assertNotIn(b'required', rendered)
        else:
            required_css_class = b'bootstrap3-req'
            required_field = self.render_form_field(b'subject')
            self.assertIn(required_css_class, required_field)
            not_required_field = self.render_form_field(b'message')
            self.assertNotIn(required_css_class, not_required_field)
        form_field = b'form.subject'
        rendered = self.render_template_with_form(b'{% propeller_field ' + form_field + b' required_css_class="test-required" %}')
        self.assertIn(b'test-required', rendered)

    def test_empty_permitted(self):
        """
        If a form has empty_permitted, no fields should get the CSS class for required.
        Django <= 1.8, also check `required` attribute.
        """
        if PROPELLER_SET_REQUIRED_SET_DISABLED:
            required_css_class = b'bootstrap3-req'
            form = TestForm()
            res = self.render_form_field(b'subject', {b'form': form})
            self.assertIn(required_css_class, res)
            form.empty_permitted = True
            res = self.render_form_field(b'subject', {b'form': form})
            self.assertNotIn(required_css_class, res)
        else:
            required_css_class = b'bootstrap3-req'
            form = TestForm()
            res = self.render_form_field(b'subject', {b'form': form})
            self.assertIn(required_css_class, res)
            form.empty_permitted = True
            res = self.render_form_field(b'subject', {b'form': form})
            self.assertNotIn(required_css_class, res)

    def test_input_group(self):
        res = self.render_template_with_form(b'{% propeller_field form.subject addon_before="$"  addon_after=".00" %}')
        self.assertIn(b'class="input-group"', res)
        self.assertIn(b'class="input-group-addon">$', res)
        self.assertIn(b'class="input-group-addon">.00', res)

    def test_input_group_addon_button(self):
        res = self.render_template_with_form(b'{% propeller_field form.subject addon_before="$" addon_before_class="input-group-btn" addon_after=".00" addon_after_class="input-group-btn" %}')
        self.assertIn(b'class="input-group"', res)
        self.assertIn(b'class="input-group-btn">$', res)
        self.assertIn(b'class="input-group-btn">.00', res)

    def test_size(self):

        def _test_size(param, klass):
            res = self.render_template_with_form(b'{% propeller_field form.subject size="' + param + b'" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = self.render_template_with_form(b'{% propeller_field form.subject size="' + param + b'" %}')
            self.assertNotIn(b'input-lg', res)
            self.assertNotIn(b'input-sm', res)
            self.assertNotIn(b'input-md', res)

        _test_size(b'sm', b'input-sm')
        _test_size(b'small', b'input-sm')
        _test_size(b'lg', b'input-lg')
        _test_size(b'large', b'input-lg')
        _test_size_medium(b'md')
        _test_size_medium(b'medium')
        _test_size_medium(b'')

    def test_datetime(self):
        field = self.render_form_field(b'datetime')
        self.assertIn(b'vDateField', field)
        self.assertIn(b'vTimeField', field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = self.render_form_field(b'addon', context)
        rendered_b = self.render_form_field(b'addon', context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = self.render_template_with_form(b'{% propeller_label "foobar" label_for="subject" %}')
        self.assertEqual(b'<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields[b'addon'].widget.attrs.copy()
        context = dict(form=form)
        field_alone = self.render_form_field(b'addon', context)
        self.assertEqual(attrs, form.fields[b'addon'].widget.attrs)


class ComponentsTest(TestCase):

    def test_icon(self):
        res = self.render_template_with_form(b'{% propeller_icon "star" %}')
        self.assertEqual(res.strip(), b'<i class="material-icons pmd-sm">star</i>')
        res = self.render_template_with_form(b'{% propeller_icon "star" title="alpha centauri" %}')
        self.assertIn(res.strip(), [
         b'<i class="material-icons pmd-sm" title="alpha centauri">star</i>',
         b'<span title="alpha centauri" class="glyphicon glyphicon-star"></span>'])

    def test_alert(self):
        res = self.render_template_with_form(b'{% propeller_alert "content" alert_type="danger" %}')
        self.assertEqual(res.strip(), b'<div class="alert alert-danger alert-dismissable">' + b'<button type="button" class="close" data-dismiss="alert" ' + b'aria-hidden="true">' + b'&times;</button>content</div>')


class MessagesTest(TestCase):

    def test_messages(self):

        class FakeMessage(object):
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """
            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(b'\\s+')
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, b'hello')]
        res = self.render_template_with_form(b'{% propeller_messages messages %}', {b'messages': messages})
        expected = b'\n    <div class="alert alert-warning alert-dismissable">\n        <button type="button" class="close" data-dismiss="alert"\n            aria-hidden="true">&#215;</button>\n        hello\n    </div>\n'
        self.assertEqual(re.sub(pattern, b'', res), re.sub(pattern, b'', expected))
        messages = [
         FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, b'hello')]
        res = self.render_template_with_form(b'{% propeller_messages messages %}', {b'messages': messages})
        expected = b'\n    <div class="alert alert-danger alert-dismissable">\n        <button type="button" class="close" data-dismiss="alert"\n            aria-hidden="true">&#215;</button>\n        hello\n    </div>\n        '
        self.assertEqual(re.sub(pattern, b'', res), re.sub(pattern, b'', expected))
        messages = [
         FakeMessage(None, b'hello')]
        res = self.render_template_with_form(b'{% propeller_messages messages %}', {b'messages': messages})
        expected = b'\n    <div class="alert alert-danger alert-dismissable">\n        <button type="button" class="close" data-dismiss="alert"\n            aria-hidden="true">&#215;</button>\n        hello\n    </div>\n        '
        self.assertEqual(re.sub(pattern, b'', res), re.sub(pattern, b'', expected))
        messages = [
         FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, b'hello http://example.com')]
        res = self.render_template_with_form(b'{% propeller_messages messages %}', {b'messages': messages})
        expected = b'\n    <div class="alert alert-danger alert-dismissable">\n        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>\n        hello http://example.com\n    </div>        '
        self.assertEqual(re.sub(pattern, b'', res).replace(b'rel="nofollow"', b''), re.sub(pattern, b'', expected).replace(b'rel="nofollow"', b''))
        messages = [
         FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, b'hello\nthere')]
        res = self.render_template_with_form(b'{% propeller_messages messages %}', {b'messages': messages})
        expected = b'\n    <div class="alert alert-danger alert-dismissable">\n        <button type="button" class="close" data-dismiss="alert"\n            aria-hidden="true">&#215;</button>\n        hello there\n    </div>\n        '
        self.assertEqual(re.sub(pattern, b'', res), re.sub(pattern, b'', expected))
        return


class UtilsTest(TestCase):

    def test_add_css_class(self):
        css_classes = b'one two'
        css_class = b'three four'
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, b'one two three four')
        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, b'three four one two')

    def test_text_value(self):
        self.assertEqual(text_value(b''), b'')
        self.assertEqual(text_value(b' '), b' ')
        self.assertEqual(text_value(None), b'')
        self.assertEqual(text_value(1), b'1')
        return

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), b'12')
        self.assertEqual(text_concat(1, 2, separator=b'='), b'1=2')
        self.assertEqual(text_concat(None, 2, separator=b'='), b'2')
        return

    def test_render_tag(self):
        self.assertEqual(render_tag(b'span'), b'<span></span>')
        self.assertEqual(render_tag(b'span', content=b'foo'), b'<span>foo</span>')
        self.assertEqual(render_tag(b'span', attrs={b'bar': 123}, content=b'foo'), b'<span bar="123">foo</span>')


class ButtonTest(TestCase):

    def test_button(self):
        res = self.render_template_with_form(b"{% propeller_button 'button' size='lg' %}")
        self.assertEqual(b'<button class="btn btn-default pmd-ripple-effect btn-lg pmd-btn-default" type="button">button</button>', res.strip())
        res = self.render_template_with_form(b"{% propeller_button 'button' size='lg' href='#' %}")
        self.assertIn(b'<a class="btn btn-default pmd-ripple-effect btn-lg pmd-btn-default" href="#" type="button">button</a>', res.strip())


class ShowLabelTest(TestCase):

    def test_show_label(self):
        form = TestForm()
        res = self.render_template_with_form(b'{% propeller_form form show_label=False %}', {b'form': form})
        self.assertIn(b'sr-only', res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = self.render_template_with_form(b'{% propeller_formset formset show_label=False %}', {b'formset': test_formset})
        self.assertIn(b'sr-only', res)

    def test_button_with_icon(self):
        res = self.render_template_with_form(b"{% propeller_button 'test' icon='info-sign' %}")
        self.assertEqual(b'<button class="btn btn-default pmd-ripple-effect pmd-btn-default" href="#" type="button"><i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())
        res = self.render_template_with_form(b"{% propeller_button 'test' icon='info-sign' button_class='btn-primary' %}")
        self.assertEqual(b'<button class="btn btn-primary pmd-ripple-effect pmd-btn-default" href="#" type="button"><i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())
        res = self.render_template_with_form(b"{% propeller_button 'test' icon='info-sign' button_type='submit' %}")
        self.assertEqual(b'<button class="btn btn-default pmd-ripple-effect pmd-btn-default" href="#" type="submit"><i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())


class TypographyTest(TestCase):

    def test_marked_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_mark_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<mark>This is a test</mark>', res)

    def test_striked_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_strike_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<s>This is a test</s>', res)

    def test_underlined_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_underline_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<u>This is a test</u>', res)

    def test_bold_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_bold_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<strong>This is a test</strong>', res)

    def test_italic_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_italic_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<em>This is a test</em>', res)

    def test_lead_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_lead_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="lead">This is a test</span>', res)

    def test_display_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_display_text:1 }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="pmd-display1">This is a test</span>', res)
        res = self.render_template_with_propeller(b'{{ text|pmd_display_text:2 }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="pmd-display2">This is a test</span>', res)
        res = self.render_template_with_propeller(b'{{ text|pmd_display_text:3 }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="pmd-display3">This is a test</span>', res)
        res = self.render_template_with_propeller(b'{{ text|pmd_display_text:4 }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="pmd-display4">This is a test</span>', res)

    def test_muted_text_filter(self):
        res = self.render_template_with_propeller(b'{{ text|pmd_muted_text }}', {b'text': b'This is a test'})
        self.assertInHTML(b'<span class="text-muted">This is a test</span>', res)


class FABsTests(TestCase):

    def test_default_fab(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="star" %}')
        self.assertInHTML(b'<button class="btn pmd-btn-fab pmd-btn-default pmd-ripple-effect btn-default" type="button"><i class="material-icons pmd-sm">star</i></button>', res)

    def test_default_fab_with_btn_class(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="warning" button_class="btn-warning" %}')
        self.assertInHTML(b'<button class="btn btn-warning pmd-btn-fab pmd-ripple-effect pmd-btn-default" type="button"><i class="material-icons pmd-sm">warning</i></button>', res)

    def test_default_fab_with_link(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "Link" button_class="btn-link" %}')
        self.assertInHTML(b'<button class="btn pmd-btn-fab pmd-btn-default pmd-ripple-effect btn-link" type="button">Link</button>', res)

    def test_raised_fab(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="star" style="raised" %}')
        self.assertInHTML(b'<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button"><i class="material-icons pmd-sm">star</i></button>', res)

    def test_raised_fab_with_btn_class(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="error" style="raised" button_class="btn-danger" %}')
        self.assertInHTML(b'<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button"><i class="material-icons pmd-sm">error</i></button>', res)

    def test_raised_fab_with_link(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "Link" style="raised" button_class="btn-link" %}')
        self.assertInHTML(b'<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button">Link</button>', res)

    def test_flat_fab(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="star" style="flat" %}')
        self.assertInHTML(b'<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button"><i class="material-icons pmd-sm">star</i></button>', res)

    def test_flat_fab_with_btn_class(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="info" style="flat" button_class="btn-danger" %}')
        self.assertInHTML(b'<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button"><i class="material-icons pmd-sm">info</i></button>', res)

    def test_flat_fab_with_link(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "Link" style="flat" button_class="btn-link" %}')
        self.assertInHTML(b'<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button">Link</button>', res)

    def test_outline_fab(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="star" style="outline" %}')
        self.assertInHTML(b'<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button"><i class="material-icons pmd-sm">star</i></button>', res)

    def test_outline_fab_with_btn_class(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "" icon="check" style="outline" button_class="btn-danger" %}')
        self.assertInHTML(b'<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button"><i class="material-icons pmd-sm">check</i></button>', res)

    def test_outline_fab_with_link(self):
        res = self.render_template_with_propeller(b'{% propeller_fab "Link" style="outline" button_class="btn-link" %}')
        self.assertInHTML(b'<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button">Link</button>', res)


class DjangoAppTests(TestCase):

    def test_app_config(self):
        from django_propeller.apps import DjangoPropellerConfig
        self.assertEqual(DjangoPropellerConfig.name, b'django_propeller')


class PropellerMixinTests(TestCase):

    class TestNavbar(NavBar):
        pass

    def test_navbar_mixin(self):
        from django_propeller.views import NavBarMixin, ContextMixin
        test_mixin = NavBarMixin()
        self.assertIsInstance(test_mixin, ContextMixin)
        test_mixin.navbar_class = self.TestNavbar
        self.assertIsInstance(test_mixin.get_context_data().get(b'navbar')(), self.TestNavbar)


class PropellerNavBarTests(TestCase):

    def test_navbar_config(self):
        self.assertEqual(TestNavbar1().get_brand_url(), b'https://github.com/tfroehlich82/django-propeller')
        self.assertEqual(TestNavbar1().brandname, b'propeller-test')
        self.assertEqual(TestNavbar2().get_brand_url(), b'javascript:void(0);')
        with self.assertRaises(NoReverseMatch):
            TestNavbar4().get_brand_url()

    def test_rendered_template(self):
        res = self.render_template_with_propeller(b'{% propeller_navbar testnav1 %}', context={b'testnav1': TestNavbar1()})
        self.assertInHTML(RESULT_NAVBAR1, res)
        res = self.render_template_with_propeller(b'{% propeller_navbar testnav2 %}', context={b'testnav2': TestNavbar2()})
        self.assertInHTML(RESULT_NAVBAR2, res)
        res = self.render_template_with_propeller(b'{% propeller_navbar testnav3 %}', {b'testnav3': TestNavbar3()})
        self.assertInHTML(RESULT_NAVBAR3, res)

    def test_navbar_items(self):
        for itm in TestNavbar4().items:
            if itm.name in ('Test1', ):
                self.assertIsInstance(itm, NavBarLinkItem)
                self.assertEqual(itm.get_url(), b'http://example.org')
            elif itm.name in ('Test2', ):
                self.assertIsInstance(itm, NavBarDropDownItem)
                for dd_itm in itm.items:
                    if hasattr(dd_itm, b'name') and dd_itm.name in ('Test3', 'Test4',
                                                                    'Test5'):
                        if dd_itm.name == b'Test3':
                            with self.assertRaises(NoReverseMatch):
                                dd_itm.get_url()
                        elif dd_itm.name == b'Test4':
                            self.assertEqual(dd_itm.get_url(), b'javascript:void(0);')
                        self.assertIsInstance(dd_itm, NavBarLinkItem)
                    else:
                        self.assertIsInstance(dd_itm, NavBarDropDownDivider)


class PropellerCardTests(TestCase):

    def test_rendered_template(self):
        res = self.render_template_with_propeller(b'{% propeller_card card1 %}', context={b'card1': DemoCard1()})
        self.assertInHTML(RESULT_CARD1, res)
        res = self.render_template_with_propeller(b'{% propeller_card card2 %}', context={b'card2': DemoCard2()})
        self.assertInHTML(RESULT_CARD2, res)
        res = self.render_template_with_propeller(b'{% propeller_card card3 %}', {b'card3': DemoCard3()})
        self.assertInHTML(RESULT_CARD3, res)
        res = self.render_template_with_propeller(b'{% propeller_card card4 %}', {b'card4': DemoCard4()})
        self.assertInHTML(RESULT_CARD4, res)