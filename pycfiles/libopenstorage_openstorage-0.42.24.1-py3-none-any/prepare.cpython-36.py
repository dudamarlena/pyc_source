# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/operations/prepare.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 11279 bytes
"""Prepares a distribution for installation
"""
import logging, os
from pip._vendor import requests
from pip._internal.distributions import make_distribution_for_install_requirement
from pip._internal.distributions.installed import InstalledDistribution
from pip._internal.download import unpack_url
from pip._internal.exceptions import DirectoryUrlHashUnsupported, HashUnpinned, InstallationError, PreviousBuildDirError, VcsHashUnsupported
from pip._internal.utils.compat import expanduser
from pip._internal.utils.hashes import MissingHashes
from pip._internal.utils.logging import indent_log
from pip._internal.utils.marker_files import write_delete_marker_file
from pip._internal.utils.misc import display_path, normalize_path
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional
    from pip._internal.distributions import AbstractDistribution
    from pip._internal.index import PackageFinder
    from pip._internal.network.session import PipSession
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.req.req_tracker import RequirementTracker
logger = logging.getLogger(__name__)

def _get_prepared_distribution(req, req_tracker, finder, build_isolation):
    """Prepare a distribution for installation.
    """
    abstract_dist = make_distribution_for_install_requirement(req)
    with req_tracker.track(req):
        abstract_dist.prepare_distribution_metadata(finder, build_isolation)
    return abstract_dist


class RequirementPreparer(object):
    __doc__ = 'Prepares a Requirement\n    '

    def __init__(self, build_dir, download_dir, src_dir, wheel_download_dir, progress_bar, build_isolation, req_tracker):
        super(RequirementPreparer, self).__init__()
        self.src_dir = src_dir
        self.build_dir = build_dir
        self.req_tracker = req_tracker
        if download_dir:
            download_dir = expanduser(download_dir)
        self.download_dir = download_dir
        if wheel_download_dir:
            wheel_download_dir = normalize_path(wheel_download_dir)
        self.wheel_download_dir = wheel_download_dir
        self.progress_bar = progress_bar
        self.build_isolation = build_isolation

    @property
    def _download_should_save(self):
        if not self.download_dir:
            return False
        if os.path.exists(self.download_dir):
            return True
        logger.critical('Could not find download directory')
        raise InstallationError("Could not find or access download directory '%s'" % display_path(self.download_dir))

    def prepare_linked_requirement(self, req, session, finder, require_hashes):
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
            req.ensure_has_source_dir(self.build_dir)
            if os.path.exists(os.path.join(req.source_dir, 'setup.py')):
                raise PreviousBuildDirError("pip can't proceed with requirements '%s' due to a pre-existing build directory (%s). This is likely due to a previous installation that failed. pip is being responsible and not assuming it can delete this. Please delete it and try again." % (
                 req, req.source_dir))
            if require_hashes:
                if link.is_vcs:
                    raise VcsHashUnsupported()
                else:
                    if link.is_existing_dir():
                        raise DirectoryUrlHashUnsupported()
                    if not req.original_link:
                        if not req.is_pinned:
                            raise HashUnpinned()
            hashes = req.hashes(trust_internet=(not require_hashes))
            if require_hashes:
                if not hashes:
                    hashes = MissingHashes()
            download_dir = self.download_dir
            if link.is_wheel:
                if self.wheel_download_dir:
                    download_dir = self.wheel_download_dir
            try:
                unpack_url(link,
                  (req.source_dir), download_dir, session=session,
                  hashes=hashes,
                  progress_bar=(self.progress_bar))
            except requests.HTTPError as exc:
                logger.critical('Could not install requirement %s because of error %s', req, exc)
                raise InstallationError('Could not install requirement %s because of HTTP error %s for URL %s' % (
                 req, exc, link))

            if link.is_wheel:
                if download_dir:
                    autodelete_unpacked = True
                else:
                    autodelete_unpacked = False
            else:
                autodelete_unpacked = True
            if autodelete_unpacked:
                write_delete_marker_file(req.source_dir)
            abstract_dist = _get_prepared_distribution(req, self.req_tracker, finder, self.build_isolation)
            if self._download_should_save:
                if link.is_vcs:
                    req.archive(self.download_dir)
        return abstract_dist

    def prepare_editable_requirement(self, req, require_hashes, use_user_site, finder):
        """Prepare an editable requirement
        """
        assert req.editable, 'cannot prepare a non-editable req as editable'
        logger.info('Obtaining %s', req)
        with indent_log():
            if require_hashes:
                raise InstallationError('The editable requirement %s cannot be installed when requiring hashes, because there is no single file to hash.' % req)
            req.ensure_has_source_dir(self.src_dir)
            req.update_editable(not self._download_should_save)
            abstract_dist = _get_prepared_distribution(req, self.req_tracker, finder, self.build_isolation)
            if self._download_should_save:
                req.archive(self.download_dir)
            req.check_if_exists(use_user_site)
        return abstract_dist

    def prepare_installed_requirement(self, req, require_hashes, skip_reason):
        """Prepare an already-installed requirement
        """
        if not req.satisfied_by:
            raise AssertionError("req should have been satisfied but isn't")
        elif not skip_reason is not None:
            raise AssertionError('did not get skip reason skipped but req.satisfied_by is set to %r' % (
             req.satisfied_by,))
        logger.info('Requirement %s: %s (%s)', skip_reason, req, req.satisfied_by.version)
        with indent_log():
            if require_hashes:
                logger.debug('Since it is already installed, we are trusting this package without checking its hash. To ensure a completely repeatable environment, install into an empty virtualenv.')
            abstract_dist = InstalledDistribution(req)
        return abstract_dist