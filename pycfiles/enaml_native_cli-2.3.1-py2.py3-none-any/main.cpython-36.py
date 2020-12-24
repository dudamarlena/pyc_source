# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jrm/Workspace/codelv/enaml-native-cli/enamlnativecli/main.py
# Compiled at: 2018-09-23 10:45:47
# Size of source mod 2**32: 63906 bytes
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPLv3 License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 10, 2017

@author: jrm
"""
import os, re, sys, json, shutil, tarfile, fnmatch, compileall, pkg_resources
from glob import glob
from os.path import join, exists, abspath, expanduser, realpath, dirname
from argparse import ArgumentParser, Namespace, REMAINDER
from atom.api import Atom, Bool, Callable, Dict, List, Unicode, Float, Int, Instance, set_default
from contextlib import contextmanager
from cookiecutter.main import cookiecutter
from cookiecutter.log import configure_logger
from distutils.dir_util import copy_tree
try:
    import ruamel_yaml as yaml
except:
    from ruamel import yaml

try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

IS_WIN = 'win' in sys.platform and not 'darwin' == sys.platform
if IS_WIN:
    import pbs

    class Sh(object):

        def __getattr__(self, attr):
            if hasattr(pbs, attr):
                return getattr(pbs, attr)
            else:
                return pbs.Command(attr)


    sh = Sh()
    ANDROID_SDK = join(os.environ.get('LOCALAPPDATA', ''), 'Android', 'Sdk')
    adb = join(ANDROID_SDK, 'platform-tools', 'adb.exe')
    emulator = join(ANDROID_SDK, 'emulator', 'emulator.exe')
    if exists(adb):
        sh.adb = sh.Command(adb)
    else:
        raise EnvironmentError("Couldn't find a adb in your System, Make sure android studio is installed")
    if exists(emulator):
        sh.emulator = sh.Command(emulator)
    else:
        raise EnvironmentError("Couldn't find a emulator in your System, Make sure android studio is installed")
else:
    import sh

def find_conda():
    """ Try to find conda on the system """
    USER_HOME = os.path.expanduser('~')
    CONDA_HOME = os.environ.get('CONDA_HOME', '')
    PROGRAMDATA = os.environ.get('PROGRAMDATA', '')
    search_paths = [
     join(PROGRAMDATA, 'miniconda2', 'scripts'),
     join(PROGRAMDATA, 'miniconda3', 'scripts'),
     join(USER_HOME, 'miniconda2', 'scripts'),
     join(USER_HOME, 'miniconda3', 'scripts'),
     join(CONDA_HOME, 'scripts'),
     join(USER_HOME, 'miniconda2', 'bin'),
     join(USER_HOME, 'miniconda3', 'bin'),
     join(CONDA_HOME, 'bin')] + os.environ.get('PATH', '').split(';' if 'win' in sys.path else ':')
    cmd = 'conda.exe' if IS_WIN else 'conda'
    for conda_path in search_paths:
        conda = join(conda_path, cmd)
        if exists(conda):
            return sh.Command(conda)

    return sh.conda


class Colors:
    RED = '\x1b[1;31m'
    BLUE = '\x1b[1;34m'
    CYAN = '\x1b[1;36m'
    GREEN = '\x1b[0;32m'
    RESET = '\x1b[0;0m'
    BOLD = '\x1b[;1m'
    REVERSE = '\x1b[;7m'


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    print('[DEBUG]:   -> running cd {}'.format(newdir))
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        print('[DEBUG]:   -> running  cd {}'.format(prevdir))
        os.chdir(prevdir)


def cp(src, dst):
    """ Like cp -R src dst """
    print('[DEBUG]:   -> copying {} to {}'.format(src, dst))
    if os.path.isfile(src):
        if not exists(dirname(dst)):
            os.makedirs(dirname(dst))
        shutil.copy(src, dst)
    else:
        copy_tree(src, dst)


def shprint(cmd, *args, **kwargs):
    debug = kwargs.pop('_debug', True)
    write, flush = sys.stdout.write, sys.stdout.flush
    kwargs.update({'_err_to_out':True, 
     '_out_bufsize':0, 
     '_iter':True})
    print('{}[INFO]:   -> running  {} {}{}'.format(Colors.CYAN, cmd, ' '.join([a for a in args if not isinstance(a, sh.RunningCommand)]), Colors.RESET))
    if IS_WIN:
        kwargs.pop('_out_bufsize')
        kwargs.pop('_iter')
        kwargs['_bg'] = True
        process = cmd(*args, **kwargs).process
        for c in iter(lambda : process.stdout.read(1), ''):
            write(c.decode('utf-8'))
            if c in ('\r', '\n'):
                flush()
            elif not c:
                break

        process.wait()
        return
    buf = []
    for c in cmd(*args, **kwargs):
        if debug:
            write(c)
            if c in ('\r', '\n'):
                flush()
        else:
            if c in ('\r', '\n'):
                msg = ''.join(buf)
                color = Colors.RED if 'error' in msg else Colors.RESET
                write('{}\r[DEBUG]:       {:<{w}}{}'.format(color,
                  msg, (Colors.RESET), w=100))
                flush()
                buf = []
            else:
                buf.append(c)

    write('\n')
    flush()


ANDROID_ABIS = {'x86_64':'x86_64', 
 'x86':'x86', 
 'armeabi-v7a':'arm', 
 'arm64-v8a':'arm64'}
ANDROID_TARGETS = {v:k for k, v in ANDROID_ABIS.items()}

class Command(Atom):
    _instance = None
    title = Unicode()
    desc = Unicode()
    help = Unicode()
    ctx = Dict()
    cmds = Dict()
    args = List(tuple)
    parser = Instance(ArgumentParser)
    app_dir_required = Bool(True)
    cli = Instance(Atom)

    @classmethod
    def instance(cls):
        return cls._instance

    def run(self, args):
        pass


class Create(Command):
    title = set_default('create')
    help = set_default('Create an enaml-native project')
    args = set_default([
     (
      'what', dict(help='What to create (app, lib, package)?')),
     (
      '--no-input',
      dict(action='store_true', help='Use all defaults')),
     (
      '-f --overwrite-if-exists',
      dict(action='store_true', help='Overwrite the contents ifit already exists')),
     (
      '-v --verbose', dict(action='store_true', help='Verbose logging'))])
    app_dir_required = set_default(False)

    def run(self, args):
        template = join(dirname(__file__), 'templates', args.what)
        configure_logger(stream_level=('DEBUG' if args.verbose else 'INFO'),
          debug_file=None)
        cookiecutter(template, no_input=(args.no_input),
          overwrite_if_exists=(args.overwrite_if_exists))
        print(Colors.GREEN + '[INFO] {} created successfully!'.format(args.what.title()) + Colors.RESET)


class BuildRecipe(Command):
    title = set_default('build-recipe')
    help = set_default('Alias to conda build')
    args = set_default([
     (
      'package', dict(help='Conda recipe to build')),
     (
      'args', dict(nargs=REMAINDER, help='args to pass to conda build'))])
    app_dir_required = set_default(False)

    def run(self, args):
        env = os.environ.copy()
        if args.package.startswith('pip-'):
            env.update({'CC':'/bin/false',  'CXX':'/bin/false'})
        shprint(self.cli.conda, 'build', args.package, *(args.args), **{'_env': env})
        print(Colors.GREEN + '[INFO] Built {} successfully!'.format(args.package) + Colors.RESET)


class MakePipRecipe(Command):
    title = set_default('make-pip-recipe')
    help = set_default('Creates a universal Android and iOS recipe for a given pip package')
    args = set_default([
     (
      'package', dict(help='pip package to build a recipe for')),
     (
      '--recursive',
      dict(action='store_true', help='recursively create for all dependencies')),
     (
      '--force',
      dict(action='store_true', help='force recreation if it already exists')),
     (
      '--croot', dict(nargs='?', help='conda root for building recipes'))])
    app_dir_required = set_default(False)
    _built = List()

    def run(self, args):
        self.build(args.package, args)
        print(Colors.GREEN + '[INFO] Made successfully!' + Colors.RESET)

    def build(self, package, args):
        ctx = self.ctx
        old = set(os.listdir('.'))
        shprint(self.cli.conda, 'skeleton', 'pypi', package)
        new = set(os.listdir('.')).difference(old)
        self._built.append(package)
        for recipe in new:
            dst = 'pip-{}'.format(recipe)
            if args.force:
                if exists(dst):
                    shutil.rmtree(dst)
            shutil.move(recipe, dst)
            with open(join(dst, 'meta.yaml')) as (f):
                data = f.read().split('\n')
                var_lines = len([l for l in data if l.startswith('{%')])
                meta = yaml.load(('\n'.join(data[var_lines:])), Loader=(yaml.RoundTripLoader))
            meta['package']['name'] = 'pip-' + meta['package']['name']
            summary = meta['about'].get('summary', '')
            summary += ' Built for Android and iOS apps using enaml-native.'
            meta['about']['summary'] = summary
            script = meta['build'].pop('script', '')
            meta['build']['noarch'] = True
            build_script = ['export CC=/bin/false', 'export CXX=/bin/false']
            build_script += [('{script} --no-compile --install-base=$PREFIX/{prefix} --install-lib=$PREFIX/{prefix}/python/site-packages --install-scripts=$PREFIX/{prefix}/scripts --install-data=$PREFIX/{prefix}/data --install-headers=$PREFIX/{prefix}/include'.format)(script=script.strip(), prefix=p, **ctx) for p in ('android/arm',
                                                                                                                                                                                                                                                                                                                               'android/arm64',
                                                                                                                                                                                                                                                                                                                               'android/x86',
                                                                                                                                                                                                                                                                                                                               'android/x86_64',
                                                                                                                                                                                                                                                                                                                               'iphoneos',
                                                                                                                                                                                                                                                                                                                               'iphonesimulator')]
            meta['build']['script'] = build_script
            requires = []
            excluded = [
             'python', 'cython', 'setuptools']
            for stage in meta['requirements'].keys():
                reqs = meta['requirements'].pop(stage, [])
                requires.extend(reqs)
                r = ['pip-{}'.format(r) for r in reqs if r not in excluded]
                if r:
                    meta['requirements'][stage] = r

            if args.recursive:
                requires = list(set(requires))
                for pkg in requires:
                    pkg = re.split('[<>=]', pkg)[0].strip()
                    if not pkg in excluded:
                        if pkg in self._built:
                            pass
                        elif args.force or not exists('pip-{}'.format(pkg)):
                            self.build(pkg, args)

            meta.pop('test', None)
            with open(join(dst, 'meta.yaml'), 'w') as (f):
                f.write('\n'.join(data[:var_lines]) + '\n')
                f.write(yaml.dump(meta, Dumper=(yaml.RoundTripDumper), width=1000))
            build_args = ['--croot={}'.format(args.croot)] if args.croot else []
            env = os.environ.copy()
            env.update({'CC':'/bin/false',  'CXX':'/bin/false'})
            shprint(self.cli.conda, 'build', dst, *build_args)
            print(Colors.GREEN + '[INFO] Built {} successfully!'.format(dst) + Colors.RESET)


class NdkStack(Command):
    __doc__ = ' Shortcut to run ndk-stack to show debugging output of a crash in a \n    native library.\n    \n    See https://developer.android.com/ndk/guides/ndk-stack.html\n    '
    title = set_default('ndk-stack')
    help = set_default('Run ndk-stack on the adb output')
    args = set_default([
     (
      'arch', dict(nargs='?', default='armeabi-v7a')),
     (
      'args', dict(nargs=REMAINDER, help='Extra args for ndk-stack'))])

    def run(self, args=None):
        ctx = self.ctx
        env = ctx['android']
        ndk_stack = sh.Command(join(os.path.expanduser(env['ndk']), 'ndk-stack.cmd' if IS_WIN else 'ndk-stack'))
        arch = args.arch if args else 'armeabi-v7a'
        sym = 'venv/android/enaml-native/src/main/obj/local/{}'.format(arch)
        shprint(ndk_stack, sh.adb('logcat', _piped=True), '-sym', sym)


class NdkBuild(Command):
    __doc__ = ' Run ndk-build on enaml-native and any packages\n        that define an `enaml_native_ndk_build` entry_point.\n    '
    title = set_default('ndk-build')
    help = set_default('Run ndk-build on the android project')

    def run(self, args=None):
        ctx = self.ctx
        env = ctx['android']
        build_ver = sys.version_info.major
        for line in self.cli.conda('list').split('\n'):
            print(line)
            if 'android-python' in line:
                build_ver = 2 if 'py27' in line else 3
                py_version = '.'.join(line.split()[1].split('.')[:2])
                if build_ver > 2:
                    py_version += 'm'
                break

        print(Colors.GREEN + '[DEBUG] Building for {}'.format(py_version) + Colors.RESET)
        ndk_build = sh.Command(join(os.path.expanduser(env['ndk']), 'ndk-build.cmd' if IS_WIN else 'ndk-build'))
        arches = [ANDROID_TARGETS[arch] for arch in env['targets']]
        jni_dir = env.get('jni_dir', ('{conda_prefix}/android/enaml-native/src/main/jni'.format)(**env))
        if 'jni_dir' not in env:
            env['jni_dir'] = jni_dir
        ndk_build_dir = env.get('ndk_build_dir', ('{conda_prefix}/android/enaml-native/src/main/libs'.format)(**env))
        if 'ndk_build_dir' not in env:
            env['ndk_build_dir'] = ndk_build_dir
        with cd(jni_dir):
            with open('Application.mk') as (f):
                app_mk = f.read()
            new_mk = []
            for line in app_mk.split('\n'):
                if re.match('APP_ABI\\s*:=\\s*.+', line):
                    line = 'APP_ABI := {}'.format(' '.join(arches))
                new_mk.append(line)

            with open('Application.mk', 'w') as (f):
                f.write('\n'.join(new_mk))
            with open('Android.mk') as (f):
                android_mk = f.read()
            new_mk = []
            for line in android_mk.split('\n'):
                if re.match('PY_LIB_VER\\s*:=\\s*.+', line):
                    line = 'PY_LIB_VER := {}'.format(py_version)
                new_mk.append(line)

            with open('Android.mk', 'w') as (f):
                f.write('\n'.join(new_mk))
            shprint(ndk_build)
        dependencies = ctx['dependencies']
        for ep in pkg_resources.iter_entry_points(group='enaml_native_ndk_build'):
            for name in dependencies:
                if ep.name.replace('-', '_') == name.replace('-', '_'):
                    ndk_build_hook = ep.load()
                    print("Custom ndk_build_hook {} found for '{}'. ".format(ndk_build_hook, name))
                    ndk_build_hook(self.ctx)
                    break

        for arch in arches:
            cfg = dict(arch=arch,
              local_arch=(ANDROID_ABIS[arch]),
              ndk_build_dir=ndk_build_dir)
            cfg.update(env)
            dst = abspath(('{ndk_build_dir}/{arch}'.format)(**cfg))
            with cd(('{conda_prefix}/android/{local_arch}/lib/'.format)(**cfg)):
                for lib in glob('*.so'):
                    excluded = [p for p in env.get('excluded', []) if fnmatch.fnmatch(lib, p)]
                    if excluded:
                        pass
                    else:
                        shutil.copy(lib, dst)


class BundleAssets(Command):
    __doc__ = ' This is used by the gradle build to pack python into a zip.\n    '
    title = set_default('bundle-assets')
    help = set_default('Creates a python bundle of all .py and .enaml files')
    args = set_default([
     (
      'target',
      dict(nargs='?', default='android', help='Build for the given target (android, iphoneos, iphonesimulator)')),
     (
      '--release', dict(action='store_true', help='Create a release bundle')),
     (
      '--no-compile', dict(action='store_true', help="Don't generate python cache"))])

    def run(self, args=None):
        ctx = self.ctx
        if args.target not in ('android', 'iphoneos', 'iphonesimulator'):
            raise ValueError('Target must be either android, iphoneos, or iphonesimulator')
        else:
            if args.target == 'android':
                env = ctx['android']
            else:
                env = ctx['ios']
            bundle = 'python.tar.gz'
            root = abspath(os.getcwd())
            if args.target == 'android':
                self.cmds['ndk-build'].run(args)
            else:
                with cd(('{conda_prefix}/{target}/lib/'.format)(target=args.target, **env)):
                    dst = '{root}/ios/Libs'.format(root=root)
                    if exists(dst):
                        shutil.rmtree(dst)
                    os.makedirs(dst)
                    for lib in glob('*.dylib'):
                        excluded = [p for p in env.get('excluded', []) if fnmatch.fnmatch(lib, p)]
                        if excluded:
                            pass
                        else:
                            shutil.copy(lib, dst)

            cfg = dict(bundle_id=(ctx['bundle_id']))
            if args.target == 'android':
                for arch in env['targets']:
                    cfg.update(dict(target=('android/{}'.format(arch)),
                      local_arch=arch,
                      arch=(ANDROID_TARGETS[arch])))
                    break

            else:
                cfg['target'] = args.target
            cfg.update(env)
            if not os.path.exists(env['python_build_dir']):
                os.makedirs((env['python_build_dir'].format)(**cfg))
            with cd(env['python_build_dir']):
                if os.path.exists('build'):
                    shutil.rmtree('build')
                cp(('{conda_prefix}/{target}/python/'.format)(**cfg), ('{python_build_dir}/build'.format)(**cfg))
                for src in ctx.get('sources', ['src']):
                    cp(join(root, src), 'build')

                with cd('build'):
                    if not args.no_compile:
                        compileall.compile_dir('.')
                        for dp, dn, fn in os.walk('.'):
                            for f in glob(join(dp, '*.py')):
                                if exists(f + 'c') or exists(f + 'o'):
                                    os.remove(f)

                    for pattern in env.get('excluded', []) + ['*.dist-info',
                     '*.egg-info']:
                        matches = glob(pattern)
                        for m in matches:
                            if os.path.isdir(m):
                                shutil.rmtree(m)
                            else:
                                os.remove(m)

                for ext in ('.zip', '.tar.lz4', '.so', '.tar.gz'):
                    if exists('python.{}'.format(ext)):
                        os.remove('python.{}'.format(ext))

                with cd('build'):
                    print(Colors.CYAN + '[DEBUG] Creating python bundle...' + Colors.RESET)
                    with tarfile.open('../' + bundle, 'w:gz') as (tar):
                        tar.add('.')
            if args.target == 'android':
                cp(('{python_build_dir}/{bundle}'.format)(bundle=bundle, **env), 'android/app/src/main/assets/python/{bundle}'.format(bundle=bundle))
            else:
                cp(('{python_build_dir}/build'.format)(bundle=bundle, **env), 'ios/assets/python'.format(bundle=bundle))
        print(Colors.GREEN + '[INFO] Python bundled successfully!' + Colors.RESET)


class ListPackages(Command):
    title = set_default('list')
    help = set_default('List installed packages (alias to conda list)')
    app_dir_required = set_default(False)

    def run(self, args):
        shprint(self.cli.conda, 'list')


class Install(Command):
    __doc__ = ' The "Install" command does a `conda install` of the package names given \n    and then runs the linker command.\n      \n    '
    title = set_default('install')
    help = set_default('Install and link an enaml-native package')
    args = set_default([
     (
      'args', dict(nargs=REMAINDER, help='Alias to conda install'))])
    app_dir_required = set_default(False)

    def run(self, args):
        if os.environ.get('CONDA_DEFAULT_ENV') in (None, 'root'):
            print(Colors.RED + 'enaml-native install should only be usedwithin an app env!' + Colors.RESET)
            raise SystemExit(0)
        shprint(self.cli.conda, 'install', '-y', *args.args)
        self.cmds['link'].run()


class Uninstall(Command):
    __doc__ = ' The "Uninstall" command unlinks the package (if needed) and does a \n    `conda uninstall` of the package names given. \n\n    '
    title = set_default('uninstall')
    help = set_default('Uninstall and unlink enaml-native package')
    args = set_default([
     (
      'args', dict(help='Args to conda uninstall', nargs=REMAINDER))])
    app_dir_required = set_default(False)

    def run(self, args):
        if os.environ.get('CONDA_DEFAULT_ENV') in (None, 'root'):
            print(Colors.RED + 'enaml-native uninstall should only be usedwithin an app env!' + Colors.RESET)
            raise SystemExit(0)
        if hasattr(args, 'names'):
            self.cmds['unlink'].run(args)
        shprint(self.cli.conda, 'uninstall', '-y', *args.args)


class Link(Command):
    __doc__ = ' The "Link" command tries to modify the android and ios projects\n    to include all of the necessary changes for this package to work.\n      \n    A custom linkiner can be used by adding a "enaml_native_linker" \n    entry_point which shall be a function that receives the app package.json \n    (context) an argument. \n    \n    Example\n    ----------\n    \n    def linker(ctx):\n        # Link android and ios projects here\n        return True #: To tell the cli the linking was handled and should \n        return\n    \n    '
    title = set_default('link')
    help = set_default('Link an enaml-native package (updates android and ios projects)')
    args = set_default([
     (
      'names',
      dict(help='Package name (optional) If not set links all projects.',
        nargs='*'))])
    package_dir = 'venv'

    def run(self, args=None):
        print('Linking {}'.format(args.names if (args and args.names) else 'all packages...'))
        if args:
            if args.names:
                for name in args.names:
                    self.link(self.package_dir, name)

        else:
            for target in ('android', 'iphoneos', 'iphonesimulator'):
                sysroot = join(self.package_dir, target)
                for path in os.listdir(sysroot):
                    self.link(sysroot, path)

    def link(self, path, pkg):
        """ Link the package in the current directory.
        """
        if exists(join(path, pkg, 'build.gradle')):
            print(Colors.BLUE + '[INFO] Linking {}/build.gradle'.format(pkg) + Colors.RESET)
            self.link_android(path, pkg)
        if exists(join(path, pkg, 'Podfile')):
            print(Colors.BLUE + '[INFO] Linking {}/Podfile'.format(pkg) + Colors.RESET)
            self.link_ios(path, pkg)

    @staticmethod
    def is_settings_linked(source, pkg):
        """ Returns true if the "include ':<project>'" line exists in the file 
        """
        for line in source.split('\n'):
            if re.search('include\\s*[\'\\"]:{}[\'\\"]'.format(pkg), line):
                return True

        return False

    @staticmethod
    def is_build_linked(source, pkg):
        """ Returns true if the "compile project(':<project>')"
            line exists exists in the file """
        for line in source.split('\n'):
            if re.search('(api|compile)\\s+project\\([\'\\"]:{}[\'\\"]\\)'.format(pkg), line):
                return True

        return False

    @staticmethod
    def find_packages(path):
        """ Find all java files matching the "*Package.java" pattern within
        the given enaml package directory relative to the java source path.
        """
        matches = []
        root = join(path, 'src', 'main', 'java')
        for folder, dirnames, filenames in os.walk(root):
            for filename in fnmatch.filter(filenames, '*Package.java'):
                with open(join(folder, filename)) as (f):
                    if 'implements EnamlPackage' in f.read():
                        package = os.path.relpath(folder, root)
                        matches.append(os.path.join(package, filename))

        return matches

    @staticmethod
    def is_app_linked(source, pkg, java_package):
        """ Returns true if the compile project line exists exists in the file 
        
        """
        for line in source.split('\n'):
            if java_package in line:
                return True

        return False

    def link_android(self, path, pkg):
        """ Link's the android project to this library.

        1. Includes this project's directory in the app's 
            android/settings.gradle
            It adds:
                include ':<project-name>'
                project(':<project-name>').projectDir = new File(
                rootProject.projectDir, '../packages/<project-name>/android')

        2. Add's this project as a dependency to the android/app/build.gradle
            It adds:
                compile project(':<project-name>')
            to the dependencies.

        3. If preset, adds the import and package statement
           to the android/app/src/main/java/<bundle/id>/MainApplication.java

        """
        bundle_id = self.ctx['bundle_id']
        pkg_root = join(path, pkg)
        with open(join('android', 'settings.gradle')) as (f):
            settings_gradle = f.read()
        with open(join('android', 'app', 'build.gradle')) as (f):
            build_gradle = f.read()
        main_app_java_path = join('android', 'app', 'src', 'main', 'java', join(*bundle_id.split('.')), 'MainApplication.java')
        with open(main_app_java_path) as (f):
            main_application_java = f.read()
        try:
            new_packages = Link.find_packages(join(path, pkg))
            if not new_packages:
                print('[Android] {} No EnamlPackages found to link!'.format(pkg))
                return
            if not Link.is_settings_linked(settings_gradle, pkg):
                new_settings = settings_gradle.split('\n')
                new_settings.append('')
                new_settings.append("include ':{name}'".format(name=pkg))
                new_settings.append("project(':{name}').projectDir = new File(rootProject.projectDir, '../{path}/android/{name}')".format(name=pkg,
                  path=(self.package_dir)))
                with open(join('android', 'settings.gradle'), 'w') as (f):
                    f.write('\n'.join(new_settings))
                print('[Android] {} linked in settings.gradle!'.format(pkg))
            else:
                print('[Android] {} was already linked in settings.gradle!'.format(pkg))
            if not Link.is_build_linked(build_gradle, pkg):
                new_build = build_gradle.split('\n')
                found = False
                for i, line in enumerate(new_build):
                    if re.match('dependencies\\s*{', line):
                        found = True
                        continue
                    if found and '}' in line:
                        break

                if not found:
                    raise ValueError('Unable to find dependencies in {pkg}/app/build.gradle!'.format(pkg=pkg))
                new_build.insert(i, "    api project(':{name}')".format(name=pkg))
                with open(join('android', 'app', 'build.gradle'), 'w') as (f):
                    f.write('\n'.join(new_build))
                print('[Android] {} linked in app/build.gradle!'.format(pkg))
            else:
                print('[Android] {} was already linked in app/build.gradle!'.format(pkg))
            new_app_java = []
            for package in new_packages:
                javacls = os.path.splitext(package)[0].replace('/', '.')
                if not Link.is_app_linked(main_application_java, pkg, javacls):
                    new_app_java = new_app_java or main_application_java.split('\n')
                    j = 0
                    for i, line in enumerate(new_app_java):
                        if fnmatch.fnmatch(line, 'import *;'):
                            j = i

                    new_app_java.insert(j + 1, 'import {};'.format(javacls))
                    j = 0
                    for i, line in enumerate(new_app_java):
                        if fnmatch.fnmatch(line.strip(), 'new *Package()'):
                            j = i

                    if j == 0:
                        raise ValueError('Could not find the correct spot to add package {}'.format(javacls))
                    else:
                        new_app_java[j] = new_app_java[j] + ','
                        new_app_java.insert(j + 1, '                new {}()'.format(javacls.split('.')[(-1)]))
                else:
                    print('[Android] {} was already linked in {}!'.format(pkg, main_app_java_path))

            if new_app_java:
                with open(main_app_java_path, 'w') as (f):
                    f.write('\n'.join(new_app_java))
            print(Colors.GREEN + '[Android] {} linked successfully!'.format(pkg) + Colors.RESET)
        except Exception as e:
            print(Colors.GREEN + '[Android] {} Failed to link. Reverting due to error: {}'.format(pkg, e) + Colors.RESET)
            with open(join('android', 'settings.gradle'), 'w') as (f):
                f.write(settings_gradle)
            with open(join('android', 'app', 'build.gradle'), 'w') as (f):
                f.write(build_gradle)
            with open(main_app_java_path, 'w') as (f):
                f.write(main_application_java)
            raise

    def link_ios(self, path, pkg):
        print('[iOS] Link TODO:...')


class Unlink(Command):
    __doc__ = ' The "Unlink" command tries to undo the modifications done by the \n    linker..\n          \n    A custom unlinkiner can be used by adding a "enaml_native_unlinker" \n    entry_point which shall be a function that receives the app \n    package.json (context) an argument. \n    \n    Example\n    ----------\n    \n    def unlinker(ctx):\n        # Unlink android and ios projects here\n        return True #: To tell the cli the unlinking was handled and \n        should return\n    \n    '
    title = set_default('unlink')
    help = set_default('Unlink an enaml-native package')
    args = set_default([
     (
      'names', dict(help='Package name', nargs='+'))])

    def run(self, args=None):
        """ The name IS required here. """
        print(Colors.BLUE + '[INFO] Unlinking {}...'.format(args.names) + Colors.RESET)
        for name in args.names:
            self.unlink(Link.package_dir, name)

    def unlink(self, path, pkg):
        """ Unlink the package in the current directory.
        """
        for ep in pkg_resources.iter_entry_points(group='enaml_native_unlinker'):
            if ep.name.replace('-', '_') == pkg.replace('-', '_'):
                unlinker = ep.load()
                print("Custom unlinker {} found for '{}'. Unlinking...".format(unlinker, pkg))
                if unlinker(self.ctx, path):
                    return

        if exists(join(path, 'android', pkg, 'build.gradle')):
            print('[Android] unlinking {}'.format(pkg))
            self.unlink_android(path, pkg)
        for target in ('iphoneos', 'iphonesimulator'):
            if exists(join(path, target, pkg, 'Podfile')):
                print('[iOS] unlinking {}'.format(pkg))
                self.unlink_ios(path, pkg)

    def unlink_android(self, path, pkg):
        """ Unlink's the android project to this library.

            1. In the app's android/settings.gradle, it removes the following 
            lines (if they exist):
                    include ':<project-name>'
                    project(':<project-name>').projectDir = new File(
                    rootProject.projectDir, 
                        '../venv/packages/<project-name>/android')

            2. In the app's android/app/build.gradle, it removes the following 
            line (if present)
                    compile project(':<project-name>')

            3. In the app's
             android/app/src/main/java/<bundle/id>/MainApplication.java, 
             it removes:
                    import <package>.<Name>Package;
                     new <Name>Package(), 
                     
                  If no comma exists it will remove the comma from the previous 
                  line.
                    
        """
        bundle_id = self.ctx['bundle_id']
        with open(join('android', 'settings.gradle')) as (f):
            settings_gradle = f.read()
        with open(join('android', 'app', 'build.gradle')) as (f):
            build_gradle = f.read()
        main_app_java_path = join('android', 'app', 'src', 'main', 'java', join(*bundle_id.split('.')), 'MainApplication.java')
        with open(main_app_java_path) as (f):
            main_application_java = f.read()
        try:
            new_packages = Link.find_packages(join(path, 'android', pkg))
            if not new_packages:
                print(Colors.RED + '\t[Android] {} No EnamlPackages found to unlink!'.format(pkg) + Colors.RESET)
                return
            if Link.is_settings_linked(settings_gradle, pkg):
                new_settings = [line for line in settings_gradle.split('\n') if line.strip() not in [
                 "include ':{name}'".format(name=pkg),
                 "project(':{name}').projectDir = new File(rootProject.projectDir, '../{path}/android/{name}')".format(path=path,
                   name=pkg)]]
                with open(join('android', 'settings.gradle'), 'w') as (f):
                    f.write('\n'.join(new_settings))
                print('\t[Android] {} unlinked settings.gradle!'.format(pkg))
            else:
                print('\t[Android] {} was not linked in settings.gradle!'.format(pkg))
            if Link.is_build_linked(build_gradle, pkg):
                new_build = [line for line in build_gradle.split('\n') if line.strip() not in [
                 "compile project(':{name}')".format(name=pkg),
                 "api project(':{name}')".format(name=pkg)]]
                with open(join('android', 'app', 'build.gradle'), 'w') as (f):
                    f.write('\n'.join(new_build))
                print('\t[Android] {} unlinked in app/build.gradle!'.format(pkg))
            else:
                print('\t[Android] {} was not linked in app/build.gradle!'.format(pkg))
            new_app_java = []
            for package in new_packages:
                javacls = os.path.splitext(package)[0].replace('/', '.')
                if Link.is_app_linked(main_application_java, pkg, javacls):
                    new_app_java = new_app_java or main_application_java.split('\n')
                    new_app_java = [line for line in new_app_java if line.strip() not in [
                     'import {};'.format(javacls),
                     'new {}()'.format(javacls.split('.')[(-1)]),
                     'new {}(),'.format(javacls.split('.')[(-1)])]]
                    found = False
                    j = 0
                    for i, line in enumerate(new_app_java):
                        if fnmatch.fnmatch(line.strip(), 'new *Package()'):
                            found = True
                        elif fnmatch.fnmatch(line.strip(), 'new *Package(),'):
                            j = i

                    if not found:
                        new_app_java[j] = new_app_java[j][:new_app_java[j].rfind(',')]
                else:
                    print('\t[Android] {} was not linked in {}!'.format(pkg, main_app_java_path))

            if new_app_java:
                with open(main_app_java_path, 'w') as (f):
                    f.write('\n'.join(new_app_java))
            print(Colors.GREEN + '\t[Android] {} unlinked successfully!'.format(pkg) + Colors.RESET)
        except Exception as e:
            print(Colors.RED + '\t[Android] {} Failed to unlink. Reverting due to error: {}'.format(pkg, e) + Colors.RESET)
            with open(join('android', 'settings.gradle'), 'w') as (f):
                f.write(settings_gradle)
            with open(join('android', 'app', 'build.gradle'), 'w') as (f):
                f.write(build_gradle)
            with open(main_app_java_path, 'w') as (f):
                f.write(main_application_java)
            raise


class BuildAndroid(Command):
    title = set_default('build-android')
    help = set_default('Build android project')
    args = set_default([
     (
      '--release', dict(action='store_true', help='Release mode')),
     (
      'extra', dict(nargs=REMAINDER, help='Args to pass to gradle'))])

    def run(self, args=None):
        with cd('android'):
            gradlew = sh.Command('gradlew.bat' if IS_WIN else './gradlew')
            if args:
                if args.release:
                    shprint(gradlew, 'assembleRelease', *(args.extra), **{'_debug': True})
            else:
                shprint(gradlew, 'assembleDebug', *(args.extra), **{'_debug': True})


class CleanAndroid(Command):
    title = set_default('clean-android')
    help = set_default('Clean the android project')

    def run(self, args=None):
        with cd('android'):
            gradlew = sh.Command('gradlew.bat' if IS_WIN else './gradlew')
            shprint(gradlew, 'clean', _debug=True)


class RunAndroid(Command):
    title = set_default('run-android')
    help = set_default('Build android project, install it, and run')
    args = set_default([
     (
      '--release', dict(action='store_true', help='Build in Release mode')),
     (
      'extra', dict(nargs=REMAINDER, help='Extra args to pass to gradle'))])

    def run(self, args=None):
        ctx = self.ctx
        bundle_id = ctx['bundle_id']
        with cd('android'):
            release_apk = os.path.abspath(join('.', 'app', 'build', 'outputs', 'apk', 'app-release-unsigned.apk'))
            gradlew = sh.Command('gradlew.bat' if IS_WIN else './gradlew')
            if len(sh.adb('devices').stdout.strip()) == 1:
                device = sh.emulator('-list-avds').stdout.split('\n')[0]
                shprint(sh.emulator, '-avd', device)
            elif args and args.release:
                shprint(gradlew, 'assembleRelease', *(args.extra), **{'_debug': True})
                shprint(sh.adb, 'install', release_apk)
            else:
                shprint(gradlew, 'installDebug', *(args.extra), **{'_debug': True})
            shprint(sh.adb, 'shell', 'am', 'start', '-n', '{bundle_id}/{bundle_id}.MainActivity'.format(bundle_id=bundle_id))


class CleanIOS(Command):
    title = set_default('clean-ios')
    help = set_default('Clean the ios project')

    def run(self, args=None):
        with cd('ios'):
            shprint(sh.xcodebuild, 'clean', '-project', 'App.xcodeproj', '-configuration', 'ReleaseAdhoc', '-alltargets')


class RunIOS(Command):
    title = set_default('run-ios')
    help = set_default('Build and run the ios project')
    args = set_default([
     (
      '--release', dict(action='store_true', help='Build in Release mode'))])

    def run(self, args=None):
        ctx = self.ctx
        env = ctx['ios']
        with cd('ios'):
            ws = glob('*.xcworkspace')
            if not ws:
                raise RuntimeError("Couldn't find a xcworkspace in the ios folder! Did you run `pod install`? ")
            workspace = ws[0]
            scheme = '.'.join(workspace.split('.')[0:-1])
            shprint(sh.xcrun, 'xcodebuild', '-scheme', scheme, '-workspace', workspace, '-configuration', 'Release' if (args and args.release) else 'Debug', '-allowProvisioningUpdates', '-derivedDataPath', 'run')
            shprint(sh.xcrun, 'simctl', 'launch', 'booted', ctx['bundle_id'])


class BuildIOS(Command):
    title = set_default('build-ios')
    help = set_default('Build the ios project')
    args = set_default([
     (
      '--release', dict(action='store_true', help='Build in Release mode'))])

    def run(self, args=None):
        ctx = self.ctx
        with cd('ios'):
            ws = glob('*.xcworkspace')
            if not ws:
                raise RuntimeError("Couldn't find a xcworkspace in the ios folder! Did you run `pod install`? ")
            workspace = ws[0]
            scheme = '.'.join(workspace.split('.')[0:-1])
            shprint(sh.xcrun, 'xcodebuild', '-scheme', scheme, '-workspace', workspace, '-configuration', 'Release' if (args and args.release) else 'Debug', '-allowProvisioningUpdates', '-derivedDataPath', 'build')


class Server(Command):
    __doc__ = ' Run a dev server to host files. Only view files can be reloaded at the \n    moment. \n    \n    '
    title = set_default('start')
    help = set_default('Start a debug server for serving files to the app')
    index_page = Unicode('enaml-native dev server. When you change a source file it pushes to the app.')
    args = set_default([
     (
      '--remote-debugging',
      dict(action='store_true', help='Run in remote debugging mode'))])
    port = Int(8888)
    reload_delay = Float(1)
    _reload_count = Int()
    observer = Instance(object)
    watcher = Instance(object)
    handlers = List()
    add_callback = Callable()
    call_later = Callable()
    changes = List()
    remote_debugging = Bool()
    app_dir_required = set_default(False)

    def run(self, args=None):
        ctx = self.ctx
        use_twisted = 'twisted' in ', '.join(ctx.get('dependencies', []))
        self.remote_debugging = args and args.remote_debugging
        if self.remote_debugging:
            shprint(sh.adb, 'reverse', 'tcp:{}'.format(self.port), 'tcp:{}'.format(self.port))
        else:
            try:
                from watchdog.observers import Observer
                from watchdog.events import LoggingEventHandler
            except ImportError:
                print(Colors.RED + "[WARNING] Watchdog is required the dev server: Run 'pip install watchdog'" + Colors.RESET)
                return
            else:
                self.observer = Observer()
                server = self

                class AppNotifier(LoggingEventHandler):

                    def on_any_event(self, event):
                        super(AppNotifier, self).on_any_event(event)
                        server.add_callback(server.on_file_changed, event)

        with cd('src'):
            if not self.remote_debugging:
                print('Watching {}'.format(abspath('.')))
                self.watcher = AppNotifier()
                self.observer.schedule((self.watcher), (abspath('.')), recursive=True)
                self.observer.start()
            else:
                if use_twisted:
                    self.run_twisted(args)
                else:
                    self.run_tornado(args)

    def run_tornado(self, args):
        """ Tornado dev server implementation """
        server = self
        import tornado.ioloop, tornado.web, tornado.websocket
        ioloop = tornado.ioloop.IOLoop.current()

        class DevWebSocketHandler(tornado.websocket.WebSocketHandler):

            def open(self):
                super(DevWebSocketHandler, self).open()
                server.on_open(self)

            def on_message(self, message):
                server.on_message(self, message)

            def on_close(self):
                super(DevWebSocketHandler, self).on_close()
                server.on_close(self)

        class MainHandler(tornado.web.RequestHandler):

            def get(self):
                self.write(server.index_page)

        server.call_later = ioloop.call_later
        server.add_callback = ioloop.add_callback
        app = tornado.web.Application([
         (
          '/', MainHandler),
         (
          '/dev', DevWebSocketHandler)])
        app.listen(self.port)
        print('Tornado Dev server started on {}'.format(self.port))
        ioloop.start()

    def run_twisted(self, args):
        """ Twisted dev server implementation """
        server = self
        from twisted.internet import reactor
        from twisted.web import resource
        from twisted.web.static import File
        from twisted.web.server import Site
        from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
        from autobahn.twisted.resource import WebSocketResource

        class DevWebSocketHandler(WebSocketServerProtocol):

            def onConnect(self, request):
                super(DevWebSocketHandler, self).onConnect(request)
                server.on_open(self)

            def onMessage(self, payload, isBinary):
                server.on_message(self, payload)

            def onClose(self, wasClean, code, reason):
                super(DevWebSocketHandler, self).onClose(wasClean, code, reason)
                server.on_close(self)

            def write_message(self, message, binary=False):
                self.sendMessage(message, binary)

        server.call_later = reactor.callLater
        server.add_callback = reactor.callFromThread
        factory = WebSocketServerFactory('ws://0.0.0.0:{}'.format(self.port))
        factory.protocol = DevWebSocketHandler

        class MainHandler(resource.Resource):

            def render_GET(self, req):
                return str(server.index_page)

        root = resource.Resource()
        root.putChild('', MainHandler())
        root.putChild('dev', WebSocketResource(factory))
        reactor.listenTCP(self.port, Site(root))
        print('Twisted Dev server started on {}'.format(self.port))
        reactor.run()

    def on_open(self, handler):
        self._reload_count = 0
        print('Client {} connected!'.format(handler))
        self.handlers.append(handler)

    def on_message(self, handler, msg):
        """ In remote debugging mode this simply acts as a forwarding
        proxy for the two clients.
        """
        if self.remote_debugging:
            for h in self.handlers:
                if h != handler:
                    h.write_message(msg, True)

        else:
            print(msg)

    def send_message(self, msg):
        """ Send a message to the client. This should not be used in
        remote debugging mode.
        
        """
        if not self.handlers:
            return
        for h in self.handlers:
            h.write_message(msg)

    def on_close(self, handler):
        print('Client {} left!'.format(handler))
        self.handlers.remove(handler)

    def on_file_changed(self, event):
        """ """
        print(event)
        self._reload_count += 1
        self.changes.append(event)
        self.call_later(self.reload_delay, self._trigger_reload, event)

    def _trigger_reload(self, event):
        self._reload_count -= 1
        if self._reload_count == 0:
            files = {}
            for event in self.changes:
                path = os.path.relpath(event.src_path, os.getcwd())
                if os.path.splitext(path)[(-1)] not in ('.py', '.enaml'):
                    pass
                else:
                    with open(event.src_path) as (f):
                        data = f.read()
                files[path] = data

            if files:
                msg = {'type':'reload', 
                 'files':files}
                print('Reloading: {}'.format(files.keys()))
                self.send_message(json.dumps(msg))
            self.changes = []


def find_commands(cls):
    """ Finds commands by finding the subclasses of Command"""
    cmds = []
    for subclass in cls.__subclasses__():
        cmds.append(subclass)
        cmds.extend(find_commands(subclass))

    return cmds


class EnamlNativeCli(Atom):
    parser = Instance(ArgumentParser)
    ctx = Dict()
    args = Instance(Namespace)
    package = Unicode('environment.yml')
    in_app_directory = Bool()
    conda = Instance(sh.Command)
    commands = List(Command)

    def _default_commands(self):
        """ Build the list of CLI commands by finding subclasses of the Command 
        class

        Also allows commands to be installed using the "enaml_native_command" 
        entry point. This entry point should return a Command subclass

        """
        commands = [c() for c in find_commands(Command)]
        for ep in pkg_resources.iter_entry_points(group='enaml_native_command'):
            c = ep.load()
            if not issubclass(c, Command):
                print('Warning: entry point {} did not return a valid enaml cli command! This command will be ignored!'.format(ep.name))
            commands.append(c())

        return commands

    def _default_in_app_directory(self):
        """ Return if we are in a directory that contains the package.json file 
        which should indicate it's in the root directory of an enaml-native
        app.
        
        """
        return exists(self.package)

    def _default_ctx(self):
        """ Return the package config or context and normalize some of the 
        values 
        
        """
        if not self.in_app_directory:
            print('Warning: {} does not exist. Using the default.'.format(self.package))
            ctx = {}
        else:
            with open(self.package) as (f):
                ctx = dict(yaml.load(f, Loader=(yaml.RoundTripLoader)))
        if self.in_app_directory:
            excluded = list(ctx.get('excluded', []))
            for env in [ctx['ios'], ctx['android']]:
                if 'python_build_dir' not in env:
                    env['python_build_dir'] = expanduser(abspath('build/python'))
                if 'conda_prefix' not in env:
                    env['conda_prefix'] = os.environ.get('CONDA_PREFIX', expanduser(abspath('venv')))
                env['excluded'] = list(env.get('excluded', [])) + excluded

        return ctx

    def _default_parser(self):
        """ Generate a parser using the command list """
        parser = ArgumentParser(prog='enaml-native')
        cmds = {c.title:c for c in self.commands}
        subparsers = parser.add_subparsers()
        for c in self.commands:
            p = subparsers.add_parser((c.title), help=(c.help))
            c.parser = p
            for flags, kwargs in c.args:
                (p.add_argument)(*flags.split(), **kwargs)

            p.set_defaults(cmd=c)
            c.ctx = self.ctx
            c.cmds = cmds
            c.cli = self

        return parser

    def _default_conda(self):
        return find_conda()

    def check_dependencies(self):
        try:
            self.conda('--version')
        except:
            raise EnvironmentError('conda could not be found. Please install miniconda from https://conda.io/miniconda.html or set CONDA_HOME to thelocation where conda is installed.')

    def start(self):
        """ Run the commands"""
        self.check_dependencies()
        self.args = self.parser.parse_args()
        if not hasattr(self.args, 'cmd'):
            self.parser.print_help()
            return
        cmd = self.args.cmd
        try:
            if cmd.app_dir_required:
                if not self.in_app_directory:
                    raise EnvironmentError("'enaml-native {}' must be run within an app root directory not: {}".format(cmd.title, os.getcwd()))
            cmd.run(self.args)
        except sh.ErrorReturnCode as e:
            raise


def main():
    EnamlNativeCli().start()


if __name__ == '__main__':
    main()