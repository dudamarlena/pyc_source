# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/utils/colormaputil.py
# Compiled at: 2018-11-09 15:08:51
# Size of source mod 2**32: 5107 bytes
__doc__ = '\nCredit & source: https://gist.github.com/salotz/4f585aac1adb6b14305c\n'
from __future__ import print_function, division, absolute_import
import numpy as np
from matplotlib import pyplot as pl, cm, colors
__version__ = '2013-12-19 dec denis'

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """ mycolormap = truncate_colormap(
            cmap name or file or ndarray,
            minval=0.2, maxval=0.8 ): subset
            minval=1, maxval=0 )    : reverse
    by unutbu http://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """
    cmap = get_cmap(cmap)
    name = '%s-trunc-%.2g-%.2g' % (cmap.name, minval, maxval)
    return colors.LinearSegmentedColormap.from_list(name, cmap(np.linspace(minval, maxval, n)))


def stack_colormap(A, B, n=256):
    """ low half -> A colors, high half -> B colors """
    A = get_cmap(A)
    B = get_cmap(B)
    name = '%s-%s' % (A.name, B.name)
    lin = np.linspace(0, 1, n)
    return array_cmap((np.vstack((A(lin), B(lin)))), name, n=n)


def get_cmap(cmap, name=None, n=256):
    """ in: a name "Blues" "BuGn_r" ... of a builtin cmap (case-sensitive)
        or a filename, np.loadtxt() n x 3 or 4  ints 0..255 or floats 0..1
        or a cmap already
        or a numpy array.
        See http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
        or in IPython, pl.cm.<tab>
    """
    if isinstance(cmap, colors.Colormap):
        return cmap
    elif isinstance(cmap, str):
        if cmap in cm.cmap_d:
            return pl.get_cmap(cmap)
        A = np.loadtxt(cmap, delimiter=None)
        name = name or 
    else:
        A = cmap
    return array_cmap(A, name, n=n)


def array_cmap--- This code section failed: ---

 L.  80         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              asanyarray
                4  LOAD_FAST                'A'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'A'

 L.  81        10  LOAD_FAST                'A'
               12  LOAD_ATTR                ndim
               14  LOAD_CONST               2
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    34  'to 34'
               20  LOAD_FAST                'A'
               22  LOAD_ATTR                shape
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  LOAD_CONST               (3, 4)
               30  COMPARE_OP               in
               32  POP_JUMP_IF_TRUE     52  'to 52'
             34_0  COME_FROM            18  '18'
               34  LOAD_ASSERT              AssertionError

 L.  82        36  LOAD_STR                 'array must be n x 3 or 4, not %s'
               38  LOAD_GLOBAL              str
               40  LOAD_FAST                'A'
               42  LOAD_ATTR                shape
               44  CALL_FUNCTION_1       1  ''
               46  BINARY_MODULO    
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  ''
             52_0  COME_FROM            32  '32'

 L.  83        52  LOAD_FAST                'A'
               54  LOAD_METHOD              min
               56  CALL_METHOD_0         0  ''
               58  LOAD_FAST                'A'
               60  LOAD_METHOD              max
               62  CALL_METHOD_0         0  ''
               64  ROT_TWO          
               66  STORE_FAST               'Amin'
               68  STORE_FAST               'Amax'

 L.  84        70  LOAD_FAST                'A'
               72  LOAD_ATTR                dtype
               74  LOAD_ATTR                kind
               76  LOAD_STR                 'i'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   140  'to 140'

 L.  85        82  LOAD_CONST               0
               84  LOAD_FAST                'Amin'
               86  DUP_TOP          
               88  ROT_THREE        
               90  COMPARE_OP               <=
               92  POP_JUMP_IF_FALSE   112  'to 112'
               94  LOAD_FAST                'Amax'
               96  DUP_TOP          
               98  ROT_THREE        
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   112  'to 112'
              104  LOAD_CONST               255
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_TRUE    130  'to 130'
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM           102  '102'
            112_1  COME_FROM            92  '92'
              112  POP_TOP          
            114_0  COME_FROM           110  '110'
              114  LOAD_GLOBAL              AssertionError
              116  LOAD_STR                 'Amin %d  Amax %d must be in 0 .. 255'
              118  LOAD_FAST                'Amin'
              120  LOAD_FAST                'Amax'
              122  BUILD_TUPLE_2         2 
              124  BINARY_MODULO    
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  ''
            130_0  COME_FROM           108  '108'

 L.  86       130  LOAD_FAST                'A'
              132  LOAD_CONST               255.0
              134  BINARY_TRUE_DIVIDE
              136  STORE_FAST               'A'
              138  JUMP_FORWARD        188  'to 188'
            140_0  COME_FROM            80  '80'

 L.  88       140  LOAD_CONST               0
              142  LOAD_FAST                'Amin'
              144  DUP_TOP          
              146  ROT_THREE        
              148  COMPARE_OP               <=
              150  POP_JUMP_IF_FALSE   170  'to 170'
              152  LOAD_FAST                'Amax'
              154  DUP_TOP          
              156  ROT_THREE        
              158  COMPARE_OP               <
              160  POP_JUMP_IF_FALSE   170  'to 170'
              162  LOAD_CONST               1
              164  COMPARE_OP               <=
              166  POP_JUMP_IF_TRUE    188  'to 188'
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           160  '160'
            170_1  COME_FROM           150  '150'
              170  POP_TOP          
            172_0  COME_FROM           168  '168'
              172  LOAD_GLOBAL              AssertionError
              174  LOAD_STR                 'Amin %g  Amax %g must be in 0 .. 1'
              176  LOAD_FAST                'Amin'
              178  LOAD_FAST                'Amax'
              180  BUILD_TUPLE_2         2 
              182  BINARY_MODULO    
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  ''
            188_0  COME_FROM           166  '166'
            188_1  COME_FROM           138  '138'

 L.  89       188  LOAD_GLOBAL              colors
              190  LOAD_ATTR                LinearSegmentedColormap
              192  LOAD_ATTR                from_list
              194  LOAD_FAST                'name'
              196  JUMP_IF_TRUE_OR_POP   200  'to 200'
              198  LOAD_STR                 'noname'
            200_0  COME_FROM           196  '196'
              200  LOAD_FAST                'A'
              202  LOAD_FAST                'n'
              204  LOAD_CONST               ('N',)
              206  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 112


def save_cmap(outfile, cmap):
    """ -> a file of 256 x 4 ints 0 .. 255
        to load it, np.loadtxt() or get_cmap( filename )
    """
    cmap = get_cmap(cmap)
    A = cmap(np.linspace(0, 1, 256))
    np.savetxt(outfile, (A * 255), fmt='%4.0f', header=('colormap %s' % cmap.name))


def band_colormap(cmap, nband=10):
    """ -> a colormap with e.g. 10 bands """
    cmap = get_cmap(cmap)
    h = 0.5 / nband
    A = cmap(np.linspace(h, 1 - h, nband))
    name = '%s-band-%d' % (cmap.name, nband)
    return array_cmap(A, name, n=nband)


cmap_brown = truncate_colormap((pl.cm.PuOr), minval=0.5, maxval=0)
cmap_bluebrown = stack_colormap('Blues_r', cmap_brown)
cmap_bluebrown10 = band_colormap(cmap_bluebrown, 10)
if __name__ == '__main__':
    import sys
    cmap = cmap_bluebrown10
    bw = array_cmap([[0.0, 0, 0], [1, 1, 1]], name='bw', n=2)
    plot = 0
    exec('\n'.join(sys.argv[1:]))
    np.set_printoptions(2, threshold=100, edgeitems=10, linewidth=100, suppress=True)
    print(cmap.name, '\n', cmap(np.arange(120, 136) / 256).T)
    save_cmap(cmap.name + '.tmp', cmap)
    if plot:
        A = np.arange(64).reshape((8, 8))
        im = pl.imshow(A, cmap=cmap, interpolation='nearest')
        pl.colorbar(im)
pl.show()