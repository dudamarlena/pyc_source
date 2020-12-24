# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/init/arbitrary_project.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3621 bytes
"""
Initialize an arbitrary project
"""
import functools, shutil, logging
from cookiecutter import repository
from cookiecutter import exceptions
from cookiecutter import config
from samcli.lib.utils import osutils
from .exceptions import ArbitraryProjectDownloadFailed
LOG = logging.getLogger(__name__)
BAD_LOCATION_ERROR_MSG = 'Please verify your location. The following types of location are supported:\n\n* Github: gh:user/repo (or) https://github.com/user/repo (or) git@github.com:user/repo.git\n          For Git repositories, you must use location of the root of the repository.\n\n* Mercurial: hg+ssh://hg@bitbucket.org/repo\n\n* Http(s): https://example.com/code.zip\n\n* Local Path: /path/to/code.zip'

def generate_non_cookiecutter_project(location, output_dir):
    """
    Uses Cookiecutter APIs to download a project at given ``location`` to the ``output_dir``.
    This does *not* run cookiecutter on the downloaded project.

    Parameters
    ----------
    location : str
        Path to where the project is. This supports all formats of location cookiecutter supports
        (ex: zip, git, ssh, hg, local zipfile)

        NOTE: This value *cannot* be a local directory. We didn't see a value in simply copying the directory
        contents to ``output_dir`` without any processing.

    output_dir : str
        Directory where the project should be downloaded to

    Returns
    -------
    str
        Name of the directory where the project was downloaded to.

    Raises
    ------
    cookiecutter.exception.CookiecutterException if download failed for some reason
    """
    LOG.debug('Downloading project from %s to %s', location, output_dir)
    no_input = True
    location = repository.expand_abbreviations(location, config.BUILTIN_ABBREVIATIONS)
    if repository.is_zip_file(location):
        LOG.debug('%s location is a zip file', location)
        download_fn = functools.partial((repository.unzip),
          zip_uri=location, is_url=(repository.is_repo_url(location)), no_input=no_input)
    else:
        if repository.is_repo_url(location):
            LOG.debug('%s location is a source control repository', location)
            download_fn = functools.partial((repository.clone), repo_url=location, no_input=no_input)
        else:
            raise ArbitraryProjectDownloadFailed(msg=BAD_LOCATION_ERROR_MSG)
    try:
        return _download_and_copy(download_fn, output_dir)
    except exceptions.RepositoryNotFound:
        raise ArbitraryProjectDownloadFailed(msg=BAD_LOCATION_ERROR_MSG)


def _download_and_copy(download_fn, output_dir):
    """
    Runs the download function to download files into a temporary directory and then copy the files over to
    the ``output_dir``

    Parameters
    ----------
    download_fn : function
        Method to be called to download. It needs to accept a parameter called `clone_to_dir`. This will be
        set to the temporary directory

    output_dir : str
        Path to the directory where files will be copied to

    Returns
    -------
    output_dir
    """
    with osutils.mkdir_temp() as (tempdir):
        downloaded_dir = download_fn(clone_to_dir=tempdir)
        osutils.copytree(downloaded_dir, output_dir, ignore=(shutil.ignore_patterns('*.git')))
    return output_dir