# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/openstack/common/setup.py
# Compiled at: 2016-06-13 14:11:03
"""
Utilities with minimum-depends for use in setup.py
"""
import email, os, re, subprocess, sys
from setuptools.command import sdist

def parse_mailmap(mailmap='.mailmap'):
    mapping = {}
    if os.path.exists(mailmap):
        with open(mailmap, 'r') as (fp):
            for l in fp:
                try:
                    canonical_email, alias = re.match('[^#]*?(<.+>).*(<.+>).*', l).groups()
                except AttributeError:
                    continue

                mapping[alias] = canonical_email

    return mapping


def _parse_git_mailmap(git_dir, mailmap='.mailmap'):
    mailmap = os.path.join(os.path.dirname(git_dir), mailmap)
    return parse_mailmap(mailmap)


def canonicalize_emails(changelog, mapping):
    """Takes in a string and an email alias mapping and replaces all
       instances of the aliases in the string with their real email.
    """
    for alias, email_address in mapping.iteritems():
        changelog = changelog.replace(alias, email_address)

    return changelog


def get_reqs_from_files(requirements_files):
    for requirements_file in requirements_files:
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r') as (fil):
                return fil.read().split('\n')

    return []


def parse_requirements(requirements_files=[
 'requirements.txt',
 'tools/pip-requires']):
    requirements = []
    for line in get_reqs_from_files(requirements_files):
        if re.match('\\s*-e\\s+', line):
            requirements.append(re.sub('\\s*-e\\s+.*#egg=(.*)$', '\\1', line))
        elif re.match('\\s*https?:', line):
            requirements.append(re.sub('\\s*https?:.*#egg=(.*)$', '\\1', line))
        elif re.match('\\s*-f\\s+', line):
            pass
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(requirements_files=[
 'requirements.txt',
 'tools/pip-requires']):
    dependency_links = []
    for line in get_reqs_from_files(requirements_files):
        if re.match('(\\s*#)|(\\s*$)', line):
            continue
        if re.match('\\s*-[ef]\\s+', line):
            dependency_links.append(re.sub('\\s*-[ef]\\s+', '', line))
        elif re.match('\\s*https?:', line):
            dependency_links.append(line)

    return dependency_links


def _run_shell_command(cmd, throw_on_error=False):
    if os.name == 'nt':
        output = subprocess.Popen(['cmd.exe', '/C', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        output = subprocess.Popen(['/bin/sh', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = output.communicate()
    if output.returncode and throw_on_error:
        raise Exception('%s returned %d' % cmd, output.returncode)
    if len(out) == 0:
        return None
    else:
        if len(out[0].strip()) == 0:
            return None
        return out[0].strip()


def _get_git_directory():
    parent_dir = os.path.dirname(__file__)
    while True:
        git_dir = os.path.join(parent_dir, '.git')
        if os.path.exists(git_dir):
            return git_dir
        parent_dir, child = os.path.split(parent_dir)
        if not child:
            return

    return


def write_git_changelog():
    """Write a changelog based on the git changelog."""
    new_changelog = 'ChangeLog'
    git_dir = _get_git_directory()
    if not os.getenv('SKIP_WRITE_GIT_CHANGELOG'):
        if git_dir:
            git_log_cmd = 'git --git-dir=%s log' % git_dir
            changelog = _run_shell_command(git_log_cmd)
            mailmap = _parse_git_mailmap(git_dir)
            with open(new_changelog, 'w') as (changelog_file):
                changelog_file.write(canonicalize_emails(changelog, mailmap))
    else:
        open(new_changelog, 'w').close()


def generate_authors():
    """Create AUTHORS file using git commits."""
    jenkins_email = 'jenkins@review.(openstack|stackforge).org'
    old_authors = 'AUTHORS.in'
    new_authors = 'AUTHORS'
    git_dir = _get_git_directory()
    if not os.getenv('SKIP_GENERATE_AUTHORS'):
        if git_dir:
            git_log_cmd = 'git --git-dir=' + git_dir + " log --format='%aN <%aE>' | sort -u | egrep -v '" + jenkins_email + "'"
            changelog = _run_shell_command(git_log_cmd)
            signed_cmd = 'git --git-dir=' + git_dir + ' log | grep -i Co-authored-by: | sort -u'
            signed_entries = _run_shell_command(signed_cmd)
            if signed_entries:
                new_entries = ('\n').join([ signed.split(':', 1)[1].strip() for signed in signed_entries.split('\n') if signed
                                          ])
                changelog = ('\n').join((changelog, new_entries))
            mailmap = _parse_git_mailmap(git_dir)
            with open(new_authors, 'w') as (new_authors_fh):
                new_authors_fh.write(canonicalize_emails(changelog, mailmap))
                if os.path.exists(old_authors):
                    with open(old_authors, 'r') as (old_authors_fh):
                        new_authors_fh.write('\n' + old_authors_fh.read())
    else:
        open(new_authors, 'w').close()


_rst_template = '%(heading)s\n%(underline)s\n\n.. automodule:: %(module)s\n  :members:\n  :undoc-members:\n  :show-inheritance:\n'

def get_cmdclass():
    """Return dict of commands to run from setup.py."""
    cmdclass = dict()

    def _find_modules(arg, dirname, files):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                arg['%s.%s' % (dirname.replace('/', '.'), filename[:-3])] = True

    class LocalSDist(sdist.sdist):
        """Builds the ChangeLog and Authors files from VC first."""

        def run(self):
            write_git_changelog()
            generate_authors()
            sdist.sdist.run(self)

    cmdclass['sdist'] = LocalSDist
    try:
        from sphinx.setup_command import BuildDoc

        class LocalBuildDoc(BuildDoc):
            builders = [
             'html', 'man']

            def generate_autoindex(self):
                print '**Autodocumenting from %s' % os.path.abspath(os.curdir)
                modules = {}
                option_dict = self.distribution.get_option_dict('build_sphinx')
                source_dir = os.path.join(option_dict['source_dir'][1], 'api')
                if not os.path.exists(source_dir):
                    os.makedirs(source_dir)
                for pkg in self.distribution.packages:
                    if '.' not in pkg:
                        os.path.walk(pkg, _find_modules, modules)

                module_list = modules.keys()
                module_list.sort()
                autoindex_filename = os.path.join(source_dir, 'autoindex.rst')
                with open(autoindex_filename, 'w') as (autoindex):
                    autoindex.write('.. toctree::\n   :maxdepth: 1\n\n')
                    for module in module_list:
                        output_filename = os.path.join(source_dir, '%s.rst' % module)
                        heading = 'The :mod:`%s` Module' % module
                        underline = '=' * len(heading)
                        values = dict(module=module, heading=heading, underline=underline)
                        print 'Generating %s' % output_filename
                        with open(output_filename, 'w') as (output_file):
                            output_file.write(_rst_template % values)
                        autoindex.write('   %s.rst\n' % module)

            def run(self):
                if not os.getenv('SPHINX_DEBUG'):
                    self.generate_autoindex()
                for builder in self.builders:
                    self.builder = builder
                    self.finalize_options()
                    self.project = self.distribution.get_name()
                    self.version = self.distribution.get_version()
                    self.release = self.distribution.get_version()
                    BuildDoc.run(self)

        class LocalBuildLatex(LocalBuildDoc):
            builders = [
             'latex']

        cmdclass['build_sphinx'] = LocalBuildDoc
        cmdclass['build_sphinx_latex'] = LocalBuildLatex
    except ImportError:
        pass

    return cmdclass


def _get_revno(git_dir):
    """Return the number of commits since the most recent tag.

    We use git-describe to find this out, but if there are no
    tags then we fall back to counting commits since the beginning
    of time.
    """
    describe = _run_shell_command('git --git-dir=%s describe --always' % git_dir)
    if '-' in describe:
        return describe.rsplit('-', 2)[(-2)]
    revlist = _run_shell_command('git --git-dir=%s rev-list --abbrev-commit HEAD' % git_dir)
    return len(revlist.splitlines())


def _get_version_from_git(pre_version):
    """Return a version which is equal to the tag that's on the current
    revision if there is one, or tag plus number of additional revisions
    if the current revision has no tag."""
    git_dir = _get_git_directory()
    if git_dir:
        if pre_version:
            try:
                return _run_shell_command('git --git-dir=' + git_dir + ' describe --exact-match', throw_on_error=True).replace('-', '.')
            except Exception:
                sha = _run_shell_command('git --git-dir=' + git_dir + ' log -n1 --pretty=format:%h')
                return '%s.a%s.g%s' % (pre_version, _get_revno(git_dir), sha)

        else:
            return _run_shell_command('git --git-dir=' + git_dir + ' describe --always').replace('-', '.')
    return


def _get_version_from_pkg_info(package_name):
    """Get the version from PKG-INFO file if we can."""
    try:
        pkg_info_file = open('PKG-INFO', 'r')
    except (IOError, OSError):
        return

    try:
        pkg_info = email.message_from_file(pkg_info_file)
    except email.MessageError:
        return

    if pkg_info.get('Name', None) != package_name:
        return
    else:
        return pkg_info.get('Version', None)


def get_version(package_name, pre_version=None):
    """Get the version of the project. First, try getting it from PKG-INFO, if
    it exists. If it does, that means we're in a distribution tarball or that
    install has happened. Otherwise, if there is no PKG-INFO file, pull the
    version from git.

    We do not support setup.py version sanity in git archive tarballs, nor do
    we support packagers directly sucking our git repo into theirs. We expect
    that a source tarball be made from our git repo - or that if someone wants
    to make a source tarball from a fork of our repo with additional tags in it
    that they understand and desire the results of doing that.
    """
    version = os.environ.get('OSLO_PACKAGE_VERSION', None)
    if version:
        return version
    else:
        version = _get_version_from_pkg_info(package_name)
        if version:
            return version
        version = _get_version_from_git(pre_version)
        if version:
            return version
        raise Exception('Versioning for this project requires either an sdist tarball, or access to an upstream git repository.')
        return