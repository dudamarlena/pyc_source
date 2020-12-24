# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/models.py
# Compiled at: 2016-04-11 03:12:30
"""Models for the ``contact_form`` app."""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields

@python_2_unicode_compatible
class ContactFormCategory(TranslatableModel):
    """
    The category of the users contact request.

    Is created as translatable master data by the admin.
    For translatable fields check the ``ContactFormCategoryTranslation`` model.

    """
    slug = models.SlugField(max_length=256, verbose_name=_('Slug'))
    translations = TranslatedFields(name=models.CharField(max_length=256))

    def __str__(self):
        return self.lazy_translation_getter('name', 'Untranslated')