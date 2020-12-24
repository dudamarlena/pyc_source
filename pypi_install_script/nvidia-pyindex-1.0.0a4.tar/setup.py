#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import codecs

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

import wheel.bdist_wheel

from package_info import __version__

from package_info import __package_name__
from package_info import __contact_names__
from package_info import __contact_emails__
from package_info import __repository_url__
from package_info import __download_url__
from package_info import __description__
from package_info import __license__
from package_info import __keywords__

from edit_pip_configuration import create_pip_config_file
from edit_pip_configuration import maybe_edit_pip_config_file


def _install_nvidia_pypi_index():
    from pip._internal.configuration import get_configuration_files
    file_dict = get_configuration_files()

    print("\n######################\n")
    for key, files in file_dict.items():
        for file in files:
            print("Processing pip conf file: %s ..." % file)
            try:
                if not os.path.exists(file):
                    create_pip_config_file(file)
                else:
                    maybe_edit_pip_config_file(file)
            except (FileNotFoundError, PermissionError):
                pass
    print("\n######################\n")


class InstallCommand(install):
    """A class for "pip install".
    Handled by "pip install rpm-py-installer",
    when the package is published to PyPI as a source distribution (sdist).
    """

    def run(self):
        """Run install process."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("COMMAND: %s" % InstallCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        _install_nvidia_pypi_index()
        super(InstallCommand, self).run()


class DevelopCommand(develop):
    """A class for setuptools development mode.
    Handled by "pip install -e".
    """

    def run(self):
        """Run install process with development mode."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("COMMAND: %s" % DevelopCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        _install_nvidia_pypi_index()
        super(DevelopCommand, self).run()


class EggInfoCommand(egg_info):
    """A class for egg-info.
    Handled by "pip install .".
    """

    def run(self):
        """Run egg_info process."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("EggInfoCommand: %s" % EggInfoCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # _install_nvidia_pypi_index()
        super(EggInfoCommand, self).run()


# This mechanism insures two things:
# - prevent the package to be packaged as a wheel
# - prevent the package to be cached during install
class BdistWheelCommand(wheel.bdist_wheel.bdist_wheel):
    """A class for "pip bdist_wheel".
    Raise exception to always disable wheel cache.
    See https://github.com/pypa/pip/issues/4720
    """

    def run(self):
        """Run bdist_wheel process.
        It raises error to make the method fail intentionally.
        """
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("EggInfoCommand: %s" % BdistWheelCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        self.skip_build = True
        super(BdistWheelCommand, self).run()
        # raise distutils.errors.DistutilsClassError(
        #     "This package is not designed to be built as a wheel package."
        # )
        # pass



# Get the long description
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=__package_name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    url=__repository_url__,
    download_url=__download_url__,
    author=__contact_names__,
    author_email=__contact_emails__,
    maintainer=__contact_names__,
    maintainer_email=__contact_emails__,
    license=__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords=__keywords__,
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand,
        'egg_info': EggInfoCommand,
        'bdist_wheel': BdistWheelCommand,
    },
)