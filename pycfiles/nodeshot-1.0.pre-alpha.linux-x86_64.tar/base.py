# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/hardware/models/base.py
# Compiled at: 2013-05-18 16:02:05
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class ImageMixin(models.Model):
    """
    Abstract model with few useful methods to display an image
    """
    image_width = 80

    class Meta:
        abstract = True

    def __unicode__(self, *args, **kwargs):
        return self.name

    def image_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)

    def image_img_tag(self):
        if self.image != '':
            return '<img src="%s" alt="" style="width:%spx" />' % (self.image_url(), self.image_width)
        else:
            return _('No image available')

    image_img_tag.allow_tags = True