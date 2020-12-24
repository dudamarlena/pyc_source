#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import di
version = di.__version__

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name = "python-di",
    version = version,
    author = "Lukas Buenger",
    author_email = "lukasbuenger@gmail.com",
    description = ("A dependency injection injection library for python >= 3.3"),
    license = "BSD",
    keywords = "python dependency injection di",
    url = "https://github.com/lukasbuenger/python-di",
    packages=['di', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
    ],
)