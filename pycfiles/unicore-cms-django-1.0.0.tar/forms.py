# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-cms-django/cms/forms.py
# Compiled at: 2014-10-17 14:53:23
from pagedown.widgets import AdminPagedownWidget
from django import forms
from cms.models import Post, Category

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['localisation'].required = True

    class Meta:
        model = Post


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['localisation'].required = True

    class Meta:
        model = Category