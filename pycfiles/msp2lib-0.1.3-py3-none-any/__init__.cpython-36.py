# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/domdfcoding/msp2lib/msp2lib/__init__.py
# Compiled at: 2020-04-26 17:39:03
# Size of source mod 2**32: 1363 bytes
"""
Convert an MSP file representing one or more Mass Spectra to a NIST MS Search user library.

Docker must be installed to use this program.
"""
__author__ = 'Dominic Davis-Foster'
__copyright__ = '2020 Dominic Davis-Foster'
__license__ = 'LGPLv3'
__version__ = '0.1.3'
__email__ = 'dominic@davis-foster.co.uk'
from .core import msp2lib, test_docker, main
from .utils import test_docker, version, about, download_docker_image, build_docker_image, subprocess_with_log