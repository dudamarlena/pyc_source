# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lilcom/lilcom_interface.py
# Compiled at: 2019-08-13 01:34:25
# Size of source mod 2**32: 6700 bytes
import numpy as np
from ctypes import *

def _compress(data, axis=-1, lpc_order=5, default_exponent=0, out=None):
    """ This function compresses sequence data (for example, audio data) to 1 byte per
        sample.

       Args:
         data:            A numpy.ndarray, with dtype in [np.int16, np.float32, np.float64].
                          Must not be empty, and must not contain infinities, NaNs, or
                          (if dtype if np.float64), numbers so large that if converted to
                          np.float32 they would become infinity.
             axis (int):  The axis of `sequence_data` that corresponds to the time
                          dimension.  (Does not have to really correspond to time, but this
                          is the dimension we do linear prediction in.) . -1 means the last
                          axis.
       lpc_order (int):   A number in [0..15] that determines the order of linear
                          prediction.  Compression/decompression time will rise
                          roughly linearly with lpc_order, and the compression will
                          get more lossy for small lpc_order.
       default_exponent (int):  This number, which must be in the range [-127..128],
                          affects the range of the output only in cases where the
                          array was compressed from int16_t source but is
                          decompressed to floating-point output.  The integer
                          values i in the range [-32768..32767] will be scaled
                          by 2^{default_exponent - 15} when converting to float or
                          double in such a case.  The value default_exponent=0 would
                          produce output iwhere the range of int64_t corresponds
                          to the floating-point range [-1.0,1.0].
       out                The user may pass in numpy.ndarray with dtype=np.int8, of the same
                          dimension as the output of this function would have been.
                          In that case, the output will be placed here.  If an array
                          of the wrong dimension is passed, ValueError will be raised.

       Returns:
           On success, returns a numpy.ndarray with dtype=np.int8, and with
           shape the same as `data` except the dimension on the axis numbered
           `axis` will have been increased by 4.  This can be decompressed by
           calling lilcom.decompress().

       Raises:
           TypeError if one of the arguments had the wrong type
           ValueError if an argument was out of range, e.g. invalid `axis` or
              `lpc_order` or an input array with no elements.
   """
    if not istype(data, np.ndarray):
        raise TypeError('Expected data to be of type numpy.ndarray, got {}'.format(type(data)))
    else:
        if data.dtype in [np.int16, np.float32, np.float64]:
            if not data.size != 0:
                raise TypeError('Expected data-type of NumPy array to be int16, float32 or float64 and it to be nonempty, got dtype={}, size={}'.format(data.dtype, data.size))
            if data.size == 0:
                raise ValueError('Input array is empty')
            if not (istype(axis, int) and axis >= -num_axes and axis < num_axes):
                raise ValueError('axis={} invalid or out of range for ndim={}'.format(axis, num_axes))
            if not (istype(lpc_order, int) and lpc_order >= 0 and lpc_order <= 15):
                raise ValueError('lpc_order={} is not valid'.format(lpc_order))
            if istype(default_exponent, int):
                if not (default_exponent >= 0 and default_exponent <= 15):
                    raise ValueError('default_exponent={} is not valid'.format(default_exponent))
        else:
            if axis != -1:
                if axis != num_axes - 1:
                    data = data.transpose(axis, -1)
            shape = data.shape[:-1] + (data.shape[(-1)] + 4,)
            if out is None:
                out = np.empty(shape, dtype=(np.int8))
            assert istype(out, np.ndarray), 'Expected `out` to be of type numpy.ndarray, got {}'.format(type(out))
        raise out.dtype == np.int8 and out.shape == shape or ValueError('Expected `out` to have dtype=int8 and shape={}, got {} and {}'.format(shape, out.dtype, out.shape))


def compress--- This code section failed: ---

 L. 108         0  LOAD_CONST               True
                2  STORE_FAST               'intMode'

 L. 109         4  LOAD_FAST                'inputSignal'
                6  LOAD_ATTR                dtype
                8  LOAD_CONST               ('float64', 'float32', 'float16')
               10  COMPARE_OP               in
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 110        14  LOAD_CONST               False
               16  STORE_FAST               'intMode'
             18_0  COME_FROM            12  '12'

 L. 112        18  LOAD_FAST                'inputSignal'
               20  LOAD_METHOD              flatten
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  STORE_FAST               'inputSignal_vectorized'

 L. 113        26  LOAD_FAST                'inputSignal'
               28  LOAD_ATTR                shape
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  STORE_FAST               'numSamples'

 L. 114        36  SETUP_EXCEPT         52  'to 52'

 L. 115        38  LOAD_FAST                'inputSignal'
               40  LOAD_ATTR                shape
               42  LOAD_CONST               1
               44  BINARY_SUBSCR    
               46  STORE_FAST               'inputStride'
               48  POP_BLOCK        
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_EXCEPT     36  '36'

 L. 116        52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 117        58  LOAD_CONST               1
               60  STORE_FAST               'inputStride'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            50  '50'

 L. 124        68  LOAD_FAST                'intMode'
               70  POP_JUMP_IF_FALSE    74  'to 74'

 L. 125        72  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            72  '72'
             74_1  COME_FROM            70  '70'

Parse error at or near `COME_FROM' instruction at offset 74_0


def decompress--- This code section failed: ---

 L. 148         0  LOAD_CONST               True
                2  STORE_FAST               'intMode'

 L. 149         4  LOAD_FAST                'inputSignal'
                6  LOAD_ATTR                dtype
                8  LOAD_CONST               ('float64', 'float32', 'float16')
               10  COMPARE_OP               in
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 150        14  LOAD_CONST               False
               16  STORE_FAST               'intMode'
             18_0  COME_FROM            12  '12'

 L. 152        18  LOAD_FAST                'inputSignal'
               20  LOAD_METHOD              flatten
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  STORE_FAST               'inputSignal_vectorized'

 L. 153        26  LOAD_FAST                'inputSignal'
               28  LOAD_ATTR                shape
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  STORE_FAST               'numSamples'

 L. 154        36  SETUP_EXCEPT         52  'to 52'

 L. 155        38  LOAD_FAST                'inputSignal'
               40  LOAD_ATTR                shape
               42  LOAD_CONST               1
               44  BINARY_SUBSCR    
               46  STORE_FAST               'inputStride'
               48  POP_BLOCK        
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_EXCEPT     36  '36'

 L. 156        52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 157        58  LOAD_CONST               1
               60  STORE_FAST               'inputStride'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            50  '50'

 L. 163        68  LOAD_FAST                'intMode'
               70  POP_JUMP_IF_FALSE    74  'to 74'

 L. 164        72  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            72  '72'
             74_1  COME_FROM            70  '70'

Parse error at or near `COME_FROM' instruction at offset 74_0