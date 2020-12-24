# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wlfilebrowser/settings.py
# Compiled at: 2016-04-20 06:45:07
from __future__ import unicode_literals
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
try:
    import tinymce.settings
    DEFAULT_URL_TINYMCE = tinymce.settings.JS_BASE_URL + b'/'
    DEFAULT_PATH_TINYMCE = tinymce.settings.JS_ROOT + b'/'
except ImportError:
    DEFAULT_URL_TINYMCE = settings.STATIC_URL + b'wladmin/tinymce/jscripts/tiny_mce/'
    DEFAULT_PATH_TINYMCE = os.path.join(settings.MEDIA_ROOT, b'admin/tinymce/jscripts/tiny_mce/')

DEBUG = getattr(settings, b'FILEBROWSER_DEBUG', False)
MEDIA_ROOT = getattr(settings, b'FILEBROWSER_MEDIA_ROOT', settings.MEDIA_ROOT)
MEDIA_URL = getattr(settings, b'FILEBROWSER_MEDIA_URL', settings.MEDIA_URL)
DIRECTORY = getattr(settings, b'FILEBROWSER_DIRECTORY', b'uploads/')
URL_FILEBROWSER_MEDIA = getattr(settings, b'FILEBROWSER_URL_FILEBROWSER_MEDIA', b'%swlfilebrowser/' % settings.STATIC_URL)
PATH_FILEBROWSER_MEDIA = getattr(settings, b'FILEBROWSER_PATH_FILEBROWSER_MEDIA', os.path.join(settings.MEDIA_ROOT, b'wlfilebrowser/'))
URL_TINYMCE = getattr(settings, b'FILEBROWSER_URL_TINYMCE', DEFAULT_URL_TINYMCE)
PATH_TINYMCE = getattr(settings, b'FILEBROWSER_PATH_TINYMCE', DEFAULT_PATH_TINYMCE)
EXTENSIONS = getattr(settings, b'FILEBROWSER_EXTENSIONS', {b'Folder': [
             b''], 
   b'Image': [
            b'.jpg', b'.jpeg', b'.gif', b'.png', b'.tif', b'.tiff'], 
   b'Video': [
            b'.mov', b'.wmv', b'.mpeg', b'.mpg', b'.avi', b'.rm'], 
   b'Document': [
               b'.pdf', b'.doc', b'.rtf', b'.txt', b'.xls', b'.csv'], 
   b'Audio': [
            b'.mp3', b'.mp4', b'.wav', b'.aiff', b'.midi', b'.m4p'], 
   b'Code': [
           b'.html', b'.py', b'.js', b'.css']})
SELECT_FORMATS = getattr(settings, b'FILEBROWSER_SELECT_FORMATS', {b'File': [
           b'Folder', b'Document'], 
   b'Image': [
            b'Image'], 
   b'Media': [
            b'Video', b'Audio'], 
   b'Document': [
               b'Document'], 
   b'image': [
            b'Image'], 
   b'file': [
           b'Folder', b'Image', b'Document'], 
   b'media': [
            b'Video', b'Audio']})
VERSIONS_BASEDIR = getattr(settings, b'FILEBROWSER_VERSIONS_BASEDIR', b'')
VERSIONS = getattr(settings, b'FILEBROWSER_VERSIONS', {})
ADMIN_VERSIONS = getattr(settings, b'FILEBROWSER_ADMIN_VERSIONS', [
 b'thumbnail', b'small', b'medium', b'big'])
ADMIN_THUMBNAIL = getattr(settings, b'FILEBROWSER_ADMIN_THUMBNAIL', b'fb_thumb')
SAVE_FULL_URL = getattr(settings, b'FILEBROWSER_SAVE_FULL_URL', True)
STRICT_PIL = getattr(settings, b'FILEBROWSER_STRICT_PIL', False)
IMAGE_MAXBLOCK = getattr(settings, b'FILEBROWSER_IMAGE_MAXBLOCK', 1048576)
EXTENSION_LIST = []
for exts in list(EXTENSIONS.values()):
    EXTENSION_LIST += exts

EXCLUDE = getattr(settings, b'FILEBROWSER_EXCLUDE', (b'_(%(exts)s)_.*_q\\d{1,3}\\.(%(exts)s)' % {b'exts': (b'|').join(EXTENSION_LIST)},))
MAX_UPLOAD_SIZE = getattr(settings, b'FILEBROWSER_MAX_UPLOAD_SIZE', 10485760)
NORMALIZE_FILENAME = getattr(settings, b'FILEBROWSER_NORMALIZE_FILENAME', False)
CONVERT_FILENAME = getattr(settings, b'FILEBROWSER_CONVERT_FILENAME', True)
LIST_PER_PAGE = getattr(settings, b'FILEBROWSER_LIST_PER_PAGE', 50)
DEFAULT_SORTING_BY = getattr(settings, b'FILEBROWSER_DEFAULT_SORTING_BY', b'date')
DEFAULT_SORTING_ORDER = getattr(settings, b'FILEBROWSER_DEFAULT_SORTING_ORDER', b'desc')
FOLDER_REGEX = getattr(settings, b'FILEBROWSER_FOLDER_REGEX', b'^[\\sa-zA-Z0-9._/-]+$')
_(b'Folder')
_(b'Image')
_(b'Video')
_(b'Document')
_(b'Audio')
_(b'Code')