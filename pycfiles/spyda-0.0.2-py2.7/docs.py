# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fabfile/docs.py
# Compiled at: 2013-11-18 22:33:39
"""Documentation Tasks"""
from fabric.api import lcd, local, task
from .utils import pip, requires, tobool

@task()
@requires('sphinx-apidoc')
def apidoc():
    """Generate API Documentation"""
    local('sphinx-apidoc -f -T -o docs/source/api spyda')


@task(default=True)
@requires('make', 'sphinx-build')
def build(**options):
    """Generate the Sphinx documentation

    The following options are recognized:

    - ``clean``
      Perform a clean of the docs build
    - ``view``
      Open a web browser to display the built documentation
    """
    clean = tobool(options.get('clean', False))
    view = tobool(options.get('view', False))
    with lcd('docs'):
        pip(requirements='requirements.txt')
        local('make clean html') if clean else local('make html')
        if view:
            local('open build/html/index.html')