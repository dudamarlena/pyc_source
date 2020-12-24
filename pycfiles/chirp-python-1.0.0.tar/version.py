# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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