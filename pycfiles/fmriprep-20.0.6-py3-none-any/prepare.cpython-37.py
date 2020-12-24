# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_internal/operations/prepare.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 20942 bytes
"""Prepares a distribution for installation
"""
import logging, mimetypes, os, shutil, sys
from pip._vendor import requests
from pip._vendor.six import PY2
from pip._internal.distributions import make_distribution_for_install_requirement
from pip._internal.distributions.installed import InstalledDistribution
from pip._internal.exceptions import DirectoryUrlHashUnsupported, HashMismatch, HashUnpinned, InstallationError, PreviousBuildDirError, VcsHashUnsupported
from pip._internal.utils.filesystem import copy2_fixed
from pip._internal.utils.hashes import MissingHashes
from pip._internal.utils.logging import indent_log
from pip._internal.utils.marker_files import write_delete_marker_file
from pip._internal.utils.misc import ask_path_exists, backup_dir, display_path, hide_url, path_to_display, rmtree
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.unpacking import unpack_file
import pip._internal.vcs as vcs
if MYPY_CHECK_RUNNING:
    from typing import Callable, List, Optional, Tuple
    from mypy_extensions import TypedDict
    from pip._internal.distributions import AbstractDistribution
    from pip._internal.index.package_finder import PackageFinder
    from pip._internal.models.link import Link
    from pip._internal.network.download import Downloader
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.req.req_tracker import RequirementTracker
    from pip._internal.utils.hashes import Hashes
    if PY2:
        CopytreeKwargs = TypedDict('CopytreeKwargs',
          {'ignore':Callable[([str, List[str]], List[str])], 
         'symlinks':bool},
          total=False)
    else:
        CopytreeKwargs = TypedDict('CopytreeKwargs',
          {'copy_function':Callable[([str, str], None)], 
         'ignore':Callable[([str, List[str]], List[str])], 
         'ignore_dangling_symlinks':bool, 
         'symlinks':bool},
          total=False)
logger = logging.getLogger(__name__)

def _get_prepared_distribution(req, req_tracker, finder, build_isolation):
    """Prepare a distribution for installation.
    """
    abstract_dist = make_distribution_for_install_requirement(req)
    with req_tracker.track(req):
        abstract_dist.prepare_distribution_metadata(finder, build_isolation)
    return abstract_dist


def unpack_vcs_link(link, location):
    vcs_backend = vcs.get_backend_for_scheme(link.scheme)
    assert vcs_backend is not None
    vcs_backend.unpack(location, url=(hide_url(link.url)))


def _copy_file(filename, location, link):
    copy = True
    download_location = os.path.join(location, link.filename)
    if os.path.exists(download_location):
        response = ask_path_exists('The file {} exists. (i)gnore, (w)ipe, (b)ackup, (a)abort'.format(display_path(download_location)), ('i',
                                                                                                                                        'w',
                                                                                                                                        'b',
                                                                                                                                        'a'))
        if response == 'i':
            copy = False
        else:
            if response == 'w':
                logger.warning('Deleting %s', display_path(download_location))
                os.remove(download_location)
            else:
                if response == 'b':
                    dest_file = backup_dir(download_location)
                    logger.warning('Backing up %s to %s', display_path(download_location), display_path(dest_file))
                    shutil.move(download_location, dest_file)
                else:
                    if response == 'a':
                        sys.exit(-1)
    if copy:
        shutil.copy(filename, download_location)
        logger.info('Saved %s', display_path(download_location))


def unpack_http_url(link, location, downloader, download_dir=None, hashes=None):
    temp_dir = TempDirectory(kind='unpack', globally_managed=True)
    already_downloaded_path = None
    if download_dir:
        already_downloaded_path = _check_download_dir(link, download_dir, hashes)
    elif already_downloaded_path:
        from_path = already_downloaded_path
        content_type = mimetypes.guess_type(from_path)[0]
    else:
        from_path, content_type = _download_http_url(link, downloader, temp_dir.path, hashes)
    unpack_file(from_path, location, content_type)
    return from_path


def _copy2_ignoring_special_files(src, dest):
    """Copying special files is not supported, but as a convenience to users
    we skip errors copying them. This supports tools that may create e.g.
    socket files in the project source directory.
    """
    try:
        copy2_fixed(src, dest)
    except shutil.SpecialFileError as e:
        try:
            logger.warning("Ignoring special file error '%s' encountered copying %s to %s.", str(e), path_to_display(src), path_to_display(dest))
        finally:
            e = None
            del e


def _copy_source_tree(source, target):

    def ignore(d, names):
        if d == source:
            return ['.tox', '.nox']
        return []

    kwargs = dict(ignore=ignore, symlinks=True)
    if not PY2:
        kwargs['copy_function'] = _copy2_ignoring_special_files
    (shutil.copytree)(source, target, **kwargs)


def unpack_file_url(link, location, download_dir=None, hashes=None):
    """Unpack link into location.
    """
    link_path = link.file_path
    if link.is_existing_dir():
        if os.path.isdir(location):
            rmtree(location)
        _copy_source_tree(link_path, location)
        return
    already_downloaded_path = None
    if download_dir:
        already_downloaded_path = _check_download_dir(link, download_dir, hashes)
    elif already_downloaded_path:
        from_path = already_downloaded_path
    else:
        from_path = link_path
    if hashes:
        hashes.check_against_path(from_path)
    content_type = mimetypes.guess_type(from_path)[0]
    unpack_file(from_path, location, content_type)
    return from_path


def unpack_url(link, location, downloader, download_dir=None, hashes=None):
    """Unpack link into location, downloading if required.

    :param hashes: A Hashes object, one of whose embedded hashes must match,
        or HashMismatch will be raised. If the Hashes is empty, no matches are
        required, and unhashable types of requirements (like VCS ones, which
        would ordinarily raise HashUnsupported) are allowed.
    """
    if link.is_vcs:
        unpack_vcs_link(link, location)
        return
    if link.is_file:
        return unpack_file_url(link, location, download_dir, hashes=hashes)
    return unpack_http_url(link,
      location,
      downloader,
      download_dir,
      hashes=hashes)


def _download_http_url(link, downloader, temp_dir, hashes):
    """Download link url into temp_dir using provided session"""
    download = downloader(link)
    file_path = os.path.join(temp_dir, download.filename)
    with open(file_path, 'wb') as (content_file):
        for chunk in download.chunks:
            content_file.write(chunk)

    if hashes:
        hashes.check_against_path(file_path)
    return (file_path, download.response.headers.get('content-type', ''))


def _check_download_dir(link, download_dir, hashes):
    """ Check download_dir for previously downloaded file with correct hash
        If a correct file is found return its path else None
    """
    download_path = os.path.join(download_dir, link.filename)
    if not os.path.exists(download_path):
        return
    logger.info('File was already downloaded %s', download_path)
    if hashes:
        try:
            hashes.check_against_path(download_path)
        except HashMismatch:
            logger.warning('Previously-downloaded file %s has bad hash. Re-downloading.', download_path)
            os.unlink(download_path)
            return

    return download_path


class RequirementPreparer(object):
    __doc__ = 'Prepares a Requirement\n    '

    def __init__(self, build_dir, download_dir, src_dir, wheel_download_dir, build_isolation, req_tracker, downloader, finder, require_hashes, use_user_site):
        super(RequirementPreparer, self).__init__()
        self.src_dir = src_dir
        self.build_dir = build_dir
        self.req_tracker = req_tracker
        self.downloader = downloader
        self.finder = finder
        self.download_dir = download_dir
        self.wheel_download_dir = wheel_download_dir
        self.build_isolation = build_isolation
        self.require_hashes = require_hashes
        self.use_user_site = use_user_site

    @property
    def _download_should_save(self):
        if not self.download_dir:
            return False
        if os.path.exists(self.download_dir):
            return True
        logger.critical('Could not find download directory')
        raise InstallationError("Could not find or access download directory '{}'".format(self.download_dir))

    def prepare_linked_requirement(self, req):
        """Prepare a requirement that would be obtained from req.link
        """
        if not req.link:
            raise AssertionError
        else:
            link = req.link
            if link.scheme == 'file':
                path = link.file_path
                logger.info('Processing %s', display_path(path))
            else:
                logger.info('Collecting %s', req.req or req)
        with indent_log():
            if not req.source_dir is None:
                raise AssertionError
            else:
                req.ensure_has_source_dir(self.build_dir)
                if os.path.exists(os.path.join(req.source_dir, 'setup.py')):
                    raise PreviousBuildDirError("pip can't proceed with requirements '{}' due to a pre-existing build directory ({}). This is likely due to a previous installation that failed. pip is being responsible and not assuming it can delete this. Please delete it and try again.".format(req, req.source_dir))
                if self.require_hashes:
                    if link.is_vcs:
                        raise VcsHashUnsupported()
                    else:
                        if link.is_existing_dir():
                            raise DirectoryUrlHashUnsupported()
                        elif not req.original_link:
                            if not req.is_pinned:
                                raise HashUnpinned()
                hashes = req.hashes(trust_internet=(not self.require_hashes))
                if self.require_hashes:
                    if not hashes:
                        hashes = MissingHashes()
                download_dir = self.download_dir
                if link.is_wheel:
                    if self.wheel_download_dir:
                        download_dir = self.wheel_download_dir
                try:
                    local_path = unpack_url(link,
                      (req.source_dir), (self.downloader), download_dir, hashes=hashes)
                except requests.HTTPError as exc:
                    try:
                        logger.critical('Could not install requirement %s because of error %s', req, exc)
                        raise InstallationError('Could not install requirement {} because of HTTP error {} for URL {}'.format(req, exc, link))
                    finally:
                        exc = None
                        del exc

                if local_path:
                    req.local_file_path = local_path
                if link.is_wheel:
                    if download_dir:
                        autodelete_unpacked = True
                    else:
                        autodelete_unpacked = False
                else:
                    autodelete_unpacked = True
                if autodelete_unpacked:
                    write_delete_marker_file(req.source_dir)
                abstract_dist = _get_prepared_distribution(req, self.req_tracker, self.finder, self.build_isolation)
                if download_dir:
                    if link.is_existing_dir():
                        logger.info('Link is a directory, ignoring download_dir')
                    else:
                        if local_path:
                            if not os.path.exists(os.path.join(download_dir, link.filename)):
                                _copy_file(local_path, download_dir, link)
                if self._download_should_save and link.is_vcs:
                    req.archive(self.download_dir)
        return abstract_dist

    def prepare_editable_requirement(self, req):
        """Prepare an editable requirement
        """
        assert req.editable, 'cannot prepare a non-editable req as editable'
        logger.info('Obtaining %s', req)
        with indent_log():
            if self.require_hashes:
                raise InstallationError('The editable requirement {} cannot be installed when requiring hashes, because there is no single file to hash.'.format(req))
            req.ensure_has_source_dir(self.src_dir)
            req.update_editable(not self._download_should_save)
            abstract_dist = _get_prepared_distribution(req, self.req_tracker, self.finder, self.build_isolation)
            if self._download_should_save:
                req.archive(self.download_dir)
            req.check_if_exists(self.use_user_site)
        return abstract_dist

    def prepare_installed_requirement(self, req, skip_reason):
        """Prepare an already-installed requirement
        """
        assert req.satisfied_by, "req should have been satisfied but isn't"
        assert skip_reason is not None, 'did not get skip reason skipped but req.satisfied_by is set to {}'.format(req.satisfied_by)
        logger.info('Requirement %s: %s (%s)', skip_reason, req, req.satisfied_by.version)
        with indent_log():
            if self.require_hashes:
                logger.debug('Since it is already installed, we are trusting this package without checking its hash. To ensure a completely repeatable environment, install into an empty virtualenv.')
            abstract_dist = InstalledDistribution(req)
        return abstract_dist