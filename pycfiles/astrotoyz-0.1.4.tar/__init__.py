# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/astro-toyz/astrotoyz/__init__.py
# Compiled at: 2015-09-05 20:16:20
"""
This is an Astropy affiliated package.
"""
from ._astropy_init import *
if not _ASTROPY_SETUP_:
    from example_mod import *
    from astrotoyz import tasks
    from astrotoyz import viewer
    from astrotoyz import detect_sources
    from astrotoyz import io
    from astrotoyz import data_types
    from astrotoyz import config