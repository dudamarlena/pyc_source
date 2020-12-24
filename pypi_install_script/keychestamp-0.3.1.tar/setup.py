# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module: keychestamp
***
"""
# Copyright (C) KeyChest Ltd, registered in the United Kingdom.
#
# This file is provided under a license as specified in the "LICENSE" file, which is part
# of this software package.
#
# Written by KeyChest <support@keychest.net>, 2019

import sys
from setuptools import setup, find_packages
from keychestamp.version import proxy_version

version = proxy_version

# pypi publishing
# 1. set $HOME/.pypirc
#      [distutils]
#      index-servers =
#          pypi
#
#      [pypi]
#      username: <name>
#      password: <password>
# 2. deactivate  // if there's an active env
# 3. cd pycharmenv3; source bin/activate
# 4. pip3 install --upgrade wheel setuptools twine
# 5. cd <whatever_to>/keychestamp
# 6. rm -rf dist/*
# 7. python3 setup.py sdist bdist_wheel
# 7a.twine check dist/*
# 8. twine upload dist/<latest>.tar.gz
# 9. you can test it with "pip3 install --upgrade --no-cache-dir keychestamp"


install_requires = [
    'requests',
    'certifi'
]

if sys.version_info < (3,):
    print("Python 2 and Python 3.5 or lower are not supported")
    pass

setup(
    name='keychestamp',
    version=version,
    packages=find_packages(),
    namespace_packages=['keychestamp'],
    include_package_data=True,
    package_data={'keychestamp': ['LICENSE']},
    install_requires=install_requires,
    url='https://gitlab.com/keychest/keychestamp',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='KeyChest Ltd',
    author_email='support@keychest.net',
    python_requires='>=3.5',
    description='ACMEv2 proxy to manage clients and observe rate limits of Let\'s Encrypt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Networking',
        'Topic :: Internet :: Proxy Servers'
    ],
    extras_require={
        # 'dev': dev_extras,
        # 'docs': docs_extras,
    },

    entry_points={
        'console_scripts': [
            'keychestamp=keychestamp.main:main'
        ],
    }
)
