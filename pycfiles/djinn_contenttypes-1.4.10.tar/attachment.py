# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/models/attachment.py
# Compiled at: 2015-11-24 06:20:01
import os
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from photologue.models import ImageModel
import magic

class Attachment(models.Model):
    title = models.CharField(_('title'), max_length=100, null=True, blank=True)

    @property
    def permission_authority(self):
        return

    @property
    def _file(self):
        raise NotImplementedError

    @property
    def absolute_url(self):
        return os.path.join(settings.MEDIA_URL, self._file.name)

    @property
    def absolute_path(self):
        return self._file.path

    def mimetype(self, lexical=False):
        if lexical:
            magic.from_file(self._file.name)
        else:
            magic.from_file(self._file.name, mime=True)

    def __unicode__(self):
        if self.title:
            return '%s' % self.title
        return '%s' % self._file.name

    class Meta:
        abstract = True
        app_label = 'djinn_contenttypes'


class ImgAttachment(Attachment, ImageModel):

    @property
    def _file(self):
        return self.image

    class Meta:
        app_label = 'djinn_contenttypes'


class FileAttachment(Attachment):
    ffile = models.FileField(upload_to='files')

    @property
    def _file(self):
        return self.ffile