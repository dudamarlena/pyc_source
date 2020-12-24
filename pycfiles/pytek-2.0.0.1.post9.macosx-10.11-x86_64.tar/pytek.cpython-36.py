# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/pytek/pytek.py
# Compiled at: 2017-11-16 14:11:13
# Size of source mod 2**32: 1379 bytes
"""
.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.

.. py:class:: TDS3k

This is simply a synonym for `pytek.TDS3k` to support the incorrect placement
of this class in verion 1.0.0.0-r1.

.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.

.. py:class:: TDS3xxx

This is simply a synonym for `pytek.TDS3xxx` to support the incorrect placement
of this class in verion 1.0.0.0-r1.

.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.

"""
from . import TDS3k as top_TDS3k
from . import TDS3xxx as top_TDS3xxx
TDS3k = top_TDS3k
TDS3xxx = top_TDS3xxx