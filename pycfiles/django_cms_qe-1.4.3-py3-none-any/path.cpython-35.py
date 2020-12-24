# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/path.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 523 bytes
"""
Paths settings for Django app.
"""
STATICFILES_STORAGE = 'cms_qe.staticfiles.ManifestStaticFilesStorage'
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'