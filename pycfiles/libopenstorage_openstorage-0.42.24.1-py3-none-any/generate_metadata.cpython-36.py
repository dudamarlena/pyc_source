# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/operations/generate_metadata.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 4699 bytes
"""Metadata generation logic for source distributions.
"""
import logging, os
from pip._internal.exceptions import InstallationError
from pip._internal.utils.misc import ensure_dir
from pip._internal.utils.setuptools_build import make_setuptools_shim_args
from pip._internal.utils.subprocess import call_subprocess
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.vcs import vcs
if MYPY_CHECK_RUNNING:
    from typing import Callable, List
    from pip._internal.req.req_install import InstallRequirement
logger = logging.getLogger(__name__)

def get_metadata_generator(install_req):
    """Return a callable metadata generator for this InstallRequirement.

    A metadata generator takes an InstallRequirement (install_req) as an input,
    generates metadata via the appropriate process for that install_req and
    returns the generated metadata directory.
    """
    if not install_req.use_pep517:
        return _generate_metadata_legacy
    else:
        return _generate_metadata


def _find_egg_info(source_directory, is_editable):
    """Find an .egg-info in `source_directory`, based on `is_editable`.
    """

    def looks_like_virtual_env(path):
        return os.path.lexists(os.path.join(path, 'bin', 'python')) or os.path.exists(os.path.join(path, 'Scripts', 'Python.exe'))

    def locate_editable_egg_info(base):
        candidates = []
        for root, dirs, files in os.walk(base):
            for dir_ in vcs.dirnames:
                if dir_ in dirs:
                    dirs.remove(dir_)

            for dir_ in list(dirs):
                if looks_like_virtual_env(os.path.join(root, dir_)):
                    dirs.remove(dir_)
                else:
                    if dir_ == 'test' or dir_ == 'tests':
                        dirs.remove(dir_)

            candidates.extend(os.path.join(root, dir_) for dir_ in dirs)

        return [f for f in candidates if f.endswith('.egg-info')]

    def depth_of_directory(dir_):
        return dir_.count(os.path.sep) + (os.path.altsep and dir_.count(os.path.altsep) or 0)

    base = source_directory
    if is_editable:
        filenames = locate_editable_egg_info(base)
    else:
        base = os.path.join(base, 'pip-egg-info')
        filenames = os.listdir(base)
    if not filenames:
        raise InstallationError('Files/directories not found in %s' % base)
    if len(filenames) > 1:
        filenames.sort(key=depth_of_directory)
    return os.path.join(base, filenames[0])


def _generate_metadata_legacy(install_req):
    req_details_str = install_req.name or 'from {}'.format(install_req.link)
    logger.debug('Running setup.py (path:%s) egg_info for package %s', install_req.setup_py_path, req_details_str)
    base_cmd = make_setuptools_shim_args(install_req.setup_py_path)
    if install_req.isolated:
        base_cmd += ['--no-user-cfg']
    egg_base_option = []
    if not install_req.editable:
        egg_info_dir = os.path.join(install_req.unpacked_source_directory, 'pip-egg-info')
        egg_base_option = [
         '--egg-base', egg_info_dir]
        ensure_dir(egg_info_dir)
    with install_req.build_env:
        call_subprocess((base_cmd + ['egg_info'] + egg_base_option),
          cwd=(install_req.unpacked_source_directory),
          command_desc='python setup.py egg_info')
    return _find_egg_info(install_req.unpacked_source_directory, install_req.editable)


def _generate_metadata(install_req):
    return install_req.prepare_pep517_metadata()