#!/usr/bin/env python
#
# Copyright 2014 Xavier Bruhiere


import os
from glob import glob
from setuptools import setup, find_packages
from okdoc import __version__, __author__, __licence__


requires = [
    'sh==1.09',
    'Jinja2==2.7.2',
    'docopt==0.6.1']


def long_description():
    try:
        #with codecs.open(readme, encoding='utf8') as f:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return "failed to read README.md"


setup(
    name='okdoc',
    version=__version__,
    description='Automatic documentation website, with style and lazyness',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    packages=find_packages(),
    long_description=long_description(),
    license=__licence__,
    install_requires=requires,
    url="https://github.com/hackliff/okdoc",
    entry_points={
        'console_scripts': [
            'okdoc = okdoc.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
    ],
    data_files=[(os.path.expanduser('~/.okdoc/'), glob('./templates/*'))]
)
