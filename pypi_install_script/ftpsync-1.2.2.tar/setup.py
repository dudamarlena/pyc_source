#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re


def version_get():
    with open('ftpsync/__init__.py') as fd:
        for line in fd:
            m = re.match('^PROGRAM_VERSION = "(?P<version>[0-9.]+)"',
                         line)
            if m:
                return m.group('version')


setup(name="ftpsync",
      version=version_get(),
      description="Sync local path with FTP remote efficiently "
      "by transmitting only what is necessary",
      author="Leandro Lisboa Penz",
      author_email="lpenz@lpenz.org",
      url="http://github.com/lpenz/ftpsync",
      data_files=[('share/man/man1', ['ftpsync.1'])],
      packages=['ftpsync'],
      scripts=["bin/ftpsync"],
      long_description="""\
ftpsync is a program that synchronizes all files beneath the current
directory with an FTP host efficiently by keeping a remote file with
the hashes of the files sent.
""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'License :: OSI Approved :: '
          'GNU General Public License v2 or later (GPLv2+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          ],
      license="GPL2")
