# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/math.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 700 bytes
"""
    pygments.lexers.math
    ~~~~~~~~~~~~~~~~~~~~

    Just export lexers that were contained in this module.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexers.python import NumPyLexer
from pygments.lexers.matlab import MatlabLexer, MatlabSessionLexer, OctaveLexer, ScilabLexer
from pygments.lexers.julia import JuliaLexer, JuliaConsoleLexer
from pygments.lexers.r import RConsoleLexer, SLexer, RdLexer
from pygments.lexers.modeling import BugsLexer, JagsLexer, StanLexer
from pygments.lexers.idl import IDLLexer
from pygments.lexers.algebra import MuPADLexer
__all__ = []