# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\align.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 10513 bytes
"""
This module is used in order to align two different images.
Usually one from an SPM and the other from the ToF-SIMS.

This module also gives the ability to perform shift correction on images
which is used in order to align the different scans from ToF-SIMS images.
"""
from __future__ import print_function
import numpy as np
from skimage import transform as tf
from scipy.ndimage.filters import gaussian_filter

class Aligner:

    def __init__(self, fixed, other, prog=True, FFT=True):
        self.fixed = np.copy(fixed)
        self.other = np.copy(other)
        self.size = fixed.shape
        self.FFT = FFT
        self.trans = [0, 0]
        self.scale = [1, 1]
        self.rotation = 0
        self.initIDX = self.getMatchingIndex()

    def compute(self, prog=False):
        if prog:
            print('Progress [1/4] Improve Shift...', end='\r')
        else:
            self.ImproveShift()
            if prog:
                print('Progress [2/6] Improve Scale X...', end='\r')
            self.ImproveScaleX()
            if prog:
                print('Progress [3/6] Improve Scale Y...', end='\r')
            self.ImproveScaleY()
            if prog:
                print('Progress [4/6] Improve Rotation...', end='\r')
            self.ImproveRotation()
            if prog:
                print('Progress [5/6] Improve Scale X...', end='\r')
            self.ImproveScaleX()
            if prog:
                print('Progress [6/6] Improve Scale Y...', end='\r')
            self.ImproveScaleY()
            if prog:
                print('', end='\r')

    def ImproveShift(self, verbose=False, **kargs):
        tform = tf.AffineTransform(scale=(self.scale),
          rotation=(self.rotation),
          translation=(0, 0))
        O = tf.warp((self.other), tform, output_shape=(self.other.shape), preserve_range=True)
        if self.FFT:
            Corr = np.real(np.fft.fftshift(np.fft.ifft2(np.conj(np.fft.fft2(self.fixed)) * np.fft.fft2(O))))
            cord = np.unravel_index(np.argmax(Corr), self.fixed.shape)
            self.trans = [cord[1] - self.size[0] / 2, cord[0] - self.size[1] / 2]
        else:
            shift, D = AutoShift(self.fixed, O, shift=[-self.trans[0], self.trans[1]], **kargs)
            if verbose:
                print('ImproveShift', shift, D)
            self.trans = [
             -shift[0], shift[1]]

    def getTf(self, verbose=False):
        """
        Get the Afdfine transform.
        You can apply it to a pySPM Image (img) with: img.align(this.getTf())
        """
        if verbose:
            print('Transpose: {0[0]}, {0[1]}'.format(self.trans))
        return tf.AffineTransform(scale=(self.scale), rotation=(self.rotation), translation=(self.trans))

    def getMatchingIndex(self, power=1):
        img = tf.warp((self.other), (self.getTf()), output_shape=(self.other.shape), preserve_range=True)[:self.fixed.shape[0], :self.fixed.shape[1]]
        return np.sum(np.abs(self.fixed - img) ** power)

    def ImproveScaleX--- This code section failed: ---

 L.  84         0  LOAD_FAST                'self'
                2  LOAD_ATTR                scale
                4  STORE_FAST               'old'

 L.  85         6  LOAD_FAST                'self'
                8  LOAD_ATTR                getMatchingIndex
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'IDX1'

 L.  86        14  LOAD_FAST                'self'
               16  LOAD_ATTR                scale
               18  LOAD_CONST               0
               20  DUP_TOP_TWO      
               22  BINARY_SUBSCR    
               24  LOAD_CONST               1
               26  LOAD_FAST                'fact'
               28  BINARY_ADD       
               30  INPLACE_MULTIPLY 
               32  ROT_THREE        
               34  STORE_SUBSCR     

 L.  87        36  LOAD_FAST                'self'
               38  LOAD_ATTR                ImproveShift
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  POP_TOP          

 L.  88        44  LOAD_FAST                'self'
               46  LOAD_ATTR                getMatchingIndex
               48  CALL_FUNCTION_0       0  '0 positional arguments'
               50  STORE_FAST               'IDX2'

 L.  89        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'ImproveX'
               56  LOAD_FAST                'count'
               58  LOAD_FAST                'IDX1'
               60  LOAD_FAST                'IDX2'
               62  CALL_FUNCTION_4       4  '4 positional arguments'
               64  POP_TOP          

 L.  90        66  LOAD_FAST                'IDX2'
               68  LOAD_FAST                'IDX1'
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE   180  'to 180'

 L.  91        74  LOAD_FAST                'old'
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_CONST               1
               82  LOAD_FAST                'fact'
               84  BINARY_SUBTRACT  
               86  BINARY_MULTIPLY  
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                scale
               92  LOAD_CONST               0
               94  STORE_SUBSCR     

 L.  92        96  LOAD_FAST                'self'
               98  LOAD_ATTR                ImproveShift
              100  CALL_FUNCTION_0       0  '0 positional arguments'
              102  POP_TOP          

 L.  93       104  LOAD_FAST                'self'
              106  LOAD_ATTR                getMatchingIndex
              108  CALL_FUNCTION_0       0  '0 positional arguments'
              110  STORE_FAST               'IDX2'

 L.  94       112  LOAD_FAST                'IDX2'
              114  LOAD_FAST                'IDX1'
              116  COMPARE_OP               >
              118  POP_JUMP_IF_FALSE   154  'to 154'

 L.  95       120  LOAD_FAST                'old'
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                scale
              130  LOAD_CONST               0
              132  STORE_SUBSCR     

 L.  96       134  LOAD_FAST                'fact'
              136  LOAD_CONST               0.001
              138  COMPARE_OP               >
              140  POP_JUMP_IF_FALSE   178  'to 178'

 L.  97       142  LOAD_FAST                'self'
              144  LOAD_ATTR                ImproveScaleY
              146  LOAD_FAST                'fact'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  POP_TOP          
              152  JUMP_ABSOLUTE       204  'to 204'
              154  ELSE                     '178'

 L.  98       154  LOAD_FAST                'count'
              156  LOAD_CONST               11
              158  COMPARE_OP               <=
              160  POP_JUMP_IF_FALSE   204  'to 204'

 L.  99       162  LOAD_FAST                'self'
              164  LOAD_ATTR                ImproveScaleX
              166  LOAD_FAST                'fact'
              168  LOAD_FAST                'count'
              170  LOAD_CONST               1
              172  BINARY_ADD       
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  POP_TOP          
            178_0  COME_FROM           140  '140'
              178  JUMP_FORWARD        204  'to 204'
              180  ELSE                     '204'

 L. 100       180  LOAD_FAST                'count'
              182  LOAD_CONST               11
              184  COMPARE_OP               <=
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 101       188  LOAD_FAST                'self'
              190  LOAD_ATTR                ImproveScaleX
              192  LOAD_FAST                'fact'
              194  LOAD_FAST                'count'
              196  LOAD_CONST               1
              198  BINARY_ADD       
              200  CALL_FUNCTION_2       2  '2 positional arguments'
              202  POP_TOP          
            204_0  COME_FROM           186  '186'
            204_1  COME_FROM           178  '178'
            204_2  COME_FROM           160  '160'

Parse error at or near `COME_FROM' instruction at offset 204_1

    def ImproveRotation(self, delta=0.1, count=0, prog=False):
        IDX1 = self.getMatchingIndex()
        IDX2 = IDX1
        init = self.rotation
        if prog:
            print('Progress [{i}/4] Improve Rotation. Passes: {count} (max 11)'.format(i=prog,
              count=(count + 1)),
              end='\r')
        while IDX2 <= IDX1:
            IDX1 = IDX2
            count += 1
            self.rotation += delta
            self.ImproveShift()
            IDX2 = self.getMatchingIndex()

        self.rotation -= delta
        if delta > 0:
            self.ImproveRotation((-delta), count=(count + 1))
        elif abs(delta) > 1e-05:
            self.ImproveRotation((abs(delta) / 10.0), count=(count + 1))

    def ImproveScaleY--- This code section failed: ---

 L. 123         0  LOAD_FAST                'self'
                2  LOAD_ATTR                scale
                4  STORE_FAST               'old'

 L. 124         6  LOAD_FAST                'self'
                8  LOAD_ATTR                getMatchingIndex
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'IDX1'

 L. 125        14  LOAD_FAST                'self'
               16  LOAD_ATTR                scale
               18  LOAD_CONST               1
               20  DUP_TOP_TWO      
               22  BINARY_SUBSCR    
               24  LOAD_CONST               1
               26  LOAD_FAST                'fact'
               28  BINARY_ADD       
               30  INPLACE_MULTIPLY 
               32  ROT_THREE        
               34  STORE_SUBSCR     

 L. 126        36  LOAD_FAST                'self'
               38  LOAD_ATTR                ImproveShift
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  POP_TOP          

 L. 127        44  LOAD_FAST                'self'
               46  LOAD_ATTR                getMatchingIndex
               48  CALL_FUNCTION_0       0  '0 positional arguments'
               50  STORE_FAST               'IDX2'

 L. 128        52  LOAD_FAST                'IDX2'
               54  LOAD_FAST                'IDX1'
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE   170  'to 170'

 L. 129        60  LOAD_FAST                'old'
               62  LOAD_CONST               1
               64  BINARY_SUBSCR    
               66  LOAD_CONST               1
               68  LOAD_FAST                'fact'
               70  BINARY_SUBTRACT  
               72  BINARY_MULTIPLY  
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                scale
               78  LOAD_CONST               1
               80  STORE_SUBSCR     

 L. 130        82  LOAD_FAST                'self'
               84  LOAD_ATTR                ImproveShift
               86  CALL_FUNCTION_0       0  '0 positional arguments'
               88  POP_TOP          

 L. 131        90  LOAD_FAST                'self'
               92  LOAD_ATTR                getMatchingIndex
               94  CALL_FUNCTION_0       0  '0 positional arguments'
               96  STORE_FAST               'IDX2'

 L. 132        98  LOAD_FAST                'IDX2'
              100  LOAD_FAST                'IDX1'
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   144  'to 144'

 L. 133       106  LOAD_FAST                'old'
              108  LOAD_CONST               1
              110  BINARY_SUBSCR    
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                scale
              116  LOAD_CONST               1
              118  STORE_SUBSCR     

 L. 134       120  LOAD_FAST                'fact'
              122  LOAD_CONST               0.001
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   168  'to 168'

 L. 135       128  LOAD_FAST                'self'
              130  LOAD_ATTR                ImproveScaleX
              132  LOAD_FAST                'fact'
              134  LOAD_CONST               10
              136  BINARY_TRUE_DIVIDE
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  POP_TOP          
              142  JUMP_ABSOLUTE       194  'to 194'
              144  ELSE                     '168'

 L. 136       144  LOAD_FAST                'count'
              146  LOAD_CONST               11
              148  COMPARE_OP               <=
              150  POP_JUMP_IF_FALSE   194  'to 194'

 L. 137       152  LOAD_FAST                'self'
              154  LOAD_ATTR                ImproveScaleY
              156  LOAD_FAST                'fact'
              158  LOAD_FAST                'count'
              160  LOAD_CONST               1
              162  BINARY_ADD       
              164  CALL_FUNCTION_2       2  '2 positional arguments'
              166  POP_TOP          
            168_0  COME_FROM           126  '126'
              168  JUMP_FORWARD        194  'to 194'
              170  ELSE                     '194'

 L. 138       170  LOAD_FAST                'count'
              172  LOAD_CONST               11
              174  COMPARE_OP               <=
              176  POP_JUMP_IF_FALSE   194  'to 194'

 L. 139       178  LOAD_FAST                'self'
              180  LOAD_ATTR                ImproveScaleY
              182  LOAD_FAST                'fact'
              184  LOAD_FAST                'count'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  CALL_FUNCTION_2       2  '2 positional arguments'
              192  POP_TOP          
            194_0  COME_FROM           176  '176'
            194_1  COME_FROM           168  '168'
            194_2  COME_FROM           150  '150'

Parse error at or near `COME_FROM' instruction at offset 194_1

    def __repr__(self):
        return 'Scale: ({scale[0]},{scale[1]})\nRotation: {rot:.6f} deg.\nTranslation: ({trans[0]},{trans[1]})'.format(rot=(self.rotation), scale=(self.scale), trans=(self.trans))


def ApplyShift(Img, shift):
    dx, dy = [-int(x) for x in shift]
    return np.pad(Img, ((max(0, dy), max(0, -dy)), (max(0, -dx), max(0, dx))), mode='constant',
      constant_values=0)[max(0, -dy):max(0, -dy) + Img.shape[0],
     max(0, dx):max(0, dx) + Img.shape[1]]


def ShiftScore(Ref, Img, shift, gauss=5, mean=True, norm=False, debug=False, normData=False):
    if not Ref.shape[0] <= Img.shape[0]:
        raise AssertionError
    else:
        if not Ref.shape[1] <= Img.shape[1]:
            raise AssertionError
        else:
            if mean:
                Ref = Ref - np.mean(Ref)
                Img = Img - np.mean(Img)
            else:
                if normData:
                    if not np.std(Ref) > 0:
                        raise AssertionError
                    elif not np.std(Img) > 0:
                        raise AssertionError
                    Ref /= np.std(Ref)
                    Img /= np.std(Img)
                if gauss in (0, None, False):
                    im1 = Ref
                    im2 = Img
                else:
                    im1 = gaussian_filter(Ref, gauss)
                im2 = gaussian_filter(Img, gauss)
            corr2 = ApplyShift(im2, shift)
            dx, dy = shift
            DSX = Img.shape[1] - Ref.shape[1]
            DSY = Img.shape[0] - Ref.shape[0]
            Or = np.copy(im1)
            if dy < 0:
                Or[:-dy, :] = 0
            else:
                if DSY - dy < 0:
                    Or[DSY - dy:, :] = 0
                if dx > 0:
                    Or[:, :dx] = 0
                elif DSX + dx < 0:
                    Or[:, dx + DSX:] = 0
        corr2 = corr2[:Ref.shape[0], :Ref.shape[1]]
        D = np.sum(np.abs(Or - corr2))
        if norm:
            D /= (Ref.shape[0] - 2 * dy) * (Ref.shape[1] - 2 * dx)
    if debug:
        return (D, Or, corr2)
    else:
        return D


def AutoShift(Ref, Img, Delta=50, shift=(0, 0), step=5, gauss=5, mean=True, test=False, norm=False, normData=False):
    """Function to find the best shift between two images by using brute force
    It shift the two iumages and calculate a difference score between the two.
    The function will return the shift which gives the lowerst score (least difference)
    The score is the norm of the difference between the two images where all non-overlaping parts of the images
    due to the shifts are set to 0. The score is then normes by the effective area.
    In order to avoid the errors due to shot-noise, the images are gaussian blured.
  
    Delta: shifts between shift[0/1]-Delta and shift[0/1]+Delta will be tested
    step: The step between tested delta values
    gauss: For noisy image it is better to use a gaussian filter in order to improve the score accuracy.
           The value is the gaussian size.
    mean: If True, the mean value of each image are subtracted. This is prefered when the intensities of the two images does not match perfectly.
          Set it to False if you know that the intensities of your two images are identical
    Note: This function was developed as the maximum in FFT correlation does not seems to give very acurate
          result for images with low counts. If the shifts is expected to be big, the first guess shift can be calculated
          by FFT correlation. ie.:
          s = np.fft.fftshift( np.abs( np.fft.ifft2( np.fft.fft2(Reference) * np.conj(np.fft.fft2(Image)))))
          shift = [x-s.shape[i]/2 for i,x in enumerate(np.unravel_index(np.argmax(s), s.shape))]
    """
    if not Ref.shape[0] <= Img.shape[0]:
        raise AssertionError
    else:
        if not Ref.shape[1] <= Img.shape[1]:
            raise AssertionError
        else:
            if mean:
                Ref = Ref - np.mean(Ref)
                Img = Img - np.mean(Img)
            else:
                assert normData and np.std(Ref) > 0
                assert np.std(Img) > 0
            Ref /= np.std(Ref)
            Img /= np.std(Img)
        if gauss in (0, None, False):
            im1 = Ref
            im2 = Img
        else:
            im1 = gaussian_filter(Ref, gauss)
        im2 = gaussian_filter(Img, gauss)
    best = (0, 0)
    Dbest = Ref.shape[0] * Ref.shape[1] * max(np.max(im2), np.max(im1))
    tested = np.zeros((int(2 * Delta / step) + 1, int(2 * Delta / step) + 1))
    for iy, Dy in enumerate(np.arange(shift[1] - Delta, shift[1] + Delta + 1, step)):
        dy = int(Dy)
        for ix, Dx in enumerate(np.arange(shift[0] - Delta, shift[0] + Delta + 1, step)):
            dx = int(Dx)
            corr2 = ApplyShift(im2, (dx, dy))
            DSX = Img.shape[1] - Ref.shape[1]
            DSY = Img.shape[0] - Ref.shape[0]
            Or = np.copy(im1)
            if dy < 0:
                Or[:-dy, :] = 0
            else:
                if DSY - dy < 0:
                    Or[DSY - dy:, :] = 0
                if dx > 0:
                    Or[:, :dx] = 0
                elif DSX + dx < 0:
                    Or[:, dx + DSX:] = 0
            corr2 = corr2[:Ref.shape[0], :Ref.shape[1]]
            D = np.sum(np.abs(Or - corr2))
            if norm:
                D /= (Ref.shape[0] - 2 * dy) * (Ref.shape[1] - 2 * dx)
            if test:
                tested[(iy, ix)] = D
            if D < Dbest:
                Dbest = D
                best = (dx, dy)

    if test:
        return (best, Dbest, tested)
    else:
        return (
         best, Dbest)