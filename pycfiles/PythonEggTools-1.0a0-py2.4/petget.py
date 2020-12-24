# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pet/petget.py
# Compiled at: 2006-12-22 07:59:52
"""
This module provides an interface to the pet-cache script.
"""
from setuptools.command.easy_install import main as easy_install
import optparse, pkg_resources, operator, sys
__all__ = [
 'install', 'source', 'remove', 'update', 'upgrade', 'main']

def install(args):
    if not args:
        return 'E: You must supply at least one package name'
    easy_install(args)


def source(args):
    if not args:
        return 'E: You must supply at least one package name'
    easy_install(['--editable', '--build-directory=.'] + args)


def remove(args):
    if not args:
        return 'E: You must supply at least one package name'
    easy_install(['--multi-version'] + args)


def update(args):
    if not args:
        return 'E: You must supply at least one package name'
    easy_install(['--upgrade'] + args)


def upgrade(args):
    if args:
        return "E: The 'upgrade' command does not take any arguments."
    distname = operator.attrgetter('project_name')
    packages = map(distname, pkg_resources.working_set)
    return update(packages)


def get_module_func(fname):
    return globals().get(fname)


def main(args=None):
    if not args:
        args = sys.argv[1:]
    usage = "Usage:  pet-get [options] upgrade\n        pet-get [options] install|remove pkg1 [pkg2 ...]\n        pet-get [options] update pkg1 [pkg2 ...]\n        pet-get [options] source pkg1 [pkg2 ...]\n\npet-get is a simple command line interface for downloading and managing\nPython packages.  It wraps setuptool's 'easy_install' script and\naccepts the same options.\n\nCommands:\n    install - Install new packages\n    update - Update packages to the latest version\n    upgrade - Update ALL packages\n    remove - De-activate a package\n    source - Install editable packages in the current directory\n    \nWe will now print the options from 'easy_install' that may be passed\nto pet-get:\n"
    if '--help' in args or '-h' in args or '-?' in args or not args:
        print usage
        easy_install(['--help'])
        return
    commands = ['install', 'source', 'remove', 'update', 'upgrade']
    command = ''
    for x in args:
        if x in commands:
            command = x
            break
        elif not x.startswith('-'):
            return "E: '%s' is not a valid package command" % x

    if not command:
        return 'E: You must supply a package command'
    args.remove(command)
    fun = get_module_func(command)
    if not fun:
        return "E: '%s' is not a valid package command" % command
    return fun(args)


if __name__ == '__main__':
    main()