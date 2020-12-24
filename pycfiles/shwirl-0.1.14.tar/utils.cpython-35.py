# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/ext/_bundled/cassowary/utils.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 772 bytes
from __future__ import print_function, unicode_literals, absolute_import, division
EPSILON = 1e-08
REQUIRED = 1001001000
STRONG = 1000000
MEDIUM = 1000
WEAK = 1

def approx_equal(a, b, epsilon=EPSILON):
    """A comparison mechanism for floats"""
    return abs(a - b) < epsilon


def repr_strength(strength):
    """Convert a numerical strength constant into a human-readable value.

    We could wrap this up in an enum, but enums aren't available in Py2;
    we could use a utility class, but we really don't need the extra
    implementation weight. In practice, this repr is only used for debug
    purposes during development.
    """
    return {REQUIRED: 'Required', 
     STRONG: 'Strong', 
     MEDIUM: 'Medium', 
     WEAK: 'Weak'}[strength]