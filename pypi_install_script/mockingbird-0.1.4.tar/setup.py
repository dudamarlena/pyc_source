#!/usr/bin/env python
import os
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

packages = [
    'mockingbird',
    'mockingbird.generators',
    'mockingbird.repositories',
    'mockingbird.repositories.collections',
    'mockingbird.repositories.numbers',
    'mockingbird.repositories.strings',
]

requires = []

setup(
    name='mockingbird',
    version='0.1.4',
    description='Your models, fake data',
    long_description=readme,
    author='Adam Venturella',
    author_email='aventurella@gmail.com',
    url='http://github.com/aventurella/mockingbird',
    license=license,
    packages=packages,
    package_data={'': ['LICENSE'],
                  'mockingbird': ['resources/*.txt']},
    include_package_data=True,
    install_requires=requires,
    package_dir={'mockingbird': 'mockingbird'},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
    ),

)
