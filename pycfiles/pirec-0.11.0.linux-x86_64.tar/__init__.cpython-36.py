# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/__init__.py
# Compiled at: 2017-02-10 11:03:56
# Size of source mod 2**32: 268 bytes
"""pirec is a module for recording the activity of file processing pipelines.

.. moduleauthor:: Jon Stutters <j.stutters@ucl.ac.uk>
"""
from .processresult import pipeline, record, call
from .__version__ import __version__
__all__ = ('pipeline', 'record', 'call')