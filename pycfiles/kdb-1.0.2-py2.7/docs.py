# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fabfile/docs.py
# Compiled at: 2014-04-26 09:00:59
"""Documentation Tasks"""
from fabric.api import lcd, local, task
from .utils import pip, requires
PACKAGE = 'kdb'

@task()
def api():
    """Generate the API Documentation"""
    if PACKAGE is not None:
        pip(requirements='docs/requirements.txt')
        local(('sphinx-apidoc -f -e -T -o docs/source/api {0:s}').format(PACKAGE))
    return


@task()
@requires('make')
def clean():
    """Delete Generated Documentation"""
    with lcd('docs'):
        pip(requirements='requirements.txt')
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
        import webbrowser
        webbrowser.open_new_tab('build/html/index.html')