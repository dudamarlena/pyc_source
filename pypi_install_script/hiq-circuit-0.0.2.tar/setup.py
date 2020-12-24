import os
import re
import sys
import platform
import subprocess

import setuptools
from setuptools.command.build_ext import build_ext
from distutils.command.clean import clean
from distutils.version import LooseVersion

# This reads the __version__ variable from _version.py
exec(open('_version.py').read())

# Readme file as long_description:
long_description = open('README.rst').read()

# Readthedocs env value
on_rtd = os.environ.get('READTHEDOCS') == 'True'


def get_python_executable():
    try:
        root_path = os.environ['VIRTUAL_ENV']
        python = os.path.basename(sys.executable)
        python_path = os.path.join(root_path, python)
        if os.path.exists(python_path):
            return python_path
        else:
            return os.path.join(root_path, 'bin', python)
    except KeyError:
        return sys.executable


def get_cmake_command():
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(['cmake', '--version'],
                                  stdout=devnull,
                                  stderr=devnull)
        return ['cmake']
    except (OSError, subprocess.CalledProcessError):
        pass

    # CMake not in PATH, should have installed Python CMake module
    # -> try to find out where it is
    try:
        root_path = os.environ['VIRTUAL_ENV']
        python = os.path.basename(sys.executable)
    except KeyError:
        root_path, python = os.path.split(sys.executable)

    search_paths = [
        root_path,
        os.path.join(root_path, 'bin'),
        os.path.join(root_path, 'Scripts')
    ]

    # First try executing CMake directly
    for base_path in search_paths:
        try:
            cmake_cmd = os.path.join(base_path, 'cmake')
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([cmake_cmd, '--version'],
                                      stdout=devnull,
                                      stderr=devnull)
            return [cmake_cmd]
        except (OSError, subprocess.CalledProcessError):
            pass

    # That did not work: try calling it through Python
    for base_path in search_paths:
        try:
            cmake_cmd = [python, os.path.join(base_path, 'cmake')]
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(cmake_cmd + ['--version'],
                                      stdout=devnull,
                                      stderr=devnull)
            return cmake_cmd
        except (OSError, subprocess.CalledProcessError):
            pass

    # Nothing worked -> give up!
    return None


def get_install_requires():
    if on_rtd:
        requirements_file = 'docs/requirements_rtd.txt'
    else:
        requirements_file = 'requirements.txt'

    # Read in requirements.txt
    with open(requirements_file, 'r') as f_requirements:
        requirements = f_requirements.readlines()
    requirements = [r.strip() for r in requirements]

    # Add CMake as dependency if we cannot find the command
    if get_cmake_command() is None:
        requirements.append('cmake')

    return requirements


class CMakeExtension(setuptools.Extension):
    def __init__(self, name, sourcedir=''):
        """
        Constructor

        Note:
            CMake target name is automatically deduced from the name.
            E.g. projectq.backends._ext
                 |_ target = _ext
                 |_ destination_path ~ projectq/backends
        """
        module_path = name.split('.')
        self.target = module_path[-1]
        self.lib_filepath = os.path.join(*module_path)
        self.sourcedir = os.path.abspath(sourcedir)
        setuptools.Extension.__init__(self, name, sources=[])


class CMakeBuild(build_ext):
    def build_extensions(self):
        self.cmake_cmd = get_cmake_command()
        assert self.cmake_cmd is not None
        print('using cmake command:', self.cmake_cmd)
        out = subprocess.check_output(self.cmake_cmd + ['--version'])

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        self.cmake_configure_build()
        self.parallel = 2
        build_ext.build_extensions(self)

    def cmake_configure_build(self):
        self.cfg = 'Debug' if self.debug else 'Release'
        cmake_args = ['-DPYTHON_EXECUTABLE=' + get_python_executable(),
                      '-DBoost_NO_BOOST_CMAKE=ON',
                      '-DBUILD_TESTING=OFF',
                      '-DIS_PYTHON_BUILD=ON',
                      '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON']
        for ext in self.extensions:
            dest_path = os.path.abspath(
                os.path.dirname(self.get_ext_fullpath(ext.lib_filepath)))
            cmake_args.append('-D{}_LIBRARY_OUTPUT_DIRECTORY={}'.format(
                ext.target.upper(), dest_path))

        self.build_args = ['--config', self.cfg]

        if platform.system() == "Windows":
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            self.build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + self.cfg]
            self.build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''), self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(self.cmake_cmd + [ext.sourcedir] + cmake_args,
                              cwd=self.build_temp,
                              env=env)

    def build_extension(self, ext):
        subprocess.check_call(
            self.cmake_cmd + ['--build', '.', '--target', ext.target]
            + self.build_args,
            cwd=self.build_temp)


ext_modules = [
    CMakeExtension('projectq.backends._hiqsim._cppsim_mpi'),
    CMakeExtension('projectq.backends._hiqsim._cppstabsim'),
    CMakeExtension('projectq.cengines._sched_cpp'),
]


class Clean(clean):
    def run(self):
        # Execute the classic clean command
        clean.run(self)
        import glob
        from distutils.dir_util import remove_tree
        egg_info = glob.glob('pysrc/*.egg-info')
        if egg_info:
            remove_tree(egg_info[0])


if on_rtd:
    setuptools.setup(
        name='hiq-circuit',
        version=__version__,
        author='hiq',
        author_email='hiqinfo@huawei.com',
        description='A high performance distributed quantum simulator',
        long_description=long_description,
        url="https://github.com/Huawei-HiQ/HiQsimulator",
        install_requires=get_install_requires(),
        zip_safe=False,
        license='Apache 2',
        packages=['projectqy/backends',
                  'projectq/backends/_hiqsim',
                  'projectq/cengines',
                  'projectq/ops'],
        package_dir={'': 'pysrc'},
    )
else:
    setuptools.setup(
        name='hiq-circuit',
        version=__version__,
        author='hiq',
        author_email='hiqinfo@huawei.com',
        description='A high performance distributed quantum simulator',
        long_description=long_description,
        url="https://github.com/Huawei-HiQ/HiQsimulator",
        install_requires=get_install_requires(),
        cmdclass=dict(build_ext=CMakeBuild, clean=Clean),
        zip_safe=False,
        license='Apache 2',
        packages=setuptools.find_packages(where='pysrc'),
        package_dir={'': 'pysrc'},
        ext_modules=ext_modules)
