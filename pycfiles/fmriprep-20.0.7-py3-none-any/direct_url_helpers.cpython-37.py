# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/utils/direct_url_helpers.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 4359 bytes
import logging
from pip._internal.models.direct_url import DIRECT_URL_METADATA_NAME, ArchiveInfo, DirectUrl, DirectUrlValidationError, DirInfo, VcsInfo
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
import pip._internal.vcs as vcs
try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

if MYPY_CHECK_RUNNING:
    from typing import Optional
    from pip._internal.models.link import Link
    from pip._vendor.pkg_resources import Distribution
logger = logging.getLogger(__name__)

def direct_url_as_pep440_direct_reference(direct_url, name):
    """Convert a DirectUrl to a pip requirement string."""
    direct_url.validate()
    requirement = name + ' @ '
    fragments = []
    if isinstance(direct_url.info, VcsInfo):
        requirement += '{}+{}@{}'.format(direct_url.info.vcs, direct_url.url, direct_url.info.commit_id)
    else:
        if isinstance(direct_url.info, ArchiveInfo):
            requirement += direct_url.url
            if direct_url.info.hash:
                fragments.append(direct_url.info.hash)
        else:
            assert isinstance(direct_url.info, DirInfo)
            assert not direct_url.info.editable
            requirement += direct_url.url
    if direct_url.subdirectory:
        fragments.append('subdirectory=' + direct_url.subdirectory)
    if fragments:
        requirement += '#' + '&'.join(fragments)
    return requirement


def direct_url_from_link(link, source_dir=None, link_is_in_wheel_cache=False):
    if link.is_vcs:
        vcs_backend = vcs.get_backend_for_scheme(link.scheme)
        assert vcs_backend
        url, requested_revision, _ = vcs_backend.get_url_rev_and_auth(link.url_without_fragment)
        if link_is_in_wheel_cache:
            assert requested_revision
            commit_id = requested_revision
        else:
            assert source_dir
            commit_id = vcs_backend.get_revision(source_dir)
        return DirectUrl(url=url,
          info=VcsInfo(vcs=(vcs_backend.name),
          commit_id=commit_id,
          requested_revision=requested_revision),
          subdirectory=(link.subdirectory_fragment))
    if link.is_existing_dir():
        return DirectUrl(url=(link.url_without_fragment),
          info=(DirInfo()),
          subdirectory=(link.subdirectory_fragment))
    hash = None
    hash_name = link.hash_name
    if hash_name:
        hash = '{}={}'.format(hash_name, link.hash)
    return DirectUrl(url=(link.url_without_fragment),
      info=ArchiveInfo(hash=hash),
      subdirectory=(link.subdirectory_fragment))


def dist_get_direct_url(dist):
    """Obtain a DirectUrl from a pkg_resource.Distribution.

    Returns None if the distribution has no `direct_url.json` metadata,
    or if `direct_url.json` is invalid.
    """
    if not dist.has_metadata(DIRECT_URL_METADATA_NAME):
        return
    try:
        return DirectUrl.from_json(dist.get_metadata(DIRECT_URL_METADATA_NAME))
    except (DirectUrlValidationError,
     JSONDecodeError,
     UnicodeDecodeError) as e:
        try:
            logger.warning('Error parsing %s for %s: %s', DIRECT_URL_METADATA_NAME, dist.project_name, e)
            return
        finally:
            e = None
            del e