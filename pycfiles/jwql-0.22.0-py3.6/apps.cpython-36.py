# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/apps/jwql/apps.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 609 bytes
"""Customizes the ``jwql`` app settings.

** CURRENTLY NOT IN USE **

Optionally defines an ``AppConfig`` class that can be called in
``INSTALLED_APPS`` in settings.py to configure the web app.

Authors
-------

    - Lauren Chambers

Use
---

    This module is called in ``settings.py`` as such:
    ::
        INSTALLED_APPS = ['apps.jwql.PlotsExampleConfig',
        ...
        ]

References
----------
    For more information please see:
        ``https://docs.djangoproject.com/en/2.0/ref/applications/``
"""
from django.apps import AppConfig

class PlotsExampleConfig(AppConfig):
    name = 'jwql'