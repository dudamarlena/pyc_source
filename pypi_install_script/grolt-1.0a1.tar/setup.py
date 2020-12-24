#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2002-2016 "Neo Technology,"
# Network Engine for Objects in Lund AB [http://neotechnology.com]
#
# This file is part of Neo4j.
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


from setuptools import setup, find_packages

from grolt.meta import package, version


packages = find_packages(exclude=("tests", "tests.*"))
package_metadata = {
    "name": package,
    "version": version,
    "description": "Runner for Neo4j + Docker",
    "long_description": "Please see https://github.com/neo4j-drivers/grolt "
                        "for details.",
    "author": "Neo4j",
    "author_email": "drivers@neo4j.com",
    "entry_points": {
        "console_scripts": [
            "grolt = grolt.__main__:grolt",
        ],
    },
    "packages": packages,
    "install_requires": [
        "certifi",
        "click~=7.0",
        "docker",
        "urllib3<1.25,>=1.23",
        'pyreadline>=2.1 ; platform_system=="Windows"',
    ],
    "license": "Apache License, Version 2.0",
    "classifiers": [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database",
        "Topic :: Software Development",
    ],
}

setup(**package_metadata)
