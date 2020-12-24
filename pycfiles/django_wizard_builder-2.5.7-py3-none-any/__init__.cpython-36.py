# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lynn/apps/django-wizard-builder/wizard_builder/__init__.py
# Compiled at: 2017-11-23 06:04:05
# Size of source mod 2**32: 248 bytes
import os
__version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.txt')
with open(__version_path, 'r') as (f):
    __version__ = f.read()
default_app_config = 'wizard_builder.apps.WizardBuilderConfig'