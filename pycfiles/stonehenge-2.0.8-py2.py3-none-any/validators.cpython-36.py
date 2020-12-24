# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rtownley/Projects/stonehenge/stonehenge/validators.py
# Compiled at: 2018-08-31 14:07:54
# Size of source mod 2**32: 540 bytes
import os
from stonehenge.utils import get_user_project_from_filepath
from stonehenge.utils import PROJECT_DIR

def validate_config_file():
    filepath = os.path.join(PROJECT_DIR, 'stonehenge.py')
    if not os.path.isfile(filepath):
        raise FileNotFoundError('File not found at {0}'.format(filepath))
    project = get_user_project_from_filepath(filepath)
    errors = []
    if errors:
        raise Exception(str(errors))
    return project