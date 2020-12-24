# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/tests/fields.py
# Compiled at: 2014-11-25 00:16:59
from django import test, forms
from ginger.forms import FileOrUrlInput

class DummyForm(forms.Form):
    file = forms.FileField(widget=FileOrUrlInput, required=False)


class RequiredDummyForm(forms.Form):
    file = forms.FileField(widget=FileOrUrlInput, required=True)


class TestFileOrUrlInput(test.SimpleTestCase):
    image_url = 'http://media-cache-ec0.pinimg.com/236x/cb/99/03/cb9903c463fda9a46f6d79005f29a9be.jpg'

    def test_valid(self):
        form = DummyForm(data={'file': self.image_url}, files={})
        self.assertTrue(form.is_valid())
        file_obj = form.cleaned_data['file']
        self.assertEqual(file_obj.url, self.image_url)

    def test_contradiction(self):
        form = DummyForm(data={'file': self.image_url, 'file-clear': 'on'}, files={})
        self.assertFalse(form.is_valid())