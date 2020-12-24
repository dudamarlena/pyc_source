#!/usr/bin/env python

import glob
import os
import re
import sys
from io import open

from setuptools import setup, Command


if sys.version_info < (2, 7) or (3, 0) <= sys.version_info < (3, 4):
    print('Miko requires at least Python 2.7 or 3.4 to run.')
    sys.exit(1)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# Global functions
##################

with open(os.path.join('miko', '__init__.py'), encoding='utf-8') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

if not version:
    raise RuntimeError('Cannot find Miko version information.')

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


def get_data_files():
    data_files = [
        ('share/doc/miko', ['README.md', 'conf/miko.conf'])
    ]

    return data_files


def get_install_requires():
    requires = ['psutil>=5.3.0', 'click>=4.0,<7.0']
    if sys.platform.startswith('win'):
        requires.append('bottle')

    return requires

# Setup !

setup(
    name='miko',
    version=version,
    description="A cross-platform tool",
    long_description=long_description,
    author='ysicing',
    author_email='i@spanda.io',
    url='https://repo.spanda.io/ysicing/miko-cli',
    license='AGPLv3',
    keywords=['miko', 'cli', 'docker'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=get_install_requires(),
    extras_require={
        'cpuinfo': ['py-cpuinfo'],
        'docker': ['docker>=2.0.0'],
        'ip': ['netifaces']
    },
    packages=['miko'],
    include_package_data=True,
    data_files=get_data_files(),
    entry_points={"console_scripts": ["miko=miko:main"]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)