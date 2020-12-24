# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bxa/sherpa/galabs.py
# Compiled at: 2020-01-28 12:31:59
# Size of source mod 2**32: 983 bytes
from __future__ import print_function
import os
from math import log10, isnan, isinf
if 'MAKESPHINXDOC' not in os.environ:
    import sherpa.astro.ui as ui
    from sherpa.stats import Cash, CStat
from .cachedmodel import CachedModel

def auto_galactic_absorption(id=None):
    filename = ui._session.get_data(id).name + '.nh'
    print('loading nH from %s (expecting something like 1e21 in there)' % filename)
    nH = float(open(filename).read().strip())
    galabso = ui.xstbabs('galabso%s' % id)
    galabso.nH = nH / 1e+22
    print('setting galactic nH to %s [units of 1e22/cm²]' % galabso.nH.val)
    galabso.nH.freeze()
    return galabso