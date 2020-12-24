# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pielgrzym/work/imaging/git/example_project/imaging/models.py
# Compiled at: 2012-06-07 16:17:50
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
try:
    from imagekit.models import ImageSpecField
    from imagekit.processors import ResizeToFill
except ImportError:
    raise ImportError('Django Imaging needs imagekit >1.0 to work.             Please install imagekit: pip install django-imagekit')

DEFAULT_IMAGING_SETTINGS = {'image_dir': 'imaging_photos'}
try:
    IMAGING_SETTINGS = settings.IMAGING_SETTINGS
except:
    IMAGING_SETTINGS = DEFAULT_IMAGING_SETTINGS

class Image(models.Model):
    name = models.CharField(max_length=200)
    alt = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to=IMAGING_SETTINGS['image_dir'])
    imaging_thumbnail = ImageSpecField([
     ResizeToFill(200, 200)], image_field='image', format='JPEG', options={'quality': 90})
    ordering = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('ordering', 'name')
        permissions = (
         ('imaging_upload_images', 'Can upload using AJAX'),
         ('imaging_delete_images', 'Can delete using AJAX'))

    def __unicode__(self):
        return self.name