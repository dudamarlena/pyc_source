#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2016-2018 Cyril Desjouy <cyril.desjouy@univ-lemans.fr>
#
# This file is part of plight
#
# plight is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# plight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with plight. If not, see <http://www.gnu.org/licenses/>.
#
#
# Creation Date : mar. 10 avril 2018 17:52:42 CEST
"""
-----------

setup file for plight

-----------
"""

from setuptools import setup, find_packages

setup(
    name='plight',
    description="Screen backlight adjustment",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    version="0.0.1",
    license="GPL",
    url='https://github.com/ipselium/plight',
    author="Cyril Desjouy",
    author_email="cyril.desjouy@univ-lemans.fr",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    entry_points={
        'console_scripts': [
            'plight = plight.plight:main',
        ],
    }
)
