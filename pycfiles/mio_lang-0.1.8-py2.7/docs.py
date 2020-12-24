# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabfile/docs.py
# Compiled at: 2013-12-10 05:49:08
"""Documentation Tasks"""
from fabric.api import lcd, local, task
from .utils import pip, requires
PACKAGE = 'mio'

@task()
@requires('make', 'sphinx-apidoc')
def clean():
    """Delete Generated Documentation"""
    with lcd('docs'):
        local('make clean')


@task(default=True)
@requires('make')
def build(**options):
    """Build the Documentation"""
    pip(requirements='docs/requirements.txt')
    if PACKAGE is not None:
        local(('sphinx-apidoc -f -T -o docs/source/api {0:s}').format(PACKAGE))
    with lcd('docs'):
        local('make html')
    return


@task()
@requires('open')
def view(**options):
    """View the Documentation"""
    with lcd('docs'):
        local('open build/html/index.html')