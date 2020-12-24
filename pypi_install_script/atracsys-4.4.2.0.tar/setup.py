#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for atracsys.
    Use setup.cfg to configure your project.
"""

import os
import re
import sys
import platform
import subprocess

from setuptools import setup, find_packages, Extension, Distribution
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from distutils.version import LooseVersion
from pkg_resources import require, VersionConflict
from distutils import log

class AtracysDistribution(Distribution):
    global_options = Distribution.global_options + [
        ('sdk-ftk-lib-path=', None, 'The path to atracsys SDK libs'),
        ('sdk-stk-lib-path=', None, 'The path to atracsys SDK libs'),
        ('sdk-include-path=', None, 'The path to atracsys SDK includes'),
        ('sdk-samples-path=', None, 'The path to atracsys SDK samples'),
        ('sdk-build-type=', None, 'The build type of the SDK'),
        ('private=', None, 'True is the build is private'),
    ]

    def __init__(self, attrs=None):
        self.sdk_ftk_lib_path = None
        self.sdk_stk_lib_path = None
        self.sdk_include_path = None
        self.sdk_samples_path = None
        self.sdk_build_type = 'Release'
        self.private = False
        super().__init__(attrs)

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.join(os.path.abspath(sourcedir),'src','atracsys','cpp')

class CMakeBuild(build_ext):

    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
        if cmake_version < '3.10.0':
            raise RuntimeError("CMake >= 3.10.0 is required.")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'

        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            cmake_args += ['-DCMAKE_GENERATOR_PLATFORM=x64']
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            build_args += ['--', '-j2']

        if self.distribution.sdk_build_type is None:
            self.distribution.sdk_build_type = 'RelWithDebInfo'
        cmake_args += ['-DCMAKE_BUILD_TYPE=' + self.distribution.sdk_build_type]

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Three possibilities here:

        # 1. We are building from setup.py directly at Atracsys (for dev.). In that case,
        # the global parameters should be set correctly.
        if self.distribution.sdk_ftk_lib_path is not None or self.distribution.sdk_stk_lib_path is not None :
            
            if self.distribution.private:
                cmake_args += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=ON']
            else:
                cmake_args += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=OFF']

            cmake_args += ['-DATRACSYS_SDK_INCLUDE_PATH=' + self.distribution.sdk_include_path]
            cmake_args += ['-DATRACSYS_SDK_SAMPLES_PATH=' + self.distribution.sdk_samples_path]
            
            # ftk build
            if self.distribution.sdk_ftk_lib_path is not None:
                cmake_args_for_ftk = cmake_args
                cmake_args_for_ftk += ['-DTRACKER_TYPE=ftk']
                cmake_args_for_ftk += ['-DATRACSYS_SDK_LIB_PATH=' + self.distribution.sdk_ftk_lib_path]
                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_ftk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

            # stk build
            if self.distribution.sdk_stk_lib_path is not None:
                cmake_args_for_stk = cmake_args
                cmake_args_for_stk += ['-DTRACKER_TYPE=stk']
                cmake_args_for_stk += ['-DATRACSYS_SDK_LIB_PATH=' + self.distribution.sdk_stk_lib_path]
                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_stk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

        # 2. We are building on target, through pip install and on Windows
        elif os.name == 'nt':
            
            import winreg

            # If fusionTrack is installed, build for it.
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Atracsys\fusionTrack" , 0,
                                    winreg.KEY_READ)
                cmake_args_for_ftk = cmake_args
                cmake_args_for_ftk += ['-DTRACKER_TYPE=ftk']

                value, regtype = winreg.QueryValueEx(registry_key, 'Root')
                log.info("fusionTrack folder is {0}".format(value))
                if os.path.isfile(os.path.join(value,'include','ftkInterfacePrivate.h')):
                    # We are building in private
                    log.info("Building PRIVATE python wrapper")
                    cmake_args_for_ftk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=ON']
                else:
                    cmake_args_for_ftk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=OFF']

                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_ftk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
            except:
                pass

            # If spryTrack is installed, build for it.
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Atracsys\spryTrack" , 0,
                                    winreg.KEY_READ)
                cmake_args_for_stk = cmake_args
                cmake_args_for_stk += ['-DTRACKER_TYPE=stk']

                value, regtype = winreg.QueryValueEx(registry_key, 'Root')
                log.info("spryTrack folder is {0}".format(value))
                if os.path.isfile(os.path.join(value,'include','ftkInterfacePrivate.h')):
                    # We are building in private
                    log.info("Building PRIVATE python wrapper")
                    cmake_args_for_stk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=ON']
                else:
                    cmake_args_for_stk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=OFF']

                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_stk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
            except:
                pass

        # 3. We are building on Linux
        else:

            if ( not 'ATRACSYS_FTK_HOME' in os.environ ) and ( not 'ATRACSYS_STK_HOME' in os.environ ):
                raise RuntimeError("Please make the env variable ATRACSYS_FTK_HOME or ATRACSYS_STK_HOME (or both) point to your fusionTrack/spryTrack installation folder.")

            # If fusionTrack is installed, build for it.
            if 'ATRACSYS_FTK_HOME' in os.environ:
                cmake_args_for_ftk = cmake_args
                cmake_args_for_ftk += ['-DTRACKER_TYPE=ftk']

                if os.path.isfile(os.path.join(os.environ['ATRACSYS_FTK_HOME'],'include','ftkInterfacePrivate.h')):
                    # We are building in private
                    cmake_args_for_ftk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=ON']
                else:
                    cmake_args_for_ftk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=OFF']

                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_ftk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

            # If spryTrack is installed, build for it.
            if 'ATRACSYS_STK_HOME' in os.environ:
                cmake_args_for_stk = cmake_args
                cmake_args_for_stk += ['-DTRACKER_TYPE=stk']

                if os.path.isfile(os.path.join(os.environ['ATRACSYS_STK_HOME'],'include','ftkInterfacePrivate.h')):
                    # We are building in private
                    cmake_args_for_stk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=ON']
                else:
                    cmake_args_for_stk += ['-DBUILD_WITH_PRIVATE_SDK:BOOL=OFF']

                subprocess.check_call(['cmake', ext.sourcedir] + cmake_args_for_stk, cwd=self.build_temp, env=env)
                subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

if __name__ == "__main__":

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        name='atracsys',
        long_description=long_description,
        long_description_content_type="text/markdown",
        use_scm_version = {"root": "..", "relative_to": __file__},
        setup_requires=['setuptools_scm==3.2.0','sphinx'],
        packages=find_packages(),
        ext_modules=[CMakeExtension('cmake')],
        distclass=AtracysDistribution,
        cmdclass={
            'build_ext': CMakeBuild,
        },
    )
