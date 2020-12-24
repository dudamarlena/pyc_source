# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/share/containershare-python/containershare/defaults.py
# Compiled at: 2018-07-30 07:43:57
# Size of source mod 2**32: 2803 bytes
"""

defaults.py: this script acts as a gateway between variables defined at
runtime, and defaults. Any variable that has an unchanging default value 
can be found here. The order of operations works as follows:
  
    1. First preference goes to environment variable set at runtime
    2. Second preference goes to default defined in this file
    3. Then, if neither is found, null is returned except in the 
       case that required = True. A required = True variable not found
       will system exit with an error.

Copyright (c) 2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
from containershare.utils import convert2boolean, getenv
import tempfile, os, pwd, sys
CONTAINERSHARE_REGISTRY = getenv('CONTAINERSHARE_REGISTRY_BASE', default='https://vsoch.github.io')
CONTAINERSHARE_LIBRARY = '%s/containershare/library.json' % CONTAINERSHARE_REGISTRY
COLORIZE = getenv('CONTAINERSHARE_COLORIZE', default=None)
if COLORIZE is not None:
    COLORIZE = convert2boolean(COLORIZE)