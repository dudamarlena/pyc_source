# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/urlresolvers.py
# Compiled at: 2019-02-14 00:35:17
import warnings
from django.urls import *
from django.utils.deprecation import RemovedInDjango20Warning
warnings.warn('Importing from django.core.urlresolvers is deprecated in favor of django.urls.', RemovedInDjango20Warning, stacklevel=2)