# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/__init__.py
# Compiled at: 2019-11-20 10:27:00
# Size of source mod 2**32: 384 bytes
""" __init__.py
~~~~~~~~~~~~~~~~~~~~
Initialises when multiqc module is loaded.

Makes the following available under the main multiqc namespace:
- run()
- config
- config.logger
- __version__
"""
import logging
from .utils import config
from .multiqc import run
config.logger = logging.getLogger(__name__)
__version__ = config.version