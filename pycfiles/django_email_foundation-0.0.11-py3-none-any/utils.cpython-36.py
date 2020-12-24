# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/utils.py
# Compiled at: 2019-03-18 03:08:32
# Size of source mod 2**32: 486 bytes
import os

def get_relative_from_manage_path(path: str) -> str:
    """
    In some cases we could have the manage.py inside the distinct folder where are gulpfile. It's could
    cause problems. This method return the relative path from the manage.py script.
    :return:
    """
    current_split = os.getcwd().split('/')
    path_split = path.split('/')
    response = [part for part in path_split if part not in current_split]
    response = '/'.join(response)
    return response