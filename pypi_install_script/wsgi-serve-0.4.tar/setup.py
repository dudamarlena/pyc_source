#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.build import build

import os
import sys

# load the script, to extract info
wsgi_serve = {}
exec file('wsgi-serve') in wsgi_serve

# if building a distribution package, make sure to generate manpage
if True in ['dist' in arg for arg in sys.argv[1:]]:
    os.system('make')

setup(
    name = 'wsgi-serve',
    version = wsgi_serve['__version__'],
    description = 'Small WSGI development server based on werkzeug.',
    author = 'Florian Wagner',
    author_email = 'florian@wagner-flo.net',
    url = 'http://projects.wagner-flo.net/wsgi-serve/',
    scripts = ['wsgi-serve'],
    data_files = [('man/man1', ['wsgi-serve.1'])],
    classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
          'Topic :: Software Development',
          ],
    )
