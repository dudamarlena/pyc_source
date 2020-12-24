# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/color_matcher/normalizer.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 3047 bytes
__author__ = 'Christopher Hahne'
__email__ = 'info@christopherhahne.de'
__license__ = '\n    Copyright (c) 2019 Christopher Hahne <info@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
import numpy as np

class Normalizer(object):

    def __init__(self, data=None, min=None, max=None):
        self._data, self._min, self._max = (None, None, None)
        self._var_init(data, min, max)

    def _var_init--- This code section failed: ---

 L.  35         0  LOAD_FAST                'data'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _data
               12  JUMP_FORWARD         26  'to 26'
             14_0  COME_FROM             6  '6'
               14  LOAD_GLOBAL              np
               16  LOAD_ATTR                asarray
               18  LOAD_FAST                'data'
               20  LOAD_STR                 'float64'
               22  LOAD_CONST               ('dtype',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             26_0  COME_FROM            12  '12'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _data

 L.  36        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _data
               36  LOAD_GLOBAL              np
               38  LOAD_ATTR                ndarray
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  LOAD_GLOBAL              str
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _data
               50  LOAD_ATTR                dtype
               52  CALL_FUNCTION_1       1  ''
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            42  '42'
               56  LOAD_STR                 'float64'
             58_0  COME_FROM            54  '54'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _dtype

 L.  38        62  LOAD_FAST                'min'
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  POP_JUMP_IF_FALSE    76  'to 76'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _min
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            68  '68'
               76  LOAD_FAST                'min'
             78_0  COME_FROM            74  '74'
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _min

 L.  39        82  LOAD_FAST                'max'
               84  LOAD_CONST               None
               86  COMPARE_OP               is
               88  POP_JUMP_IF_FALSE    96  'to 96'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _max
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            88  '88'
               96  LOAD_FAST                'max'
             98_0  COME_FROM            94  '94'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _max

 L.  40       102  LOAD_GLOBAL              any
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _min
              108  LOAD_FAST                'min'
              110  BUILD_LIST_2          2 
              112  CALL_FUNCTION_1       1  ''
              114  POP_JUMP_IF_TRUE    140  'to 140'
              116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _data
              122  LOAD_GLOBAL              np
              124  LOAD_ATTR                ndarray
              126  CALL_FUNCTION_2       2  ''
              128  POP_JUMP_IF_FALSE   140  'to 140'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                _data
              134  LOAD_METHOD              min
              136  CALL_METHOD_0         0  ''
              138  JUMP_FORWARD        144  'to 144'
            140_0  COME_FROM           128  '128'
            140_1  COME_FROM           114  '114'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                _min
            144_0  COME_FROM           138  '138'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               _min

 L.  41       148  LOAD_GLOBAL              any
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _max
              154  LOAD_FAST                'max'
              156  BUILD_LIST_2          2 
              158  CALL_FUNCTION_1       1  ''
              160  POP_JUMP_IF_TRUE    186  'to 186'
              162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                _data
              168  LOAD_GLOBAL              np
              170  LOAD_ATTR                ndarray
              172  CALL_FUNCTION_2       2  ''
              174  POP_JUMP_IF_FALSE   186  'to 186'
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                _data
              180  LOAD_METHOD              max
              182  CALL_METHOD_0         0  ''
              184  JUMP_FORWARD        190  'to 190'
            186_0  COME_FROM           174  '174'
            186_1  COME_FROM           160  '160'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _max
            190_0  COME_FROM           184  '184'
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _max

Parse error at or near `COME_FROM' instruction at offset 144_0

    def uint16_norm(self):
        """ normalize image array to 16-bit unsigned integer """
        return np.asarray((np.round(self.norm_fun * 65535)), dtype=(np.uint16))

    def uint8_norm(self):
        """ normalize image array to 8-bit unsigned integer """
        return np.asarray((np.round(self.norm_fun * 255)), dtype=(np.uint8))

    def type_norm(self, data=None, min=None, max=None, new_min=None, new_max=None):
        """ normalize numpy image array for provided data type """
        self._var_init(data, min, max)
        if self._dtype.startswith(('int', 'uint')):
            new_max = np.iinfo(np.dtype(self._dtype)).max if new_max is None else new_max
            new_min = np.iinfo(np.dtype(self._dtype)).min if new_min is None else new_min
            img_norm = np.round(self.norm_fun * (new_max - new_min) + new_min)
        else:
            new_max = 1.0 if new_max is None else new_max
            new_min = 0.0 if new_min is None else new_min
            img_norm = self.norm_fun * (new_max - new_min) + new_min
        return np.asarray(img_norm, dtype=(self._dtype))

    def norm_fun(self):
        """ normalize image to values between 1 and 0 """
        norm = (self._data - self._min) / (self._max - self._min) if self._max != (self._min and 0) else self._data
        norm[norm < 0] = 0
        norm[norm > 1] = 1
        return norm