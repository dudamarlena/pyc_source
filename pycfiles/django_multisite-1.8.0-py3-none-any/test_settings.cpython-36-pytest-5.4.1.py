# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/test_settings.py
# Compiled at: 2019-05-02 13:24:49
# Size of source mod 2**32: 729 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, django
from multisite import SiteID
SECRET_KEY = 'iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':'test'}}
INSTALLED_APPS = [
 'django.contrib.sites',
 'multisite']
SITE_ID = SiteID(default=1)
MIDDLEWARE = [
 'multisite.middleware.DynamicSiteMiddleware']
if django.VERSION < (1, 10, 0):
    MIDDLEWARE_CLASSES = list(MIDDLEWARE)
    del MIDDLEWARE
TEST_RUNNER = 'django.test.runner.DiscoverRunner'