# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kurzfile/release.py
# Compiled at: 2011-01-30 18:33:07
"""A library to handle Kurzweil K-series synthesizer object files.

Currently this provides classes and functions to parse and represent .KRZ/.K25
and .K26 files and a script to list all objects contained in such files.

**This is still alpha-quality software!**

There is a public, read-only Subversion repository for this package located at
``svn://svn.chrisarndt.de/projects/kurzfile``. To check out a working copy of
the current trunk, do::

    svn co svn://svn.chrisarndt.de/projects/kurzfile/trunk kurzfile

"""
name = 'kurzfile'
version = '0.4a'
description = __doc__.splitlines()
long_description = ('\n').join(description[2:])
description = description[0]
keywords = 'kurzweil, music'
author = 'Christopher Arndt'
author_email = 'chris@chrisarndt.de'
url = 'http://chrisarndt.de/projects/python-kurzfile/'
download_url = url + 'download/'
license = 'MIT License'
platforms = 'POSIX, Windows, MacOS X'
classifiers = 'Development Status :: 3 - Alpha\n#Environment :: MacOS X\n#Environment :: Win32 (MS Windows)\nEnvironment :: Console\nIntended Audience :: Developers\nIntended Audience :: End Users/Desktop\nLicense :: OSI Approved :: BSD License\nOperating System :: Microsoft :: Windows\nOperating System :: POSIX\nOperating System :: MacOS :: MacOS X\nProgramming Language :: Python\nTopic :: Multimedia :: Sound/Audio\nTopic :: Utilities\n'
classifiers = [ c.strip() for c in classifiers.splitlines() if c.strip() if not c.startswith('#')
              ]
del c