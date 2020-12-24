# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/tests/testsettings.py
# Compiled at: 2018-01-31 09:25:36
# Size of source mod 2**32: 908 bytes
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':':memory:'}}
SECRET_KEY = 'r4dy'
INSTALLED_APPS = [
 'menu_generator',
 'menu_generator.tests.test_apps.app1',
 'menu_generator.tests.test_apps.app2',
 'menu_generator.tests.test_apps.app3']
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = 'menu_generator.tests.urls'
NAV_MENU = [
 {'name':'Main', 
  'url':'/'},
 {'name':'Account', 
  'url':'/account', 
  'validators':[
   'menu_generator.validators.is_authenticated'], 
  'submenu':[
   {'name':'Profile', 
    'url':'/account/profile/'}]},
 {'name':'Create User', 
  'url':'users:create'},
 {'name':'Update User', 
  'url':{'viewname':'users:update', 
   'kwargs':{'pk': 1}}}]