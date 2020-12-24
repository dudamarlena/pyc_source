# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/_mymako.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import absolute_import
try:
    import mako.template
except ImportError:
    raise ImportError("Some of PyCUDA's facilities require the Mako templating engine.\nYou or a piece of software you have used has tried to call such a\npart of PyCUDA, but there was a problem importing Mako.\n\nYou may install mako now by typing one of:\n- easy_install Mako\n- pip install Mako\n- aptitude install python-mako\n\nor whatever else is appropriate for your system.")

from mako import *