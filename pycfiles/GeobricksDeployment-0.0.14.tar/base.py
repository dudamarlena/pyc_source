# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../geobricks_deployment/base.py
# Compiled at: 2015-01-13 10:19:21
import subprocess, os, glob
from shutil import rmtree, copy
library_path = __file__
virtualenv_path = 'env'
resources_path = 'resources'
print library_path

def install_virtualenv_and_package(package_file, install_path='', virtualenv=True):
    print package_file
    print install_path
    install_path += virtualenv_path
    if not check_virtualenv(install_path):
        install_virtualenv(install_path)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), package_file)) as (f):
        libraries = f.read().splitlines()
        for library in libraries:
            install_pip(library)

    copy_resources_to_env()


def upgrade_packages(package_file, install_path='', virtualenv=True):
    with open(package_file) as (f):
        libraries = f.readlines()
        for library in libraries:
            install_pip(library, install_path, virtualenv, True)


def check_virtualenv(path):
    if os.path.isdir(path):
        return True
    else:
        return False


def install_virtualenv(install_path=''):
    output = subprocess.check_call(['virtualenv', install_path])
    print output


def install_pip(name, install_path='', virtualenv=True, upgrade=False):
    cmd = os.path.join(install_path, 'env', 'bin') if virtualenv else install_path
    cmd = os.path.join(cmd, 'pip')
    name = name.split(' ')
    cmd = [cmd, 'install']
    for n in name:
        cmd.append(n)

    if upgrade:
        cmd.append('--upgrade')
    print cmd
    output = subprocess.check_call(cmd)
    print output


def copy_resources_to_env():
    src_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), resources_path, '*')
    files = glob.glob(src_path)
    for f in files:
        copy(f, '.')