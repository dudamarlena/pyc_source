# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/twine/twine/commands/upload.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 4702 bytes
import argparse, os.path
from twine.commands import _find_dists
from twine.package import PackageFile
from twine import exceptions
from twine import settings
from twine import utils

def skip_upload(response, skip_existing, package):
    if not skip_existing:
        return False
    else:
        status = response.status_code
        reason = getattr(response, 'reason', '').lower()
        text = getattr(response, 'text', '').lower()
        return status == 409 or status == 400 and 'already exist' in reason or status == 400 and 'updating asset' in reason or status == 403 and 'overwrite artifact' in text


def upload(upload_settings, dists):
    dists = _find_dists(dists)
    signatures = {os.path.basename(d):d for d in dists if d.endswith('.asc') if d.endswith('.asc')}
    uploads = [i for i in dists if not i.endswith('.asc')]
    upload_settings.check_repository_url()
    repository_url = upload_settings.repository_config['repository']
    print(f"Uploading distributions to {repository_url}")
    repository = upload_settings.create_repository()
    uploaded_packages = []
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
            raise exceptions.RedirectDetected.from_args(repository_url, resp.headers['location'])
        if skip_upload(resp, upload_settings.skip_existing, package):
            print(skip_message)
        else:
            utils.check_status_code(resp, upload_settings.verbose)
            uploaded_packages.append(package)

    release_urls = repository.release_urls(uploaded_packages)
    if release_urls:
        print('\nView at:')
        for url in release_urls:
            print(url)

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