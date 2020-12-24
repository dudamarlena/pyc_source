# -*- coding: utf-8 -*-
'''
    The venvm is small webtool for manager virtualenv.
    Copyright (C) 2013  Rodrigo Pinheiro Matias <rodrigopmatias@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see {http://www.gnu.org/licenses/}.
'''
from setuptools import setup, find_packages

import venvm


setup(
    name='venvm',
    author='Rodrigo Pinheiro Matias',
    author_email='rodrigopmatias@gmail.com',
    license='GLPv3',
    description='The venvm is small webtool for manager virtualenv',
    long_description='',
    version=venvm.__version__,
    include_package_data=True,
    packages=find_packages(),
    url='https://github.com/rodrigopmatias/venvm',
    package_data={
        'venvm': [
            'static/images/*.jpg',
            'static/*.css',
            'static/*.js',
            'templates/*.html',
            'migrate/*.ddl',
            'migrate/*.sql',
            'i18n/*.json',
        ],
    },
    install_requires=[
        'Flask>=0.10.1',
    ],
    entry_points={
        'console_scripts': [
            'venvmd = venvm.server:main',
        ]
    }
)
