#!/usr/bin/env python

import os.path
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setupconf = dict(
    name='aldjemy_forked',
    version="1.0.3",
    license='BSD',
    url='https://github.com/onosendi/aldjemy',
    author='Mihail Krivushin',
    author_email='onosendi@protonmail.com',
    description=('SQLAlchemy to Django integration library'),
    long_description = read('README.rst'),
    packages = find_packages(),

    install_requires = ['sqlalchemy>0.7.1'],

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        ],
    )

if __name__ == '__main__':
    setup(**setupconf)
