# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridjug/__init__.py
# Compiled at: 2015-08-24 13:16:46
# Size of source mod 2**32: 689 bytes
"""
Notes
-----

For some reason, pickle does not work on some cluster environments if the
submodule has the same name as the package.
Hence, we call the submodule ``grid_jug`` instead of ``gridjug``.

See Also
--------

`GridMap <https://github.com/pygridtools/gridmap>`_
    Easily map Python functions onto a cluster using a DRMAA-compatible grid
    engine like Sun Grid Engine (SGE).

`Jug <http://luispedro.org/software/jug/>`_
    A Task-Based Parallelization Framework

"""
from __future__ import absolute_import, division, print_function
import pkg_resources
from gridjug.grid_jug import grid_jug
__version__ = pkg_resources.get_distribution(__name__).version