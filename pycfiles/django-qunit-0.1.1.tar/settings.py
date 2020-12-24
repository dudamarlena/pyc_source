# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/csoyland/src/django-qunit/example/settings.py
# Compiled at: 2010-04-01 01:33:43
import os
BASE_PATH = os.path.dirname(__file__)
QUNIT_TEST_DIRECTORY = os.path.join(BASE_PATH, 'qunit_tests')
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'example.urls'
INSTALLED_APPS = ('django_qunit', )