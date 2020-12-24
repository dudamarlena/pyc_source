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
from setuptools import find_packages
from setuptools.command.install import install

from auto_pip_idx import __version__

from auto_pip_idx import __package_name__
from auto_pip_idx import __contact_names__
from auto_pip_idx import __contact_emails__
from auto_pip_idx import __repository_url__
from auto_pip_idx import __download_url__
from auto_pip_idx import __description__
from auto_pip_idx import __license__
from auto_pip_idx import __keywords__

from edit_pip_configuration import create_pip_config_file


class InstallWrapper(install):

    def run(self):
        # Run this first so the install stops in case
        # these fail otherwise the Python package is
        # successfully installed
        self.pre_build_script()

        # Run the standard PyPi copy
        install.run(self)

        self.post_build_script()

    def pre_build_script(self):
        from pip._internal.configuration import get_configuration_files
        file_dict = get_configuration_files()

        for key, files in file_dict.items():
            print(
                "\n\t#################\n\tKey: %s\n\t#################\n" % key)
            for file in files:
                try:
                    if not os.path.exists(file):
                        create_pip_config_file(file)
                    print(file, os.path.exists(file))
                except (FileNotFoundError, PermissionError):
                    pass

        print("\n#################\nthis is PRE build\n#################\n")

    def post_build_script(self):
        print("\n##################\nthis is POST build\n##################\n")


# Get the long description
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=__package_name__,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    description=__description__,
    long_description=long_description,

    # The project's main homepage.
    url=__repository_url__,
    download_url=__download_url__,

    # Author details
    author=__contact_names__,
    author_email=__contact_emails__,

    # maintainer Details
    maintainer=__contact_names__,
    maintainer_email=__contact_emails__,

    # The licence under which the project is released
    license=__license__,
    classifiers=[
        # How mature is this project? Common values are
        #  1 - Planning
        #  2 - Pre-Alpha
        #  3 - Alpha
        #  4 - Beta
        #  5 - Production/Stable
        #  6 - Mature
        #  7 - Inactive
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',

        # Indicate what your project relates to
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        # Additional Settings
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    keywords=__keywords__,
    packages=find_packages(),
    cmdclass={'install': InstallWrapper},
)

