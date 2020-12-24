# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cookiecutter/{{cookiecutter.project_name}}/pavement.py
# Compiled at: 2017-01-01 18:58:14
# Size of source mod 2**32: 3604 bytes
import os, re
from paver.easy import *
import paver.path as path

def _setup(args, capture=False):
    return sh(('python setup.py %s 2> /dev/null' % args), capture=capture)


NAME, VERSION, AUTHOR, *_ = _setup('--name --version --author', capture=True).split('\n')
FULL_NAME = '-'.join([NAME, VERSION])
TESTS_DIR = '{{ cookiecutter.src_dir }}/tests'
SRC_DIRS = ['{{ cookiecutter.src_dir }}/{{ cookiecutter.py_module }}',
 TESTS_DIR]
options(test=Bunch(pdb=False,
  coverage=False),
  cookiecutter=Bunch(template='https://bitbucket.org/nicfit/cookiecutter-pypackage'))

@task
def lint():
    sh('flake8 {}'.format(' '.join(SRC_DIRS)))


@task
@cmdopts([('pdb', '', 'Run with all output and launch pdb on errors and failures'),
 ('coverage', '', 'Run tests with coverage analysis')])
def test(options):
    if options.test and options.test.pdb:
        debug_opts = '--pdb --pdb-failures -s'
    else:
        debug_opts = ''
    coverage_build_d = 'build/tests/coverage'
    if options.test and options.test.coverage:
        coverage_opts = '--cover-erase --with-coverage --cover-tests --cover-inclusive --cover-package={{ cookiecutter.project_slug }} --cover-branches --cover-html --cover-html-dir=%s %s' % (
         coverage_build_d, TESTS_DIR)
    else:
        coverage_opts = ''
    sh('nosetests --verbosity=1 --detailed-errors %(debug_opts)s %(coverage_opts)s' % {'debug_opts':debug_opts, 
     'coverage_opts':coverage_opts})
    if coverage_opts:
        report = '%s/%s/index.html' % (os.getcwd(), coverage_build_d)
        print('Coverage Report: file://%s' % report)
        _browser(report)


@task
def test_all():
    """Run tests for all Python versions."""
    sh('tox')


@task
def clean_build():
    sh('rm -fr build/')
    sh('rm -fr dist/')
    sh('rm -fr .eggs/')
    sh("find . -name '*.egg-info' -exec rm -fr {} +")
    sh("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc():
    sh("find . -name '*.pyc' -exec rm -f {} +")
    sh("find . -name '*.pyo' -exec rm -f {} +")
    sh("find . -name '*~' -exec rm -f {} +")
    sh("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_test():
    sh('rm -fr .tox/')
    sh('rm -f .coverage')
    sh('rm -fr htmlcov/')


@task
def clean_patch():
    sh("find . -name '*.rej' -exec rm -f '{}' \\;")
    sh("find . -name '*.orig' -exec rm -f '{}' \\;")


@task
@needs('clean_build', 'clean_pyc', 'clean_test', 'clean_patch')
def clean():
    sh('rm -fr htmlcov/')
    sh('rm -rf tags')


@task
@needs('clean')
def dist():
    _setup('sdist')
    _setup('bdist_wheel')
    sh('ls -l dist')


def _browser(file_path):
    import webbrowser
    try:
        from urllib import pathname2url
    except:
        from urllib.request import pathname2url
    else:
        webbrowser.open('file://' + pathname2url(os.path.abspath(file_path)))


@task
@cmdopts([
 ('template=', '', ' Repo URL or file path containing Cookiecutter template')])
def cookiecutter(options):
    from cookiecutter.main import cookiecutter
    cookiecutter((options.cookiecutter.template), extra_context={
     {
      cookiecutter | pprint}},
      output_dir='..',
      no_input=True,
      overwrite_if_exists=True)