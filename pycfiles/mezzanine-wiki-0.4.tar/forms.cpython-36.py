# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\forms.py
# Compiled at: 2018-01-31 10:14:17
# Size of source mod 2**32: 897 bytes
from builtins import object
from django import forms
from django.utils.translation import ugettext_lazy as _
from mezzanine_wiki.models import WikiPage

class PlainWidget(forms.Textarea):
    __doc__ = '\n    A regular Textarea widget that is compatible with mezzanine richtext.\n    '

    class Media(object):
        pass


class WikiPageForm(forms.ModelForm):
    summary = forms.CharField(label=(_('Edit summary')), max_length=400,
      required=False)

    class Meta(object):
        model = WikiPage
        fields = ('title', 'content', 'summary', 'status')

    def __init__(self, *args, **kwargs):
        (super(WikiPageForm, self).__init__)(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'wiki-textarea'
        if 'instance' in kwargs:
            del self.fields['title']