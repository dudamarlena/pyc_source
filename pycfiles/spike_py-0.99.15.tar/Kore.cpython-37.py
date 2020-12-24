# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/Kore.py
# Compiled at: 2020-01-11 13:05:37
# Size of source mod 2**32: 56160 bytes
"""
Kore.py

Created by Marie-Aude Coutouly on 2010-03-26.

"""
from __future__ import print_function
import numpy as np
from .. import NPKData as npkd
from ..File import GifaFile as gf
import array, sys, inspect

class Kore(object):

    def __init__(self, debug=0):
        self.debug = debug
        self._column = npkd.NPKData(dim=1)
        self._plane2d = npkd.NPKData(dim=2)
        self._image = npkd.NPKData(dim=3)
        self._datab = npkd.NPKData(dim=1)
        self._window = npkd.NPKData(dim=1)
        self._filter = npkd.NPKData(dim=1)
        self._tab = npkd.NPKData(dim=1)
        self._last_row = 0
        self._last_plane = 0
        self._last_col = 0
        self._last_ph0 = 0
        self._last_ph1 = 0
        self._shift = 0.0
        self._noise = 0.0
        self.peaks = []
        self.dim(1)

    def _getcurrent(self):
        """
        getter for _current
        """
        if self._dim == 1:
            return self._column
        if self._dim == 2:
            return self._plane2d
        if self._dim == 3:
            return self._image

    def _setcurrent(self, npkdata):
        """
        setter for _current
        """
        if self._dim == 1:
            npkdata.check1D()
            self._column = npkdata
        else:
            if self._dim == 2:
                npkdata.check2D()
                self._plane2d = npkdata
            else:
                if self._dim == 3:
                    npkdata.check3D()
                    self._image = npkdata
                else:
                    raise Exception('Kore internal problem')

    _doc_current = 'doc'
    _current = property(_getcurrent, _setcurrent, None, _doc_current)

    def report(self):
        """print a summary of the internal state of the kernel"""
        report = '\n        buffer 1D : %s\n        buffer 2D : %s\n        buffer 3D : %s\n        current   : %s\n        ' % (self._column.report(), self._plane2d.report(), self._image.report(), self._current.report())
        print(report)

    def status(self):
        """
        print a summary of the internal state of the kernel
        """
        d = self.get_dim()
        if d == 1:
            d1 = '- current working buffer'
        else:
            d1 = ''
        if d == 2:
            d2 = '- current working buffer'
        else:
            d2 = ''
        if d == 3:
            d3 = '- current working buffer'
        else:
            d3 = ''
        self.dim(1)
        self.com_max()
        report = '\n    DIM 1 %s\n    =====\n       buffer size : %i - itype %i\n       values from : %f to %f\n       Spectral width : %f\n       %i peak(s) in database\n\n    ' % (d1, self.get_si1_1d(), self.get_itype_1d(), self.geta_max(2), self.geta_max(1), self.get_specw_1d(), self.get_npk1d())
        self.dim(2)
        self.com_max()
        report = report + '\n    DIM 2 %s\n    =====\n        buffer sizes : %i x %i - itype %i\n         values from : %f to %f\n    Spectral widthes : %f x %f\n    %i peak(s) in database\n\n    ' % (d2, self.get_si1_2d(), self.get_si2_2d(), self.get_itype_2d(), self.geta_max(2), self.geta_max(1), self.get_specw_1_2d(), self.get_specw_2_2d(), self.get_npk2d())
        self.dim(3)
        self.com_max()
        report = report + '\n    DIM 3 %s\n    =====\n        buffer sizes : %i x %i x %i - itype %i\n         values from : %f to %f\n    Spectral widthes : %f x %f x %f\n    %i peak(s) in database\n\n    ' % (d3, self.get_si1_3d(), self.get_si2_3d(), self.get_si3_3d(), self.get_itype_3d(), self.geta_max(2), self.geta_max(1), self.get_specw_1_3d(), self.get_specw_2_3d(), self.get_specw_3_3d(), self.get_npk3d())
        self.dim(d)
        return report

    def dim(self, d):
        """
        Declaration of the ._current buffer
        """
        if d not in (1, 2, 3):
            raise Exception('dim can only take the value : 1 2 3')
        self._dim = d

    def checknD(self, n):
        if self._dim != n:
            raise Exception('The buffer set is not a %1dD experiment, as required' % n)

    def check1D(self):
        """true for a 1D"""
        self.checknD(1)

    def check2D(self):
        """true for a 2D"""
        self.checknD(2)

    def check3D(self):
        """true for a 3D"""
        self.checknD(3)

    def power2(self, i):
        """
        Compute the power of 2 that is under or equal to i 
        """
        import math as m
        return int(m.pow(2, m.floor(m.log(i) / m.log(2))))

    def _test_axis(self, axis):
        """
        takes axis as
            F1 f1 F2 f2 F12 or f12 in 2D
        or  F1 f1 F2 f2 F3 f3 F12 f12 F13 f13 F23 f23 F123 or f123 in 3D
        and return a list of axis to process :
        1 / 2 / 3
        used by axis relative commands
        """
        ret = []
        if axis in ('F3', 'F13', 'F23', 'F123', 'f3', 'f13', 'f23', 'f123', 3):
            ret.append(3)
        if axis in ('F2', 'F12', 'F23', 'F123', 'f2', 'f12', 'f23', 'f123', 2):
            ret.append(2)
        if axis in ('F1', 'F12', 'F13', 'F123', 'f1', 'f12', 'f13', 'f123', 1):
            ret.append(1)
        if ret == []:
            raise Exception('Error with axis')
        return ret

    def addbase(self, constant):
        """
        Removes a constant to the data. The default value is the value of 
        SHIFT (computed by EVALN).
        
        see also : bcorr evaln shift
        """
        self._current.addbase(constant)

    def addnoise(self, noise, seed=0):
        """
        add to the current data-set (1D, 2D, 3D) a white-gaussian, 
        characterized by its level noise, and the random generator seed.
        """
        self._current.addnoise(noise, seed)

    def adddata(self, debug=False):
        """
        Add the contents of the DATA buffer to the current data-set. 
        Equivalent to ADD but in-memory.
        """
        if self._datab.buffer.shape == self._current.buffer.shape:
            self._current.buffer += self._datab.buffer
        else:
            raise Exception('diff sizes ', self._datab.buffer.shape, self._current.buffer.shape)

    def mult1d(self, axis=0):
        """
        multiply the current 2D or 3D with the contents of the 1d buffer considered as a f1(i)f2(j) concatenated buffer
        
        
        see also : multdata add adddata filter
        """
        for ax in self._test_axis(axis):
            if ax == 2:
                c = npkd.NPKData(buffer=(self._column.buffer))
                c.chsize(self.get_si1_2d() + self.get_si2_2d())
                c.buffer[self.get_si2_2d():self.get_si1_2d() + self.get_si2_2d()] = 1.0
                for j in range(self.get_si1_2d()):
                    a = c.buffer[(self.get_si2_2d() + j)]
                    for i in range(self.get_si2_2d()):
                        self._current.buffer[(j, i)] = self._current.buffer[(j, i)] * c.buffer[i] * a

    def mult(self, constant):
        self._current = self._current.mult(constant)

    def multdata(self):
        """
        Multiplies point by point, the content of the current working buffer 
        with the content of the DATA buffer. Permits to realize convolution 
        product. Works in 1D, 2D, in real, complex and hypercomplex modes.

        see also : ADDDATA MINDATA MAXDATA EXCHDATA MULT PUT
        """
        if self._current.dim != self._datab.dim:
            raise Exception('wrong buffer dim: %s' % str(self._current.dim()))
        elif self._current.dim == 1:
            if self.get_si1_1d() != self._datab.size1:
                raise Exception('wrong buffer size: %s %s' % (str(self.get_si1_1d()), str(self._datab.size1)))
        elif not self._current.dim == 2 or self.get_si1_2d() != self._datab.size1 or self.get_si2_2d() != self._datab.size2:
            raise Exception('wrong buffer size 2D : %s' % str(self.get_si1_2d()))
        else:
            if self._current.dim == 3:
                if self.get_si1_3d() != self._datab.size1 or self.get_si2_3d() != self._datab.size2 or self.get_si3_3d() != self._datab.size3:
                    raise Exception('wrong buffer size 3D : %s' % str(self.get_si1_3d()))
        self._current.buffer *= self._datab.buffer
        return self

    def maxdata(self):
        """
        Compare the content of the current buffer with the content of the 
        DATA buffer, and leave in memory the largest of the 2 values. 
        Usefull for projections or symetrisation macros.

        see also : mindata exchdata adddata multdata sym put
        """
        if self._current.dim != self._datab.dim:
            raise Exception('wrong buffer dim: %i %i' % (self._current.dim, self._datab.dim))
        elif self._current.dim == 1:
            if self.get_si1_1d() != self._datab.size1:
                raise Exception('wrong buffer size: %s %s' % (str(self.get_si1_1d()), str(self._datab.size1)))
        elif not self._current.dim == 2 or self.get_si1_2d() != self._datab.size1 or self.get_si2_2d() != self._datab.size2:
            raise Exception('wrong buffer size 2D : %s' % str(self.get_si1_2d()))
        else:
            if self._current.dim == 3:
                if self.get_si1_3d() != self._datab.size1 or self.get_si2_3d() != self._datab.size2 or self.get_si3_3d() != self._datab.size3:
                    raise Exception('wrong buffer size 3D : %s' % str(self.get_si1_3d()))
        self._current.buffer = np.maximum(self._current.buffer, self._datab.buffer)
        return self

    def mindata(self):
        """
        Compare the content of the current buffer with the content of the 
        DATA buffer, and leave in memory the smallest of the 2 values. 
        Usefull for projections or symetrisation macros.

        see also : maxdata exchdata adddata multdata sym put
        """
        if self._current.dim != self._datab.dim:
            raise Exception('wrong buffer dim: %i %i' % (self._current.dim, self._datab.dim))
        elif self._current.dim == 1:
            if self.get_si1_1d() != self._datab.size1:
                raise Exception('wrong buffer size: %s %s' % (str(self.get_si1_1d()), str(self._datab.size1)))
        elif not self._current.dim == 2 or self.get_si1_2d() != self._datab.size1 or self.get_si2_2d() != self._datab.size2:
            raise Exception('wrong buffer size 2D : %s' % str(self.get_si1_2d()))
        else:
            if self._current.dim == 3:
                if self.get_si1_3d() != self._datab.size1 or self.get_si2_3d() != self._datab.size2 or self.get_si3_3d() != self._datab.size3:
                    raise Exception('wrong buffer size 3D : %s' % str(self.get_si1_3d()))
        self._current.buffer = np.minimum(self._current.buffer, self._datab.buffer)
        return self

    def modulus(self):
        self._current = self._current.modulus()

    def itype(self, value):
        if self._dim == 1:
            if value not in (0, 1):
                raise Exception('wrong value for itype')
            self._column.axis1.itype = value
        else:
            if self._dim == 2:
                if value not in (0, 1, 2, 3):
                    raise Exception('wrong value for itype')
                self._plane2d.axis1.itype = value / 2
                self._plane2d.axis2.itype = value % 2
            else:
                if self._dim == 3:
                    if value not in (0, 1, 2, 3, 4, 5, 6, 7):
                        raise Exception('wrong value for itype')
                    self._image.axis1.itype = value / 4
                    self._image.axis2.itype = value / 2 % 2
                    self._image.axis3.itype = value % 2

    def col(self, i):
        self.check2D()
        self._column = self._plane2d.col(i - 1)
        self._last_col = i

    def diag(self, direc='F12'):
        if self._dim == 2:
            self._column = self._plane2d.diag()
        else:
            if self._dim == 3:
                self._plane2d = self._image.diag(direc)

    def one--- This code section failed: ---

 L. 353         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _dim
                4  LOAD_CONST               1
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 354        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _current
               14  LOAD_ATTR                axis1
               16  LOAD_ATTR                itype
               18  LOAD_CONST               0
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    44  'to 44'

 L. 355        24  LOAD_GLOBAL              np
               26  LOAD_METHOD              ones_like
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _current
               32  LOAD_ATTR                buffer
               34  CALL_METHOD_1         1  '1 positional argument'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _current
               40  STORE_ATTR               buffer
               42  JUMP_FORWARD        624  'to 624'
             44_0  COME_FROM            22  '22'

 L. 357        44  LOAD_CONST               1.0
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _current
               50  LOAD_ATTR                buffer
               52  LOAD_CONST               None
               54  LOAD_CONST               None
               56  LOAD_CONST               2
               58  BUILD_SLICE_3         3 
               60  STORE_SUBSCR     

 L. 358        62  LOAD_CONST               0.0
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _current
               68  LOAD_ATTR                buffer
               70  LOAD_CONST               1
               72  LOAD_CONST               None
               74  LOAD_CONST               2
               76  BUILD_SLICE_3         3 
               78  STORE_SUBSCR     
            80_82  JUMP_FORWARD        624  'to 624'
             84_0  COME_FROM             8  '8'

 L. 359        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _dim
               88  LOAD_CONST               2
               90  COMPARE_OP               ==
            92_94  POP_JUMP_IF_FALSE   316  'to 316'

 L. 360        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _current
              100  LOAD_ATTR                axis1
              102  LOAD_ATTR                itype
              104  LOAD_CONST               0
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   198  'to 198'

 L. 361       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _current
              114  LOAD_ATTR                axis2
              116  LOAD_ATTR                itype
              118  LOAD_CONST               0
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   144  'to 144'

 L. 362       124  LOAD_GLOBAL              np
              126  LOAD_METHOD              ones_like
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _current
              132  LOAD_ATTR                buffer
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _current
              140  STORE_ATTR               buffer
              142  JUMP_FORWARD        196  'to 196'
            144_0  COME_FROM           122  '122'

 L. 364       144  LOAD_CONST               1.0
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _current
              150  LOAD_ATTR                buffer
              152  LOAD_CONST               None
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  LOAD_CONST               None
              160  LOAD_CONST               None
              162  LOAD_CONST               2
              164  BUILD_SLICE_3         3 
              166  BUILD_TUPLE_2         2 
              168  STORE_SUBSCR     

 L. 365       170  LOAD_CONST               0.0
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _current
              176  LOAD_ATTR                buffer
              178  LOAD_CONST               None
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  LOAD_CONST               1
              186  LOAD_CONST               None
              188  LOAD_CONST               2
              190  BUILD_SLICE_3         3 
              192  BUILD_TUPLE_2         2 
              194  STORE_SUBSCR     
            196_0  COME_FROM           142  '142'
              196  JUMP_FORWARD        624  'to 624'
            198_0  COME_FROM           108  '108'

 L. 367       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _current
              202  LOAD_ATTR                axis2
              204  LOAD_ATTR                itype
              206  LOAD_CONST               0
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   250  'to 250'

 L. 368       212  LOAD_CONST               1.0
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                _current
              218  LOAD_ATTR                buffer
              220  LOAD_CONST               None
              222  LOAD_CONST               None
              224  LOAD_CONST               2
              226  BUILD_SLICE_3         3 
              228  STORE_SUBSCR     

 L. 369       230  LOAD_CONST               0.0
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                _current
              236  LOAD_ATTR                buffer
              238  LOAD_CONST               1
              240  LOAD_CONST               None
              242  LOAD_CONST               2
              244  BUILD_SLICE_3         3 
              246  STORE_SUBSCR     
              248  JUMP_FORWARD        624  'to 624'
            250_0  COME_FROM           210  '210'

 L. 371       250  LOAD_CONST               1.0
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                _current
              256  LOAD_ATTR                buffer
              258  LOAD_CONST               None
              260  LOAD_CONST               None
              262  LOAD_CONST               2
              264  BUILD_SLICE_3         3 
              266  STORE_SUBSCR     

 L. 372       268  LOAD_CONST               0.0
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                _current
              274  LOAD_ATTR                buffer
              276  LOAD_CONST               1
              278  LOAD_CONST               None
              280  LOAD_CONST               2
              282  BUILD_SLICE_3         3 
              284  STORE_SUBSCR     

 L. 373       286  LOAD_CONST               0.0
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                _current
              292  LOAD_ATTR                buffer
              294  LOAD_CONST               None
              296  LOAD_CONST               None
              298  BUILD_SLICE_2         2 
              300  LOAD_CONST               1
              302  LOAD_CONST               None
              304  LOAD_CONST               2
              306  BUILD_SLICE_3         3 
              308  BUILD_TUPLE_2         2 
              310  STORE_SUBSCR     
          312_314  JUMP_FORWARD        624  'to 624'
            316_0  COME_FROM            92  '92'

 L. 374       316  LOAD_FAST                'self'
              318  LOAD_ATTR                _dim
              320  LOAD_CONST               3
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   624  'to 624'

 L. 375       328  LOAD_GLOBAL              print
              330  LOAD_STR                 'ONE 3D A FINIR'
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  POP_TOP          

 L. 376       336  LOAD_FAST                'self'
              338  LOAD_ATTR                _current
              340  LOAD_ATTR                axis1
              342  LOAD_ATTR                itype
              344  LOAD_CONST               0
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   454  'to 454'

 L. 377       352  LOAD_FAST                'self'
              354  LOAD_ATTR                _current
              356  LOAD_ATTR                axis3
              358  LOAD_ATTR                itype
              360  LOAD_CONST               0
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   388  'to 388'

 L. 378       368  LOAD_GLOBAL              np
              370  LOAD_METHOD              ones_like
              372  LOAD_FAST                'self'
              374  LOAD_ATTR                _current
              376  LOAD_ATTR                buffer
              378  CALL_METHOD_1         1  '1 positional argument'
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                _current
              384  STORE_ATTR               buffer
              386  JUMP_FORWARD        452  'to 452'
            388_0  COME_FROM           364  '364'

 L. 380       388  LOAD_CONST               1.0
              390  LOAD_FAST                'self'
              392  LOAD_ATTR                _current
              394  LOAD_ATTR                buffer
              396  LOAD_CONST               None
              398  LOAD_CONST               None
              400  BUILD_SLICE_2         2 
              402  LOAD_CONST               None
              404  LOAD_CONST               None
              406  BUILD_SLICE_2         2 
              408  LOAD_CONST               None
              410  LOAD_CONST               None
              412  LOAD_CONST               2
              414  BUILD_SLICE_3         3 
              416  BUILD_TUPLE_3         3 
              418  STORE_SUBSCR     

 L. 381       420  LOAD_CONST               0.0
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                _current
              426  LOAD_ATTR                buffer
              428  LOAD_CONST               None
              430  LOAD_CONST               None
              432  BUILD_SLICE_2         2 
              434  LOAD_CONST               None
              436  LOAD_CONST               None
              438  BUILD_SLICE_2         2 
              440  LOAD_CONST               1
              442  LOAD_CONST               None
              444  LOAD_CONST               2
              446  BUILD_SLICE_3         3 
              448  BUILD_TUPLE_3         3 
              450  STORE_SUBSCR     
            452_0  COME_FROM           386  '386'
              452  JUMP_FORWARD        624  'to 624'
            454_0  COME_FROM           348  '348'

 L. 382       454  LOAD_FAST                'self'
              456  LOAD_ATTR                _current
              458  LOAD_ATTR                axis2
              460  LOAD_ATTR                itype
              462  LOAD_CONST               0
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   624  'to 624'

 L. 383       470  LOAD_FAST                'self'
              472  LOAD_ATTR                _current
              474  LOAD_ATTR                axis1
              476  LOAD_ATTR                itype
              478  LOAD_CONST               0
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   540  'to 540'

 L. 384       486  LOAD_CONST               1.0
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                _current
              492  LOAD_ATTR                buffer
              494  LOAD_CONST               None
              496  LOAD_CONST               None
              498  BUILD_SLICE_2         2 
              500  LOAD_CONST               None
              502  LOAD_CONST               None
              504  LOAD_CONST               2
            506_0  COME_FROM           196  '196'
              506  BUILD_SLICE_3         3 
              508  BUILD_TUPLE_2         2 
              510  STORE_SUBSCR     

 L. 385       512  LOAD_CONST               0.0
              514  LOAD_FAST                'self'
              516  LOAD_ATTR                _current
              518  LOAD_ATTR                buffer
              520  LOAD_CONST               None
              522  LOAD_CONST               None
              524  BUILD_SLICE_2         2 
              526  LOAD_CONST               1
              528  LOAD_CONST               None
              530  LOAD_CONST               2
              532  BUILD_SLICE_3         3 
              534  BUILD_TUPLE_2         2 
              536  STORE_SUBSCR     
              538  JUMP_FORWARD        624  'to 624'
            540_0  COME_FROM           482  '482'

 L. 387       540  LOAD_CONST               1.0
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                _current
              546  LOAD_ATTR                buffer
              548  LOAD_CONST               None
              550  LOAD_CONST               None
              552  BUILD_SLICE_2         2 
              554  LOAD_CONST               None
              556  LOAD_CONST               None
            558_0  COME_FROM           248  '248'
              558  LOAD_CONST               2
              560  BUILD_SLICE_3         3 
              562  BUILD_TUPLE_2         2 
              564  STORE_SUBSCR     

 L. 388       566  LOAD_CONST               0.0
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                _current
              572  LOAD_ATTR                buffer
              574  LOAD_CONST               None
              576  LOAD_CONST               None
              578  BUILD_SLICE_2         2 
              580  LOAD_CONST               1
              582  LOAD_CONST               None
            584_0  COME_FROM            42  '42'
              584  LOAD_CONST               2
              586  BUILD_SLICE_3         3 
              588  BUILD_TUPLE_2         2 
              590  STORE_SUBSCR     

 L. 389       592  LOAD_CONST               0.0
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                _current
              598  LOAD_ATTR                buffer
              600  LOAD_CONST               None
              602  LOAD_CONST               None
              604  BUILD_SLICE_2         2 
              606  LOAD_CONST               None
              608  LOAD_CONST               None
              610  BUILD_SLICE_2         2 
              612  LOAD_CONST               1
              614  LOAD_CONST               None
              616  LOAD_CONST               2
              618  BUILD_SLICE_3         3 
              620  BUILD_TUPLE_3         3 
              622  STORE_SUBSCR     
            624_0  COME_FROM           538  '538'
            624_1  COME_FROM           466  '466'
            624_2  COME_FROM           452  '452'
            624_3  COME_FROM           324  '324'
            624_4  COME_FROM           312  '312'
            624_5  COME_FROM            80  '80'

Parse error at or near `COME_FROM' instruction at offset 506_0

    def bcorr(self, mode, *arg):
        """Apply a baseline correction
        Computes and applies a base-line correction to the current data set.
        mode   describe the algorithm used:
          *  1 is linear correction
          *  2 is cubic spline correction.
          *  3 is polynomial (and related) correction  NOT IMPLEMENTED YET !

          if mode == 1 or 2

          then in 1D *arg is radius, list_of_points
            or in 2D *arg is radius, axis, list_of_points

        axis in 2D is either f1 or f2 (dimension in which correction is  applied).
        radius   is the radius around which each pivot point is averaged.
        
         list_of_points is then the list of the pivot points used for the 
        base-line correction.
        Linear correction can use 1 or more pivot points. 1 point 
        corresponds to correction of a continuous level. Spline corrections 
        needs at least 3 points.
        In any case maximum is 100 pivot points.
        """
        if mode in (1, 2):
            radius = arg[0]
            if self.get_dim() == 1:
                if self.get_itype_1d() != 0:
                    raise Exception('not available')
                xpoints = arg[1]
                if mode == 1:
                    self._current.bcorr_lin(xpoints)
                elif mode == 2:
                    self._current.bcorr_spline(xpoints, kind=3)
                elif self.get_dim() == 2:
                    axis = arg[1]
                    xpoints = arg[2]
                    if mode == 1:
                        print("attention, c'est faux")
                        self._current.bcorr_lin(xpoints, axis=axis)
                    elif mode == 2:
                        self._current.bcorr_spline(xpoints, axis=axis, kind=3)
            else:
                raise Exception('not implemented')
        else:
            if mode == 3:
                print(' bcorr 3 a faire')

    def bcorrp1(self):
        print('bcorrp1 a faire')

    def bcorrp0(self):
        print('bcorrp0 a faire')

    def chsize(self, *args):
        """
        Change size of data, zero-fill or truncate.
        DO NOT change the value of OFFSET and SPECW, so EXTRACT should
        always be preferred on spectra (unless you know exactly what your are doing).

        see also : extract modifysize
        """
        (self._current.chsize)(*args)

    def modifysize(self, si1, si2=-1, si3=-1):
        """
        modifysize( si1, si2 )
        modifysize( si1, si2, si3 )

        Permits to modify the leading sizes of a 2D or a 3D data-set, 
        provided the product of the sizes : si1*si2{*si3} is equal to the 
        product of the old ones.
        
        Does not actually modify the data.
        
        see also : chsize
        """
        print('modifisize A VALIDER')
        if self._dim == 2:
            self._plane2d.chsize(si1, si2)
        else:
            if self._dim == 3:
                self._image.chsize(si1, si2, si3)
        self._current.adapt_size()

    def plus(self):
        self._current.plus()

    def minus(self):
        self._current.minus()

    def extract(self, *args):
        (self._current.extract)(*args)

    def noise(self, value):
        """
        Contains the level of noise in the data-set. When loading data (1 or 
        2D) the noise level is evaluated automatically from the last 10th of 
        the data. Can also be set with EVALN.
        Used by INTEG and by Maximum Entropy run.
        """
        self._noise = value

    def shift(self, value):
        """
        This context holds the systematic baseline shift of the current 
        data-set, computed automatically by EVALN.
        Used by INTEG.
        see also : evaln noise addbase
        """
        self._shift = value

    def evaln(self, a, b, c=-1, d=-1):
        """
        evaluates the noise level as well as the overall offset of the data,over a area of the data. The results are stored in the NOISE and SHIFT 
        contexts This command is called automatically whenever a data set is read. The command will prompt for the last selected region with the POINT command
        
        in 2D, a,b,c,d is llf1, llf2, ur1, ur2
        """
        if self._dim == 1:
            shift = self._current.mean((a, b))
            noise = self._current.std((a, b))
        else:
            if self._dim == 2:
                shift = self._current.mean(((a, c), (b, d)))
                noise = self._current.std(((a, c), (b, d)))
            else:
                raise Exception('Not available in 3D')
        self._shift = shift
        self._noise = noise

    def fill(self, value):
        self._current.fill(value)

    def pkclear(self):
        self.peaks = []

    def peak(self, pkradius=0):
        if self._dim == 1:
            self.peaks = self._current.peak(threshold=(self.mini), offset=None)
            self.index = np.where(self.peaks <= self.maxi)[0]
        else:
            if self._dim == 2:
                self.peaks2d = self._current.peaks2d(threshold=(self.mini), zoom=((self._current.zo_2_1l, self._current.zo_2_1m), (self._current.zo_2_2l, self._current.zo_2_2m)))
            else:
                print('3D Pick peaker is not yet written')

    def geta_pk1d_a(self, i):
        return self._current.buffer[self.peaks[self.index[(i - 1)]]]

    def geta_pk1d_a_err(self, i):
        return 0

    def geta_pk1d_f(self, i):
        return self.peaks[self.index[(i - 1)]]

    def geta_pk1d_f_err(self, i):
        return 0

    def geta_pk1d_p(self, i):
        return 0

    def geta_pk1d_t(self, i):
        return 0

    def geta_pk1d_w(self, i):
        return 0

    def geta_pk1d_w_err(self, i):
        return 0

    def geta_pk2d_a(self, i):
        return self._current.buffer[(self.peaks2d[0][(i - 1)], self.peaks2d[1][(i - 1)])]

    def geta_pk2d_a_err(self, i):
        return 0

    def geta_pk2d_f1f(self, i):
        return self.peaks2d[0][(i - 1)]

    def geta_pk2d_f1f_err(self, i):
        return 0

    def geta_pk2d_f1w(self, i):
        return 0

    def geta_pk2d_f1w_err(self, i):
        return 0

    def geta_pk2d_f2f(self, i):
        return self.peaks2d[1][(i - 1)]

    def geta_pk2d_f2f_err(self, i):
        return 0

    def geta_pk2d_f2w(self, i):
        return 0

    def geta_pk2d_f2w_err(self, i):
        return 0

    def geta_pk3d_a(self, i):
        return 0

    def geta_pk3d_f1f(self, i):
        return 0

    def geta_pk3d_f1w(self, i):
        return 0

    def geta_pk3d_f2f(self, i):
        return 0

    def geta_pk3d_f2w(self, i):
        return 0

    def geta_pk3d_f3f(self, i):
        return 0

    def geta_pk3d_f3w(self, i):
        return 0

    def freq(self, *args):
        """
        
        The context FREQ holds the basic frequency of the spectrometer (in MHz).
        freq_H1 is meant to be the basic frequency of the spectrometer (1H freq)
        and is not used in the program. freq2 (and freq1 in 2D) are the freq
        associated to each dimension (different if in heteronuclear mode).
        Values are in MHz.
        
        see also : specw offset
        """
        if self._dim == 1:
            (self.freq1d)(*args)
        else:
            if self._dim == 2:
                (self.freq2d)(*args)
            else:
                if self._dim == 3:
                    (self.freq3d)(*args)
                else:
                    print('This should never happen', self._dim)

    def freq1d(self, freq_h1, freq1):
        self._column.frequency = freq_h1
        self._column.axis1.frequency = freq1

    def freq2d(self, freq_h1, freq1, freq2):
        self._plane2d.frequency = freq_h1
        self._plane2d.axis1.frequency = freq1
        self._plane2d.axis2.frequency = freq2

    def freq3d(self, freq_h1, freq1, freq2, freq3):
        self._image.frequency = freq_h1
        self._image.axis1.frequency = freq1
        self._image.axis2.frequency = freq2
        self._image.axis3.frequency = freq3

    def ft(self, axis='F1'):
        """
        Performs in-place complex Fourier Transform on the current data-set; 
        Data-set must be Complex.
         
         
        All FT commands work in 1D, 2D or 3D
         
        <ul>
        <li> in 1D axis, is not needed
        <li> in 2D axis, is F1, F2 or F12
        <li> in 3D axis, is F1, F2, F3, F12, F13, F23 or F123
        </ul>
         
         
        Here is a complete overview of FT routines : C stands for Complex, R  stands for Real
        <pre>
                FIDs            Spectra
                C       ---FT--->       C
                C       <--IFT---       C
                R       --RFT-->        C
                R       <--IRFT--       C
                C       -FTBIS->        R
                C       <-IFTBIS-       R
                R       Does not exist  R
        </pre>
        """
        for ax in self._test_axis(axis):
            self._current.fft(ax)

    def ift(self, axis='F1'):
        """
        Performs in-place inverse complex Fourier Transform on the current data-set; 
        Data-set must be Complex.
        """
        for ax in self._test_axis(axis):
            print(ax)
            self._current.ifft(ax)

    def ftbis(self, axis='F1'):
        """
        Data-set must be Complex.
        """
        for ax in self._test_axis(axis):
            self._current.fftr(ax)

    def iftbis(self, axis='F1'):
        """
        Data-set must be Real.
        """
        for ax in self._test_axis(axis):
            self._current.ifftr(ax)

    def com_max(self):
        self.maxi = self._current.buffer.max()
        self.mini = self._current.buffer.min()
        self.imaxi = self._current.buffer.argmax()
        self.imini = self._current.buffer.argmin()
        return self

    def minimax(self, mini, maxi):
        self.mini = mini
        self.maxi = maxi
        return self

    def geta_max(self, index):
        if index == 1:
            return self.maxi
        if index == 2:
            return self.mini
        print('we have a problem')

    def dmax(self, value):
        """
        Determines the fastest decaying component during Laplace analysis
        Given in arbitrary unit, use DFACTOR to relate to actual values.
        
        see also : dmin dfactor laplace tlaplace invlap invtlap
        
        sets the final value for the laplace transform
        """
        self._current.diffaxis.dmax = value

    def dmin(self, value):
        """
        Determines the fastest decaying component during Laplace analysis
        Given in arbitrary unit, use DFACTOR to relate to actual values.

        see also : dmin dfactor laplace tlaplace invlap invtlap

        sets the final value for the laplace transform
        """
        self._current.diffaxis.dmin = value

    def dfactor(self, value):
        self._current.diffaxis.dfactor = value

    def offset(self, *args):
        """
        Permits to specify the offset of the right-most (upper right most in
        2D) point of the data set. The value for offset are changed by @extract
        see also : specw
        """
        if self._dim == 1:
            (self.offset1d)(*args)
        else:
            if self._dim == 2:
                (self.offset2d)(*args)
            else:
                if self._dim == 3:
                    (self.offset3d)(*args)
                else:
                    print('This should never happen', self._dim)

    def offset1d(self, off1):
        self._column.axis1.offset = off1

    def offset2d(self, off1, off2):
        self._plane2d.axis1.offset = off1
        self._plane2d.axis2.offset = off2

    def offset3d(self, off1, off2, off3):
        self._image.axis1.offset = off1
        self._image.axis2.offset = off2
        self._image.axis3.offset = off3

    def read(self, file_name):
        """
        read( file_name )

        Reads the file as the new data set in standard format . 
        Same as readc 

        see also : write 
        """
        F = gf.GifaFile(file_name, 'r')
        F.load()
        self.dim(F.dim)
        self._current = F.get_data()
        self._current.check()

    def real(self, axis='F1'):
        for ax in self._test_axis(axis):
            self._current.real(ax)

    def reverse(self, axis='F1'):
        for ax in self._test_axis(axis):
            self._current.reverse(ax)

    def revf(self, axis='F1'):
        """
        Processes FID data-sets by multiplying by -1 2 points out of 4. 
        Permits to preprocess Bruker FIDs in Dim 2 (Bruker trick) before 
        RFT, or permits to bring back zero frequency in the center for some 
        other data formats
        """
        for ax in self._test_axis(axis):
            self._current.revf(ax)

    def invf(self, axis='F1'):
        """
        Process data-sets by multiplying by -1 1 point every 2 points. 
        Equivalent to taking the conjugated on complex data-sets, or 
        hyperconjugated on hypercomplex data-sets. If applied on a complex 
        FID, inverses the final spectrum obtained after Fourier transform. 

        see also : revf itype ft reverse
        """
        for ax in self._test_axis(axis):
            self._current.revf(ax)

    def irft(self, axis='F1'):
        """
        Perform  real-to-complex Fourier Transform on data
        """
        for ax in self._test_axis(axis):
            self._current.irfft(ax)

    def rft(self, axis='F1'):
        """
        Perform  real-to-complex Fourier Transform on data
        """
        for ax in self._test_axis(axis):
            self._current.rfft(ax)

    def row(self, i):
        """
        Extract the nth 1D row (along F2 axis) from the 2D data-set, and put 
        it in the 1D buffer. The row will be available as a 1D data set when 
        going from 2D to 1D
        """
        self.check2D()
        self._column = self._plane2d.row(i - 1)
        self._last_row = i

    def plane(self, axis, i):
        """
        Extract the nth 1D row (along F2 axis) from the 2D data-set, and put 
        it in the 1D buffer. The row will be available as a 1D data set when 
        going from 2D to 1D
        """
        self.check3D()
        self._plane2d = self._image.plane(axis, i - 1)
        self._last_plane = axis

    def proj(self, axis, projtype):
        if self._dim == 2:
            for axes in self._test_axis(axis):
                self._column = self._current.proj(axes, projtype)

        return self

    def vert(self, i, j):
        """
        In 3D mode, extract a column orthogonal to the last displayed plane.
        The column is taken at coordinates i and j in this plane.
        
        see also : plane col row dim
        """
        self.check3D()
        if self._last_plane == 1:
            self._column.buffer = self._image.buffer[:, i, j].copy()
        else:
            if self._last_plane == 2:
                self._column.buffer = self._image.buffer[i, :, j].copy()
            else:
                if self._last_plane == 3:
                    self._column.buffer = self._image.buffer[i, j, :].copy()

    def setval(self, *args):
        """
        Will set the value of the data point to x. The number of coordinates 
        of the point depends of dim. In dim 2 or 3, coordinates are F1 F2 or 
        F1 F2 F3. Can be usefully used when associated to the functions 
        valnd() to change data point value.
        """
        if self._dim == 1:
            (self.setval1d)(*args)
        else:
            if self._dim == 2:
                (self.setval2d)(*args)
            else:
                if self._dim == 3:
                    (self.setval3d)(*args)
                else:
                    print('This should never happen', self._dim)

    def setval1d(self, i, x):
        self._column.buffer[i - 1] = x

    def setval2d(self, i, j, x):
        try:
            self._plane2d.buffer[(i - 1)][j - 1] = x
        except:
            print('Pb in setval 2D ', i, j, x)

    def setval3d(self, i, j, k, x):
        try:
            self._image.buffer[(i - 1)][(j - 1)][k - 1] = x
        except:
            print('Pb in setval 3D ', i, j, k, x)

    def val1d(self, i):
        return self._column.buffer[(i - 1)]

    def val2d(self, i, j):
        return self._plane2d.buffer[(i - 1)][(j - 1)]

    def val3d(self, i, j, k, x):
        return self._image.buffer[(i - 1)][(j - 1)][(k - 1)]

    def specw(self, *args):
        """
        Permits to enter the value for the spectral width of the current
        data-set. One parameter will be needed for each dimension of the
        data-set.

        When reading a file the spectral width is set to 2000 * 3.1416 if no
        parameter block is available.

        The value for spectral width are changed by EXTRACT

        see also : offset extract
        """
        if self._dim == 1:
            (self.specw1d)(*args)
        else:
            if self._dim == 2:
                (self.specw2d)(*args)
            else:
                if self._dim == 3:
                    (self.specw3d)(*args)
                else:
                    print('This should never happen', self._dim)

    def specw1d(self, x):
        self._column.axis1.specwidth = x

    def specw2d(self, x, y):
        self._plane2d.axis1.specwidth = x
        self._plane2d.axis2.specwidth = y

    def specw3d(self, x, y, z):
        self._image.axis1.specwidth = x
        self._image.axis2.specwidth = y
        self._image.axis3.specwidth = z

    def write(self, file_name):
        """
        write( file_name )

        Writes the current data set to a file in standard format. 
        same as writec

        see also : read
        """
        F = gf.GifaFile(file_name, 'w')
        F.set_data(self._current)
        F.save()
        F.close()

    writec = write

    def set_task(self, task):
        print(task)

    def window(self):
        """
        window( {axis}, x, y)

        Define the window (with the starting point and the ending
        point) on which data is actually used for the iteration. Data
        outside this window(displayed as 0 during the interactive input) are
        just ignored for the processing. Window can be entered several time,
        the result being cumulative.

        see also : window_reset window_mode put apply
        """
        pass

    def window_reset(self):
        """
        window_reset( {axis})

        Resets the window to 1.0

        see also : window window_mode
        """
        pass

    def zero(self):
        self._current.buffer = np.zeros_like(self._current.buffer)

    def phase(self, ph0, ph1, axis=1):
        for ax in self._test_axis(axis):
            self._current.phase(ph0, ph1, ax)

    def apmin(self):
        self._current.apmin()
        self._last_ph0 = self._current.axis1.P0
        self._last_ph1 = self._current.axis1.P1

    def zoom(self, *args):
        if self._dim == 1:
            (self._current.zoom)(*(1, ), *args)
        else:
            if self._dim == 2:
                (self._current.zoom)(*(2, ), *args)
            else:
                if self._dim == 3:
                    (self._current.zoom)(*(3, ), *args)
        return self

    def get_debug(self):
        return self.debug

    def get_si1_1d(self):
        return self._column.size1

    def get_si1_2d(self):
        return self._plane2d.size1

    def get_si2_2d(self):
        return self._plane2d.size2

    def get_si1_3d(self):
        return self._image.size1

    def get_si2_3d(self):
        return self._image.size2

    def get_si3_3d(self):
        return self._image.size3

    def get_freq(self):
        return self._current.frequency

    def get_freq_1d(self):
        return self._column.axis1.frequency

    def get_freq_1_2d(self):
        return self._plane2d.axis1.frequency

    def get_freq_2_2d(self):
        return self._plane2d.axis2.frequency

    def get_freq_1_3d(self):
        return self._image.axis1.frequency

    def get_freq_2_3d(self):
        return self._image.axis2.frequency

    def get_freq_3_3d(self):
        return self._image.axis3.frequency

    def get_itype_1d(self):
        return self._column.axis1.itype

    def get_itype_2d(self):
        return 2 * self._plane2d.axis1.itype + self._plane2d.axis2.itype

    def get_itype_3d(self):
        return 4 * self._image.axis1.itype + 2 * self._image.axis2.itype + self._image.axis3.itype

    def get_shift(self):
        return self._shift

    def get_noise(self):
        return self._noise

    def get_offset_1d(self):
        return self._column.axis1.offset

    def get_offset_1_2d(self):
        return self._plane2d.axis1.offset

    def get_offset_1_3d(self):
        return self._image.axis1.offset

    def get_offset_2_2d(self):
        return self._plane2d.axis2.offset

    def get_offset_2_3d(self):
        return self._image.axis2.offset

    def get_offset_3_3d(self):
        return self._image.axis3.offset

    def get_specw_1d(self):
        return self._column.axis1.specwidth

    def get_specw_1_2d(self):
        return self._plane2d.axis1.specwidth

    def get_specw_2_2d(self):
        return self._plane2d.axis2.specwidth

    def get_specw_1_3d(self):
        return self._image.axis1.specwidth

    def get_specw_2_3d(self):
        return self._image.axis2.specwidth

    def get_specw_3_3d(self):
        return self._image.axis3.specwidth

    def get_dmin(self):
        return self.diffaxis.dmin

    def get_dmax(self):
        return self.diffaxis.dmax

    def get_dfactor(self):
        return self.diffaxis.dfactor

    def get_dim(self):
        return self._dim

    def get_version(self):
        from .. import SPIKE_version
        return '%s' % SPIKE_version

    def get_npk1d(self):
        return len(self.peaks)

    def get_npk2d(self):
        return len(self.peaks2d[0])

    def get_npk3d(self):
        return len(self.peaks)

    def get_ph0(self):
        return self._last_ph0

    def get_ph1(self):
        return self._last_ph1

    def get_row(self):
        return self._last_row

    def get_col(self):
        return self._last_col

    def get_si_tab(self):
        return self._tab.size1

    def itoh(self, index, dim, axis):
        if dim == 1:
            return self._column.itoh(axis, index)
        if dim == 2:
            return self._plane2d.itoh(axis, index)
        if dim == 3:
            return self._image.itoh(axis, index)
        print('problem in itoh')

    def itop(self, index, dim, axis):
        if dim == 1:
            return self._column.itop(axis, index)
        if dim == 2:
            return self._plane2d.itop(axis, index)
        if dim == 3:
            return self._image.itop(axis, index)
        print('problem in itop')

    def htop(self, index, dim, axis):
        if dim == 1:
            return self._column.htop(axis, index)
        if dim == 2:
            return self._plane2d.htop(axis, index)
        if dim == 3:
            return self._image.htop(axis, index)
        print('problem in htop')

    def htoi(self, index, dim, axis):
        if dim == 1:
            return self._column.htoi(axis, index)
        if dim == 2:
            return self._plane2d.htoi(axis, index)
        if dim == 3:
            return self._image.htoi(axis, index)
        print('problem in htoi')

    def ptoh(self, index, dim, axis):
        if dim == 1:
            return self._column.ptoh(axis, index)
        if dim == 2:
            return self._plane2d.ptoh(axis, index)
        if dim == 3:
            return self._image.ptoh(axis, index)
        print('problem in ptoh')

    def ptoi(self, index, dim, axis):
        if dim == 1:
            return self._column.ptoi(axis, index)
        if dim == 2:
            return self._plane2d.ptoi(axis, index)
        if dim == 3:
            return self._image.ptoi(axis, index)
        print('problem in ptoi')

    def bruker_corr(self):
        self._current.bruker_corr()

    def lb(self, value):
        self.lb = value

    def em(self, axis=0, lb=1.0):
        self._current.apod_em(axis, lb)
        self.lb = lb

    def tm(self, tm1, tm2, axis=0):
        print('TM still to do', tm1, tm2)

    def sqsin(self, maxi, axis=1):
        for ax in self._test_axis(axis):
            self._current.apod_sq_sin(ax, maxi)

    def sin(self, maxi, axis=1):
        for ax in self._test_axis(axis):
            self._current.apod_sin(ax, maxi)

    join = writec

    def put(self, parameter, n=0):
        """
        put(parameter)
        put(parameter, n) 
        
        Moves the content of the current buffer to an other buffer
        With parameter equal to:
        
        xx* DATA
            load the data to be used for MaxEnt processing or
                 as a off-hand place for processing
        
        in 1D only
        FILTER   load the filter used for Deconvolution.  If NCHANNEL is 
          greater than 1, then which channel you want to put.  eg.  PUT FILTER 
          3.  PUT FILTER 0  will consider the current data set as the 
          multichannel filter, and will load the whole filter. Useful when 
          associated with GET FILTER to store filters as files.
        WINDOW   load the window to be used for MaxEnt processing
        TAB      load the TAB buffer, used for tabulated fit.
        
        in 2D only
        ROW n   load the 1D buffer in the ROW n
        COL n   load the 1D buffer in the COL n
        
        in 3D only
        PLANE Fx n   load the 2D buffer in the plane Fx n
         
        see also : GET SHOW APPLY
        
        """
        if parameter == 'DATA' or parameter == 'data':
            self._datab = self._current.copy()
        else:
            if self._dim == 1:
                if parameter == 'WINDOW':
                    self._window = self._current.copy()
                elif parameter == 'TAB':
                    self._tab = self._current.copy()
                else:
                    print('********************* Nothing has been done yet')
            else:
                print('********************* Nothing has been done yet')

    def get(self, buffer_name):
        """
        get(buffer_name)

        if parameter == "DATA":
                self._datab = self._current.copy()
            

        
        Moves the content of another buffer, back to the current buffer with 
        buffer_name equal to:
        "data":      get the content of the data buffer
        "linefit":   get the simulated spectrum obtained form the current peak table
        "window":    get actual window used to compute the chisquare
        "filter":    get filter used for deconvolution
        "residue":   get residue of the spectrum after a maxent run
        "tab":        get the tab buffer used for tabulated fit
        see also : put apply
        """
        if buffer_name == 'DATA' or buffer_name == 'data':
            self._current = self._datab.copy()
        else:
            if buffer_name == 'WINDOW':
                self._current = self._window.copy()
            else:
                if buffer_name == 'TAB':
                    self._current = self._tab.copy()
                else:
                    if buffer_name == 'FILTER':
                        self._current = self._filter.copy()

    def exchdata--- This code section failed: ---

 L.1316         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _current
                4  LOAD_ATTR                dim
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _datab
               10  LOAD_ATTR                dim
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    38  'to 38'

 L.1317        16  LOAD_GLOBAL              Exception
               18  LOAD_STR                 'wrong buffer dim: %s'
               20  LOAD_GLOBAL              str
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _current
               26  LOAD_METHOD              dim
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  BINARY_MODULO    
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            14  '14'

 L.1318        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _current
               42  LOAD_ATTR                dim
               44  LOAD_CONST               1
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE   116  'to 116'

 L.1319        50  LOAD_FAST                'self'
               52  LOAD_METHOD              get_si1_1d
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _datab
               60  LOAD_ATTR                size1
               62  COMPARE_OP               !=
               64  POP_JUMP_IF_TRUE     82  'to 82'
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_itype_1d
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _datab
               76  LOAD_ATTR                itype
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE   114  'to 114'
             82_0  COME_FROM            64  '64'

 L.1320        82  LOAD_GLOBAL              Exception
               84  LOAD_STR                 'wrong buffer size: %s %s'
               86  LOAD_GLOBAL              str
               88  LOAD_FAST                'self'
               90  LOAD_METHOD              get_si1_1d
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_GLOBAL              str
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                _datab
              102  LOAD_ATTR                size1
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  BUILD_TUPLE_2         2 
              108  BINARY_MODULO    
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            80  '80'
              114  JUMP_FORWARD        304  'to 304'
            116_0  COME_FROM            48  '48'

 L.1321       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _current
              120  LOAD_ATTR                dim
              122  LOAD_CONST               2
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   198  'to 198'

 L.1322       128  LOAD_FAST                'self'
              130  LOAD_METHOD              get_si1_2d
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                _datab
              138  LOAD_ATTR                size1
              140  COMPARE_OP               !=
              142  POP_JUMP_IF_TRUE    176  'to 176'
              144  LOAD_FAST                'self'
              146  LOAD_METHOD              get_si2_2d
              148  CALL_METHOD_0         0  '0 positional arguments'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                _datab
              154  LOAD_ATTR                size2
              156  COMPARE_OP               !=
              158  POP_JUMP_IF_TRUE    176  'to 176'
              160  LOAD_FAST                'self'
              162  LOAD_METHOD              get_itype_2d
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _datab
              170  LOAD_ATTR                itype
              172  COMPARE_OP               !=
              174  POP_JUMP_IF_FALSE   196  'to 196'
            176_0  COME_FROM           158  '158'
            176_1  COME_FROM           142  '142'

 L.1323       176  LOAD_GLOBAL              Exception
              178  LOAD_STR                 'wrong buffer size 2D : %s'
              180  LOAD_GLOBAL              str
              182  LOAD_FAST                'self'
              184  LOAD_METHOD              get_si1_2d
              186  CALL_METHOD_0         0  '0 positional arguments'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  BINARY_MODULO    
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  RAISE_VARARGS_1       1  'exception instance'
            196_0  COME_FROM           174  '174'
              196  JUMP_FORWARD        304  'to 304'
            198_0  COME_FROM           126  '126'

 L.1324       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _current
              202  LOAD_ATTR                dim
              204  LOAD_CONST               3
              206  COMPARE_OP               ==
          208_210  POP_JUMP_IF_FALSE   304  'to 304'

 L.1325       212  LOAD_FAST                'self'
              214  LOAD_METHOD              get_si1_3d
              216  CALL_METHOD_0         0  '0 positional arguments'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _datab
              222  LOAD_ATTR                size1
              224  COMPARE_OP               !=
          226_228  POP_JUMP_IF_TRUE    284  'to 284'
              230  LOAD_FAST                'self'
              232  LOAD_METHOD              get_si2_3d
              234  CALL_METHOD_0         0  '0 positional arguments'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                _datab
              240  LOAD_ATTR                size2
              242  COMPARE_OP               !=
          244_246  POP_JUMP_IF_TRUE    284  'to 284'
              248  LOAD_FAST                'self'
              250  LOAD_METHOD              get_si3_3d
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                _datab
              258  LOAD_ATTR                size3
              260  COMPARE_OP               !=
          262_264  POP_JUMP_IF_TRUE    284  'to 284'
              266  LOAD_FAST                'self'
              268  LOAD_METHOD              get_itype_3d
              270  CALL_METHOD_0         0  '0 positional arguments'
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                _datab
              276  LOAD_ATTR                itype
              278  COMPARE_OP               !=
          280_282  POP_JUMP_IF_FALSE   304  'to 304'
            284_0  COME_FROM           262  '262'
            284_1  COME_FROM           244  '244'
            284_2  COME_FROM           226  '226'

 L.1326       284  LOAD_GLOBAL              Exception
              286  LOAD_STR                 'wrong buffer size 3D : %s'
              288  LOAD_GLOBAL              str
              290  LOAD_FAST                'self'
              292  LOAD_METHOD              get_si1_3d
              294  CALL_METHOD_0         0  '0 positional arguments'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  BINARY_MODULO    
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  RAISE_VARARGS_1       1  'exception instance'
            304_0  COME_FROM           280  '280'
            304_1  COME_FROM           208  '208'
            304_2  COME_FROM           196  '196'
            304_3  COME_FROM           114  '114'

 L.1327       304  LOAD_GLOBAL              npkd
              306  LOAD_ATTR                NPKData
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                _current
              312  LOAD_ATTR                buffer
              314  LOAD_METHOD              copy
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  LOAD_CONST               ('buffer',)
              320  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              322  STORE_FAST               'c'

 L.1328       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _datab
              328  LOAD_METHOD              copy
              330  CALL_METHOD_0         0  '0 positional arguments'
              332  LOAD_FAST                'self'
              334  STORE_ATTR               _current

 L.1329       336  LOAD_FAST                'c'
              338  LOAD_FAST                'self'
              340  STORE_ATTR               _datab

 L.1330       342  LOAD_FAST                'self'
              344  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 304_0

    def escale(self, value=1.0):
        """
        The Entropy expression during Maximum Entropy run is computed as follow :
        
            A = Escale * Sum(F(i))
            P(i) = F(i)/A
            S = -Sum( log(P(i)) * P(i) )
        
        Escale should be set to 1.0 for normal operation
        
        see also : maxent
        
        """
        if value != 0:
            self.escale = value
        else:
            self.escale = 1

    def get_Kore_1D(self):
        """return a working copy of the 1D Kore internal buffer"""
        return self._column.copy()

    def get_Kore_2D(self):
        """return a working copy of the 2D Kore internal buffer"""
        return self._plane2d.copy()

    def get_Kore_3D(self):
        """return a working copy of the 3D Kore internal buffer"""
        return self._image.copy()

    def set_Kore_1D(self, npkdata):
        """uses npkdata as the 1D Kore buffer"""
        if npkdata.dim != 1:
            NPKError('SHould be a 1D', data=npkdata)
        self._column = npkdata

    def set_Kore_2D(self, npkdata):
        """uses npkdata as the 1D Kore buffer"""
        if npkdata.dim != 2:
            NPKError('SHould be a 2D', data=npkdata)
        self._plane2d = npkdata

    def set_Kore_3D(self, npkdata):
        """uses npkdata as the 3D Kore buffer"""
        if npkdata.dim != 3:
            NPKError('SHould be a 3D', data=npkdata)
        self._image = npkdata


def compatibility(context):
    """
    inject Kore definition into context given by the caller
    """
    global kore
    for i in dir(kore):
        f = getattr(kore, i)
        if callable(f):
            context[i] = i.startswith('_') or f
            context['com_' + i] = f


kore = Kore()
compatibility(globals())