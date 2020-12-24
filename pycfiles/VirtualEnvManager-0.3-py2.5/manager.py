# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vem/manager.py
# Compiled at: 2011-02-01 06:18:57
"""
notes on windows
----------------

A standard windows python installation is assumed. This means that the python directory contains
a directory called 'Scripts' which is the default location for executables that are installed
by distutils.

usage on windows
----------------

create a new virtualenv via 'vem create <virtenv_name>'
An activation script named 'activate_<virtenv_name>.bat' will be placed into the standard Scripts
directory.
Running 'vem remove <virtenv_name>' will remove that script.
The virtual environment is activated by calling 'activate_<virtenv_name>.bat' (assuming the
Scripts directory is in the path).
"""
import sys, os, subprocess, glob, optparse, shutil, platform, logging, virtualenv
virtualenv.logger = virtualenv.Logger([])
is_windows = platform.system() == 'Windows'
version = '%i.%i' % sys.version_info[:2]
_ACTIVE_MARKER = '.active'
_DEFAULT_BASE = '~/.virtualenvs%s' % version
if is_windows:
    _ACTIVE_MARKER = '_active'
    _DEFAULT_BASE = os.path.join(os.environ.get('USERPROFILE', 'C:\\'), '_virtualenvs%s') % version

class Manager(object):
    ACTIVE_MARKER = _ACTIVE_MARKER
    DEFAULT_BASE = _DEFAULT_BASE

    def __init__(self):
        self.opts = None
        self._active_ve = None
        self._environments = None
        self._base_path = None
        self.restargs = None
        if is_windows:
            self.python_base = os.path.split(os.path.split(os.__file__)[0])[0]
        return

    def run(self):
        (self.opts, rest) = self.parser.parse_args(sys.argv[1:])
        if len(rest) < 1:
            self.error('Please give a subcommand!')
        command = rest[0]
        self.restargs = rest[1:]

        def unknown_command():
            self.unknown_command(command)

        command_method = getattr(self, 'cmd_%s' % command, unknown_command)
        command_method()

    def cmd_list(self):
        bp = self.base_path
        quiet = self.opts.quiet
        active_ve = self.active_ve
        if os.path.exists(bp):
            envs = self.environments
            if envs:
                if not quiet:
                    print 'Existing environments:\n'
                for env in envs:
                    sys.stdout.write(env)
                    if not quiet and env == active_ve:
                        sys.stdout.write(' *')
                    sys.stdout.write('\n')

            if not quiet:
                print 'No environments'
            if not quiet:
                print

    def cmd_create(self, vems=None):
        if vems is None:
            vems = self.restargs
        bp = self.base_path
        if not os.path.exists(bp):
            os.mkdir(bp)
        for vem in vems:
            home_path = os.path.join(bp, vem)
            virtualenv.create_environment(home_path, site_packages=not self.opts.no_site_packages, use_distribute=self.opts.use_distribute)
            if is_windows:
                virtualenv_name = [ x for x in self.restargs if not x.startswith('-') ][0]
                newname = 'activate_%s.bat' % virtualenv_name
                src = os.path.join(bp, virtualenv_name, 'Scripts', 'activate.bat')
                dst = os.path.join(self.python_base, 'Scripts', newname)
                shutil.copyfile(src, dst)

        return

    def cmd_remove(self, vems=None):
        if vems is None:
            vems = self.restargs
        if len(vems) < 1:
            self.error('Please give existing VE(s) as argument.')
        for ve in vems:
            if ve not in self.environments:
                self.error('No such environment: %s' % ve, dont_exit=True)
                continue
            shutil.rmtree(os.path.join(self.base_path, ve))
            if self.active_ve == ve:
                self.active_ve = ''
            if is_windows:
                name = 'activate_%s.bat' % ve
                dst = os.path.join(self.python_base, 'Scripts', name)
                if os.path.exists(dst):
                    os.unlink(os.path.join(self.python_base, 'Scripts', name))

        return

    def cmd_recreate(self):
        if len(self.restargs) < 1:
            self.error('Please give existing VE(s) as argument.')
        for ve in self.restargs:
            self.cmd_remove([ve])
            self.cmd_create([ve])

    def cmd_location(self):
        """
        Where the current active VE is located.
        """
        if 'VIRTUAL_ENV' in os.environ:
            print os.environ['VIRTUAL_ENV']
        else:
            environments = self.environments
            active = self.active_ve
            if active not in environments:
                sys.stderr("Can't determine active VE!")
                sys.exit(1)
            print os.path.join(self.base_path, active)

    def cmd_compare(self):
        vems = self.restargs
        assert len(vems) == 2
        envs = self.environments
        for vem in vems:
            assert vem in envs

        left = glob.glob(os.path.join(self.base_path, vems[0], 'lib', 'python*', 'site-packages'))[0]
        right = glob.glob(os.path.join(self.base_path, vems[1], 'lib', 'python*', 'site-packages'))[0]
        ignore_equal = self.opts.ignore_equal
        left = sorted(os.listdir(left))
        right = sorted(os.listdir(right))
        lit = iter(left)
        rit = iter(right)

        def next(it):
            name = it.next()
            base = name.split('-')[0]
            return (name, base)

        leftmax = max((len(e) for e in left))

        def output(left, right):
            if left is None:
                left = ' ' * leftmax
            else:
                left = left + ' ' * (leftmax - len(left))
            if right is None:
                right = ''
            print '%s | %s' % (left, right)
            return

        (left, left_base) = next(lit)
        (right, right_base) = next(rit)
        try:
            while True:
                while left_base < right_base:
                    output(left, None)
                    (left, left_base) = next(lit)

                while right_base < left_base:
                    output(None, right)
                    (right, right_base) = next(rit)

                while left_base == right_base:
                    if left < right:
                        output(left, None)
                        (left, left_base) = next(lit)
                        continue
                    elif right < left:
                        output(None, right)
                        (right, right_base) = next(rit)
                        continue
                    elif not ignore_equal:
                        output(left, right)
                    (left, left_base) = next(lit)
                    try:
                        (right, right_base) = next(rit)
                    except StopIteration:
                        output(left, None)
                        for rest in lit:
                            output(rest, None)

                        raise

        except StopIteration:
            pass

        for rest in lit:
            output(rest, None)

        for rest in rit:
            output(None, rest)

        return

    def cmd_activate(self):
        envs = self.environments
        try:
            to_activate = self.restargs[0]
            if to_activate not in envs:
                self.error('No such environment: %s' % to_activate)
            self.active_ve = to_activate
            bindir = 'bin'
            activate_command = os.path.join(self.base_path, to_activate, bindir, 'activate')
            if not self.opts.quiet:
                sys.stdout.write('Please make sure you execute the following command to activate the environment\nin the shell:\n\nsource ')
            sys.stdout.write(activate_command)
            if not self.opts.quiet:
                sys.stdout.write('\n')
        except IndexError:
            self.error('You need to give an ve name')

    def cmd_scripts(self):
        command = os.path.basename(sys.argv[0])
        scripts = 'function %(command)s_activate() {\n    cmd=`%(command)s activate -q $@`\n    source $cmd\n}\n\n_%(command)s_activate()\n{\n    local cur\n    COMPREPLY=()\n    cur="${COMP_WORDS[COMP_CWORD]}"\n    opts=`%(command)s list -q`\n\n    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )\n    return 0\n}\ncomplete -F _%(command)s_activate %(command)s_activate\n\n#\n# Activate the virtualenv whose name is the current working directory\nfunction %(command)sac()\n{\n  deactivate;\n  vename=`pwd | awk -F / "{print \\$NF}"`\n  %(command)s_activate $vename\n}\n\n#\n# Remove, recreate, and activate the virtualenv whose name is the\n# current working directory, then run "python setup.py develop".\nfunction %(command)sfresh()\n{\n  deactivate;\n  vename=`pwd | awk -F / "{print \\$NF}"`\n  %(command)s remove $vename\n  %(command)s create $vename\n  %(command)s_activate $vename\n  python setup.py develop\n}\n\n' % dict(command=command)
        print scripts

    @property
    def base_path(self):
        if self._base_path is None:
            if self.opts is None or self.opts.base_path is None:
                bp = os.environ.get('VEM_BASE_PATH', self.DEFAULT_BASE)
            else:
                bp = self.opts.base_path
            self._base_path = os.path.abspath(os.path.expanduser(bp))
        return self._base_path

    @property
    def environments(self):
        if self._environments is None:
            self._environments = envs = []
            bp = self.base_path
            if os.path.exists(bp) and os.path.isdir(bp):
                for fname in glob.glob(os.path.join(bp, '*')):
                    name = os.path.basename(fname)
                    if name == self.ACTIVE_MARKER:
                        continue
                    envs.append(name)

        return self._environments

    @apply
    def active_ve():
        """
        Get or set the name of the active VE.
        """

        def fget(self):
            if self._active_ve is None:
                fname = os.path.join(self.base_path, self.ACTIVE_MARKER)
                if os.path.exists(fname) and os.path.isfile(fname):
                    inf = open(fname)
                    active_ve = inf.read().strip()
                    inf.close()
                else:
                    active_ve = ''
                self._active_ve = active_ve
            return self._active_ve

        def fset(self, value):
            fname = os.path.join(self.base_path, self.ACTIVE_MARKER)
            if os.path.exists(fname) and os.path.isfile(fname):
                outf = open(fname, 'w')
                outf.write(value.strip())
                outf.close()
            self._active_ve = value

        return property(**locals())

    @property
    def active_prefix(self):
        av = self.active_ve
        if av is not None:
            return os.path.join(self.base_path, av)
        return

    def unknown_command(self, command):
        """
        Unknown command.
        """
        self.error("Unknown command '%s'" % command)

    def error(self, message, dont_exit=False):
        sys.stderr.write('\n')
        sys.stderr.write(message)
        sys.stderr.write('\n')
        if not dont_exit:
            sys.exit(1)

    def python(self):
        """
        """
        try:
            if self.active_prefix:
                bindir = 'bin'
                if is_windows:
                    bindir = 'Scripts'
                exe = glob.glob(os.path.join(self.active_prefix, bindir, 'python*'))[0]
                os.execv(exe, [exe] + sys.argv[1:])
            else:
                [][0]
        except IndexError:
            raise Exception('No interpreter found for VE %r' % self.active_ve)

    COMMANDS = [ name[4:] for name in locals().keys() if name[:4] == 'cmd_' ]
    USAGE = 'usage: %%prog <command> [options] <args>\n\nwhere command is one of:\n  %s' % ('\n  ').join(COMMANDS)
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('-b', '--base-path', action='store', default=None)
    parser.add_option('-q', '--quiet', action='store_true', default=False, help='Quiet output mode')
    parser.add_option('-S', '--no-site-packages', action='store_true', default=False, help="Don't make packages in site-packages available to this venv")
    parser.add_option('-D', '--use-distribute', action='store_true', default=False, help='Use Distribute instead of setuptools.')
    parser.add_option('-i', '--ignore-equal', action='store_true', default=False, help='When compairing, only report diffing module.')


def main():
    Manager().run()


def python():
    Manager().python()