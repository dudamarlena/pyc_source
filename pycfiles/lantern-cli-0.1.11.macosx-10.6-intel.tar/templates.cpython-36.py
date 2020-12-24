# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/Documents/coding/lantern/lantern-cli/.virtualenv/lib/python3.6/site-packages/lantern_cli/templates.py
# Compiled at: 2019-05-22 17:38:48
# Size of source mod 2**32: 183 bytes
import click
from cookiecutter.main import cookiecutter

def startapp(template):
    """
      Create a new project based on template coockiecutter
    """
    cookiecutter(template)