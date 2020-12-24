# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/staticfiles/testing.py
# Compiled at: 2019-02-14 00:35:17
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.test import LiveServerTestCase

class StaticLiveServerTestCase(LiveServerTestCase):
    """
    Extends django.test.LiveServerTestCase to transparently overlay at test
    execution-time the assets provided by the staticfiles app finders. This
    means you don't need to run collectstatic before or as a part of your tests
    setup.
    """
    static_handler = StaticFilesHandler