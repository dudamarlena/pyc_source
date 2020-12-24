# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/cms.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1477 bytes
"""
Base settings for Django CMS and all plugins for Django CMS.
"""
from cms.constants import X_FRAME_OPTIONS_SAMEORIGIN
import django.utils.translation as _
CMS_TEMPLATES = [
 ('cms_qe/home.html', 'Home page template')]
CMS_TOOLBAR_ANONYMOUS_ON = False
CMS_PERMISSION = True
CMS_DEFAULT_X_FRAME_OPTIONS = X_FRAME_OPTIONS_SAMEORIGIN
CMS_PAGE_CACHE = True
CMS_PLACEHOLDER_CACHE = True
CMS_PLUGIN_CACHE = True
FILER_ENABLE_PERMISSIONS = True
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = ('easy_thumbnails.processors.colorspace', 'easy_thumbnails.processors.autocrop',
                        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
                        'easy_thumbnails.processors.filters')
TEXT_ADDITIONAL_TAGS = ('iframe', )
CMSPLUGIN_FILER_FOLDER_STYLE_CHOICES = (
 (
  'list', _('List')),
 (
  'slideshow', _('Slideshow')),
 (
  'gallery', _('Gallery')))
CMSPLUGIN_FILER_IMAGE_DEFAULT_STYLE = 'main'