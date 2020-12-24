# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = 'weave-minimal-uberspace',
    version          = '0.9.1',
    url              = 'https://bitbucket.org/oa/weave-minimal-uberspace',
    license          = 'Apache License 2.0',
    description      = 'A fastcgi wrapper for weave-minimal (for uberspace).',
    long_description = read('README.rst'),
    author           = 'Oliver Andrich',
    author_email     = 'oliver@andrich.me',
    packages         = find_packages('src'),
    package_dir      = {'': 'src'},
    install_requires = ['setuptools', 'weave-minimal'],

    entry_points = {
        'console_scripts': ['weave-minimal.fcgi = weave_minimal_uberspace:main', ],
    },

    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
