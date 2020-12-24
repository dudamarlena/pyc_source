# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/req/req_install.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 36573 bytes
from __future__ import absolute_import
import atexit, logging, os, shutil, sys, sysconfig, zipfile
from distutils.util import change_root
from pip._vendor import pkg_resources, six
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.utils import canonicalize_name
from pip._vendor.packaging.version import Version
from pip._vendor.packaging.version import parse as parse_version
from pip._vendor.pep517.wrappers import Pep517HookCaller
from pip._internal import pep425tags, wheel
from pip._internal.build_env import NoOpBuildEnvironment
from pip._internal.exceptions import InstallationError
from pip._internal.models.link import Link
from pip._internal.operations.generate_metadata import get_metadata_generator
from pip._internal.pyproject import load_pyproject_toml, make_pyproject_path
from pip._internal.req.req_uninstall import UninstallPathSet
from pip._internal.utils.compat import native_str
from pip._internal.utils.hashes import Hashes
from pip._internal.utils.logging import indent_log
from pip._internal.utils.marker_files import PIP_DELETE_MARKER_FILENAME, has_delete_marker_file
from pip._internal.utils.misc import _make_build_dir, ask_path_exists, backup_dir, display_path, dist_in_site_packages, dist_in_usersite, ensure_dir, get_installed_version, hide_url, redact_auth_from_url, rmtree
from pip._internal.utils.packaging import get_metadata
from pip._internal.utils.setuptools_build import make_setuptools_shim_args
from pip._internal.utils.subprocess import call_subprocess, runner_with_spinner_message
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv
from pip._internal.vcs import vcs
if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, Iterable, List, Optional, Sequence, Union
    from pip._internal.build_env import BuildEnvironment
    from pip._internal.cache import WheelCache
    from pip._internal.index import PackageFinder
    from pip._vendor.pkg_resources import Distribution
    from pip._vendor.packaging.specifiers import SpecifierSet
    from pip._vendor.packaging.markers import Marker
logger = logging.getLogger(__name__)

class InstallRequirement(object):
    __doc__ = '\n    Represents something that may be installed later on, may have information\n    about where to fetch the relevant requirement and also contains logic for\n    installing the said requirement.\n    '

    def __init__(self, req, comes_from, source_dir=None, editable=False, link=None, markers=None, use_pep517=None, isolated=False, options=None, wheel_cache=None, constraint=False, extras=()):
        if not req is None:
            if not isinstance(req, Requirement):
                raise AssertionError(req)
        else:
            self.req = req
            self.comes_from = comes_from
            self.constraint = constraint
            if source_dir is None:
                self.source_dir = None
            else:
                self.source_dir = os.path.normpath(os.path.abspath(source_dir))
            self.editable = editable
            self._wheel_cache = wheel_cache
            if link is None:
                if req:
                    if req.url:
                        link = Link(req.url)
            self.link = self.original_link = link
            if extras:
                self.extras = extras
            else:
                if req:
                    self.extras = {pkg_resources.safe_extra(extra) for extra in req.extras}
                else:
                    self.extras = set()
        if markers is None:
            if req:
                markers = req.marker
        self.markers = markers
        self.satisfied_by = None
        self.conflicts_with = None
        self._temp_build_dir = None
        self._ideal_build_dir = None
        self.install_succeeded = None
        self.options = options if options else {}
        self.prepared = False
        self.is_direct = False
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
                s += ' from %s' % redact_auth_from_url(self.link.url)
        else:
            if self.link:
                s = redact_auth_from_url(self.link.url)
            else:
                s = '<InstallRequirement>'
            if self.satisfied_by is not None:
                s += ' in %s' % display_path(self.satisfied_by.location)
            if self.comes_from:
                if isinstance(self.comes_from, six.string_types):
                    comes_from = self.comes_from
                else:
                    comes_from = self.comes_from.from_path()
                if comes_from:
                    s += ' (from %s)' % comes_from
        return s

    def __repr__(self):
        return '<%s object: %s editable=%r>' % (
         self.__class__.__name__, str(self), self.editable)

    def format_debug(self):
        """An un-tested helper for getting state, for debugging.
        """
        attributes = vars(self)
        names = sorted(attributes)
        state = ('{}={!r}'.format(attr, attributes[attr]) for attr in sorted(names))
        return '<{name} object: {{{state}}}>'.format(name=(self.__class__.__name__),
          state=(', '.join(state)))

    def populate_link(self, finder, upgrade, require_hashes):
        """Ensure that if a link can be found for this, that it is found.

        Note that self.link may still be None - if Upgrade is False and the
        requirement is already installed.

        If require_hashes is True, don't use the wheel cache, because cached
        wheels, always built locally, have different hashes than the files
        downloaded from the index server and thus throw false hash mismatches.
        Furthermore, cached wheels at present have undeterministic contents due
        to file modification times.
        """
        if self.link is None:
            self.link = finder.find_requirement(self, upgrade)
        if self._wheel_cache is not None:
            if not require_hashes:
                old_link = self.link
                supported_tags = pep425tags.get_supported()
                self.link = self._wheel_cache.get(link=(self.link),
                  package_name=(self.name),
                  supported_tags=supported_tags)
                if old_link != self.link:
                    logger.debug('Using cached wheel link: %s', self.link)

    @property
    def name(self):
        if self.req is None:
            return
        else:
            return native_str(pkg_resources.safe_name(self.req.name))

    @property
    def specifier(self):
        return self.req.specifier

    @property
    def is_pinned(self):
        """Return whether I am pinned to an exact version.

        For example, some-package==1.2 is pinned; some-package>1.2 is not.
        """
        specifiers = self.specifier
        return len(specifiers) == 1 and next(iter(specifiers)).operator in frozenset({'==', '==='})

    @property
    def installed_version(self):
        return get_installed_version(self.name)

    def match_markers(self, extras_requested=None):
        if not extras_requested:
            extras_requested = ('', )
        if self.markers is not None:
            return any(self.markers.evaluate({'extra': extra}) for extra in extras_requested)
        else:
            return True

    @property
    def has_hash_options(self):
        """Return whether any known-good hashes are specified as options.

        These activate --require-hashes mode; hashes specified as part of a
        URL do not.

        """
        return bool(self.options.get('hashes', {}))

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
        good_hashes = self.options.get('hashes', {}).copy()
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
        else:
            s = str(self.req)
            if self.comes_from:
                if isinstance(self.comes_from, six.string_types):
                    comes_from = self.comes_from
                else:
                    comes_from = self.comes_from.from_path()
                if comes_from:
                    s += '->' + comes_from
            return s

    def ensure_build_location(self, build_dir):
        assert build_dir is not None
        if self._temp_build_dir is not None:
            assert self._temp_build_dir.path
            return self._temp_build_dir.path
        if self.req is None:
            self._temp_build_dir = TempDirectory(kind='req-build')
            self._ideal_build_dir = build_dir
            return self._temp_build_dir.path
        else:
            if self.editable:
                name = self.name.lower()
            else:
                name = self.name
            if not os.path.exists(build_dir):
                logger.debug('Creating directory %s', build_dir)
                _make_build_dir(build_dir)
            return os.path.join(build_dir, name)

    def move_to_correct_build_directory(self):
        """Move self._temp_build_dir to "self._ideal_build_dir/self.req.name"

        For some requirements (e.g. a path to a directory), the name of the
        package is not available until we run egg_info, so the build_location
        will return a temporary directory and store the _ideal_build_dir.

        This is only called to "fix" the build directory after generating
        metadata.
        """
        if self.source_dir is not None:
            return
        else:
            if not self.req is not None:
                raise AssertionError
            else:
                if not self._temp_build_dir:
                    raise AssertionError
                elif not (self._ideal_build_dir is not None and self._ideal_build_dir.path):
                    raise AssertionError
                old_location = self._temp_build_dir
                self._temp_build_dir = None
                new_location = self.ensure_build_location(self._ideal_build_dir)
                if os.path.exists(new_location):
                    raise InstallationError('A package already exists in %s; please remove it to continue' % display_path(new_location))
            logger.debug('Moving package %s from %s to new location %s', self, display_path(old_location.path), display_path(new_location))
            shutil.move(old_location.path, new_location)
            self.source_dir = os.path.normpath(os.path.abspath(new_location))
            self._temp_build_dir = TempDirectory(path=new_location,
              kind='req-install')
            if self.metadata_directory:
                old_meta = self.metadata_directory
                rel = os.path.relpath(old_meta, start=(old_location.path))
                new_meta = os.path.join(new_location, rel)
                new_meta = os.path.normpath(os.path.abspath(new_meta))
                self.metadata_directory = new_meta
        self._ideal_build_dir = None

    def remove_temporary_source(self):
        """Remove the source files from this requirement, if they are marked
        for deletion"""
        if self.source_dir:
            if has_delete_marker_file(self.source_dir):
                logger.debug('Removing source in %s', self.source_dir)
                rmtree(self.source_dir)
        self.source_dir = None
        if self._temp_build_dir:
            self._temp_build_dir.cleanup()
            self._temp_build_dir = None
        self.build_env.cleanup()

    def check_if_exists(self, use_user_site):
        """Find an installed distribution that satisfies or conflicts
        with this requirement, and set self.satisfied_by or
        self.conflicts_with appropriately.
        """
        if self.req is None:
            return False
        else:
            try:
                no_marker = Requirement(str(self.req))
                no_marker.marker = None
                self.satisfied_by = pkg_resources.get_distribution(str(no_marker))
                if self.editable:
                    if self.satisfied_by:
                        self.conflicts_with = self.satisfied_by
                        self.satisfied_by = None
                        return True
            except pkg_resources.DistributionNotFound:
                return False
            except pkg_resources.VersionConflict:
                existing_dist = pkg_resources.get_distribution(self.req.name)
                if use_user_site:
                    if dist_in_usersite(existing_dist):
                        self.conflicts_with = existing_dist
                    elif running_under_virtualenv():
                        if dist_in_site_packages(existing_dist):
                            raise InstallationError('Will not install to the user site because it will lack sys.path precedence to %s in %s' % (
                             existing_dist.project_name, existing_dist.location))
                else:
                    self.conflicts_with = existing_dist

            return True

    @property
    def is_wheel(self):
        if not self.link:
            return False
        else:
            return self.link.is_wheel

    def move_wheel_files(self, wheeldir, root=None, home=None, prefix=None, warn_script_location=True, use_user_site=False, pycompile=True):
        wheel.move_wheel_files((self.name),
          (self.req), wheeldir, user=use_user_site,
          home=home,
          root=root,
          prefix=prefix,
          pycompile=pycompile,
          isolated=(self.isolated),
          warn_script_location=warn_script_location)

    @property
    def unpacked_source_directory(self):
        return os.path.join(self.source_dir, self.link and self.link.subdirectory_fragment or '')

    @property
    def setup_py_path(self):
        assert self.source_dir, 'No source dir for %s' % self
        setup_py = os.path.join(self.unpacked_source_directory, 'setup.py')
        if six.PY2:
            if isinstance(setup_py, six.text_type):
                setup_py = setup_py.encode(sys.getfilesystemencoding())
        return setup_py

    @property
    def pyproject_toml_path(self):
        assert self.source_dir, 'No source dir for %s' % self
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
        requires, backend, check = pyproject_toml_data
        self.requirements_to_check = check
        self.pyproject_requires = requires
        self.pep517_backend = Pep517HookCaller(self.unpacked_source_directory, backend)

    def prepare_metadata(self):
        """Ensure that project metadata is available.

        Under PEP 517, call the backend hook to prepare the metadata.
        Under legacy processing, call setup.py egg-info.
        """
        assert self.source_dir
        metadata_generator = get_metadata_generator(self)
        with indent_log():
            self.metadata_directory = metadata_generator(self)
        if not self.req:
            if isinstance(parse_version(self.metadata['Version']), Version):
                op = '=='
            else:
                op = '==='
            self.req = Requirement(''.join([
             self.metadata['Name'],
             op,
             self.metadata['Version']]))
            self.move_to_correct_build_directory()
        else:
            metadata_name = canonicalize_name(self.metadata['Name'])
        if canonicalize_name(self.req.name) != metadata_name:
            logger.warning('Generating metadata for package %s produced metadata for project name %s. Fix your #egg=%s fragments.', self.name, metadata_name, self.name)
            self.req = Requirement(metadata_name)

    def prepare_pep517_metadata(self):
        assert self.pep517_backend is not None
        metadata_tmpdir = TempDirectory(kind='modern-metadata')
        atexit.register(metadata_tmpdir.cleanup)
        metadata_dir = metadata_tmpdir.path
        with self.build_env:
            runner = runner_with_spinner_message('Preparing wheel metadata')
            backend = self.pep517_backend
            with backend.subprocess_runner(runner):
                distinfo_dir = backend.prepare_metadata_for_build_wheel(metadata_dir)
        return os.path.join(metadata_dir, distinfo_dir)

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            self._metadata = get_metadata(self.get_dist())
        return self._metadata

    def get_dist(self):
        """Return a pkg_resources.Distribution for this requirement"""
        dist_dir = self.metadata_directory.rstrip(os.sep)
        if dist_dir.endswith('.egg-info'):
            dist_cls = pkg_resources.Distribution
        else:
            assert dist_dir.endswith('.dist-info')
            dist_cls = pkg_resources.DistInfoDistribution
        base_dir, dist_dir_name = os.path.split(dist_dir)
        dist_name = os.path.splitext(dist_dir_name)[0]
        metadata = pkg_resources.PathMetadata(base_dir, dist_dir)
        return dist_cls(base_dir,
          project_name=dist_name,
          metadata=metadata)

    def assert_source_matches_version(self):
        if not self.source_dir:
            raise AssertionError
        else:
            version = self.metadata['version']
            if self.req.specifier and version not in self.req.specifier:
                logger.warning('Requested %s, but installing version %s', self, version)
            else:
                logger.debug('Source in %s has version %s, which satisfies requirement %s', display_path(self.source_dir), version, self)

    def ensure_has_source_dir(self, parent_dir):
        """Ensure that a source_dir is set.

        This will create a temporary build dir if the name of the requirement
        isn't known yet.

        :param parent_dir: The ideal pip parent_dir for the source_dir.
            Generally src_dir for editables and build_dir for sdists.
        :return: self.source_dir
        """
        if self.source_dir is None:
            self.source_dir = self.ensure_build_location(parent_dir)

    def install_editable(self, install_options, global_options=(), prefix=None):
        logger.info('Running setup.py develop for %s', self.name)
        if prefix:
            prefix_param = [
             '--prefix={}'.format(prefix)]
            install_options = list(install_options) + prefix_param
        base_cmd = make_setuptools_shim_args((self.setup_py_path),
          global_options=global_options,
          no_user_config=(self.isolated))
        with indent_log():
            with self.build_env:
                call_subprocess((base_cmd + ['develop', '--no-deps'] + list(install_options)),
                  cwd=(self.unpacked_source_directory))
        self.install_succeeded = True

    def update_editable(self, obtain=True):
        if not self.link:
            logger.debug('Cannot update repository at %s; repository location is unknown', self.source_dir)
            return
        elif not self.editable:
            raise AssertionError
        else:
            if not self.source_dir:
                raise AssertionError
            else:
                if self.link.scheme == 'file':
                    return
                assert '+' in self.link.url, 'bad url: %r' % self.link.url
            vc_type, url = self.link.url.split('+', 1)
            vcs_backend = vcs.get_backend(vc_type)
            if vcs_backend:
                hidden_url = hide_url(self.link.url)
                if obtain:
                    vcs_backend.obtain((self.source_dir), url=hidden_url)
                else:
                    vcs_backend.export((self.source_dir), url=hidden_url)
            elif not 0:
                raise AssertionError('Unexpected version control type (in %s): %s' % (
                 self.link, vc_type))

    def uninstall(self, auto_confirm=False, verbose=False, use_user_site=False):
        """
        Uninstall the distribution currently satisfying this requirement.

        Prompts before removing or modifying files unless
        ``auto_confirm`` is True.

        Refuses to delete or modify files outside of ``sys.prefix`` -
        thus uninstallation within a virtual environment can only
        modify that virtual environment, even if the virtualenv is
        linked to global site-packages.

        """
        if not self.check_if_exists(use_user_site):
            logger.warning('Skipping %s as it is not installed.', self.name)
            return
        else:
            dist = self.satisfied_by or self.conflicts_with
            uninstalled_pathset = UninstallPathSet.from_dist(dist)
            uninstalled_pathset.remove(auto_confirm, verbose)
            return uninstalled_pathset

    def _clean_zip_name(self, name, prefix):
        assert name.startswith(prefix + os.path.sep), "name %r doesn't start with prefix %r" % (name, prefix)
        name = name[len(prefix) + 1:]
        name = name.replace(os.path.sep, '/')
        return name

    def _get_archive_name(self, path, parentdir, rootdir):
        path = os.path.join(parentdir, path)
        name = self._clean_zip_name(path, rootdir)
        return self.name + '/' + name

    def archive(self, build_dir):
        """Saves archive to provided build_dir.

        Used for saving downloaded VCS requirements as part of `pip download`.
        """
        if not self.source_dir:
            raise AssertionError
        else:
            create_archive = True
            archive_name = '%s-%s.zip' % (self.name, self.metadata['version'])
            archive_path = os.path.join(build_dir, archive_name)
            if os.path.exists(archive_path):
                response = ask_path_exists('The file %s exists. (i)gnore, (w)ipe, (b)ackup, (a)bort ' % display_path(archive_path), ('i',
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
                        elif response == 'a':
                            sys.exit(-1)
            if not create_archive:
                return
        zip_output = zipfile.ZipFile(archive_path,
          'w', (zipfile.ZIP_DEFLATED), allowZip64=True)
        with zip_output:
            dir = os.path.normcase(os.path.abspath(self.unpacked_source_directory))
            for dirpath, dirnames, filenames in os.walk(dir):
                if 'pip-egg-info' in dirnames:
                    dirnames.remove('pip-egg-info')
                for dirname in dirnames:
                    dir_arcname = self._get_archive_name(dirname,
                      parentdir=dirpath, rootdir=dir)
                    zipdir = zipfile.ZipInfo(dir_arcname + '/')
                    zipdir.external_attr = 32309248
                    zip_output.writestr(zipdir, '')

                for filename in filenames:
                    if filename == PIP_DELETE_MARKER_FILENAME:
                        pass
                    else:
                        file_arcname = self._get_archive_name(filename,
                          parentdir=dirpath, rootdir=dir)
                        filename = os.path.join(dirpath, filename)
                        zip_output.write(filename, file_arcname)

        logger.info('Saved %s', display_path(archive_path))

    def install(self, install_options, global_options=None, root=None, home=None, prefix=None, warn_script_location=True, use_user_site=False, pycompile=True):
        global_options = global_options if global_options is not None else []
        if self.editable:
            self.install_editable(install_options,
              global_options, prefix=prefix)
            return
        if self.is_wheel:
            version = wheel.wheel_version(self.source_dir)
            wheel.check_compatibility(version, self.name)
            self.move_wheel_files((self.source_dir),
              root=root, prefix=prefix, home=home, warn_script_location=warn_script_location,
              use_user_site=use_user_site,
              pycompile=pycompile)
            self.install_succeeded = True
            return
        global_options = list(global_options) + self.options.get('global_options', [])
        install_options = list(install_options) + self.options.get('install_options', [])
        with TempDirectory(kind='record') as (temp_dir):
            record_filename = os.path.join(temp_dir.path, 'install-record.txt')
            install_args = self.get_install_args(global_options, record_filename, root, prefix, pycompile)
            runner = runner_with_spinner_message('Running setup.py install for {}'.format(self.name))
            with indent_log():
                with self.build_env:
                    runner(cmd=(install_args + install_options),
                      cwd=(self.unpacked_source_directory))
            if not os.path.exists(record_filename):
                logger.debug('Record file %s not found', record_filename)
                return
            self.install_succeeded = True

            def prepend_root(path):
                if root is None or not os.path.isabs(path):
                    return path
                else:
                    return change_root(root, path)

            with open(record_filename) as (f):
                for line in f:
                    directory = os.path.dirname(line)
                    if directory.endswith('.egg-info'):
                        egg_info_dir = prepend_root(directory)
                        break
                else:
                    logger.warning('Could not find .egg-info directory in install record for %s', self)
                    return

            new_lines = []
            with open(record_filename) as (f):
                for line in f:
                    filename = line.strip()
                    if os.path.isdir(filename):
                        filename += os.path.sep
                    new_lines.append(os.path.relpath(prepend_root(filename), egg_info_dir))

            new_lines.sort()
            ensure_dir(egg_info_dir)
            inst_files_path = os.path.join(egg_info_dir, 'installed-files.txt')
            with open(inst_files_path, 'w') as (f):
                f.write('\n'.join(new_lines) + '\n')

    def get_install_args(self, global_options, record_filename, root, prefix, pycompile):
        install_args = make_setuptools_shim_args((self.setup_py_path),
          global_options=global_options,
          no_user_config=(self.isolated),
          unbuffered_output=True)
        install_args += ['install', '--record', record_filename]
        install_args += ['--single-version-externally-managed']
        if root is not None:
            install_args += ['--root', root]
        else:
            if prefix is not None:
                install_args += ['--prefix', prefix]
            if pycompile:
                install_args += ['--compile']
            else:
                install_args += ['--no-compile']
        if running_under_virtualenv():
            py_ver_str = 'python' + sysconfig.get_python_version()
            install_args += ['--install-headers',
             os.path.join(sys.prefix, 'include', 'site', py_ver_str, self.name)]
        return install_args