# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/carlos/projects/wagtail-jsonschema-forms/wagtail_jsonschema_forms/models.py
# Compiled at: 2017-10-13 14:00:05
# Size of source mod 2**32: 1063 bytes
from django.db import models
from wagtail.wagtailforms.models import AbstractForm, AbstractEmailForm
from wagtail_jsonschema_forms.mixins import JsonSchemaFormMixin, JsonSchemaEmailFormMixin

class AbstractJsonSchemaForm(JsonSchemaFormMixin, AbstractForm):
    __doc__ = '\n    A Form Page that generates a JSON Schema representation of the fields and save it to the model.\n    Pages implementing a form that need to generate JSON Schema should inherit from it\n    '
    json_schema = models.TextField(help_text='Form json Schema representation', blank=True)

    class Meta:
        abstract = True


class AbstractJsonSchemaEmailForm(JsonSchemaEmailFormMixin, AbstractEmailForm):
    __doc__ = '\n    A Form Page that generates a JSON Schema representation of the fields and save it to the model. It also send email.\n    Pages implementing a form that need to generate JSON Schema and need to send an email should inherit from it\n    '
    json_schema = models.TextField(help_text='Form json Schema representation', blank=True)

    class Meta:
        abstract = True