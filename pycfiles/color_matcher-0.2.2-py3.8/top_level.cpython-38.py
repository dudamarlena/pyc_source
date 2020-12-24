# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_matcher/top_level.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 2515 bytes
__author__ = 'Christopher Hahne'
__email__ = 'info@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from color_matcher.hist_matcher import HistogramMatcher
from color_matcher.mvgd_matcher import TransferMVGD
from color_matcher.reinhard_matcher import ReinhardMatcher
import numpy as np
METHODS = ('default', 'mvgd', 'hm', 'hm-mkl-hm', 'reinhard')

class ColorMatcher(HistogramMatcher, TransferMVGD, ReinhardMatcher):

    def __init__(self, *args, **kwargs):
        (super(ColorMatcher, self).__init__)(*args, **kwargs)
        self._method = kwargs['method'] if 'method' in kwargs else 'default'

    def main(self, method: str=None) -> np.ndarray:
        """
        The main function and high-level entry point performing the mapping. Valid methods are

        :param method: ('default', 'mvgd', 'hm', 'hm-mkl-hm', 'reinhard') describing how to conduct color mapping
        :type method: :class:`str`

        :return: Resulting image after color mapping
        :rtype: np.ndarray
        """
        self._method = self._method if method is None else method
        if self._method == METHODS[0]:
            funs = [
             self.transfer]
        else:
            if self._method == METHODS[1]:
                funs = [
                 self.transfer]
            else:
                if self._method == METHODS[2]:
                    funs = [
                     self.hist_match]
                else:
                    if self._method == METHODS[3]:
                        funs = [
                         self.hist_match, self.transfer, self.hist_match]
                    else:
                        if self._method == METHODS[4]:
                            funs = [
                             self.reinhard]
                        else:
                            raise BaseException("Method type '%s' not recognized" % method)
        for fun in funs:
            self._src = fun(self._src, self._ref)
        else:
            return self._src