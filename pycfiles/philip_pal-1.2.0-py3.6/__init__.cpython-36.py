# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/philip_pal/__init__.py
# Compiled at: 2020-02-25 08:49:57
# Size of source mod 2**32: 405 bytes
"""packet init for PHiLIP PAL
This exposes useful modules in the PHiLIP PAL packet
"""
from .philip_if import PhilipExtIf as Phil
__all__ = [
 'Phil']