# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/command/svntag.py
# Compiled at: 2007-08-08 19:58:56
__doc__ = '\nTag an svn project:\n\n* Copy the trunk to ../tags/VERSION\n* Update setup.py with VERSION\n* Update the trunk setup.py with NEXT_VERSION\n* Check out the new tag in ../PACKAGE-VERSION\n'
from buildutils.cmd import Command
from ConfigParser import NoSectionError
from distutils.errors import *
from distutils import log
subprocess = None
import re, sys, os, tempfile, shutil, shlex

class svntag(Command):
    __module__ = __name__
    description = 'Tag a Subversion project for release'
    user_options = [
     ('version=', 'v', 'Specify version'), ('next-version=', None, 'The next version (the trunk setup.py will be modified with this version)'), ('message=', 'm', 'Specify a log message'), ('build=', 'b', 'Specify directory to build tag files in'), ('setup-commands', 's', "Commands to run on the checkout setup.py after doing updates.  This must be shell quoted, like --setup-commands='bdist --tag-build=dev'"), ('clean', None, 'Remove tag checkout after finishing')]
    version = None
    message = None
    build = None
    next_version = None
    setup_commands = None
    clean = False

    def initialize_options(self):
        pass

    def finalize_options(self):
        if self.version is None:
            raise DistutilsOptionError('You must specify a version')
        if self.message is None:
            self.message = 'Tagging %s version' % self.version
        if self.build and os.path.exists(self.build):
            raise DistutilsOptionError('The build directory %s already exists' % self.build)
        if self.build is None:
            self.build = os.path.join(os.path.dirname(os.getcwd()), os.path.basename(os.getcwd()) + '-' + self.version)
        if self.setup_commands:
            self.setup_commands = shlex.split(self.setup_commands)
        return

    _svn_url_re = re.compile('\\bURL: (.*)')
    _setup_version_re = re.compile('((?:__)?version(?:__)?\\s+=\\s+)([^ \\n\\r,)]*)')
    _egg_info_re = re.compile('^[egg_info]$')

    def run(self):
        stdout = run_command(['svn', 'info', '.'])
        match = self._svn_url_re.search(stdout)
        if not match:
            raise DistutilsExecError('svn output did not contain "URL: ...":\n' + stdout)
        svn_url = match.group(1)
        if not svn_url.endswith('/trunk'):
            raise DistutilsExecError('svn URL must end with "/trunk" (current: %r)' % svn_url)
        package_url = svn_url.rsplit('/', 1)[0]
        tag_url = package_url + '/tags/' + self.version
        run_command(['svn', 'cp', '--message', self.message, svn_url, tag_url])
        run_command(['svn', 'co', '--quiet', tag_url, self.build])
        self.update_setup_cfg()
        self.update_setup_py(os.path.join(self.build, 'setup.py'), self.version)
        run_command(['svn', 'commit', '--message', 'Auto-update of version strings', self.build])
        if self.setup_commands:
            run_command([sys.executable, 'setup.py'] + self.setup_commands, self.build)
        if self.clean:
            log.info('Removing tag directory %s' % self.build)
            shutil.rmtree(self.build)
        if self.next_version:
            self.update_setup_py('setup.py', self.next_version)
            run_command(['svn', 'commit', '--message', 'Auto-update of version strings', 'setup.py', os.getcwd()])

    def update_setup_py(self, setup_py, version):
        if not os.path.exists(setup_py):
            log.warn('setup.py file cannot be found at %s' % setup_py)
            return
        f = open(setup_py)
        content = f.read()
        f.close()
        match = self._setup_version_re.search(content)
        if not match:
            log.fatal('Cannot find version info in %s' % setup_py)
            raise DistutilsFileError('Cannot find version info in %s (searching for version=X)' % setup_py)
        else:
            new_content = content[:match.start()] + match.group(1) + repr(version) + content[match.end():]
            if new_content == content:
                log.info('Version string up-to-date (%s) in %s' % (version, setup_py))
            else:
                f = open(setup_py, 'w')
                f.write(new_content)
                f.close()
                log.info('%s version updated to %s' % (setup_py, version))
        command = [
         sys.executable, setup_py, 'egg_info']

    def update_setup_cfg(self):
        try:
            from setuptools.command import setopt
        except ImportError, e:
            log.warn('Cannot import setuptools (%s); cannot edit setup.cfg' % e)
            return

        setup_cfg = os.path.join(self.build, 'setup.cfg')
        if not os.path.exists(setup_cfg):
            log.warn('setup.cfg file cannot be found at %s' % setup_cfg)
            return
        try:
            setopt.edit_config(setup_cfg, {'egg_info': {'tag_build': None, 'tag_svn_revision': None}})
        except NoSectionError:
            pass

        f = open(setup_cfg)
        content = f.read()
        f.close()
        if not content.strip():
            log.info('%s empty; deleting' % setup_cfg)
            run_command(['svn', 'rm', '--force', setup_cfg])
        return


def run_command(command_list, stdin=None):
    global subprocess
    if subprocess is None:
        try:
            import subprocess
        except ImportError:
            log.fatal('Cannot run command %s without the Python 2.4 subprocess module' % (' ').join(command_list))
            raise

    log.info('Running %s', format_command(command_list))
    proc = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate(stdin)
    if stderr:
        log.warn('Ouput from %s:\n%s', format_command(command_list), stderr)
    returncode = proc.returncode
    if returncode:
        error = 'Exit code %s from %s' % (returncode, format_command(command_list))
        if stderr:
            error += '; stderr output:\n' + stderr
        raise DistutilsExecError(error)
    return stdout


def format_command(lst):
    return (' ').join(map(quote_command_item, lst))


def quote_command_item(item):
    if ' ' in item:
        for char in ('\\', '"', "'", '$'):
            item = item.replace(char, '\\' + char)

        item = '"%s"' % item
    return item