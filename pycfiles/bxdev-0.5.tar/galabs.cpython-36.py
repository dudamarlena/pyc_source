# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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