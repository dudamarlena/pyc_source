# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/release.py
# Compiled at: 2006-12-15 14:28:17
"""CBlog is a simple weblog application based on the TurboGears_ framework.

Apart from being used by myself as the software that drives my personal blog,
it is also a useful showcase for various TG programming patterns.

The software is currently in alpha state, because the data model and the API
(internal and external, i.e. URls) may still change frequently and some
features I consider important are still missing. That being said, I already use
it on a regular basis for my own blog site.

.. _TurboGears: http://turbogears.org
"""
import sys
_doclines = __doc__.split('\n')
_py_major_version = '%i.%i' % sys.version_info[:2]
name = 'CBlog'
version = '0.1a'
description = _doclines[0]
long_description = ('\n').join(_doclines[2:])
author = 'Christopher Arndt'
email = 'chris@chrisarndt.de'
copyright = '© 2006 Christopher Arndt'
url = 'http://chrisarndt.de/projects/cblog/'
download_url = 'http://chrisarndt.de/projects/cblog/download/%s-%s-py%s.egg' % (name, version, _py_major_version)
license = 'MIT license'
platform = 'Any'
_classifiers = 'Development Status :: 3 - Alpha\nEnvironment :: Web Environment\nFramework :: TurboGears\nFramework :: TurboGears :: Applications\nIntended Audience :: Developers\nIntended Audience :: Education\nIntended Audience :: End Users/Desktop\nLicense :: OSI Approved :: MIT License\nOperating System :: OS Independent\nProgramming Language :: Python\nTopic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary\n'
classifiers = [ c for c in _classifiers.split('\n') if c ]
_keywords = 'turbogears.widgets\nturbogears.app\n'
keywords = [ k for k in _keywords.split('\n') if k ]