# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/rawkit/__init__.py
# Compiled at: 2017-07-09 08:50:23
# Size of source mod 2**32: 702 bytes
"""Introduction
~~~~~~~~~~~~~~~

The :mod:`rawkit` module contains high-level APIs for manipulating raw photos
using the low-level :mod:`libraw` module (which in turn uses the even
lower-level LibRaw C library).

Eg. quickly processing a raw Canon CR2 file without using the camera white
balance and saving it as a PPM image might look like this:

.. sourcecode:: python

    from rawkit.raw import Raw
    from rawkit.options import WhiteBalance

    with Raw(filename='some/raw/image.CR2') as raw:
      raw.options.white_balance = WhiteBalance(camera=False, auto=True)
      raw.save(filename='some/destination/image.ppm')
"""
VERSION = '0.6.0'