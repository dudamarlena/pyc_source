#!/usr/bin/python

import os
from distutils.core import setup

def get_name_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'difio_heroku_python/version.py')) as f:
        (name, version) = (None, None)
        exec(f.read())
        return (name, version)
    raise RuntimeError('No version info found.')

with open('README.rst') as file:
    long_description = file.read()

(name, version) = get_name_version()

setup(
    name=name,
    version=version,
    description='Difio registration agent for Heroku / Python applications',
    author='Alexander Todorov',
    author_email='atodorov@nospam.dif.io',
    url = 'http://github.com/difio/difio-heroku-python',
    packages=['difio_heroku_python'],
    scripts=['difio-heroku-python'],
    keywords = ['heroku', 'difio', 'updates', 'cloud', 'diff'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        ],
    long_description = long_description,
     )
