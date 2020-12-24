# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/frapwings/skels/tests/test_package.py
# Compiled at: 2010-10-11 10:32:40
import os, sys, shutil
from os import chdir
from nose.tools import *
from paste.script.command import run
cur_dir = os.path.abspath(os.path.dirname(__file__))
exe_dir = os.path.abspath(os.path.dirname(sys.executable))
tmp_dir = os.getenv('TEMP', '/tmp')
package_name = 'package'

def paster(args):
    try:
        run(args.split(' '))
    except SystemExit:
        pass


def rmdir(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)


def ls(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        filenames = os.listdir(dirname)
        for filename in sorted(filenames):
            print filename

    else:
        print 'No directory named %s' % dirname


def setup_func():
    package_dir = os.path.split(cur_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    chdir(tmp_dir)


def teardown_func():
    rmdir(tmp_dir, package_name)
    chdir(cur_dir)


def _diff_elements(elements1, elements2):
    return [ element for element in elements2 if element not in elements1 ]


@with_setup(setup_func, teardown_func)
def test_package():
    paster('create -t frapwings_package %s --no-interactive' % package_name)
    dir_path = os.path.join(tmp_dir, package_name)
    assert os.path.isdir(dir_path)
    elements = ('.gitignore', 'CHANGES.txt', 'LICENSE.txt', 'README.txt', 'MANIFEST.in',
                'frapwings', 'package.egg-info', 'setup.py')
    assert len(_diff_elements(elements, os.listdir(dir_path))) == 0
    dir_path = os.path.join(dir_path, 'frapwings')
    assert os.path.isdir(dir_path)
    elements = ('__init__.py', '__init__.pyc', 'package')
    assert len(_diff_elements(elements, os.listdir(dir_path))) == 0
    dir_path = os.path.join(dir_path, 'package')
    assert os.path.isdir(dir_path)
    elements = '__init__.py'
    assert len(_diff_elements(elements, os.listdir(dir_path))) == 0