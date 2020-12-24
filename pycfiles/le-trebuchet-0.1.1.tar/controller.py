# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/trebuchet/trebuchet/lib/controller.py
# Compiled at: 2013-11-27 06:07:03
import itertools
from .package import get_packages
from .my_yaml import load_yaml_config, print_pretty, get_yaml_config
from .callbacks import do_web_callback, jsonfy_pkg

def _get_all_packages(project, architecture=None, options=None, version_options=None):
    """
    Generator of packages to be built.
    """
    configs = get_yaml_config(project.config_file)
    pkg_list = []
    for config in configs:
        pkg = get_packages(project.full_path, config=config, architecture=architecture, options=options, version_options=version_options)
        pkg_list.append(pkg)

    for pkg in itertools.chain.from_iterable(pkg_list):
        yield pkg


def check_config(project):
    """
    """
    return [ pkg.full_package_name for pkg in _get_all_packages(project) ]


def build_app(project, prepare, package, version_options=None):
    """
    Locally build the application packages
    """
    pkg_list = []
    for pkg in _get_all_packages(project, architecture=prepare.architecture, options={'pip_options': prepare.pip_options}, version_options=version_options):
        pkg.build(package.debs_path, extra_description=prepare.extra_description)
        pkg_list.append(pkg.final_deb_name)
        print 'Built: ' + str(jsonfy_pkg(pkg))
        if package.web_callback_url:
            do_web_callback(package.web_callback_url, pkg)

    print pkg_list


def develop_app(project, prepare, version_options=None):
    """
    Locally prepare the working copy to be built for the application packages
    """
    pkg_list = []
    for pkg in _get_all_packages(project, architecture=prepare.architecture, options={'pip_options': prepare.pip_options}, version_options=version_options):
        pkg.develop(extra_description=prepare.extra_description)
        pkg_list.append(pkg.final_deb_name)

    print pkg_list


def print_build_details(project, versions):
    """
    Print some details related to the build.
    """
    print 'config file to use: ' + project.config_file
    print 'project to use: ' + project.full_path
    print versions