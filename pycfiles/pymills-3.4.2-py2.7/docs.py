# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabfile/docs.py
# Compiled at: 2013-11-29 23:01:51
"""Documentation Tasks"""
from fabric.api import lcd, local, task
from .utils import pip, requires
PACKAGE = 'src/ccav'

@task()
@requires('sphinx-apidoc')
def api():
    """Generate the API Documentation"""
    if PACKAGE is not None:
        local(('sphinx-apidoc -f -T -o docs/source/api {0:s}').format(PACKAGE))
    return


@task()
@requires('make')
def clean():
    """Delete Generated Documentation"""
    with lcd('docs'):
        local('make clean')


@task(default=True)
@requires('make')
def build(**options):
    """Build the Documentation"""
    pip(requirements='docs/requirements.txt')
    with lcd('docs'):
        local('make html')


@task()
@requires('open')
def view(**options):
    """View the Documentation"""
    with lcd('docs'):
        local('open build/html/index.html')