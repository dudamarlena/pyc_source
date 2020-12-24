# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/req/req_install.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 31713 bytes
from __future__ import absolute_import
import logging, os, shutil, sys, zipfile
from pip._vendor import pkg_resources, six
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.utils import canonicalize_name
from pip._vendor.packaging.version import Version
import pip._vendor.packaging.version as parse_version
from pip._vendor.pep517.wrappers import Pep517HookCaller
from pip._internal.build_env import NoOpBuildEnvironment
from pip._internal.exceptions import InstallationError
from pip._internal.locations import get_scheme
from pip._internal.models.link import Link
from pip._internal.operations.build.metadata import generate_metadata
import pip._internal.operations.build.metadata_legacy as generate_metadata_legacy
import pip._internal.operations.install.editable_legacy as install_editable_legacy
from pip._internal.operations.install.legacy import LegacyInstallFailure
import pip._internal.operations.install.legacy as install_legacy
from pip._internal.operations.install.wheel import install_wheel
from pip._internal.pyproject import load_pyproject_toml, make_pyproject_path
from pip._internal.req.req_uninstall import UninstallPathSet
from pip._internal.utils.deprecation import deprecated
from pip._internal.utils.direct_url_helpers import direct_url_from_link
from pip._internal.utils.hashes import Hashes
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import ask_path_exists, backup_dir, display_path, dist_in_site_packages, dist_in_usersite, get_installed_version, hide_url, redact_auth_from_url
from pip._internal.utils.packaging import get_metadata
from pip._internal.utils.temp_dir import TempDirectory, tempdir_kinds
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv
import pip._internal.vcs as vcs
if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, Iterable, List, Optional, Sequence, Union
    from pip._internal.build_env import BuildEnvironment
    from pip._vendor.pkg_resources import Distribution
    from pip._vendor.packaging.specifiers import SpecifierSet
    from pip._vendor.packaging.markers import Marker
logger = logging.getLogger(__name__)

def _get_dist(metadata_directory):
    """Return a pkg_resources.Distribution for the provided
    metadata directory.
    """
    dist_dir = metadata_directory.rstrip(os.sep)
    base_dir, dist_dir_name = os.path.split(dist_dir)
    metadata = pkg_resources.PathMetadata(base_dir, dist_dir)
    if dist_dir.endswith('.egg-info'):
        dist_cls = pkg_resources.Distribution
        dist_name = os.path.splitext(dist_dir_name)[0]
    else:
        assert dist_dir.endswith('.dist-info')
        dist_cls = pkg_resources.DistInfoDistribution
        dist_name = os.path.splitext(dist_dir_name)[0].split('-')[0]
    return dist_cls(base_dir,
      project_name=dist_name,
      metadata=metadata)


class InstallRequirement(object):
    __doc__ = '\n    Represents something that may be installed later on, may have information\n    about where to fetch the relevant requirement and also contains logic for\n    installing the said requirement.\n    '

    def __init__(self, req, comes_from, editable=False, link=None, markers=None, use_pep517=None, isolated=False, install_options=None, global_options=None, hash_options=None, constraint=False, extras=()):
        if not req is None:
            if not isinstance(req, Requirement):
                raise AssertionError(req)
            else:
                self.req = req
                self.comes_from = comes_from
                self.constraint = constraint
                self.editable = editable
                self.source_dir = None
                if self.editable:
                    assert link
                    if link.is_file:
                        self.source_dir = os.path.normpath(os.path.abspath(link.file_path))
            if link is None:
                if req:
                    if req.url:
                        link = Link(req.url)
        else:
            self.link = self.original_link = link
            self.original_link_is_in_wheel_cache = False
            self.local_file_path = None
            if self.link:
                if self.link.is_file:
                    self.local_file_path = self.link.file_path
            elif extras:
                self.extras = extras
            else:
                if req:
                    self.extras = {pkg_resources.safe_extra(extra) for extra in req.extras}
                else:
                    self.extras = set()
            if markers is None and req:
                markers = req.marker
        self.markers = markers
        self.satisfied_by = None
        self.should_reinstall = False
        self._temp_build_dir = None
        self.install_succeeded = None
        self.install_options = install_options if install_options else []
        self.global_options = global_options if global_options else []
        self.hash_options = hash_options if hash_options else {}
        self.prepared = False
        self.is_direct = False
        self.successfully_downloaded = False
        self.isolated = isolated
        self.build_env = NoOpBuildEnvironment()
        self.metadata_directory = None
        self.pyproject_requires = None
        self.requirements_to_check = []
        self.pep517_backend = None
        self.use_pep517 = use_pep517

    def __str__(self):
        if self.req:
            s = str(self.req)
            if self.link:
                s += ' from {}'.format(redact_auth_from_url(self.link.url))
            else:
                if self.link:
                    s = redact_auth_from_url(self.link.url)
                else:
                    s = '<InstallRequirement>'
        else:
            if self.satisfied_by is not None:
                s += ' in {}'.format(display_path(self.satisfied_by.location))
            if self.comes_from:
                if isinstance(self.comes_from, six.string_types):
                    comes_from = self.comes_from
                else:
                    comes_from = self.comes_from.from_path()
                if comes_from:
                    s += ' (from {})'.format(comes_from)
        return s

    def __repr__(self):
        return '<{} object: {} editable={!r}>'.format(self.__class__.__name__, str(self), self.editable)

    def format_debug(self):
        """An un-tested helper for getting state, for debugging.
        """
        attributes = vars(self)
        names = sorted(attributes)
        state = ('{}={!r}'.format(attr, attributes[attr]) for attr in sorted(names))
        return '<{name} object: {{{state}}}>'.format(name=(self.__class__.__name__),
          state=(', '.join(state)))

    @property
    def name(self):
        if self.req is None:
            return
        return six.ensure_str(pkg_resources.safe_name(self.req.name))

    @property
    def specifier(self):
        return self.req.specifier

    @property
    def is_pinned(self):
        """Return whether I am pinned to an exact version.

        For example, some-package==1.2 is pinned; some-package>1.2 is not.
        """
        specifiers = self.specifier
        return len(specifiers) == 1 and next(iter(specifiers)).operator in {'==', '==='}

    @property
    def installed_version(self):
        return get_installed_version(self.name)

    def match_markers(self, extras_requested=None):
        if not extras_requested:
            extras_requested = ('', )
        if self.markers is not None:
            return any((self.markers.evaluate({'extra': extra}) for extra in extras_requested))
        return True

    @property
    def has_hash_options(self):
        """Return whether any known-good hashes are specified as options.

        These activate --require-hashes mode; hashes specified as part of a
        URL do not.

        """
        return bool(self.hash_options)

    def hashes(self, trust_internet=True):
        """Return a hash-comparer that considers my option- and URL-based
        hashes to be known-good.

        Hashes in URLs--ones embedded in the requirements file, not ones
        downloaded from an index server--are almost peers with ones from
        flags. They satisfy --require-hashes (whether it was implicitly or
        explicitly activated) but do not activate it. md5 and sha224 are not
        allowed in flags, which should nudge people toward good algos. We
        always OR all hashes together, even ones from URLs.

        :param trust_internet: Whether to trust URL-based (#md5=...) hashes
            downloaded from the internet, as by populate_link()

        """
        good_hashes = self.hash_options.copy()
        link = self.link if trust_internet else self.original_link
        if link:
            if link.hash:
                good_hashes.setdefault(link.hash_name, []).append(link.hash)
        return Hashes(good_hashes)

    def from_path(self):
        """Format a nice indicator to show where this "comes from"
        """
        if self.req is None:
            return
        s = str(self.req)
        if self.comes_from:
            if isinstance(self.comes_from, six.string_types):
                comes_from = self.comes_from
            else:
                comes_from = self.comes_from.from_path()
            if comes_from:
                s += '->' + comes_from
        return s

    def ensure_build_location(self, build_dir, autodelete):
        if not build_dir is not None:
            raise AssertionError
        else:
            if self._temp_build_dir is not None:
                if not self._temp_build_dir.path:
                    raise AssertionError
            else:
                return self._temp_build_dir.path
                if self.req is None:
                    self._temp_build_dir = TempDirectory(kind=(tempdir_kinds.REQ_BUILD),
                      globally_managed=True)
                    return self._temp_build_dir.path
                    if self.editable:
                        name = self.name.lower()
                else:
                    name = self.name
            os.path.exists(build_dir) or logger.debug('Creating directory %s', build_dir)
            os.makedirs(build_dir)
        actual_build_dir = os.path.join(build_dir, name)
        delete_arg = None if autodelete else False
        return TempDirectory(path=actual_build_dir,
          delete=delete_arg,
          kind=(tempdir_kinds.REQ_BUILD),
          globally_managed=True).path

    def _set_requirement(self):
        """Set requirement after generating metadata.
        """
        if not self.req is None:
            raise AssertionError
        else:
            assert self.metadata is not None
            assert self.source_dir is not None
            if isinstance(parse_version(self.metadata['Version']), Version):
                op = '=='
            else:
                op = '==='
        self.req = Requirement(''.join([
         self.metadata['Name'],
         op,
         self.metadata['Version']]))

    def warn_on_mismatching_name(self):
        metadata_name = canonicalize_name(self.metadata['Name'])
        if canonicalize_name(self.req.name) == metadata_name:
            return
        logger.warning('Generating metadata for package %s produced metadata for project name %s. Fix your #egg=%s fragments.', self.name, metadata_name, self.name)
        self.req = Requirement(metadata_name)

    def check_if_exists(self, use_user_site):
        """Find an installed distribution that satisfies or conflicts
        with this requirement, and set self.satisfied_by or
        self.should_reinstall appropriately.
        """
        if self.req is None:
            return
        no_marker = Requirement(str(self.req))
        no_marker.marker = None
        try:
            self.satisfied_by = pkg_resources.get_distribution(str(no_marker))
        except pkg_resources.DistributionNotFound:
            return
        except pkg_resources.VersionConflict:
            existing_dist = pkg_resources.get_distribution(self.req.name)
            if use_user_site:
                if dist_in_usersite(existing_dist):
                    self.should_reinstall = True
            elif running_under_virtualenv():
                if dist_in_site_packages(existing_dist):
                    raise InstallationError('Will not install to the user site because it will lack sys.path precedence to {} in {}'.format(existing_dist.project_name, existing_dist.location))
                else:
                    self.should_reinstall = True
        else:
            if self.editable:
                if self.satisfied_by:
                    self.should_reinstall = True
                    self.satisfied_by = None

    @property
    def is_wheel(self):
        if not self.link:
            return False
        return self.link.is_wheel

    @property
    def unpacked_source_directory(self):
        return os.path.join(self.source_dir, self.link and self.link.subdirectory_fragment or '')

    @property
    def setup_py_path(self):
        assert self.source_dir, 'No source dir for {}'.format(self)
        setup_py = os.path.join(self.unpacked_source_directory, 'setup.py')
        if six.PY2:
            if isinstance(setup_py, six.text_type):
                setup_py = setup_py.encode(sys.getfilesystemencoding())
        return setup_py

    @property
    def pyproject_toml_path(self):
        assert self.source_dir, 'No source dir for {}'.format(self)
        return make_pyproject_path(self.unpacked_source_directory)

    def load_pyproject_toml(self):
        """Load the pyproject.toml file.

        After calling this routine, all of the attributes related to PEP 517
        processing for this requirement have been set. In particular, the
        use_pep517 attribute can be used to determine whether we should
        follow the PEP 517 or legacy (setup.py) code path.
        """
        pyproject_toml_data = load_pyproject_toml(self.use_pep517, self.pyproject_toml_path, self.setup_py_path, str(self))
        if pyproject_toml_data is None:
            self.use_pep517 = False
            return
        self.use_pep517 = True
        requires, backend, check, backend_path = pyproject_toml_data
        self.requirements_to_check = check
        self.pyproject_requires = requires
        self.pep517_backend = Pep517HookCaller((self.unpacked_source_directory),
          backend, backend_path=backend_path)

    def _generate_metadata(self):
        """Invokes metadata generator functions, with the required arguments.
        """
        if not self.use_pep517:
            assert self.unpacked_source_directory
            return generate_metadata_legacy(build_env=(self.build_env),
              setup_py_path=(self.setup_py_path),
              source_dir=(self.unpacked_source_directory),
              isolated=(self.isolated),
              details=(self.name or 'from {}'.format(self.link)))
        assert self.pep517_backend is not None
        return generate_metadata(build_env=(self.build_env),
          backend=(self.pep517_backend))

    def prepare_metadata(self):
        """Ensure that project metadata is available.

        Under PEP 517, call the backend hook to prepare the metadata.
        Under legacy processing, call setup.py egg-info.
        """
        if not self.source_dir:
            raise AssertionError
        else:
            with indent_log():
                self.metadata_directory = self._generate_metadata()
            if not self.name:
                self._set_requirement()
            else:
                self.warn_on_mismatching_name()
        self.assert_source_matches_version()

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            self._metadata = get_metadata(self.get_dist())
        return self._metadata

    def get_dist(self):
        return _get_dist(self.metadata_directory)

    def assert_source_matches_version(self):
        assert self.source_dir
        version = self.metadata['version']
        if self.req.specifier and version not in self.req.specifier:
            logger.warning('Requested %s, but installing version %s', self, version)
        else:
            logger.debug('Source in %s has version %s, which satisfies requirement %s', display_path(self.source_dir), version, self)

    def ensure_has_source_dir(self, parent_dir, autodelete=False):
        """Ensure that a source_dir is set.

        This will create a temporary build dir if the name of the requirement
        isn't known yet.

        :param parent_dir: The ideal pip parent_dir for the source_dir.
            Generally src_dir for editables and build_dir for sdists.
        :return: self.source_dir
        """
        if self.source_dir is None:
            self.source_dir = self.ensure_build_location(parent_dir, autodelete)

    def update_editable(self, obtain=True):
        if not self.link:
            logger.debug('Cannot update repository at %s; repository location is unknown', self.source_dir)
            return
            if not self.editable:
                raise AssertionError
            else:
                assert self.source_dir
                if self.link.scheme == 'file':
                    return
                    assert '+' in self.link.url, ('bad url: {self.link.url!r}'.format)(**locals())
                    vc_type, url = self.link.url.split('+', 1)
                    vcs_backend = vcs.get_backend(vc_type)
                    if vcs_backend:
                        if not self.link.is_vcs:
                            reason = 'This form of VCS requirement is being deprecated: {}.'.format(self.link.url)
                            replacement = None
                            if self.link.url.startswith('git+git@'):
                                replacement = 'git+https://git@example.com/..., git+ssh://git@example.com/..., or the insecure git+git://git@example.com/...'
                            deprecated(reason, replacement, gone_in='21.0', issue=7554)
                        hidden_url = hide_url(self.link.url)
                        if obtain:
                            vcs_backend.obtain((self.source_dir), url=hidden_url)
                else:
                    vcs_backend.export((self.source_dir), url=hidden_url)
        else:
            assert 0, 'Unexpected version control type (in {}): {}'.format(self.link, vc_type)

    def uninstall(self, auto_confirm=False, verbose=False):
        """
        Uninstall the distribution currently satisfying this requirement.

        Prompts before removing or modifying files unless
        ``auto_confirm`` is True.

        Refuses to delete or modify files outside of ``sys.prefix`` -
        thus uninstallation within a virtual environment can only
        modify that virtual environment, even if the virtualenv is
        linked to global site-packages.

        """
        assert self.req
        try:
            dist = pkg_resources.get_distribution(self.req.name)
        except pkg_resources.DistributionNotFound:
            logger.warning('Skipping %s as it is not installed.', self.name)
            return
        else:
            logger.info('Found existing installation: %s', dist)
            uninstalled_pathset = UninstallPathSet.from_dist(dist)
            uninstalled_pathset.remove(auto_confirm, verbose)
            return uninstalled_pathset

    def _get_archive_name(self, path, parentdir, rootdir):

        def _clean_zip_name(name, prefix):
            assert name.startswith(prefix + os.path.sep), ("name {name!r} doesn't start with prefix {prefix!r}".format)(**locals())
            name = name[len(prefix) + 1:]
            name = name.replace(os.path.sep, '/')
            return name

        path = os.path.join(parentdir, path)
        name = _clean_zip_name(path, rootdir)
        return self.name + '/' + name

    def archive(self, build_dir):
        """Saves archive to provided build_dir.

        Used for saving downloaded VCS requirements as part of `pip download`.
        """
        if not self.source_dir:
            raise AssertionError
        else:
            create_archive = True
            archive_name = '{}-{}.zip'.format(self.name, self.metadata['version'])
            archive_path = os.path.join(build_dir, archive_name)
            if os.path.exists(archive_path):
                response = ask_path_exists('The file {} exists. (i)gnore, (w)ipe, (b)ackup, (a)bort '.format(display_path(archive_path)), ('i',
                                                                                                                                           'w',
                                                                                                                                           'b',
                                                                                                                                           'a'))
                if response == 'i':
                    create_archive = False
                else:
                    if response == 'w':
                        logger.warning('Deleting %s', display_path(archive_path))
                        os.remove(archive_path)
                    else:
                        if response == 'b':
                            dest_file = backup_dir(archive_path)
                            logger.warning('Backing up %s to %s', display_path(archive_path), display_path(dest_file))
                            shutil.move(archive_path, dest_file)
                        else:
                            if response == 'a':
                                sys.exit(-1)
            return create_archive or None
        zip_output = zipfile.ZipFile(archive_path,
          'w', (zipfile.ZIP_DEFLATED), allowZip64=True)
        with zip_output:
            dir = os.path.normcase(os.path.abspath(self.unpacked_source_directory))
            for dirpath, dirnames, filenames in os.walk(dir):
                for dirname in dirnames:
                    dir_arcname = self._get_archive_name(dirname,
                      parentdir=dirpath, rootdir=dir)
                    zipdir = zipfile.ZipInfo(dir_arcname + '/')
                    zipdir.external_attr = 32309248
                    zip_output.writestr(zipdir, '')

                for filename in filenames:
                    file_arcname = self._get_archive_name(filename,
                      parentdir=dirpath, rootdir=dir)
                    filename = os.path.join(dirpath, filename)
                    zip_output.write(filename, file_arcname)

        logger.info('Saved %s', display_path(archive_path))

    def install(self, install_options, global_options=None, root=None, home=None, prefix=None, warn_script_location=True, use_user_site=False, pycompile=True):
        scheme = get_scheme((self.name),
          user=use_user_site,
          home=home,
          root=root,
          isolated=(self.isolated),
          prefix=prefix)
        global_options = global_options if global_options is not None else []
        if self.editable:
            install_editable_legacy(install_options,
              global_options,
              prefix=prefix,
              home=home,
              use_user_site=use_user_site,
              name=(self.name),
              setup_py_path=(self.setup_py_path),
              isolated=(self.isolated),
              build_env=(self.build_env),
              unpacked_source_directory=(self.unpacked_source_directory))
            self.install_succeeded = True
            return
        if self.is_wheel:
            assert self.local_file_path
            direct_url = None
            if self.original_link:
                direct_url = direct_url_from_link(self.original_link, self.source_dir, self.original_link_is_in_wheel_cache)
            install_wheel((self.name),
              (self.local_file_path),
              scheme=scheme,
              req_description=(str(self.req)),
              pycompile=pycompile,
              warn_script_location=warn_script_location,
              direct_url=direct_url)
            self.install_succeeded = True
            return
        global_options = list(global_options) + self.global_options
        install_options = list(install_options) + self.install_options
        try:
            success = install_legacy(install_options=install_options,
              global_options=global_options,
              root=root,
              home=home,
              prefix=prefix,
              use_user_site=use_user_site,
              pycompile=pycompile,
              scheme=scheme,
              setup_py_path=(self.setup_py_path),
              isolated=(self.isolated),
              req_name=(self.name),
              build_env=(self.build_env),
              unpacked_source_directory=(self.unpacked_source_directory),
              req_description=(str(self.req)))
        except LegacyInstallFailure as exc:
            try:
                self.install_succeeded = False
                (six.reraise)(*exc.parent)
            finally:
                exc = None
                del exc

        except Exception:
            self.install_succeeded = True
            raise

        self.install_succeeded = success