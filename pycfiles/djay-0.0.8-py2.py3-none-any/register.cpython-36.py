# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/twine/twine/commands/register.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2072 bytes
from __future__ import absolute_import, unicode_literals, print_function
import argparse, os.path
from twine.package import PackageFile
from twine import exceptions
from twine import settings

def register(register_settings, package):
    repository_url = register_settings.repository_config['repository']
    print('Registering package to {}'.format(repository_url))
    repository = register_settings.create_repository()
    if not os.path.exists(package):
        raise exceptions.PackageNotFound('"{}" does not exist on the file system.'.format(package))
    resp = repository.register(PackageFile.from_filename(package, register_settings.comment))
    repository.close()
    if resp.is_redirect:
        raise exceptions.RedirectDetected('"{0}" attempted to redirect to "{1}" during registration. Aborting...'.format(repository_url, resp.headers['location']))
    resp.raise_for_status()


def main(args):
    parser = argparse.ArgumentParser(prog='twine register')
    settings.Settings.register_argparse_arguments(parser)
    parser.add_argument('package',
      metavar='package',
      help='File from which we read the package metadata.')
    args = parser.parse_args(args)
    register_settings = settings.Settings.from_argparse(args)
    register(register_settings, args.package)