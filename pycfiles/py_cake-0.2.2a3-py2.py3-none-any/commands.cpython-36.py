# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\pycake\src\pycake\commands.py
# Compiled at: 2018-11-08 01:59:35
# Size of source mod 2**32: 469 bytes
import os
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(CUR_DIR, 'pycake_template')

def prepare():
    """
    Prepare all the stuff for start a new Python project.

    This function use cookiecutter(https://github.com/audreyr/cookiecutter)
    The template dir is ./project_template

    """
    from cookiecutter.main import cookiecutter
    return cookiecutter(TEMPLATE_PATH)