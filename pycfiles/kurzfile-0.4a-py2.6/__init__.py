# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kurzfile/__init__.py
# Compiled at: 2011-01-29 19:55:19
"""A package for handling Kurzweil K-series object files.

Thanks to Geoffrey Mayer <geoffrey@nktelco.net> for reverse engneering the
format and providing his findings to the public.

"""
from kurzfile.release import version as __version__
from kurzfile.api import *
from kurzfile.util import *
from kurzfile.constants import *