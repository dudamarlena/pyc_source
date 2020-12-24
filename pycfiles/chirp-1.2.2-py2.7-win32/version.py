# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\version.py
# Compiled at: 2013-12-11 23:17:46
version = '1.2.1'

def lib_versions():
    import sys
    from libtfr import __version__ as tfrver
    from shapely.geos import geos_capi_version
    from numpy import __version__ as npyver
    return dict(chirp=version, python=sys.version.split()[0], numpy=npyver, libtfr=tfrver, geos='%d.%d.%d' % geos_capi_version)


__doc__ = 'This is chirp, a program for bioacoustic analysis.\n\nVersion information:\nchirp:        %(chirp)s\npython:       %(python)s\nnumpy:        %(numpy)s\nlibtfr:       %(libtfr)s\ngeos/shapely: %(geos)s\n\nCopyright (C) 2011-2012 Dan Meliza <dan // meliza.org>\nProject site: https://github.com/dmeliza/chirp\n' % lib_versions()