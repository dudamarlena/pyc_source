# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/packaging.py
# Compiled at: 2017-12-12 12:08:29
"""
Utilities with minimum-depends for use in setup.py
"""
from __future__ import unicode_literals
from distutils.command import install as du_install
from distutils import log
import email, email.errors, os, re, sys, pkg_resources, setuptools
from setuptools.command import develop
from setuptools.command import easy_install
from setuptools.command import egg_info
from setuptools.command import install
from setuptools.command import install_scripts
from setuptools.command import sdist
from pbr import extra_files
from pbr import git
from pbr import options
import pbr.pbr_json
from pbr import pipfile
from pbr import testr_command
from pbr import version
try:
    basestring
except NameError:
    basestring = str

REQUIREMENTS_FILES = ('requirements.txt', 'tools/pip-requires')
TEST_REQUIREMENTS_FILES = ('test-requirements.txt', 'tools/test-requires')

def get_requirements_files():
    files = os.environ.get(b'PBR_REQUIREMENTS_FILES')
    if files:
        return tuple(f.strip() for f in files.split(b','))
    return list(map((b'-py' + str(sys.version_info[0])).join, map(os.path.splitext, REQUIREMENTS_FILES))) + list(REQUIREMENTS_FILES)


def append_text_list(config, key, text_list):
    """Append a 
 separated list to possibly existing value."""
    new_value = []
    current_value = config.get(key, b'')
    if current_value:
        new_value.append(current_value)
    new_value.extend(text_list)
    config[key] = (b'\n').join(new_value)


def _any_existing(file_list):
    return [ f for f in file_list if os.path.exists(f) ]


def get_reqs_from_files(requirements_files):
    for requirements_file in _any_existing(requirements_files):
        with open(requirements_file, b'r') as (fil):
            return fil.read().split(b'\n')

    return []


def parse_pipfile(pipfile_path=None):
    """Parse a pipfile if present

    Returns None if no Pipfile is found.
    Returns an empty list if a Pipfile is found but no dependency are found.
    Returns a list of dependencies if found
    """
    if pipfile_path is None:
        pipfile_path = b'Pipfile'
    if not os.path.exists(pipfile_path):
        return
    else:
        pfl = pipfile.load(pipfile_path)
        requirements = []
        for pkg_name, pkg_cfg in pfl.data.get(b'default', {}).items():
            if isinstance(pkg_cfg, basestring):
                pkg_cfg = pkg_cfg.strip()
                if not pkg_cfg or pkg_cfg == b'*':
                    requirements.append(pkg_name)
                else:
                    requirements.append(pkg_name + pkg_cfg)
            else:
                git = pkg_cfg.get(b'git')
                editable = pkg_cfg.get(b'editable')
                path = pkg_cfg.get(b'path')
                fil = pkg_cfg.get(b'file')
                version = pkg_cfg.get(b'version')
                ref = pkg_cfg.get(b'ref')
                if version:
                    version = version.strip()
                    if version == b'*':
                        version = None
                if fil:
                    continue
                if editable:
                    line = b'-e '
                else:
                    line = b''
                if git:
                    if ref:
                        line += (b'git+{0}@{1}#{1}').format(git, ref, pkg_name)
                    else:
                        line += (b'git+{0}#{1}').format(git, pkg_name)
                    requirements.append(line)
                elif path:
                    continue
                else:
                    line += pkg_name
                    if version:
                        line += version
                    requirements.append(line)

        return requirements


def parse_requirements(requirements_files=None, strip_markers=False):
    if requirements_files is None:
        requirements_files = get_requirements_files()
    for requirements_file in requirements_files:
        if os.path.basename(requirements_file) == b'Pipfile':
            requirements = parse_pipfile(requirements_file)
            break
    else:
        requirements = parse_pipfile()

    if requirements is not None:
        return requirements
    else:

        def egg_fragment(match):
            return re.sub(b'([\\w.]+)-([\\w.-]+)', b'\\1>=\\2', match.groups()[(-1)])

        requirements = []
        for line in get_reqs_from_files(requirements_files):
            if not line.strip() or line.startswith(b'#'):
                continue
            if re.match(b'^\\s*(-i|--index-url|--extra-index-url).*', line):
                continue
            if line.startswith(b'-r'):
                req_file = line.partition(b' ')[2]
                requirements += parse_requirements([
                 req_file], strip_markers=strip_markers)
                continue
            try:
                project_name = pkg_resources.Requirement.parse(line).project_name
            except ValueError:
                project_name = None

            if re.match(b'\\s*-e\\s+', line):
                line = re.sub(b'\\s*-e\\s+.*#egg=(.*)$', egg_fragment, line)
            elif re.match(b'\\s*(https?|git(\\+(https|ssh))?):', line):
                line = re.sub(b'\\s*(https?|git(\\+(https|ssh))?):.*#egg=(.*)$', egg_fragment, line)
            elif re.match(b'\\s*-f\\s+', line):
                line = None
                reason = b'Index Location'
            if line is not None:
                line = re.sub(b'#.*$', b'', line)
                if strip_markers:
                    semi_pos = line.find(b';')
                    if semi_pos < 0:
                        semi_pos = None
                    line = line[:semi_pos]
                requirements.append(line)
            else:
                log.info(b'[pbr] Excluding %s: %s' % (project_name, reason))

        return requirements


def parse_dependency_links(requirements_files=None):
    if requirements_files is None:
        requirements_files = get_requirements_files()
    dependency_links = []
    for line in get_reqs_from_files(requirements_files):
        if re.match(b'(\\s*#)|(\\s*$)', line):
            continue
        if re.match(b'\\s*-[ef]\\s+', line):
            dependency_links.append(re.sub(b'\\s*-[ef]\\s+', b'', line))
        elif re.match(b'\\s*(https?|git(\\+(https|ssh))?):', line):
            dependency_links.append(line)

    return dependency_links


class InstallWithGit(install.install):
    """Extracts ChangeLog and AUTHORS from git then installs.

    This is useful for e.g. readthedocs where the package is
    installed and then docs built.
    """
    command_name = b'install'

    def run(self):
        _from_git(self.distribution)
        return install.install.run(self)


class LocalInstall(install.install):
    """Runs python setup.py install in a sensible manner.

    Force a non-egg installed in the manner of
    single-version-externally-managed, which allows us to install manpages
    and config files.
    """
    command_name = b'install'

    def run(self):
        _from_git(self.distribution)
        return du_install.install.run(self)


class TestrTest(testr_command.Testr):
    """Make setup.py test do the right thing."""
    command_name = b'test'

    def run(self):
        testr_command.Testr.run(self)


class LocalRPMVersion(setuptools.Command):
    """Output the rpm *compatible* version string of this package"""
    description = __doc__
    user_options = []
    command_name = b'rpm_version'

    def run(self):
        log.info(b'[pbr] Extracting rpm version')
        name = self.distribution.get_name()
        print version.VersionInfo(name).semantic_version().rpm_string()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class LocalDebVersion(setuptools.Command):
    """Output the deb *compatible* version string of this package"""
    description = __doc__
    user_options = []
    command_name = b'deb_version'

    def run(self):
        log.info(b'[pbr] Extracting deb version')
        name = self.distribution.get_name()
        print version.VersionInfo(name).semantic_version().debian_string()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def have_testr():
    return testr_command.have_testr


try:
    from nose import commands

    class NoseTest(commands.nosetests):
        """Fallback test runner if testr is a no-go."""
        command_name = b'test'

        def run(self):
            commands.nosetests.run(self)


    _have_nose = True
except ImportError:
    _have_nose = False

def have_nose():
    return _have_nose


_wsgi_text = b'#PBR Generated from %(group)r\n\nimport threading\n\nfrom %(module_name)s import %(import_target)s\n\nif __name__ == "__main__":\n    import argparse\n    import socket\n    import sys\n    import wsgiref.simple_server as wss\n\n    my_ip = socket.gethostbyname(socket.gethostname())\n\n    parser = argparse.ArgumentParser(\n        description=%(import_target)s.__doc__,\n        formatter_class=argparse.ArgumentDefaultsHelpFormatter,\n        usage=\'%%(prog)s [-h] [--port PORT] [--host IP] -- [passed options]\')\n    parser.add_argument(\'--port\', \'-p\', type=int, default=8000,\n                        help=\'TCP port to listen on\')\n    parser.add_argument(\'--host\', \'-b\', default=\'\',\n                        help=\'IP to bind the server to\')\n    parser.add_argument(\'args\',\n                        nargs=argparse.REMAINDER,\n                        metavar=\'-- [passed options]\',\n                        help="\'--\' is the separator of the arguments used "\n                        "to start the WSGI server and the arguments passed "\n                        "to the WSGI application.")\n    args = parser.parse_args()\n    if args.args:\n        if args.args[0] == \'--\':\n            args.args.pop(0)\n        else:\n            parser.error("unrecognized arguments: %%s" %% \' \'.join(args.args))\n    sys.argv[1:] = args.args\n    server = wss.make_server(args.host, args.port, %(invoke_target)s())\n\n    print("*" * 80)\n    print("STARTING test server %(module_name)s.%(invoke_target)s")\n    url = "http://%%s:%%d/" %% (server.server_name, server.server_port)\n    print("Available at %%s" %% url)\n    print("DANGER! For testing only, do not use in production")\n    print("*" * 80)\n    sys.stdout.flush()\n\n    server.serve_forever()\nelse:\n    application = None\n    app_lock = threading.Lock()\n\n    with app_lock:\n        if application is None:\n            application = %(invoke_target)s()\n\n'
_script_text = b'# PBR Generated from %(group)r\n\nimport sys\n\nfrom %(module_name)s import %(import_target)s\n\n\nif __name__ == "__main__":\n    sys.exit(%(invoke_target)s())\n'
ENTRY_POINTS_MAP = {b'console_scripts': _script_text, 
   b'gui_scripts': _script_text, 
   b'wsgi_scripts': _wsgi_text}

def generate_script(group, entry_point, header, template):
    """Generate the script based on the template.

    :param str group:
        The entry-point group name, e.g., "console_scripts".
    :param str header:
        The first line of the script, e.g., "!#/usr/bin/env python".
    :param str template:
        The script template.
    :returns:
        The templated script content
    :rtype:
        str
    """
    if not entry_point.attrs or len(entry_point.attrs) > 2:
        raise ValueError(b"Script targets must be of the form 'func' or 'Class.class_method'.")
    script_text = template % dict(group=group, module_name=entry_point.module_name, import_target=entry_point.attrs[0], invoke_target=(b'.').join(entry_point.attrs))
    return header + script_text


def override_get_script_args(dist, executable=os.path.normpath(sys.executable), is_wininst=False):
    """Override entrypoints console_script."""
    header = easy_install.get_script_header(b'', executable, is_wininst)
    for group, template in ENTRY_POINTS_MAP.items():
        for name, ep in dist.get_entry_map(group).items():
            yield (
             name, generate_script(group, ep, header, template))


class LocalDevelop(develop.develop):
    command_name = b'develop'

    def install_wrapper_scripts(self, dist):
        if not self.exclude_scripts:
            for args in override_get_script_args(dist):
                self.write_script(*args)


class LocalInstallScripts(install_scripts.install_scripts):
    """Intercepts console scripts entry_points."""
    command_name = b'install_scripts'

    def _make_wsgi_scripts_only(self, dist, executable, is_wininst):
        header = easy_install.get_script_header(b'', executable, is_wininst)
        wsgi_script_template = ENTRY_POINTS_MAP[b'wsgi_scripts']
        for name, ep in dist.get_entry_map(b'wsgi_scripts').items():
            content = generate_script(b'wsgi_scripts', ep, header, wsgi_script_template)
            self.write_script(name, content)

    def run(self):
        import distutils.command.install_scripts
        self.run_command(b'egg_info')
        if self.distribution.scripts:
            distutils.command.install_scripts.install_scripts.run(self)
        else:
            self.outfiles = []
        ei_cmd = self.get_finalized_command(b'egg_info')
        dist = pkg_resources.Distribution(ei_cmd.egg_base, pkg_resources.PathMetadata(ei_cmd.egg_base, ei_cmd.egg_info), ei_cmd.egg_name, ei_cmd.egg_version)
        bs_cmd = self.get_finalized_command(b'build_scripts')
        executable = getattr(bs_cmd, b'executable', easy_install.sys_executable)
        is_wininst = getattr(self.get_finalized_command(b'bdist_wininst'), b'_is_running', False)
        if b'bdist_wheel' in self.distribution.have_run:
            self._make_wsgi_scripts_only(dist, executable, is_wininst)
        if self.no_ep:
            return
        for args in override_get_script_args(dist, executable, is_wininst):
            self.write_script(*args)


class LocalManifestMaker(egg_info.manifest_maker):
    """Add any files that are in git and some standard sensible files."""

    def _add_pbr_defaults(self):
        for template_line in [
         b'include AUTHORS',
         b'include ChangeLog',
         b'exclude .gitignore',
         b'exclude .gitreview',
         b'global-exclude *.pyc']:
            self.filelist.process_template_line(template_line)

    def add_defaults(self):
        option_dict = self.distribution.get_option_dict(b'pbr')
        sdist.sdist.add_defaults(self)
        self.filelist.append(self.template)
        self.filelist.append(self.manifest)
        self.filelist.extend(extra_files.get_extra_files())
        should_skip = options.get_boolean_option(option_dict, b'skip_git_sdist', b'SKIP_GIT_SDIST')
        if not should_skip:
            rcfiles = git._find_git_files()
            if rcfiles:
                self.filelist.extend(rcfiles)
        elif os.path.exists(self.manifest):
            self.read_manifest()
        ei_cmd = self.get_finalized_command(b'egg_info')
        self._add_pbr_defaults()
        self.filelist.include_pattern(b'*', prefix=ei_cmd.egg_info)


class LocalEggInfo(egg_info.egg_info):
    """Override the egg_info command to regenerate SOURCES.txt sensibly."""
    command_name = b'egg_info'

    def find_sources(self):
        """Generate SOURCES.txt only if there isn't one already.

        If we are in an sdist command, then we always want to update
        SOURCES.txt. If we are not in an sdist command, then it doesn't
        matter one flip, and is actually destructive.
        However, if we're in a git context, it's always the right thing to do
        to recreate SOURCES.txt
        """
        manifest_filename = os.path.join(self.egg_info, b'SOURCES.txt')
        if not os.path.exists(manifest_filename) or os.path.exists(b'.git') or b'sdist' in sys.argv:
            log.info(b'[pbr] Processing SOURCES.txt')
            mm = LocalManifestMaker(self.distribution)
            mm.manifest = manifest_filename
            mm.run()
            self.filelist = mm.filelist
        else:
            log.info(b'[pbr] Reusing existing SOURCES.txt')
            self.filelist = egg_info.FileList()
            for entry in open(manifest_filename, b'r').read().split(b'\n'):
                self.filelist.append(entry)


def _from_git(distribution):
    option_dict = distribution.get_option_dict(b'pbr')
    changelog = git._iter_log_oneline()
    if changelog:
        changelog = git._iter_changelog(changelog)
    git.write_git_changelog(option_dict=option_dict, changelog=changelog)
    git.generate_authors(option_dict=option_dict)


class LocalSDist(sdist.sdist):
    """Builds the ChangeLog and Authors files from VC first."""
    command_name = b'sdist'

    def checking_reno(self):
        """Ensure reno is installed and configured.

        We can't run reno-based commands if reno isn't installed/available, and
        don't want to if the user isn't using it.
        """
        if hasattr(self, b'_has_reno'):
            return self._has_reno
        try:
            from reno import setup_command
        except ImportError:
            log.info(b'[pbr] reno was not found or is too old. Skipping release notes')
            self._has_reno = False
            return False

        conf, output_file, cache_file = setup_command.load_config(self.distribution)
        if not os.path.exists(os.path.join(conf.reporoot, conf.notespath)):
            log.info(b'[pbr] reno does not appear to be configured. Skipping release notes')
            self._has_reno = False
            return False
        self._files = [output_file, cache_file]
        log.info(b'[pbr] Generating release notes')
        self._has_reno = True
        return True

    sub_commands = [
     (
      b'build_reno', checking_reno)] + sdist.sdist.sub_commands

    def run(self):
        _from_git(self.distribution)
        sdist.sdist.run(self)

    def make_distribution(self):
        if self.checking_reno():
            self.filelist.extend(self._files)
            self.filelist.sort()
        sdist.sdist.make_distribution(self)


try:
    from pbr import builddoc
    _have_sphinx = True
    LocalBuildDoc = builddoc.LocalBuildDoc
except ImportError:
    _have_sphinx = False
    LocalBuildDoc = None

def have_sphinx():
    return _have_sphinx


def _get_increment_kwargs(git_dir, tag):
    """Calculate the sort of semver increment needed from git history.

    Every commit from HEAD to tag is consider for Sem-Ver metadata lines.
    See the pbr docs for their syntax.

    :return: a dict of kwargs for passing into SemanticVersion.increment.
    """
    result = {}
    if tag:
        version_spec = tag + b'..HEAD'
    else:
        version_spec = b'HEAD'
    changelog = git._run_git_command([b'log', version_spec], git_dir)
    header_len = len(b'    sem-ver:')
    commands = [ line[header_len:].strip() for line in changelog.split(b'\n') if line.lower().startswith(b'    sem-ver:')
               ]
    symbols = set()
    for command in commands:
        symbols.update([ symbol.strip() for symbol in command.split(b',') ])

    def _handle_symbol(symbol, symbols, impact):
        if symbol in symbols:
            result[impact] = True
            symbols.discard(symbol)

    _handle_symbol(b'bugfix', symbols, b'patch')
    _handle_symbol(b'feature', symbols, b'minor')
    _handle_symbol(b'deprecation', symbols, b'minor')
    _handle_symbol(b'api-break', symbols, b'major')
    for symbol in symbols:
        log.info(b'[pbr] Unknown Sem-Ver symbol %r' % symbol)

    result.pop(b'patch', None)
    return result


def _get_revno_and_last_tag(git_dir):
    """Return the commit data about the most recent tag.

    We use git-describe to find this out, but if there are no
    tags then we fall back to counting commits since the beginning
    of time.
    """
    changelog = git._iter_log_oneline(git_dir=git_dir)
    row_count = 0
    for row_count, (ignored, tag_set, ignored) in enumerate(changelog):
        version_tags = set()
        semver_to_tag = dict()
        for tag in list(tag_set):
            try:
                semver = version.SemanticVersion.from_pip_string(tag)
                semver_to_tag[semver] = tag
                version_tags.add(semver)
            except Exception:
                pass

        if version_tags:
            return (semver_to_tag[max(version_tags)], row_count)

    return (
     b'', row_count)


def _get_version_from_git_target(git_dir, target_version):
    """Calculate a version from a target version in git_dir.

    This is used for untagged versions only. A new version is calculated as
    necessary based on git metadata - distance to tags, current hash, contents
    of commit messages.

    :param git_dir: The git directory we're working from.
    :param target_version: If None, the last tagged version (or 0 if there are
        no tags yet) is incremented as needed to produce an appropriate target
        version following semver rules. Otherwise target_version is used as a
        constraint - if semver rules would result in a newer version then an
        exception is raised.
    :return: A semver version object.
    """
    tag, distance = _get_revno_and_last_tag(git_dir)
    last_semver = version.SemanticVersion.from_pip_string(tag or b'0')
    if distance == 0:
        new_version = last_semver
    else:
        new_version = last_semver.increment(**_get_increment_kwargs(git_dir, tag))
    if target_version is not None and new_version > target_version:
        raise ValueError(b'git history requires a target version of %(new)s, but target version is %(target)s' % dict(new=new_version, target=target_version))
    if distance == 0:
        return last_semver
    else:
        new_dev = new_version.to_dev(distance)
        if target_version is not None:
            target_dev = target_version.to_dev(distance)
            if target_dev > new_dev:
                return target_dev
        return new_dev


def _get_version_from_git(pre_version=None):
    """Calculate a version string from git.

    If the revision is tagged, return that. Otherwise calculate a semantic
    version description of the tree.

    The number of revisions since the last tag is included in the dev counter
    in the version for untagged versions.

    :param pre_version: If supplied use this as the target version rather than
        inferring one from the last tag + commit messages.
    """
    git_dir = git._run_git_functions()
    if git_dir:
        try:
            tagged = git._run_git_command([
             b'describe', b'--exact-match'], git_dir, throw_on_error=True).replace(b'-', b'.')
            target_version = version.SemanticVersion.from_pip_string(tagged)
        except Exception:
            if pre_version:
                target_version = version.SemanticVersion.from_pip_string(pre_version)
            else:
                target_version = None

        result = _get_version_from_git_target(git_dir, target_version)
        return result.release_string()
    else:
        try:
            return unicode()
        except NameError:
            return b''

        return


def _get_version_from_pkg_metadata(package_name):
    """Get the version from package metadata if present.

    This looks for PKG-INFO if present (for sdists), and if not looks
    for METADATA (for wheels) and failing that will return None.
    """
    pkg_metadata_filenames = [
     b'PKG-INFO', b'METADATA']
    pkg_metadata = {}
    for filename in pkg_metadata_filenames:
        try:
            pkg_metadata_file = open(filename, b'r')
        except (IOError, OSError):
            continue

        try:
            pkg_metadata = email.message_from_file(pkg_metadata_file)
        except email.errors.MessageError:
            continue

    if pkg_metadata.get(b'Name', None) != package_name:
        return
    else:
        return pkg_metadata.get(b'Version', None)


def get_version(package_name, pre_version=None):
    """Get the version of the project.

    First, try getting it from PKG-INFO or METADATA, if it exists. If it does,
    that means we're in a distribution tarball or that install has happened.
    Otherwise, if there is no PKG-INFO or METADATA file, pull the version
    from git.

    We do not support setup.py version sanity in git archive tarballs, nor do
    we support packagers directly sucking our git repo into theirs. We expect
    that a source tarball be made from our git repo - or that if someone wants
    to make a source tarball from a fork of our repo with additional tags in it
    that they understand and desire the results of doing that.

    :param pre_version: The version field from setup.cfg - if set then this
        version will be the next release.
    """
    version = _get_version_from_pkg_metadata(package_name)
    if version:
        return version
    else:
        version = os.environ.get(b'PBR_VERSION', os.environ.get(b'OSLO_PACKAGE_VERSION', None))
        if version:
            return version
        version = _get_version_from_git(pre_version)
        if sys.version_info[0] == 2:
            version = version.encode(b'utf-8')
        if version:
            return version
        raise Exception((b"Versioning for this project requires either an sdist tarball, or access to an upstream git repository. It's also possible that there is a mismatch between the package name in setup.cfg and the argument given to pbr.version.VersionInfo. Project name {name} was given, but was not able to be found.").format(name=package_name))
        return


write_pbr_json = pbr.pbr_json.write_pbr_json