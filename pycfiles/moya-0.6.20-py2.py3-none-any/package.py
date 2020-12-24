# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/package.py
# Compiled at: 2016-12-08 16:29:22
"""

Package tools

"""
from __future__ import print_function
from __future__ import unicode_literals
import fnmatch, hashlib, csv
from itertools import chain
import fs.copy
from fs.zipfs import ZipFS
from fs.tempfs import TempFS
from fs import walk
from .compat import implements_bool
from .console import Console

def _make_package_fs(package_fs, output_fs, exclude_wildcards, auth_token=None):
    """Builds a package zip."""
    assert isinstance(exclude_wildcards, list), b'wildcards must be a list'

    def match_wildcards(path):
        split_path = path.lstrip(b'/').split(b'/')
        for i in range(len(split_path)):
            p = (b'/').join(split_path[i:])
            if any(fnmatch.fnmatchcase(p, w) for w in exclude_wildcards):
                return False

        return True

    manifest = []
    console = Console()
    paths = []
    for dir_path, _, files in walk.walk(package_fs):
        output_fs.makedir(dir_path, recreate=True)
        for info in files:
            path = info.make_path(dir_path)
            if not match_wildcards(path):
                continue
            paths.append(path)

    with console.progress(b'building package...', len(paths)) as (progress):
        for path in sorted(paths):
            progress.step()
            data = package_fs.getbytes(path)
            m = hashlib.md5()
            m.update(data)
            file_hash = m.hexdigest()
            if auth_token is None:
                auth_hash = b''
            else:
                m.update(auth_token.encode(b'utf-8'))
                auth_hash = m.hexdigest()
            output_fs.setbytes(path, data)
            manifest.append((path, file_hash, auth_hash))

    return manifest


def export_manifest(manifest, output_fs, filename=b'manifest.csv'):
    """Write a manifest file."""
    lines = [
     b'"path","md5","auth md5"']
    for path, file_hash, auth_hash in manifest:
        lines.append((b'"{}",{},{}').format(path.replace(b'"', b'\\"'), file_hash, auth_hash))

    manifest_data = (b'\n').join(lines)
    output_fs.settext(filename, manifest_data, encoding=b'utf-8')


def read_manifest(manifest_fs, manifest_filename):
    """Read a manifest file."""
    with manifest_fs.open(manifest_filename, b'rb') as (manifest_file):
        csv_reader = csv.reader(manifest_file, delimiter=b',', quotechar=b'"')
        manifest = list(csv_reader)[1:]
    return manifest


@implements_bool
class ManifestComparision(object):
    """Stores the result of comparison with a directory and a manifest."""

    def __init__(self, new_files, changed_files, deleted_files):
        self.new_files = new_files
        self.changed_files = changed_files
        self.deleted_files = deleted_files

    def __bool__(self):
        return bool(self.new_files or self.changed_files or self.deleted_files)


def get_md5(input_file, chunk_size=16384):
    """Get the md5 of a file without reading entire file in to memory."""
    m = hashlib.md5()
    while 1:
        chunk = input_file.read(chunk_size)
        if not chunk:
            break
        m.update(chunk)

    return m.hexdigest()


def make_package(package_fs, output_fs, output_path, exclude_wildcards, auth_token):
    """Make a Moya package."""
    manifest_filename = b'manifest.csv'
    with TempFS() as (temp_fs):
        manifest = _make_package_fs(package_fs, temp_fs, exclude_wildcards, auth_token=auth_token)
        with output_fs.open(output_path, b'wb') as (dest_file):
            with ZipFS(dest_file, b'w') as (zip_fs):
                fs.copy.copy_dir(temp_fs, b'/', zip_fs, b'/')
                export_manifest(manifest, zip_fs, filename=manifest_filename)