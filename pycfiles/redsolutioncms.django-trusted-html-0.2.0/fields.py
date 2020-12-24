# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\fields.py
# Compiled at: 2014-04-29 06:05:21
from django.db import models
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from trustedhtml.rules import pretty
from trustedhtml.widgets import TrustedTextarea, AdminTrustedTextarea, TrustedTextInput, AdminTrustedTextInput, TrustedTinyMCE, AdminTrustedTinyMCE

class TrustedTextField(models.TextField):
    """
    TextField with build-in validation.
    """

    def __init__(self, validator=pretty, *args, **kwargs):
        super(TrustedTextField, self).__init__(*args, **kwargs)
        self.validator = validator

    def formfield(self, **kwargs):
        defaults = {'widget': TrustedTextarea(validator=self.validator)}
        defaults.update(kwargs)
        if defaults['widget'] == AdminTextareaWidget:
            defaults['widget'] = AdminTrustedTextarea(validator=self.validator)
        return super(TrustedTextField, self).formfield(**defaults)


class TrustedCharField(models.CharField):
    """
    TextField with build-in validation.
    """

    def __init__(self, validator=pretty, *args, **kwargs):
        super(TrustedCharField, self).__init__(*args, **kwargs)
        self.validator = validator

    def formfield(self, **kwargs):
        defaults = {'widget': TrustedTextInput(validator=self.validator)}
        defaults.update(kwargs)
        if defaults['widget'] == AdminTextInputWidget:
            defaults['widget'] = AdminTrustedTextInput(validator=self.validator)
        return super(TrustedCharField, self).formfield(**defaults)


class TrustedHTMLField(models.TextField):
    """
    TextField with build-in validation.
    """

    def __init__(self, validator=pretty, *args, **kwargs):
        super(TrustedHTMLField, self).__init__(*args, **kwargs)
        self.validator = validator

    def formfield(self, **kwargs):
        defaults = {'widget': TrustedTinyMCE(validator=self.validator)}
        defaults.update(kwargs)
        if defaults['widget'] == AdminTextareaWidget:
            defaults['widget'] = AdminTrustedTinyMCE(validator=self.validator)
        return super(TrustedHTMLField, self).formfield(**defaults)