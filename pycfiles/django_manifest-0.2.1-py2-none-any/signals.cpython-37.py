# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/dev_reactor/django-reactor/manifest/signals.py
# Compiled at: 2019-10-15 15:31:29
# Size of source mod 2**32: 321 bytes
""" Manifest Signals
"""
from django.dispatch import Signal
REGISTRATION_COMPLETE = Signal(providing_args=['user', 'request'])
ACTIVATION_COMPLETE = Signal(providing_args=['user'])
CINFIRMATION_COMPLETE = Signal(providing_args=['user'])
PASSWORD_RESET_COMPLETE = Signal(providing_args=['user'])