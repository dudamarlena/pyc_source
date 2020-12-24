# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/default_settings.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 5177 bytes
from huey.contrib.sqlitedb import SqliteHuey
import sys
from os import path
LANGUAGES = [
 ('en', 'English')]
CMS_TEMPLATES = [
 ('cms/admin_home.html', 'Administrative Function base template'),
 ('cms/home.html', 'Base Template, one column'),
 ('cms/frontpage.html', 'Front page template'),
 ('cms/twocolumn_leftsidebar.html', 'Two columns, sidebar at left'),
 ('cms/twocolumn_rightsidebar.html', 'Two columns, sidebar at right')]
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend')
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = ('easy_thumbnails.processors.colorspace', 'easy_thumbnails.processors.autocrop',
                        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
                        'easy_thumbnails.processors.filters')
FILER_ENABLE_PERMISSIONS = True
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_SETTINGS = {'language': '', 
 'toolbar_CMS': [
                 {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']},
                 {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
                 {'name': 'paragraph', 
                  'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                            'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
                 {'name': 'styles', 'items': ['Format']},
                 '/',
                 {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                 {'name': 'insert', 'items': ['FilerImage', 'Table', 'HorizontalRule', 'Smiley', 'Iframe']},
                 {'name': 'tools', 'items': ['Maximize', 'ShowBlocks', 'Source']}], 
 
 'toolbar_HTMLField': [
                       {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', '-', 'RemoveFormat']},
                       {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo']},
                       {'name': 'paragraph', 
                        'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                                  'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
                       {'name': 'styles', 'items': ['Format']},
                       '/',
                       {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                       {'name': 'insert', 'items': ['FilerImage', 'Table', 'HorizontalRule', 'Smiley', 'Iframe']},
                       {'name': 'tools', 'items': ['Maximize', 'ShowBlocks', 'Source']}], 
 
 'skin': 'moono-lisa', 
 'extraPlugins': ','.join([
                  'filerimage']), 
 
 'removePlugins': 'image'}
TEXT_ADDITIONAL_TAGS = ('iframe', )
TEXT_ADDITIONAL_ATTRIBUTES = ('scrolling', 'allowfullscreen', 'frameborder')
HUEY = SqliteHuey('danceschool', filename=path.join(path.dirname(path.abspath(getattr(sys.modules['__main__'], '__file__', path.dirname(__file__)))), 'huey.sqlite3'))
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = True
DJANGOCMS_FORMS_PLUGIN_MODULE = 'Forms'
DJANGOCMS_FORMS_TEMPLATES = (('djangocms_forms/form_template/default.html', 'Default'),
                             ('forms/djangocms_forms_crispy.html', 'Crispy Form (recommended)'))