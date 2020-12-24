# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cubicweb_postgis/__pkginfo__.py
# Compiled at: 2019-02-21 07:22:08
__doc__ = 'cubicweb-postgis application packaging information'
modname = 'postgis'
distname = 'cubicweb-postgis'
numversion = (0, 6, 0)
version = ('.').join(str(num) for num in numversion)
license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Test for postgis'
web = 'http://www.cubicweb.org/project/%s' % distname
__depends__ = {'cubicweb': '>= 3.24.0'}
__recommends__ = {}
classifiers = [
 'Environment :: Web Environment',
 'Framework :: CubicWeb',
 'Programming Language :: Python',
 'Programming Language :: Python :: 3',
 'Programming Language :: JavaScript',
 'Topic :: Scientific/Engineering :: GIS',
 'Topic :: Database']