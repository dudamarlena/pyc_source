# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/app.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2923 bytes
"""
Base settings for Django app.
"""
SITE_ID = 1
INTERNAL_IPS = [
 '127.0.0.1']
META_USE_SITES = True
META_SITE_PROTOCOL = 'https'
INSTALLED_APPS = [
 'cms_qe',
 'cms_qe_auth',
 'cms_qe_breadcrumb',
 'cms_qe_i18n',
 'cms_qe_menu',
 'cms_qe_newsletter',
 'cms_qe_table',
 'cms_qe_video',
 'cms_qe_analytical',
 'djangocms_admin_style',
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.sites',
 'django.contrib.sitemaps',
 'cms',
 'menus',
 'treebeard',
 'sekizai',
 'djangocms_text_ckeditor',
 'djangocms_googlemap',
 'aldryn_bootstrap3',
 'aldryn_boilerplates',
 'aldryn_forms',
 'aldryn_forms.contrib.email_notifications',
 'captcha',
 'djangocms_inline_comment',
 'filer',
 'easy_thumbnails',
 'mptt',
 'cmsplugin_filer_file',
 'cmsplugin_filer_folder',
 'cmsplugin_filer_link',
 'cmsplugin_filer_image',
 'axes',
 'bootstrapform',
 'constance',
 'constance.backends.database',
 'import_export',
 'mailqueue']
MIDDLEWARE = [
 'django.middleware.cache.UpdateCacheMiddleware',
 'cms.middleware.utils.ApphookReloadMiddleware',
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.locale.LocaleMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
 'django.middleware.common.BrokenLinkEmailsMiddleware',
 'cms.middleware.user.CurrentUserMiddleware',
 'cms.middleware.page.CurrentPageMiddleware',
 'cms.middleware.toolbar.ToolbarMiddleware',
 'cms.middleware.language.LanguageCookieMiddleware',
 'csp.middleware.CSPMiddleware',
 'django.middleware.cache.FetchFromCacheMiddleware']