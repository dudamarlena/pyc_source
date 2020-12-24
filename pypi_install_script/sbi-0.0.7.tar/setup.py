#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

long_description = open('README.rst').read() + '\n\n' + open('HISTORY.rst').read()

license = open('LICENSE').read()

requirements_lines = [line.strip() for line in open('requirements.txt').readlines()]
install_requires = list(filter(None, requirements_lines))

setup(
    name='sbi',
    version='0.0.7',
    description='Dead simple Python wrapper for Google Search By Image',
    long_description=long_description,
    keywords='google image search web content scraper parser crawler',
    author='Vinta Chen',
    author_email='vinta.chen@gmail.com',
    url='https://github.com/vinta/sbi.py',
    license=license,
    install_requires=install_requires,
    include_package_data=True,
    py_modules=['sbi', ],
    test_suite='test_sbi',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Chinese (Traditional)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ),
)
