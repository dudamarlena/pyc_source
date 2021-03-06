# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/utils/unpacking.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 9438 bytes
"""Utilities related archives.
"""
from __future__ import absolute_import
import logging, os, shutil, stat, tarfile, zipfile
from pip._internal.exceptions import InstallationError
from pip._internal.utils.filetypes import BZ2_EXTENSIONS, TAR_EXTENSIONS, XZ_EXTENSIONS, ZIP_EXTENSIONS
from pip._internal.utils.misc import ensure_dir
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Iterable, List, Optional, Text, Union
logger = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = ZIP_EXTENSIONS + TAR_EXTENSIONS
try:
    import bz2
    SUPPORTED_EXTENSIONS += BZ2_EXTENSIONS
except ImportError:
    logger.debug('bz2 module is not available')

try:
    import lzma
    SUPPORTED_EXTENSIONS += XZ_EXTENSIONS
except ImportError:
    logger.debug('lzma module is not available')

def current_umask():
    """Get the current umask which involves having to set it temporarily."""
    mask = os.umask(0)
    os.umask(mask)
    return mask


def split_leading_dir(path):
    path = path.lstrip('/').lstrip('\\')
    if '/' in path:
        if '\\' in path:
            if path.find('/') < path.find('\\') or '\\' not in path:
                return path.split('/', 1)
    if '\\' in path:
        return path.split('\\', 1)
    return [path, '']


def has_leading_dir(paths):
    """Returns true if all the paths have the same leading path name
    (i.e., everything is in one subdirectory in an archive)"""
    common_prefix = None
    for path in paths:
        prefix, rest = split_leading_dir(path)
        if not prefix:
            return False
            if common_prefix is None:
                common_prefix = prefix
            elif prefix != common_prefix:
                return False

    return True


def is_within_directory(directory, target):
    """
    Return true if the absolute path of target is within the directory
    """
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    prefix = os.path.commonprefix([abs_directory, abs_target])
    return prefix == abs_directory


def unzip_file(filename, location, flatten=True):
    """
    Unzip the file (with path `filename`) to the destination `location`.  All
    files are written based on system defaults and umask (i.e. permissions are
    not preserved), except that regular file members with any execute
    permissions (user, group, or world) have "chmod +x" applied after being
    written. Note that for windows, any execute changes using os.chmod are
    no-ops per the python docs.
    """
    ensure_dir(location)
    zipfp = open(filename, 'rb')
    try:
        zip = zipfile.ZipFile(zipfp, allowZip64=True)
        leading = has_leading_dir(zip.namelist()) and flatten
        for info in zip.infolist():
            name = info.filename
            fn = name
            if leading:
                fn = split_leading_dir(name)[1]
            fn = os.path.join(location, fn)
            dir = os.path.dirname(fn)
            if not is_within_directory(location, fn):
                message = 'The zip file ({}) has a file ({}) trying to install outside target directory ({})'
                raise InstallationError(message.format(filename, fn, location))
            if fn.endswith('/') or fn.endswith('\\'):
                ensure_dir(fn)
            else:
                ensure_dir(dir)
                fp = zip.open(name)
                try:
                    with open(fn, 'wb') as (destfp):
                        shutil.copyfileobj(fp, destfp)
                finally:
                    fp.close()
                    mode = info.external_attr >> 16
                    if mode:
                        if stat.S_ISREG(mode):
                            if mode & 73:
                                os.chmod(fn, 511 - current_umask() | 73)

    finally:
        zipfp.close()


def untar_file(filename, location):
    """
    Untar the file (with path `filename`) to the destination `location`.
    All files are written based on system defaults and umask (i.e. permissions
    are not preserved), except that regular file members with any execute
    permissions (user, group, or world) have "chmod +x" applied after being
    written.  Note that for windows, any execute changes using os.chmod are
    no-ops per the python docs.
    """
    ensure_dir(location)
    if filename.lower().endswith('.gz') or filename.lower().endswith('.tgz'):
        mode = 'r:gz'
    else:
        if filename.lower().endswith(BZ2_EXTENSIONS):
            mode = 'r:bz2'
        else:
            if filename.lower().endswith(XZ_EXTENSIONS):
                mode = 'r:xz'
            else:
                if filename.lower().endswith('.tar'):
                    mode = 'r'
                else:
                    logger.warning('Cannot determine compression type for file %s', filename)
                    mode = 'r:*'
    tar = tarfile.open(filename, mode)
    try:
        leading = has_leading_dir([member.name for member in tar.getmembers()])
        for member in tar.getmembers():
            fn = member.name
            if leading:
                fn = split_leading_dir(fn)[1]
            path = os.path.join(location, fn)
            if not is_within_directory(location, path):
                message = 'The tar file ({}) has a file ({}) trying to install outside target directory ({})'
                raise InstallationError(message.format(filename, path, location))
            if member.isdir():
                ensure_dir(path)
            elif member.issym():
                try:
                    tar._extract_member(member, path)
                except Exception as exc:
                    try:
                        logger.warning('In the tar file %s the member %s is invalid: %s', filename, member.name, exc)
                        continue
                    finally:
                        exc = None
                        del exc

            else:
                try:
                    fp = tar.extractfile(member)
                except (KeyError, AttributeError) as exc:
                    try:
                        logger.warning('In the tar file %s the member %s is invalid: %s', filename, member.name, exc)
                        continue
                    finally:
                        exc = None
                        del exc

                ensure_dir(os.path.dirname(path))
                with open(path, 'wb') as (destfp):
                    shutil.copyfileobj(fp, destfp)
                fp.close()
                tar.utime(member, path)
            if member.mode & 73:
                os.chmod(path, 511 - current_umask() | 73)

    finally:
        tar.close()


def unpack_file(filename, location, content_type=None):
    filename = os.path.realpath(filename)
    if not content_type == 'application/zip':
        if filename.lower().endswith(ZIP_EXTENSIONS) or zipfile.is_zipfile(filename):
            unzip_file(filename,
              location,
              flatten=(not filename.endswith('.whl')))
    elif not content_type == 'application/x-gzip':
        if tarfile.is_tarfile(filename) or filename.lower().endswith(TAR_EXTENSIONS + BZ2_EXTENSIONS + XZ_EXTENSIONS):
            untar_file(filename, location)
    else:
        logger.critical('Cannot unpack file %s (downloaded from %s, content-type: %s); cannot detect archive format', filename, location, content_type)
        raise InstallationError('Cannot determine archive format of {}'.format(location))