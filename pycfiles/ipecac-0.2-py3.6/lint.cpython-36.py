# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tasks/lint.py
# Compiled at: 2018-12-16 17:32:26
# Size of source mod 2**32: 161 bytes
from invoke import task

@task
def flake8(ctx):
    """ Run the flake8 linter """
    ctx.run('python -m flake8 --exclude=docs,env,venv,ipecac.egg-info,.idea')