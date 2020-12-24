# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/lib/python2.7/site-packages/richtext_blog/forms.py
# Compiled at: 2012-04-15 00:30:08
from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from captcha.fields import CaptchaField
from models import Post, Comment

class PostFormAdmin(forms.ModelForm):
    """
    Form for creating and editing posts in the admin section
    """
    content = forms.CharField(required=False, widget=TinyMCE())

    class Meta:
        model = Post


class BlogModelFormBase(forms.ModelForm):
    """
    Define some defaults
    """
    error_css_class = 'error'
    required_css_class = 'required'


class CommentForm(BlogModelFormBase):
    """
    Form for the creation of a new comment
    """
    author = forms.CharField(required=False)
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '10'}))
    verification = CaptchaField(help_text='Please type the letters in the image')

    class Meta:
        model = Comment
        exclude = ('post', )