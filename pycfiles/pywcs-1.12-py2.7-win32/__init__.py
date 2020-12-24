# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywcs\__init__.py
# Compiled at: 2014-03-13 12:23:51
"""
.. _wcslib: http://www.atnf.csiro.au/~mcalabre/WCS/
.. _pyfits: http://www.stsci.edu/resources/software_hardware/pyfits
.. _Paper IV: http://www.atnf.csiro.au/people/mcalabre/WCS/index.html
.. _SIP: http://ssc.spitzer.caltech.edu/postbcd/doc/shupeADASS.pdf
.. _ds9: http://hea-www.harvard.edu/RD/ds9/

Pywcs provides transformations following the `SIP`_ conventions,
`Paper IV`_ table lookup distortion, and the core WCS functionality
provided by `wcslib`_.  Each of these transformations can be used
independently or together in a standard pipeline.

The basic workflow is as follows:

    1. ``import pywcs``

    2. Call the `pywcs.WCS` constructor with a `pyfits`_ header
       and/or hdulist object.

    3. Optionally, if the FITS file uses any deprecated or
       non-standard features, you may need to call one of the
       `~pywcs.WCS.fix` methods on the object.

    4. Use one of the following transformation methods:

       - `~WCS.all_pix2sky`: Perform all three transformations from
         pixel to sky coordinates.

       - `~WCS.wcs_pix2sky`: Perform just the core WCS transformation
         from pixel to sky coordinates.

       - `~WCS.wcs_sky2pix`: Perform just the core WCS transformation
         from sky to pixel coordinates.

       - `~WCS.sip_pix2foc`: Convert from pixel to focal plane
         coordinates using the `SIP`_ polynomial coefficients.

       - `~WCS.sip_foc2pix`: Convert from focal plane to pixel
         coordinates using the `SIP`_ polynomial coefficients.

       - `~WCS.p4_pix2foc`: Convert from pixel to focal plane
         coordinates using the table lookup distortion method
         described in `Paper IV`_.

       - `~WCS.det2im`: Convert from detector coordinates to image
         coordinates.  Commonly used for narrow column correction.
"""
from __future__ import division
import sys
if sys.version_info[0] >= 3:
    exec 'from .pywcs import *'
else:
    from .core import *

def test(verbose=False):
    import os, sys, nose
    from . import tests
    dir = os.path.dirname(tests.__file__)
    argv = [
     'nosetests', '--exe', dir]
    try:
        return nose.main(argv=argv)
    except SystemExit as e:
        return e.code


from .version import *