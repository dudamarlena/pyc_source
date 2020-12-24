# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/mezzanine_settings.py
# Compiled at: 2014-06-27 19:07:27
MEZZANINE_AUTHENTICATION_BACKENDS = [
 'mezzanine.core.auth_backends.MezzanineBackend']
MEZZANINE_INSTALLED_APPS = [
 'mezzanine.boot',
 'mezzanine.conf',
 'mezzanine.core',
 'mezzanine.generic',
 'mezzanine.blog',
 'mezzanine.forms',
 'mezzanine.pages',
 'mezzanine.galleries',
 'mezzanine.twitter',
 'mezzanine.template']
MEZZANINE_TEMPLATE_CONTEXT_PROCESSORS = [
 'mezzanine.conf.context_processors.settings',
 'mezzanine.pages.context_processors.page']
MEZZANINE_MIDDLEWARE_CLASSES_PREPEND = [
 'mezzanine.core.middleware.UpdateCacheMiddleware']
MEZZANINE_MIDDLEWARE_CLASSES_APPEND = [
 'mezzanine.core.request.CurrentRequestMiddleware',
 'mezzanine.core.middleware.TemplateForDeviceMiddleware',
 'mezzanine.core.middleware.TemplateForHostMiddleware',
 'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
 'mezzanine.core.middleware.SitePermissionMiddleware',
 'mezzanine.pages.middleware.PageMiddleware',
 'mezzanine.core.middleware.FetchFromCacheMiddleware']
PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'
TESTING = False
MEZZANINE_TEMPLATE_DIRS = [
 'galleries/templates',
 'generic/templates',
 'accounts/templates',
 'mobile/templates',
 'blog/templates',
 'core/templates',
 'pages/templates',
 'conf/templates',
 'forms/templates',
 'twitter/templates']
NEVERCACHE_KEY = '57bd470d-598c-4d72-b8bb-a7be02f534fca1c6b3d0-a814-4514-b3a9-d7fad4a3d8b17041ba11-aaf7-4b1f-b6dd-b222b7191382'