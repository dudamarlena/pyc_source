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
import sys
import codecs
import fileinput
import shutil

from setuptools import setup

from package_info import __version__

from package_info import __contact_names__
from package_info import __contact_emails__
from package_info import __repository_url__
from package_info import __download_url__
from package_info import __description__
from package_info import __license__
from package_info import __keywords__

from package_info import __faked_packages__


# Get the long description
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def build_package(pkg_name):

    with codecs.open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name=pkg_name,

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
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: OS Independent',
        ],
        platforms=["Linux"],
        keywords=__keywords__,
    )


if sys.argv[1] == "sdist":
    def maybe_delete_file(filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def edit_readme(package_name):

        shutil.copyfile("README.rst.source", "README.rst")

        def replace_in_file(search_text, new_text):
            with fileinput.input("README.rst", inplace=True) as f:
                for line in f:
                    new_line = line.replace(search_text, new_text)
                    print(new_line, end='')

        replace_in_file("Fake Python Project", package_name.upper())
        replace_in_file("===================", "=" * len(package_name))

    for __package_name__ in __faked_packages__:
        maybe_delete_file("PACKAGE_NAME")

        with open("PACKAGE_NAME", "w") as f:
            f.write(__package_name__)

        edit_readme(package_name=__package_name__)

        build_package(__package_name__)
        maybe_delete_file("PACKAGE_NAME")
        maybe_delete_file("README.rst")
        shutil.rmtree("%s.egg-info" % __package_name__.replace("-", "_"))

else:
    raise RuntimeError("This package should not be installed. Please refer "
                       "to NVIDIA instructions. Your PIP command defaults to "
                       "PyPI as a package repository.")
