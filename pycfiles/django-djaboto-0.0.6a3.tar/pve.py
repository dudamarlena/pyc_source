# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-djaboto/djaboto/pve.py
# Compiled at: 2013-02-28 22:51:18
from subprocess import check_call
import os
from shutil import rmtree

def install_pve(pve_dir, leave_existing=True):
    """
    Install a fresh Python Virtual Environment
    """
    if os.path.isdir(pve_dir):
        if leave_existing:
            print '...leaving environment as is!'
        else:
            print '...removing %s and installing a fresh Python virtual environment' % pve_dir
            rmtree(pve_dir)
            check_call(['virtualenv', pve_dir])
    else:
        print '...installing Python virtual environment in %s ' % pve_dir
        check_call(['virtualenv', pve_dir])


def activate(pve_dir):
    activate_this = os.path.join(pve_dir, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))


def install_pve_base(cache_dir):
    print '...installing django-djaboto via pip'
    check_call(['pip', 'install', 'git+https://bitbucket.org/oddotterco/django-djaboto.git#egg=django-djaboto'])
    print '...installing django via pip'
    check_call(['pip', 'install', '--upgrade', '--download-cache=%s' % cache_dir, '--source=%s' % cache_dir, 'Django'])
    print '...upgrading distribute'
    check_call(['pip', 'install', '--upgrade', '--download-cache=%s' % cache_dir, '--source=%s' % cache_dir, 'distribute>=0.6.30'])
    print '...upgrading/installing MySQL-python'
    check_call(['pip', 'install', '--upgrade', '--download-cache=%s' % cache_dir, '--source=%s' % cache_dir, 'MySQL-python==1.2.3'])


def check_requirements(requirements_path):
    """
    Check all requirements and respond on mismatched ones
    """
    from pkg_resources import WorkingSet, DistributionNotFound, VersionConflict
    from setuptools.command.easy_install import main as install
    with open(requirements_path) as (f_in):
        requirements = (line.rstrip() for line in f_in)
        requirements = (line for line in requirements if line[0] != '#')
        requirements = (line for line in requirements if not line.startswith('hg+'))
        requirements = (line for line in requirements if not line.startswith('git+'))
        requirements = list(line for line in requirements if line)
    working_set = WorkingSet()
    for requirement in requirements:
        if not requirement or requirement[0] == '#':
            continue
        try:
            dep = working_set.require(requirement)
        except DistributionNotFound:
            print 'DistributionNotFound for %s' % requirement
        except VersionConflict as err:
            print 'VersionConflict for %s' % requirement