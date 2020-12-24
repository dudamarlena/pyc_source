# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tasks/build.py
# Compiled at: 2018-12-16 20:27:40
# Size of source mod 2**32: 524 bytes
from invoke import task

@task
def save_deps(ctx):
    """ Generate a new requirements.txt file """
    ctx.run('pip freeze > requirements.txt')


@task
def install_deps(ctx):
    """ Install the requirements.txt file """
    ctx.run('pip install -r requirements.txt')


@task
def install_dev(ctx):
    """ Install the current branch of ipecac """
    ctx.run('python setup.py develop')


@task
def install(ctx):
    """ Install ipecac for regular usage """
    ctx.run('inv build.install-deps && python setup.py install')