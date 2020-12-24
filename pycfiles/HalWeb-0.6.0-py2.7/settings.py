# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/conf/settings.py
# Compiled at: 2012-01-05 19:45:37
import os
from os.path import join
RUN = 'appengine'
DEBUG = True
TEMPLATE_DEBUG = True
DEFAULT_CHARSET = 'UTF-8'
from lib.halicea import dummyControllerMethods as dcm
DEFAULT_OPERATIONS = {'default': {'method': dcm.index, 'view': False}, 'index': {'method': dcm.index, 'view': True}, 'view': {'method': dcm.view, 'view': True}, 'edit': {'method': dcm.edit, 'view': True}, 'new': {'method': dcm.edit, 'view': False}, 'save': {'method': dcm.save, 'view': False}, 'delete': {'method': dcm.delete, 'view': False}}
PLUGINS = [
 ('Links', 'controllers.cmsControllers.CMSLinksController'),
 ('Contents', 'controllers.cmsControllers.CMSContentController'),
 ('Menus', 'controllers.cmsControllers.MenuController'),
 ('AjaxForm', 'lib.halicea.plugins.AjaxForm'),
 ('Authentication', 'lib.halicea.plugins.AuthenticationMixin')]
APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
if os.name == 'nt':
    APPENGINE_PATH = '/home/costa/DevApps/google_appengine'
PROJ_LOC = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = join(PROJ_LOC, 'models')
VIEWS_DIR = join(PROJ_LOC, 'views')
VIEWS_RELATIVE_DIR = 'views'
FORM_MODELS_DIR = join(PROJ_LOC, 'forms')
CONTROLLERS_DIR = join(PROJ_LOC, 'controllers')
BASE_VIEWS_DIR = join(VIEWS_DIR, 'bases')
BLOCK_VIEWS_DIR = join(VIEWS_DIR, 'blocks')
PAGE_VIEWS_DIR = join(VIEWS_DIR, 'pages')
FORM_VIEWS_DIR = join(VIEWS_DIR, 'forms')
STATIC_DATA_DIR = join(PROJ_LOC, 'static_data')
JSCRIPTS_DIR = join(STATIC_DATA_DIR, 'jscripts')
IMAGES_DIR = join(STATIC_DATA_DIR, 'images')
STYLES_DIR = join(STATIC_DATA_DIR, 'styles')
HANDLER_MAP_FILE = join(PROJ_LOC, 'handlerMap.py')
TESTS_DIR = join(PROJ_LOC, 'tests')
DOCS_DIR = join(PROJ_LOC, 'docs')
APPS_DIR = join(PROJ_LOC, 'apps')
LIB_DIR = join(PROJ_LOC, 'lib')
REPOS_DIR = join(PROJ_LOC, 'repositories')
MODEL_MODULE_SUFIX = 'Models'
MODEL_FORM_MODULE_SUFIX = 'Forms'
CONTROLLER_MODULE_SUFIX = 'Controllers'
MODEL_CLASS_SUFIX = ''
MODEL_FORM_CLASS_SUFIX = 'Form'
CONTROLLER_CLASS_SUFIX = 'Controller'
BASE_VIEW_SUFIX = ''
PAGE_VIEW_SUFFIX = ''
FORM_VIEW_SUFFIX = 'Form'
BLOCK_VIEW_SUFIX = ''
BASE_MOBILE_VIEW_EXTENSION = '_mobile'
CONTROLLER_EXTENSTION = '.py'
MODEL_EXTENSTION = '.py'
MODEL_FORM_EXTENSTION = '.py'
VIEW_EXTENSTION = '.html'
MagicLevel = 3
TEMPLATE_DIRS = (
 VIEWS_DIR,)
ROOT_URLCONF = 'handlerMap'
TEMPLATE_LOADERS = ('lib.halicea.HalTemplateLoader.HalLoader', 'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader')
USE_I18N = True
COOKIE_KEY = '2zÆœ;¾±þ”¡j:ÁõkçŸÐ÷8{»Ën¿A—jÎžQAQqõ"bøó÷*%†™ù¹b¦$vš¡¾4ÇŸ^ñ5¦'