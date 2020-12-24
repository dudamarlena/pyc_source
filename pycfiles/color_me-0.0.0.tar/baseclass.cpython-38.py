# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/color_matcher/baseclass.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 2175 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\nCopyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np

class MatcherBaseclass(object):

    def __init__(self, *args, **kwargs):
        self._src = None
        self._ref = None
        if len(args) == 2:
            self._src = args[0]
            self._ref = args[1]
        if bool(kwargs):
            self._src = kwargs['src'] if 'src' in kwargs else self._src
            self._ref = kwargs['ref'] if 'ref' in kwargs else self._ref
        self.validate_img_dims()

    def validate_img_dims(self):
        """
        This function validates the image dimensions. It throws an exception if the dimension are unequal to 2 or 3.
        """
        self._src = self._src[(..., np.newaxis)] if len(self._src.shape) == 2 else self._src
        self._ref = self._ref[(..., np.newaxis)] if len(self._ref.shape) == 2 else self._ref
        if len(self._src.shape) != 3 or len(self._ref.shape) != 3:
            raise BaseException('Wrong image dimensions')
        return True

    def validate_color_chs(self):
        """
        This function checks whether provided images consist of 3 color channels. An exception is thrown otherwise.
        """
        if self._src.shape[2] != 3 or self._ref.shape[2] != 3:
            raise BaseException('Each image must have 3 color channels')
        return True