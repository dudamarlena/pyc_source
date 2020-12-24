# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\mtrzcinski\Desktop\siggy\siglent_parser\siglent_parser\__init__.py
# Compiled at: 2019-08-02 09:15:28
# Size of source mod 2**32: 816 bytes
"""__init__.py

Copyright 2019 Matt Trzcinski

This file is part of siglent_parser.

siglent_parser is free software: you can redistribute it and/or
modify- it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

siglent_parser is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with siglent_parser.  If not, see
<https://www.gnu.org/licenses/>.

"""
from .__meta__ import version as __version__
from .parser import SiglentParser