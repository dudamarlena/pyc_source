# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/setuptools/setuptools/archive_util.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 6626 bytes
"""Utilities for extracting common archive formats"""
import zipfile, tarfile, os, shutil, posixpath, contextlib
from distutils.errors import DistutilsError
from pkg_resources import ensure_directory
__all__ = [
 'unpack_archive', 'unpack_zipfile', 'unpack_tarfile', 'default_filter',
 'UnrecognizedFormat', 'extraction_drivers', 'unpack_directory']

class UnrecognizedFormat(DistutilsError):
    __doc__ = "Couldn't recognize the archive type"


def default_filter(src, dst):
    """The default progress/filter callback; returns True for all files"""
    return dst


def unpack_archive(filename, extract_dir, progress_filter=default_filter, drivers=None):
    """Unpack `filename` to `extract_dir`, or raise ``UnrecognizedFormat``

    `progress_filter` is a function taking two arguments: a source path
    internal to the archive ('/'-separated), and a filesystem path where it
    will be extracted.  The callback must return the desired extract path
    (which may be the same as the one passed in), or else ``None`` to skip
    that file or directory.  The callback can thus be used to report on the
    progress of the extraction, as well as to filter the items extracted or
    alter their extraction paths.

    `drivers`, if supplied, must be a non-empty sequence of functions with the
    same signature as this function (minus the `drivers` argument), that raise
    ``UnrecognizedFormat`` if they do not support extracting the designated
    archive type.  The `drivers` are tried in sequence until one is found that
    does not raise an error, or until all are exhausted (in which case
    ``UnrecognizedFormat`` is raised).  If you do not supply a sequence of
    drivers, the module's ``extraction_drivers`` constant will be used, which
    means that ``unpack_zipfile`` and ``unpack_tarfile`` will be tried, in that
    order.
    """
    for driver in drivers or extraction_drivers:
        try:
            driver(filename, extract_dir, progress_filter)
        except UnrecognizedFormat:
            continue
        else:
            return
    else:
        raise UnrecognizedFormat('Not a recognized archive type: %s' % filename)


def unpack_directory(filename, extract_dir, progress_filter=default_filter):
    """"Unpack" a directory, using the same interface as for archives

    Raises ``UnrecognizedFormat`` if `filename` is not a directory
    """
    if not os.path.isdir(filename):
        raise UnrecognizedFormat('%s is not a directory' % filename)
    paths = {filename: ('', extract_dir)}
    for base, dirs, files in os.walk(filename):
        src, dst = paths[base]
        for d in dirs:
            paths[os.path.join(base, d)] = (
             src + d + '/', os.path.join(dst, d))

        for f in files:
            target = os.path.join(dst, f)
            target = progress_filter(src + f, target)
            if not target:
                continue
            ensure_directory(target)
            f = os.path.join(base, f)
            shutil.copyfile(f, target)
            shutil.copystat(f, target)


def unpack_zipfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack zip `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a zipfile (as determined
    by ``zipfile.is_zipfile()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    if not zipfile.is_zipfile(filename):
        raise UnrecognizedFormat('%s is not a zip file' % (filename,))
    with zipfile.ZipFile(filename) as (z):
        for info in z.infolist():
            name = info.filename
            if name.startswith('/') or '..' in name.split('/'):
                continue
            else:
                target = (os.path.join)(extract_dir, *name.split('/'))
                target = progress_filter(name, target)
                if not target:
                    continue
                if name.endswith('/'):
                    ensure_directory(target)
                else:
                    ensure_directory(target)
                data = z.read(info.filename)
                with open(target, 'wb') as (f):
                    f.write(data)
            unix_attributes = info.external_attr >> 16
            if unix_attributes:
                os.chmod(target, unix_attributes)


def unpack_tarfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack tar/tar.gz/tar.bz2 `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a tarfile (as determined
    by ``tarfile.open()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError:
        raise UnrecognizedFormat('%s is not a compressed or uncompressed tar file' % (filename,))

    with contextlib.closing(tarobj):
        tarobj.chown = lambda *args: None
        for member in tarobj:
            name = member.name
            if name.startswith('/') or '..' not in name.split('/'):
                prelim_dst = (os.path.join)(extract_dir, *name.split('/'))
                while not member is not None or member.islnk() or member.issym():
                    linkpath = member.linkname
                    if member.issym():
                        base = posixpath.dirname(member.name)
                        linkpath = posixpath.join(base, linkpath)
                        linkpath = posixpath.normpath(linkpath)
                    member = tarobj._getmember(linkpath)

                if not member is not None or member.isfile() or member.isdir():
                    final_dst = progress_filter(name, prelim_dst)
                    if final_dst:
                        if final_dst.endswith(os.sep):
                            final_dst = final_dst[:-1]
                        try:
                            tarobj._extract_member(member, final_dst)
                        except tarfile.ExtractError:
                            pass

        return True


extraction_drivers = (
 unpack_directory, unpack_zipfile, unpack_tarfile)