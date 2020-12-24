# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faq/forms.py
# Compiled at: 2014-03-27 06:14:42
from django.forms import ModelForm
from suit_redactor.widgets import RedactorWidget

class QuestionAdminForm(ModelForm):

    class Meta:
        widgets = {'answer': RedactorWidget(editor_options={'lang': 'en', 
                      'minHeight': '200', 
                      'buttons': [
                                'html', '|',
                                'bold', 'italic', 'deleted', 'underline', '|',
                                'unorderedlist', 'orderedlist', '|',
                                'alignleft', 'aligncenter', 'alignright', 'justify', '|',
                                'link']})}