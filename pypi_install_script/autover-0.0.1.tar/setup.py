#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = dict(
    name='autover',
    version="0.0.1",
    description='Autover provides consistent and up-to-date `__version__` strings for Python packages.',
    long_description=open('README.rst').read() if os.path.isfile('README.rst') else 'Consult README.rst',
    author= "IOAM",
    author_email= "developers@topographica.org",
    maintainer="IOAM",
    maintainer_email="developers@topographica.org",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    url='http://github.com/ioam/autover/',
    packages = ["autover"],
    provides = ["autover"],
    scripts = ["scripts/autover"],
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"]
)



if __name__=="__main__":

    if ('upload' in sys.argv) or ('sdist' in sys.argv):
        import autover
        autover.__version__.verify(setup_args['version'])

    setup(**setup_args)
