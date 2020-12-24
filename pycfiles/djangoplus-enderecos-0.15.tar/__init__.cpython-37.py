# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/enderecos/migrations/__init__.py
# Compiled at: 2018-10-05 12:52:35
# Size of source mod 2**32: 312 bytes
from django.core.management import call_command
import os

def load_fixture(apps, schema_editor):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, 'fixtures/initial_data.json.zip')
    call_command('loaddata', file_path)