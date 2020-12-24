# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name = 'couchql',
      version = '0.1',
      description = 'An SQL-like interface to CouchDB',
      author = 'Andrew Wilkinson',
      author_email = 'andrewjwilkinson@gmail.com',
      url = 'http://code.google.com/p/couchql',
      license = 'Apache Software License 2.0',
      packages = ['couchql'],
      requires = ["CouchDB"],
      classifiers = ['Intended Audience :: Developers',
                     'Programming Language :: Python',
                     'Development Status :: 3 - Alpha',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Database'
                    ]
     )
