# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/wavio.py
# Compiled at: 2011-02-20 12:48:00
"""When run as a script:
python ~/lib/wavio.py [-g gain] -wavin|-wavout infile outfile
Reads or writes .wav files from any format supported by
gpkimgclass.py .

As a library, allows reading of class gpk_img data from a .WAV
file, and writing class gpk_img to a .WAV file.
"""
import wave, gpkimgclass, Num
OV_ERROR = 0
OV_LIMIT = 1
OV_IGNORE = 2

class Overflow(ValueError):

    def __init__(self, *s):
        ValueError.__init__(self, *s)


class BadFileFormatError(Exception):

    def __init__(self, *s):
        Exception.__init__(self, *s)


_sizes = {2: (
     Num.int16, 16), 
   4: (
     Num.int32, 32)}

def read_hdr--- This code section failed: ---

 L.  43         0  SETUP_EXCEPT         22  'to 25'

 L.  44         3  LOAD_GLOBAL           0  'wave'
                6  LOAD_ATTR             1  'open'
                9  LOAD_FAST             0  'fn'
               12  LOAD_CONST               'r'
               15  CALL_FUNCTION_2       2  None
               18  STORE_FAST            1  'w'
               21  POP_BLOCK        
               22  JUMP_FORWARD         41  'to 66'
             25_0  COME_FROM             0  '0'

 L.  45        25  DUP_TOP          
               26  LOAD_GLOBAL           0  'wave'
               29  LOAD_ATTR             2  'Error'
               32  COMPARE_OP           10  exception-match
               35  POP_JUMP_IF_FALSE    65  'to 65'
               38  POP_TOP          
               39  STORE_FAST            2  'x'
               42  POP_TOP          

 L.  46        43  LOAD_GLOBAL           3  'BadFileFormatError'
               46  LOAD_CONST               '%s: %s'
               49  LOAD_FAST             2  'x'
               52  LOAD_FAST             0  'fn'
               55  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               59  RAISE_VARARGS_2       2  None
               62  JUMP_FORWARD          1  'to 66'
               65  END_FINALLY      
             66_0  COME_FROM            65  '65'
             66_1  COME_FROM            22  '22'

 L.  47        66  LOAD_FAST             1  'w'
               69  LOAD_ATTR             4  'getcomptype'
               72  CALL_FUNCTION_0       0  None
               75  LOAD_CONST               'NONE'
               78  COMPARE_OP            2  ==
               81  POP_JUMP_IF_TRUE    103  'to 103'
               84  LOAD_ASSERT              AssertionError
               87  LOAD_CONST               "Can't handle %s compression"
               90  LOAD_FAST             1  'w'
               93  LOAD_ATTR             6  'getcompname'
               96  CALL_FUNCTION_0       0  None
               99  BINARY_MODULO    
              100  RAISE_VARARGS_2       2  None

 L.  48       103  LOAD_FAST             1  'w'
              106  LOAD_ATTR             7  'getnchannels'
              109  CALL_FUNCTION_0       0  None
              112  STORE_FAST            3  'nc'

 L.  49       115  LOAD_CONST               1.0
              118  LOAD_FAST             1  'w'
              121  LOAD_ATTR             8  'getframerate'
              124  CALL_FUNCTION_0       0  None
              127  BINARY_DIVIDE    
              128  STORE_FAST            4  'dt'

 L.  50       131  LOAD_GLOBAL           9  '_sizes'
              134  LOAD_FAST             1  'w'
              137  LOAD_ATTR            10  'getsampwidth'
              140  CALL_FUNCTION_0       0  None
              143  BINARY_SUBSCR    
              144  UNPACK_SEQUENCE_2     2 
              147  STORE_FAST            5  'numtype'
              150  STORE_FAST            6  'bitpix'

 L.  51       153  LOAD_FAST             1  'w'
              156  LOAD_ATTR            11  'getnframes'
              159  CALL_FUNCTION_0       0  None
              162  STORE_FAST            7  'nf'

 L.  52       165  BUILD_MAP_8           8  None

 L.  53       168  LOAD_FAST             3  'nc'
              171  LOAD_CONST               'NAXIS1'
              174  STORE_MAP        
              175  LOAD_FAST             7  'nf'
              178  LOAD_CONST               'NAXIS2'
              181  STORE_MAP        

 L.  54       182  LOAD_FAST             4  'dt'
              185  LOAD_CONST               'CDELT2'
              188  STORE_MAP        
              189  LOAD_CONST               1
              192  LOAD_CONST               'CRPIX2'
              195  STORE_MAP        
              196  LOAD_CONST               0.0
              199  LOAD_CONST               'CRVAL2'
              202  STORE_MAP        

 L.  55       203  LOAD_FAST             6  'bitpix'
              206  LOAD_CONST               'BITPIX'
              209  STORE_MAP        
              210  LOAD_FAST             0  'fn'
              213  LOAD_CONST               '_NAME'
              216  STORE_MAP        
              217  LOAD_CONST               'WAV'
              220  LOAD_CONST               '_FILETYPE'
              223  STORE_MAP        
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 224


def read--- This code section failed: ---

 L.  73         0  SETUP_EXCEPT         22  'to 25'

 L.  74         3  LOAD_GLOBAL           0  'wave'
                6  LOAD_ATTR             1  'open'
                9  LOAD_FAST             0  'fn'
               12  LOAD_CONST               'r'
               15  CALL_FUNCTION_2       2  None
               18  STORE_FAST            3  'w'
               21  POP_BLOCK        
               22  JUMP_FORWARD         41  'to 66'
             25_0  COME_FROM             0  '0'

 L.  75        25  DUP_TOP          
               26  LOAD_GLOBAL           0  'wave'
               29  LOAD_ATTR             2  'Error'
               32  COMPARE_OP           10  exception-match
               35  POP_JUMP_IF_FALSE    65  'to 65'
               38  POP_TOP          
               39  STORE_FAST            4  'x'
               42  POP_TOP          

 L.  76        43  LOAD_GLOBAL           3  'BadFileFormatError'
               46  LOAD_CONST               '%s: %s'
               49  LOAD_FAST             4  'x'
               52  LOAD_FAST             0  'fn'
               55  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               59  RAISE_VARARGS_2       2  None
               62  JUMP_FORWARD          1  'to 66'
               65  END_FINALLY      
             66_0  COME_FROM            65  '65'
             66_1  COME_FROM            22  '22'

 L.  77        66  LOAD_FAST             3  'w'
               69  LOAD_ATTR             4  'getcomptype'
               72  CALL_FUNCTION_0       0  None
               75  LOAD_CONST               'NONE'
               78  COMPARE_OP            2  ==
               81  POP_JUMP_IF_TRUE    103  'to 103'
               84  LOAD_ASSERT              AssertionError
               87  LOAD_CONST               "Can't handle %s compression"
               90  LOAD_FAST             3  'w'
               93  LOAD_ATTR             6  'getcompname'
               96  CALL_FUNCTION_0       0  None
               99  BINARY_MODULO    
              100  RAISE_VARARGS_2       2  None

 L.  78       103  LOAD_FAST             3  'w'
              106  LOAD_ATTR             7  'getnchannels'
              109  CALL_FUNCTION_0       0  None
              112  STORE_FAST            5  'nc'

 L.  79       115  LOAD_CONST               1.0
              118  LOAD_FAST             3  'w'
              121  LOAD_ATTR             8  'getframerate'
              124  CALL_FUNCTION_0       0  None
              127  BINARY_DIVIDE    
              128  STORE_FAST            6  'dt'

 L.  80       131  LOAD_GLOBAL           9  '_sizes'
              134  LOAD_FAST             3  'w'
              137  LOAD_ATTR            10  'getsampwidth'
              140  CALL_FUNCTION_0       0  None
              143  BINARY_SUBSCR    
              144  UNPACK_SEQUENCE_2     2 
              147  STORE_FAST            7  'numtype'
              150  STORE_FAST            8  'bitpix'

 L.  81       153  LOAD_FAST             1  'tstart'
              156  LOAD_CONST               None
              159  COMPARE_OP            9  is-not
              162  POP_JUMP_IF_FALSE   231  'to 231'

 L.  82       165  LOAD_GLOBAL          12  'int'
              168  LOAD_GLOBAL          13  'round'
              171  LOAD_FAST             1  'tstart'
              174  LOAD_FAST             6  'dt'
              177  BINARY_DIVIDE    
              178  CALL_FUNCTION_1       1  None
              181  CALL_FUNCTION_1       1  None
              184  STORE_FAST            9  'istart'

 L.  83       187  LOAD_FAST             9  'istart'
              190  LOAD_CONST               0
              193  COMPARE_OP            0  <
              196  POP_JUMP_IF_FALSE   215  'to 215'

 L.  84       199  LOAD_GLOBAL          14  'ValueError'
              202  LOAD_CONST               'tstart=%.3fs < 0'
              205  LOAD_FAST             1  'tstart'
              208  BINARY_MODULO    
              209  RAISE_VARARGS_2       2  None
              212  JUMP_FORWARD          0  'to 215'
            215_0  COME_FROM           212  '212'

 L.  85       215  LOAD_FAST             3  'w'
              218  LOAD_ATTR            15  'setpos'
              221  LOAD_FAST             9  'istart'
              224  CALL_FUNCTION_1       1  None
              227  POP_TOP          
              228  JUMP_FORWARD         12  'to 243'

 L.  87       231  LOAD_CONST               0
              234  STORE_FAST            9  'istart'

 L.  88       237  LOAD_CONST               0.0
              240  STORE_FAST            1  'tstart'
            243_0  COME_FROM           228  '228'

 L.  89       243  LOAD_FAST             2  't_end'
              246  LOAD_CONST               None
              249  COMPARE_OP            9  is-not
              252  POP_JUMP_IF_FALSE   344  'to 344'

 L.  90       255  LOAD_GLOBAL          12  'int'
              258  LOAD_GLOBAL          13  'round'
              261  LOAD_FAST             2  't_end'
              264  LOAD_FAST             6  'dt'
              267  BINARY_DIVIDE    
              268  CALL_FUNCTION_1       1  None
              271  CALL_FUNCTION_1       1  None
              274  STORE_FAST           10  'nf'

 L.  91       277  LOAD_FAST            10  'nf'
              280  LOAD_FAST             3  'w'
              283  LOAD_ATTR            16  'getnframes'
              286  CALL_FUNCTION_0       0  None
              289  COMPARE_OP            4  >
              292  POP_JUMP_IF_FALSE   331  'to 331'

 L.  92       295  LOAD_GLOBAL          14  'ValueError'
              298  LOAD_CONST               't_end=%.3fs which is beyond the end of the wave file (%.3fs)'
              301  LOAD_FAST             2  't_end'
              304  LOAD_FAST             3  'w'
              307  LOAD_ATTR            16  'getnframes'
              310  CALL_FUNCTION_0       0  None
              313  LOAD_FAST             6  'dt'
              316  BINARY_MULTIPLY  
              317  LOAD_FAST             5  'nc'
              320  BINARY_DIVIDE    
              321  BUILD_TUPLE_2         2 
              324  BINARY_MODULO    
              325  RAISE_VARARGS_2       2  None
              328  JUMP_FORWARD          0  'to 331'
            331_0  COME_FROM           328  '328'

 L.  93       331  LOAD_FAST            10  'nf'
              334  LOAD_FAST             9  'istart'
              337  INPLACE_SUBTRACT 
              338  STORE_FAST           10  'nf'
              341  JUMP_FORWARD         16  'to 360'

 L.  95       344  LOAD_FAST             3  'w'
              347  LOAD_ATTR            16  'getnframes'
              350  CALL_FUNCTION_0       0  None
              353  LOAD_FAST             9  'istart'
              356  BINARY_SUBTRACT  
              357  STORE_FAST           10  'nf'
            360_0  COME_FROM           341  '341'

 L.  96       360  LOAD_FAST            10  'nf'
              363  LOAD_CONST               0
              366  COMPARE_OP            0  <
              369  POP_JUMP_IF_FALSE   394  'to 394'

 L.  97       372  LOAD_GLOBAL          14  'ValueError'
              375  LOAD_CONST               't_end=%.4f < tstart=%.4f'
              378  LOAD_FAST             2  't_end'
              381  LOAD_FAST             1  'tstart'
              384  BUILD_TUPLE_2         2 
              387  BINARY_MODULO    
              388  RAISE_VARARGS_2       2  None
              391  JUMP_FORWARD          0  'to 394'
            394_0  COME_FROM           391  '391'

 L.  98       394  LOAD_GLOBAL          17  'Num'
              397  LOAD_ATTR            18  'fromstring'
              400  LOAD_FAST             3  'w'
              403  LOAD_ATTR            19  'readframes'
              406  LOAD_FAST            10  'nf'
              409  CALL_FUNCTION_1       1  None
              412  LOAD_FAST             7  'numtype'
              415  CALL_FUNCTION_2       2  None
              418  STORE_FAST           11  'data'

 L.  99       421  LOAD_FAST             3  'w'
              424  LOAD_ATTR            20  'close'
              427  CALL_FUNCTION_0       0  None
              430  POP_TOP          

 L. 100       431  LOAD_FAST            11  'data'
              434  LOAD_ATTR            21  'shape'
              437  LOAD_CONST               0
              440  BINARY_SUBSCR    
              441  LOAD_FAST            10  'nf'
              444  LOAD_FAST             5  'nc'
              447  BINARY_MULTIPLY  
              448  COMPARE_OP            2  ==
              451  POP_JUMP_IF_TRUE    483  'to 483'
              454  LOAD_ASSERT              AssertionError
              457  LOAD_CONST               'Reshape from %d to %dx%d'
              460  LOAD_FAST            11  'data'
              463  LOAD_ATTR            21  'shape'
              466  LOAD_CONST               0
              469  BINARY_SUBSCR    
              470  LOAD_FAST            10  'nf'
              473  LOAD_FAST             5  'nc'
              476  BUILD_TUPLE_3         3 
              479  BINARY_MODULO    
              480  RAISE_VARARGS_2       2  None

 L. 101       483  LOAD_GLOBAL          17  'Num'
              486  LOAD_ATTR            22  'reshape'
              489  LOAD_FAST            11  'data'
              492  LOAD_FAST            10  'nf'
              495  LOAD_FAST             5  'nc'
              498  BUILD_TUPLE_2         2 
              501  CALL_FUNCTION_2       2  None
              504  STORE_FAST           11  'data'

 L. 102       507  BUILD_MAP_8           8  None

 L. 103       510  LOAD_FAST             5  'nc'
              513  LOAD_CONST               'NAXIS1'
              516  STORE_MAP        
              517  LOAD_FAST            10  'nf'
              520  LOAD_CONST               'NAXIS2'
              523  STORE_MAP        

 L. 104       524  LOAD_FAST             6  'dt'
              527  LOAD_CONST               'CDELT2'
              530  STORE_MAP        
              531  LOAD_CONST               1
              534  LOAD_CONST               'CRPIX2'
              537  STORE_MAP        
              538  LOAD_FAST             9  'istart'
              541  LOAD_FAST             6  'dt'
              544  BINARY_MULTIPLY  
              545  LOAD_CONST               'CRVAL2'
              548  STORE_MAP        

 L. 105       549  LOAD_FAST             8  'bitpix'
              552  LOAD_CONST               'BITPIX'
              555  STORE_MAP        
              556  LOAD_FAST             0  'fn'
              559  LOAD_CONST               '_NAME'
              562  STORE_MAP        
              563  LOAD_CONST               'WAV'
              566  LOAD_CONST               '_FILETYPE'
              569  STORE_MAP        
              570  STORE_FAST           12  'hdr'

 L. 107       573  LOAD_GLOBAL          23  'gpkimgclass'
              576  LOAD_ATTR            24  'gpk_img'
              579  LOAD_FAST            12  'hdr'
              582  LOAD_FAST            11  'data'
              585  CALL_FUNCTION_2       2  None
              588  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 585


def _itemsize(z):
    """This exists for Numeric/NumPy compatibility"""
    x = z.itemsize
    if isinstance(x, int):
        return x
    if callable(x):
        return x()
    raise RuntimeError, 'Cannot deal with %s' % str(type(x))


_typecodes = {_itemsize(Num.zeros((1, ), Num.Int32)) * 8: (
                                              Num.Int32, 2147483647.0, 1.0 - 2147483648.0), 
   _itemsize(Num.zeros((1, ), Num.Int16)) * 8: (
                                              Num.Int16, 32767.0, 1.0 - 32768.0), 
   _itemsize(Num.zeros((1, ), Num.Int8)) * 8: (
                                             Num.Int8, 127.0, 1.0 - 128.0)}

def write(data, fname, scalefac=1, allow_overflow=OV_ERROR):
    """@param data: is a class gpk_img object containing
                data to be written (note that the header information is
                ignored except for the sampling rate, bits per pixel,
                and number of channels.
        @param fname: is the name of a file to write it to (or a file object),
        @type fname: str or file,
        @param scalefac: is a factor to multiply the data
        @param allow_overflow: can be either
                - L{OV_ERROR} (default, means raise a ValueError exception
                        if the data*scalefac overflows),
                - L{OV_LIMIT} (means limit the data*scalefac to prevent
                        overflows -- this clips the audio), or
                - L{OV_IGNORE} (means let the overflows happen and don't worry.)
        @except ValueError: Missing information in C{data}.
        @except Overflow: The output format is clipping the data.   Strictly
                speaking, on 16-bit data, 32767 is considered clipping even
                though it possibly might be OK.   However such extreme values
                are very likely to be generated by clipping at an earlier
                stage of the processing, so it's probably an error even if
                the error is not being made here.
        """
    if not data.dt() > 0.0:
        raise ValueError, 'Cannot set sampling rate: dt=%g\n' % data.dt()
    hdr = data.hdr
    if not hdr.has_key('BITPIX') or int(hdr['BITPIX']) == 0:
        bitpix = 16
    else:
        bitpix = abs(int(hdr['BITPIX']))
    if not bitpix % 8 == 0:
        raise AssertionError
        if bitpix > 32:
            bitpix = 32
        tc, vmax, vmin = _typecodes[bitpix]
        dds = data.d * scalefac
        if allow_overflow == OV_ERROR:
            if not Num.alltrue(Num.greater_equal(Num.ravel(dds), vmin)):
                raise Overflow, 'Scaled data overflows negative'
            raise Num.alltrue(Num.less_equal(Num.ravel(dds), vmax)) or Overflow, 'Scaled data overflows positive'
    elif allow_overflow == OV_LIMIT:
        dds = Num.clip(dds, vmin, vmax)
    else:
        assert allow_overflow == OV_IGNORE
    d = Num.around(dds).astype(tc).tostring()
    w = wave.open(fname, 'w')
    w.setnchannels(data.d.shape[1])
    w.setnframes(data.d.shape[0])
    w.setsampwidth(bitpix / 8)
    w.setframerate(int(round(1.0 / float(data.dt()))))
    w.writeframesraw(d)
    w.close()


if __name__ == '__main__':
    import sys
    arglist = sys.argv[1:]
    gain = None
    if len(arglist) == 0:
        print __doc__
        sys.exit(1)
    if arglist[0] == '-g':
        arglist.pop(0)
        gain = float(arglist.pop(0))
    if arglist[0] == '-wavin':
        x = read(arglist[1])
        if gain is not None:
            Num.multiply(x.d, gain, x.d)
        x.write(arglist[2])
    elif arglist[0] == '-wavout':
        x = gpkimgclass.read(arglist[1])
        rxd = Num.ravel(x.d)
        mxv = max(rxd[Num.argmax(rxd)], -rxd[Num.argmin(rxd)])
        print '# max=', mxv
        if gain is None:
            gain = 32000.0 / mxv
        write(x, arglist[2], gain)
    else:
        print __doc__
        sys.exit(1)