# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/signals.py
# Compiled at: 2018-07-11 18:15:31
"""
South-specific signals
"""
from django.dispatch import Signal
from django.conf import settings
pre_migrate = Signal(providing_args=['app', 'verbosity', 'interactive', 'db'])
post_migrate = Signal(providing_args=['app', 'verbosity', 'interactive', 'db'])
ran_migration = Signal(providing_args=['app', 'migration', 'method', 'verbosity', 'interactive', 'db'])