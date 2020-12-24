# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/twine/twine/commands/upload.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 5089 bytes
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import argparse, os.path
from twine.commands import _find_dists
from twine.package import PackageFile
from twine import exceptions
from twine import settings
from twine import utils

def skip_upload(response, skip_existing, package):
    filename = package.basefilename
    msg_400 = (
     'A file named "{}" already exists for'.format(filename),
     'File already exists',
     'Repository does not allow updating assets')
    msg_403 = 'Not enough permissions to overwrite artifact'
    return skip_existing and (response.status_code == 409 or response.status_code == 400 and response.reason.startswith(msg_400) or response.status_code == 403 and msg_403 in response.text)


def upload(upload_settings, dists):
    dists = _find_dists(dists)
    signatures = {os.path.basename(d):d for d in dists if d.endswith('.asc') if d.endswith('.asc')}
    uploads = [i for i in dists if not i.endswith('.asc')]
    upload_settings.check_repository_url()
    repository_url = upload_settings.repository_config['repository']
    print('Uploading distributions to {}'.format(repository_url))
    repository = upload_settings.create_repository()
    for filename in uploads:
        package = PackageFile.from_filename(filename, upload_settings.comment)
        skip_message = '  Skipping {} because it appears to already exist'.format(package.basefilename)
        if upload_settings.skip_existing:
            if repository.package_is_uploaded(package):
                print(skip_message)
                continue
        signed_name = package.signed_basefilename
        if signed_name in signatures:
            package.add_gpg_signature(signatures[signed_name], signed_name)
        else:
            if upload_settings.sign:
                package.sign(upload_settings.sign_with, upload_settings.identity)
        resp = repository.upload(package)
        if resp.is_redirect:
            raise exceptions.RedirectDetected('"{0}" attempted to redirect to "{1}" during upload. Aborting...'.format(repository_url, resp.headers['location']))
        if skip_upload(resp, upload_settings.skip_existing, package):
            print(skip_message)
        else:
            utils.check_status_code(resp, upload_settings.verbose)

    repository.close()


def main(args):
    parser = argparse.ArgumentParser(prog='twine upload')
    settings.Settings.register_argparse_arguments(parser)
    parser.add_argument('dists',
      nargs='+',
      metavar='dist',
      help='The distribution files to upload to the repository (package index). Usually dist/* . May additionally contain a .asc file to include an existing signature with the file upload.')
    args = parser.parse_args(args)
    upload_settings = settings.Settings.from_argparse(args)
    return upload(upload_settings, args.dists)