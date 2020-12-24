# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codes/DocumentFeatureSelection/pmi/PMI.py
# Compiled at: 2017-02-23 10:26:28
# Size of source mod 2**32: 362 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import sys
python_version = sys.version_info
if python_version > (3, 0, 0):
    from DocumentFeatureSelection.pmi.PMI_python3 import PMI
else:
    raise SystemError('Not Implemented yet')