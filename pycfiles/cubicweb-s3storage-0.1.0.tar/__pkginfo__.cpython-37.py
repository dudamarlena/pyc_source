# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nspanti/workspace/rqlcontroller/cubicweb_rqlcontroller/__pkginfo__.py
# Compiled at: 2020-03-20 10:41:14
# Size of source mod 2**32: 704 bytes
__doc__ = 'cubicweb-rqlcontroller application packaging information'
modname = 'rqlcontroller'
distname = 'cubicweb-rqlcontroller'
numversion = (0, 5, 0)
version = '.'.join((str(num) for num in numversion))
license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'restfull rql edition capabilities'
web = 'http://www.cubicweb.org/project/%s' % distname
__depends__ = {'cubicweb':'>= 3.27.3', 
 'six':None}
__recommends__ = {'cubicweb-signedrequest': None}
classifiers = [
 'Environment :: Web Environment',
 'Framework :: CubicWeb',
 'Programming Language :: Python',
 'Programming Language :: JavaScript']