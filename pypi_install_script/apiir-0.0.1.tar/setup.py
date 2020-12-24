#!/usr/bin/env python
# coding=utf-8
"""
Setup.py for Mal-py
"""

from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_dsecription = f.read()

config = {
    'url': 'https://github.com/LSmith-Zenoscave/APIIR',
    'name': 'apiir',
    'version': '0.0.1',
    'description': 'API Internal Representation Translator using CherryPy',
    'long_description': long_dsecription,
    'author': 'Luke Smith',
    'author_email': 'lsmith@zenoscave.com',
    'license': 'BSD',
    'entry_points': {
        'console_scripts': [
            'apiir = apiir.__main__:main'
        ]
    },
    'packages': [
        'apiir'
    ],
    'install_requires': [],
    'tests_require': [
        'pytest',
        'nose'
    ],
    'extras_require': {
        'test': [
            'pytest'
        ],
        'docstest': [
            'doc8',
            'pyenchant',
            'readme_renderer >= 16.0',
            'sphinx',
            'sphinx_rtd_theme',
            'sphinxcontrib-spelling'
        ],
        'pep8test': [
            'flake8',
            'flake8-import-order',
            'pep8-naming'
        ]
    }
}

setup(**config)
