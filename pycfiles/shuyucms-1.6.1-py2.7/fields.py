# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/generic/fields.py
# Compiled at: 2016-08-01 10:26:41
from __future__ import division, unicode_literals
from django.db.models import TextField

class KeywordsField(TextField):

    def __init__(self, *args, **kwargs):
        self.name = b'领域标签'
        self.verbose_name = b'领域标签'
        self.null = True
        self.blank = True
        self.default = b''
        super(KeywordsField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from shuyucms.generic.forms import KeywordsWidget
        kwargs[b'widget'] = KeywordsWidget
        return super(KeywordsField, self).formfield(**kwargs)