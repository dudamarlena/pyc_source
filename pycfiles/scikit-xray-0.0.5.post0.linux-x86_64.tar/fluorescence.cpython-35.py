# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/fluorescence.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 3129 bytes
"""
This module creates a namespace for X-Ray Fluorescence
"""
import logging
logger = logging.getLogger(__name__)
from skxray.core.fitting import Lorentzian2Model, ComptonModel, ElasticModel
from skxray.core.constants import XrfElement, emission_line_search
from skxray.core.fitting.background import snip_method
__all__ = [
 'Lorentzian2Model', 'ComptonModel', 'ElasticModel',
 'XrfElement', 'emission_line_search',
 'snip_method']