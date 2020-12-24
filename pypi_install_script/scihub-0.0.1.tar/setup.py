# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='scihub',
    version='0.0.1',
    author='Alejandro Gallo',
    author_email='aamsgallo@gmail.com',
    license='GPLv3',
    url='https://github.com/alejandrogallo/python-scihub',
    install_requires=[
        "beautifulsoup4>=4.4.1",
        "requests>=2.11.1",
        "retrying",
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    description='Unofficial scihub API',
    long_description=long_description,
    keywords=[
        'bibtex', 'scihub', 'api', 'sci-hub',
        'management', 'cli', 'biliography'
    ],
    packages=['scihub'],
    platforms=['linux', 'osx'],
)
