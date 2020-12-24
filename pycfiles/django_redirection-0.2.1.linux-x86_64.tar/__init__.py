# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/django_redirection/__init__.py
# Compiled at: 2014-08-08 20:28:25
""" django_redirector  X-Accel-Redirect / X-Sendfile  application for django.

nginx and Apache has a backend redirection function named X-Accel-Rediect and X-Sendfile.
django_redirector auth user and redirect to other backends.
"""
from urls import generate_url