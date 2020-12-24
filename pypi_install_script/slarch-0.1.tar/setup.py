#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import slarch

# declarative setup
setup(
    name = 'slarch',
    version = slarch.__version__,
    description = 'Tool for managing archives of logfiles.',
    author = 'Florian Wagner',
    author_email = 'florian@wagner-flo.net',
    url = 'http://projects.wagner-flo.net/slarch/',
    scripts = ['bin/slarch'],
    packages = ['slarch'],
    data_files = [('man/man1', ['man/slarch.1'])],
    classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System :: Logging',
          'Topic :: System :: Archiving',
          'Topic :: Utilities',
          ],
)
