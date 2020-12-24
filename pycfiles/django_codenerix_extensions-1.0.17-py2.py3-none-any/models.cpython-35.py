# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_extensions/files/models.py
# Compiled at: 2017-04-28 08:28:21
# Size of source mod 2**32: 2198 bytes
from django.utils.translation import ugettext_lazy as _
from django.db import models
from codenerix.lib.helpers import upload_path
from codenerix.fields import FileAngularField, ImageAngularField

class GenDocumentFile(models.Model):
    doc_path = FileAngularField(_('Doc Path'), upload_to=upload_path, max_length=200, blank=False, null=False)
    name_file = models.CharField(_('Name'), max_length=254, blank=False, null=False)

    class Meta:
        abstract = True


class GenDocumentFileNull(models.Model):
    doc_path = FileAngularField(_('Doc Path'), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file = models.CharField(_('Name'), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True


class GenImageFile(models.Model):
    image = ImageAngularField(_('Image'), upload_to=upload_path, max_length=200, blank=False, null=False)
    name_file = models.CharField(_('Name'), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True


class GenImageFileNull(models.Model):
    image = ImageAngularField(_('Image'), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file = models.CharField(_('Name'), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True