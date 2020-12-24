# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\forms.py
# Compiled at: 2013-08-27 09:19:33
from __future__ import unicode_literals
import crispy_forms.helper

class DefaultFormHelper(crispy_forms.helper.FormHelper):

    def __init__(self, form=None):
        super(DefaultFormHelper, self).__init__(form=form)
        self.form_class = b'form-horizontal'
        self.html5_required = True
        self.help_text_inline = True