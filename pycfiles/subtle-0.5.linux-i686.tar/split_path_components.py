# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/split_path_components.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import fileutils
import os.path, logging
log = logging.getLogger(__name__)

def process(mtree):
    """Returns the filename split into [ dir*, basename, ext ]."""
    components = fileutils.split_path(mtree.value)
    basename = components.pop(-1)
    components += list(os.path.splitext(basename))
    components[-1] = components[(-1)][1:]
    mtree.split_on_components(components)