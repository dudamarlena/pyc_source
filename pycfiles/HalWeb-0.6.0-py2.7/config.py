# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/config.py
# Compiled at: 2012-01-04 16:43:36
import os, sys
from os.path import join as pjoin
from os.path import abspath, dirname, basename
from imports import PROJ_LOC, INSTALL_LOC, TEMPLATES_LOC
sys.path.append(PROJ_LOC)
import conf.settings as proj_settings
APPENGINE_PATH = proj_settings.APPENGINE_PATH
sys.path.append(APPENGINE_PATH)
sys.path.append(pjoin(APPENGINE_PATH, 'lib'))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'django_1_2'))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'webob'))
sys.path.append(pjoin(APPENGINE_PATH, 'lib', 'yaml', 'lib'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'
import renderers
modelInheritsFrom = 'db.Model'
controllerInheritsFrom = 'hrh'
formInheritsFrom = 'ModelForm'
TEMPLATE_RENDERER = renderers.Django
TMPL_DIR = pjoin(TEMPLATES_LOC, 'WEBOBTemplates', '{{magicLevel}}')
MvcTemplateDirs = {'TMPLR_DIR': TMPL_DIR, 
   'FRMTMPL_DIR': pjoin(TMPL_DIR, 'FormTemplates'), 
   'OPRTMPL_DIR': pjoin(TMPL_DIR, 'OperationTemplates'), 
   'MBTMPL_DIR': pjoin(TMPL_DIR, 'ModuleBaseTemplates')}
MvcTemplateFiles = {'MTPath': pjoin(TMPL_DIR, 'ModelTemplate.txt'), 
   'MBTPath': pjoin(MvcTemplateDirs['MBTMPL_DIR'], 'ModelModule.txt'), 
   'FTPath': pjoin(TMPL_DIR, 'ModelFormTemplate.txt'), 
   'FBTPath': pjoin(MvcTemplateDirs['MBTMPL_DIR'], 'ModelFormModule.txt'), 
   'VTPath': pjoin(TMPL_DIR, 'ViewTemplate.txt'), 
   'CTPath': pjoin(TMPL_DIR, 'ControllerTemplate.txt'), 
   'CBTPath': pjoin(MvcTemplateDirs['MBTMPL_DIR'], 'ControllerModule.txt')}
mvcPaths = {'modelsPath': basename(proj_settings.MODELS_DIR), 
   'viewsPath': basename(proj_settings.VIEWS_DIR), 
   'formsPath': basename(proj_settings.FORM_MODELS_DIR), 
   'controlersPath': basename(proj_settings.CONTROLLERS_DIR)}
djangoVars = {'ob': '{{', 
   'cb': '}}', 
   'os': '{%', 
   'cs': '%}'}
sufixesDict = {'CONTROLLER_CLASS_SUFIX': proj_settings.CONTROLLER_CLASS_SUFIX, 
   'CONTROLLER_MODULE_SUFIX': proj_settings.CONTROLLER_MODULE_SUFIX, 
   'MODEL_CLASS_SUFIX': proj_settings.MODEL_CLASS_SUFIX, 
   'MODEL_MODULE_SUFIX': proj_settings.MODEL_MODULE_SUFIX, 
   'FORM_VIEW_SUFFIX': proj_settings.FORM_VIEW_SUFFIX, 
   'BLOCK_VIEW_SUFIX': proj_settings.BLOCK_VIEW_SUFIX, 
   'MODEL_FORM_CLASS_SUFIX': proj_settings.MODEL_FORM_CLASS_SUFIX, 
   'MODEL_FORM_MODULE_SUFIX': proj_settings.MODEL_FORM_MODULE_SUFIX}
types = {'txt': 'db.TextProperty', 
   'str': 'db.StringProperty', 
   'blob': 'db.BlobProperty', 
   'bln': 'db.BooleanProperty', 
   'dtm': 'db.DateTimeProperty', 
   'date': 'db.DateProperty', 
   'time': 'db.TimeProperty', 
   'email': 'db.EmailProperty', 
   'int': 'db.IntegerProperty', 
   'float': 'db.FloatProperty', 
   'ref': 'db.ReferenceProperty', 
   'selfref': 'db.SelfReferenceProperty', 
   'list': 'db.ListProperty', 
   'strlist': 'fb.StringListProperty', 
   'cat': 'db.CategoryProperty', 
   'link': 'db.LinkProperty', 
   'im': 'db.IMProperty', 
   'geopt': 'db.GeoPtProperty', 
   'phone': 'db.PhoneNumberProperty', 
   'postal': 'db.PostalAddressProperty', 
   'rating': 'db.RatingProperty', 
   'user': 'db.UserProperty'}