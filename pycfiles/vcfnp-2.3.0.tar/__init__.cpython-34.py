# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aliman/src/github/alimanfoo/vcfnp/vcfnp/__init__.py
# Compiled at: 2016-07-20 04:37:16
# Size of source mod 2**32: 348 bytes
from __future__ import absolute_import, print_function, division
import vcfnp.config as config, vcfnp.eff as eff
from vcfnp.vcflib import PyVariantCallFile as VariantCallFile
from vcfnp.array import variants, calldata, calldata_2d, view2d
from vcfnp.table import VariantsTable
__version__ = '2.3.0'