# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/composers/common_defs.py
# Compiled at: 2018-10-05 17:13:25
# Size of source mod 2**32: 943 bytes
"""
Copyright (2018) Raydel Miranda

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or 1wmodify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""
from collections import namedtuple
WorkerParams = namedtuple('WorkerParams', ['background', 'flower', 'bundles'])