# Copyright 2019 Flowdas Inc., 오동권(Dong-gweon Oh) <propsero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

setup_requires = [
]

install_requires = [
    'importlib_resources;python_version<"3.7"',
]

tests_require = [
    'pytest',
    'coverage',
    'pytest-cov',
    'tox',
]

dev_require = tests_require + [
]

setup(
    name='calypso',
    version=open('VERSION').read().strip(),
    url='https://github.com/flowdas/flowdas',
    project_urls={
        "Code": "https://github.com/flowdas/flowdas",
        "Issue tracker": "https://github.com/flowdas/flowdas/issues",
    },
    description='Calypso',
    long_description=open('README.rst').read(),
    author='Flowdas Inc.',
    author_email='propsero@flowdas.com',
    license='MPL 2.0',
    packages=[
        'calypso',
    ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'dev': dev_require,
    },
    scripts=[],
    entry_points={
        'console_scripts': [
            # 'calypso=calypso.cli:Calypso.main',
        ],
    },
    zip_safe=False,
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
