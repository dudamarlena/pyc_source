# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/app_installation.py
# Compiled at: 2014-09-22 18:21:43
import os, shutil, subprocess
from setuptools.command.develop import develop
from setuptools.command.install import install

def get_tethysapp_directory():
    """
    Return the absolute path to the tethysapp directory.
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tethysapp')


def _run_install(self):
    """
    The definition of the "run" method for the CustomInstallCommand metaclass.
    """
    tethysapp_dir = get_tethysapp_directory()
    destination_dir = os.path.join(tethysapp_dir, self.app_package)
    print ('Copying App Package: {0} to {1}').format(self.app_package_dir, destination_dir)
    try:
        shutil.copytree(self.app_package_dir, destination_dir)
    except:
        try:
            shutil.rmtree(destination_dir)
        except:
            os.remove(destination_dir)

        shutil.copytree(self.app_package_dir, destination_dir)

    for dependency in self.dependencies:
        subprocess.call(['pip', 'install', dependency])

    install.run(self)


def _run_develop(self):
    """
    The definition of the "run" method for the CustomDevelopCommand metaclass.
    """
    tethysapp_dir = get_tethysapp_directory()
    destination_dir = os.path.join(tethysapp_dir, self.app_package)
    print ('Creating Symbolic Link to App Package: {0} to {1}').format(self.app_package_dir, destination_dir)
    try:
        os.symlink(self.app_package_dir, destination_dir)
    except:
        try:
            shutil.rmtree(destination_dir)
        except:
            os.remove(destination_dir)

        os.symlink(self.app_package_dir, destination_dir)

    for dependency in self.dependencies:
        subprocess.call(['pip', 'install', dependency])

    develop.run(self)


def custom_install_command(app_package, app_package_dir, dependencies):
    """
    Returns a custom install command class that is tailored for the app calling it.
    """
    properties = {'app_package': app_package, 'app_package_dir': app_package_dir, 
       'dependencies': dependencies, 
       'run': _run_install}
    return type('CustomInstallCommand', (install, object), properties)


def custom_develop_command(app_package, app_package_dir, dependencies):
    """
    Returns a custom develop command class that is tailored for the app calling it.
    """
    properties = {'app_package': app_package, 'app_package_dir': app_package_dir, 
       'dependencies': dependencies, 
       'run': _run_develop}
    return type('CustomDevelopCommand', (develop, object), properties)