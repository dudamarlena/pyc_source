# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/settings.py
# Compiled at: 2014-11-22 02:35:13
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
try:
    import tinymce.settings
    DEFAULT_URL_TINYMCE = tinymce.settings.JS_BASE_URL + '/'
    DEFAULT_PATH_TINYMCE = tinymce.settings.JS_ROOT + '/'
except ImportError:
    import posixpath
    DEFAULT_URL_TINYMCE = getattr(settings, 'ADMIN_MEDIA_PREFIX', posixpath.join(settings.STATIC_URL, 'admin/')) + 'tinymce/jscripts/tiny_mce/'
    DEFAULT_PATH_TINYMCE = os.path.join(settings.MEDIA_ROOT, 'admin/tinymce/jscripts/tiny_mce/')

DEBUG = getattr(settings, 'FILEBROWSER_DEBUG', False)
MEDIA_ROOT = getattr(settings, 'FILEBROWSER_MEDIA_ROOT', settings.MEDIA_ROOT)
MEDIA_URL = getattr(settings, 'FILEBROWSER_MEDIA_URL', settings.MEDIA_URL)
DIRECTORY = getattr(settings, 'FILEBROWSER_DIRECTORY', 'uploads/')
URL_FILEBROWSER_MEDIA = getattr(settings, 'FILEBROWSER_URL_FILEBROWSER_MEDIA', os.path.join(settings.STATIC_URL, 'filebrowser/'))
PATH_FILEBROWSER_MEDIA = getattr(settings, 'FILEBROWSER_PATH_FILEBROWSER_MEDIA', os.path.join(settings.STATIC_ROOT, 'filebrowser/'))
URL_TINYMCE = getattr(settings, 'FILEBROWSER_URL_TINYMCE', DEFAULT_URL_TINYMCE)
PATH_TINYMCE = getattr(settings, 'FILEBROWSER_PATH_TINYMCE', DEFAULT_PATH_TINYMCE)
EXTENSIONS = getattr(settings, 'FILEBROWSER_EXTENSIONS', {'Folder': [
            ''], 
   'Image': [
           '.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], 
   'Video': [
           '.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'], 
   'Document': [
              '.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'], 
   'Audio': [
           '.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'], 
   'Code': [
          '.html', '.py', '.js', '.css']})
SELECT_FORMATS = getattr(settings, 'FILEBROWSER_SELECT_FORMATS', {'File': [
          'Folder', 'Document'], 
   'Image': [
           'Image'], 
   'Media': [
           'Video', 'Sound'], 
   'Document': [
              'Document'], 
   'image': [
           'Image'], 
   'file': [
          'Folder', 'Image', 'Document'], 
   'media': [
           'Video', 'Sound']})
VERSIONS_BASEDIR = getattr(settings, 'FILEBROWSER_VERSIONS_BASEDIR', '')
VERSIONS = getattr(settings, 'FILEBROWSER_VERSIONS', {'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'}, 'thumbnail': {'verbose_name': 'Thumbnail (140px)', 'width': 140, 'height': '', 'opts': ''}, 'small': {'verbose_name': 'Small (300px)', 'width': 300, 'height': '', 'opts': ''}, 'medium': {'verbose_name': 'Medium (460px)', 'width': 460, 'height': '', 'opts': ''}, 'big': {'verbose_name': 'Big (620px)', 'width': 620, 'height': '', 'opts': ''}, 'cropped': {'verbose_name': 'Cropped (60x60px)', 'width': 60, 'height': 60, 'opts': 'crop'}, 'croppedthumbnail': {'verbose_name': 'Cropped Thumbnail (140x140px)', 'width': 140, 'height': 140, 'opts': 'crop'}})
ADMIN_VERSIONS = getattr(settings, 'FILEBROWSER_ADMIN_VERSIONS', ['thumbnail', 'small', 'medium', 'big'])
ADMIN_THUMBNAIL = getattr(settings, 'FILEBROWSER_ADMIN_THUMBNAIL', 'fb_thumb')
PREVIEW_VERSION = getattr(settings, 'FILEBROWSER_PREVIEW_VERSION', 'small')
SAVE_FULL_URL = getattr(settings, 'FILEBROWSER_SAVE_FULL_URL', True)
STRICT_PIL = getattr(settings, 'FILEBROWSER_STRICT_PIL', False)
IMAGE_MAXBLOCK = getattr(settings, 'FILEBROWSER_IMAGE_MAXBLOCK', 1048576)
EXTENSION_LIST = []
for exts in EXTENSIONS.values():
    EXTENSION_LIST += exts

EXCLUDE = getattr(settings, 'FILEBROWSER_EXCLUDE', ('_(%(exts)s)_.*_q\\d{1,3}\\.(%(exts)s)' % {'exts': ('|').join(EXTENSION_LIST)},))
MAX_UPLOAD_SIZE = getattr(settings, 'FILEBROWSER_MAX_UPLOAD_SIZE', 10485760)
CONVERT_FILENAME = getattr(settings, 'FILEBROWSER_CONVERT_FILENAME', True)
LIST_PER_PAGE = getattr(settings, 'FILEBROWSER_LIST_PER_PAGE', 50)
DEFAULT_SORTING_BY = getattr(settings, 'FILEBROWSER_DEFAULT_SORTING_BY', 'date')
DEFAULT_SORTING_ORDER = getattr(settings, 'FILEBROWSER_DEFAULT_SORTING_ORDER', 'desc')
FOLDER_REGEX = getattr(settings, 'FILEBROWSER_FOLDER_REGEX', '^[ \\w-][ \\w.-]*$')
_('Folder')
_('Image')
_('Video')
_('Document')
_('Audio')
_('Code')