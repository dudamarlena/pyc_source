# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/tar.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 914 bytes
"""
Tarball Archive utility
"""
import tarfile
from tempfile import TemporaryFile
from contextlib import contextmanager

@contextmanager
def create_tarball(tar_paths):
    """
    Context Manger that creates the tarball of the Docker Context to use for building the image

    Parameters
    ----------
    tar_paths dict(str, str)
        Key representing a full path to the file or directory and the Value representing the path within the tarball

    Yields
    ------
        The tarball file
    """
    tarballfile = TemporaryFile()
    with tarfile.open(fileobj=tarballfile, mode='w') as (archive):
        for path_on_system, path_in_tarball in tar_paths.items():
            archive.add(path_on_system, arcname=path_in_tarball)

    tarballfile.flush()
    tarballfile.seek(0)
    try:
        yield tarballfile
    finally:
        tarballfile.close()