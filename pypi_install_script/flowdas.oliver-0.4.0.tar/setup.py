# coding=utf-8
# Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup, find_packages, Extension

setup_requires = [
    'setuptools>=35.0',
]

install_requires = [
    'flowdas',
    'gunicorn>=19.7',
    'gevent>=1.2',
    'click>=6.7,<6.8',
    'falcon>=1.2',
    'setproctitle>=1.1',
    'PyYAML',
]

tests_require = [
    'pytest>=3.1',
    'coverage>=4.4',
    'tox>=2.7',
]

dependency_links = [
]

ext_modules = [
    Extension('flowdas.oliver.parser', [
        'flowdas/oliver/parser.c',
        'vendor/http-parser/http_parser.c',
    ]),
]

setup(
    name='flowdas.oliver',
    version=open('VERSION').read().strip(),
    url='https://bitbucket.org/flowdas/oliver',
    description='Oliver: A pretty fast WSGI server',
    author='Flowdas Inc.',
    author_email='prospero@flowdas.com',
    license='MPL 2.0',
    packages=[
        'flowdas.oliver',
    ],
    ext_modules=ext_modules,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    dependency_links=dependency_links,
    scripts=[],
    entry_points={
        'console_scripts': [
            'oliver=flowdas.oliver.base:main',
        ],
    },
    zip_safe=False,
    keywords=('http', 'wsgi', 'server', 'gevent', 'asynchronous'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
