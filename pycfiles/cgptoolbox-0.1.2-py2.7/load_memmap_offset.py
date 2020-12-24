# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\load_memmap_offset.py
# Compiled at: 2013-01-14 06:47:43
"""
Implementing offset and shape for io.load and format.open_memmap in numpy.lib.

Example using a Numpy array saved to a temporary directory.

>>> import tempfile, os, shutil
>>> dtemp = tempfile.mkdtemp()
>>> filename = os.path.join(dtemp, "test.npy")
>>> np.save(filename, np.arange(10))

>>> load(filename)
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> mmap = load(filename, mmap_mode="r+")
>>> mmap
memmap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> mmap[3:7] = 42
>>> del mmap
>>> np.load(filename)
array([ 0,  1,  2, 42, 42, 42, 42,  7,  8,  9])
>>> mmap = load(filename, mmap_mode="r+", offset=2, shape=6)
>>> mmap[-1] = 123
>>> del mmap
>>> np.load(filename)
array([  0,   1,   2,  42,  42,  42,  42, 123,   8,   9])

For loading memmaps, shape and offset apply to the first dimension only;
the remaining dimensions are read from the file.

>>> x = np.arange(24.0).view([("a", float), ("b", float)]).reshape(4, 3)
>>> np.save(filename, x)

Each sub-array has three items. This skips sub-array 0, 
then extracts sub-arrays 1 and 2.

>>> load(filename, mmap_mode="r+", offset=1, shape=2)
memmap([[(6.0, 7.0), (8.0, 9.0), (10.0, 11.0)],
        [(12.0, 13.0), (14.0, 15.0), (16.0, 17.0)]], 
        dtype=[('a', '<f8'), ('b', '<f8')])
>>> shutil.rmtree(dtemp)
"""
import numpy as np
_file = file
from numpy.lib.format import magic, read_magic, dtype_to_descr
from numpy.lib.format import read_array_header_1_0, write_array_header_1_0

def memmap_chunk_ind(filename, indices, mode='r+', check_contiguous=True):
    """
    Return a read-write memmap array containing given elements, and the offset.
    
    See memmap_chunk() if you just want chunk a.ID out of a.get_NID(), 
    where a is module "arrayjob".
    
    Example using Numpy array saved to a temporary directory.
    
    >>> import tempfile, os, shutil
    >>> dtemp = tempfile.mkdtemp()
    >>> filename = os.path.join(dtemp, "test.npy")
    >>> np.save(filename, np.arange(5))
    
    Typical usage.
    
    >>> memmap_chunk_ind(filename, range(2, 4))
    (memmap([2, 3]), 2)
    
    By default indices must make up a contiguous range (not necessarily sorted).
    
    >>> memmap_chunk_ind(filename, (1, 3, 4))
    Traceback (most recent call last):
    AssertionError: Indices not contiguous
    
    This skips the contiguity check.
    
    >>> memmap_chunk_ind(filename, (1, 3, 4), check_contiguous=False) 
    (memmap([1, 2, 3, 4]), 1)
    
    Note that the returned memmap has elements in the original order. 
    
    >>> ix = 1, 3, 2, 4
    >>> x, offset = memmap_chunk_ind(filename, ix)
    >>> x, offset
    (memmap([1, 2, 3, 4]), 1)
    
    Typical usage of the latter example:
    
    >>> [x[i - offset] for i in ix]
    [1, 3, 2, 4]
    
    Clean up after doctest.
    
    >>> del x
    >>> shutil.rmtree(dtemp)
    """
    indices = np.atleast_1d(indices)
    isort = sorted(indices)
    offset = isort[0]
    shape = 1 + isort[(-1)] - offset
    if check_contiguous:
        want = np.arange(offset, 1 + isort[(-1)])
        if len(indices) != shape or not all(isort == want):
            raise AssertionError, 'Indices not contiguous'
    mm = open_memmap(filename, mode=mode, offset=offset, shape=shape)
    return (mm, offset)


def open_memmap--- This code section failed: ---

 L. 136         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'filename'
                6  LOAD_GLOBAL           1  'basestring'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     30  'to 30'

 L. 137        15  LOAD_GLOBAL           2  'ValueError'
               18  LOAD_CONST               'Filename must be a string.  Memmap cannot use existing file handles.'
               21  CALL_FUNCTION_1       1  None
               24  RAISE_VARARGS_1       1  None
               27  JUMP_FORWARD          0  'to 30'
             30_0  COME_FROM            27  '27'

 L. 140        30  LOAD_CONST               'w'
               33  LOAD_FAST             1  'mode'
               36  COMPARE_OP            6  in
               39  POP_JUMP_IF_FALSE   265  'to 265'

 L. 141        42  LOAD_FAST             6  'offset'
               45  LOAD_CONST               0
               48  COMPARE_OP            2  ==
               51  POP_JUMP_IF_TRUE     63  'to 63'
               54  LOAD_ASSERT              AssertionError
               57  LOAD_CONST               'Cannot specify offset when creating memmap'
               60  RAISE_VARARGS_2       2  None

 L. 144        63  LOAD_FAST             5  'version'
               66  LOAD_CONST               (1, 0)
               69  COMPARE_OP            3  !=
               72  POP_JUMP_IF_FALSE   103  'to 103'

 L. 145        75  LOAD_CONST               'only support version (1,0) of file format, not %r'
               78  STORE_FAST            7  'msg'

 L. 146        81  LOAD_GLOBAL           2  'ValueError'
               84  LOAD_FAST             7  'msg'
               87  LOAD_FAST             5  'version'
               90  BUILD_TUPLE_1         1 
               93  BINARY_MODULO    
               94  CALL_FUNCTION_1       1  None
               97  RAISE_VARARGS_1       1  None
              100  JUMP_FORWARD          0  'to 103'
            103_0  COME_FROM           100  '100'

 L. 149       103  LOAD_GLOBAL           4  'np'
              106  LOAD_ATTR             5  'dtype'
              109  LOAD_FAST             2  'dtype'
              112  CALL_FUNCTION_1       1  None
              115  STORE_FAST            2  'dtype'

 L. 150       118  LOAD_FAST             2  'dtype'
              121  LOAD_ATTR             6  'hasobject'
              124  POP_JUMP_IF_FALSE   148  'to 148'

 L. 151       127  LOAD_CONST               "Array can't be memory-mapped: Python objects in dtype."
              130  STORE_FAST            7  'msg'

 L. 152       133  LOAD_GLOBAL           2  'ValueError'
              136  LOAD_FAST             7  'msg'
              139  CALL_FUNCTION_1       1  None
              142  RAISE_VARARGS_1       1  None
              145  JUMP_FORWARD          0  'to 148'
            148_0  COME_FROM           145  '145'

 L. 153       148  LOAD_GLOBAL           7  'dict'
              151  LOAD_CONST               'descr'

 L. 154       154  LOAD_GLOBAL           8  'dtype_to_descr'
              157  LOAD_FAST             2  'dtype'
              160  CALL_FUNCTION_1       1  None
              163  LOAD_CONST               'fortran_order'

 L. 155       166  LOAD_FAST             4  'fortran_order'
              169  LOAD_CONST               'shape'

 L. 156       172  LOAD_FAST             3  'shape'
              175  CALL_FUNCTION_768   768  None
              178  STORE_FAST            8  'd'

 L. 159       181  LOAD_GLOBAL           9  'open'
              184  LOAD_FAST             0  'filename'
              187  LOAD_FAST             1  'mode'
              190  LOAD_CONST               'b'
              193  BINARY_ADD       
              194  CALL_FUNCTION_2       2  None
              197  STORE_FAST            9  'fp'

 L. 160       200  SETUP_FINALLY        48  'to 251'

 L. 161       203  LOAD_FAST             9  'fp'
              206  LOAD_ATTR            10  'write'
              209  LOAD_GLOBAL          11  'magic'
              212  LOAD_FAST             5  'version'
              215  CALL_FUNCTION_VAR_0     0  None
              218  CALL_FUNCTION_1       1  None
              221  POP_TOP          

 L. 162       222  LOAD_GLOBAL          12  'write_array_header_1_0'
              225  LOAD_FAST             9  'fp'
              228  LOAD_FAST             8  'd'
              231  CALL_FUNCTION_2       2  None
              234  POP_TOP          

 L. 163       235  LOAD_FAST             9  'fp'
              238  LOAD_ATTR            13  'tell'
              241  CALL_FUNCTION_0       0  None
              244  STORE_FAST            6  'offset'
              247  POP_BLOCK        
              248  LOAD_CONST               None
            251_0  COME_FROM_FINALLY   200  '200'

 L. 165       251  LOAD_FAST             9  'fp'
              254  LOAD_ATTR            14  'close'
              257  CALL_FUNCTION_0       0  None
              260  POP_TOP          
              261  END_FINALLY      
              262  JUMP_FORWARD        273  'to 538'

 L. 168       265  LOAD_GLOBAL           9  'open'
              268  LOAD_FAST             0  'filename'
              271  LOAD_CONST               'rb'
              274  CALL_FUNCTION_2       2  None
              277  STORE_FAST            9  'fp'

 L. 169       280  SETUP_FINALLY       244  'to 527'

 L. 170       283  LOAD_GLOBAL          15  'read_magic'
              286  LOAD_FAST             9  'fp'
              289  CALL_FUNCTION_1       1  None
              292  STORE_FAST            5  'version'

 L. 171       295  LOAD_FAST             5  'version'
              298  LOAD_CONST               (1, 0)
              301  COMPARE_OP            3  !=
              304  POP_JUMP_IF_FALSE   335  'to 335'

 L. 172       307  LOAD_CONST               'only support version (1,0) of file format, not %r'
              310  STORE_FAST            7  'msg'

 L. 173       313  LOAD_GLOBAL           2  'ValueError'
              316  LOAD_FAST             7  'msg'
              319  LOAD_FAST             5  'version'
              322  BUILD_TUPLE_1         1 
              325  BINARY_MODULO    
              326  CALL_FUNCTION_1       1  None
              329  RAISE_VARARGS_1       1  None
              332  JUMP_FORWARD          0  'to 335'
            335_0  COME_FROM           332  '332'

 L. 174       335  LOAD_GLOBAL          16  'read_array_header_1_0'
              338  LOAD_FAST             9  'fp'
              341  CALL_FUNCTION_1       1  None
              344  UNPACK_SEQUENCE_3     3 
              347  STORE_FAST           10  'fullshape'
              350  STORE_FAST            4  'fortran_order'
              353  STORE_FAST            2  'dtype'

 L. 176       356  LOAD_FAST             3  'shape'
              359  POP_JUMP_IF_FALSE   410  'to 410'

 L. 177       362  LOAD_GLOBAL           4  'np'
              365  LOAD_ATTR            17  'atleast_1d'
              368  LOAD_FAST             3  'shape'
              371  CALL_FUNCTION_1       1  None
              374  STORE_FAST           11  'length'

 L. 178       377  LOAD_CONST               'Specify shape along first dimension only'
              380  STORE_FAST            7  'msg'

 L. 179       383  LOAD_FAST            11  'length'
              386  LOAD_ATTR            18  'ndim'
              389  LOAD_CONST               1
              392  COMPARE_OP            2  ==
              395  POP_JUMP_IF_TRUE    424  'to 424'
              398  LOAD_ASSERT              AssertionError
              401  LOAD_FAST             7  'msg'
              404  RAISE_VARARGS_2       2  None
              407  JUMP_FORWARD         14  'to 424'

 L. 181       410  LOAD_FAST            10  'fullshape'
              413  LOAD_CONST               0
              416  BINARY_SUBSCR    
              417  LOAD_FAST             6  'offset'
              420  BINARY_SUBTRACT  
              421  STORE_FAST           11  'length'
            424_0  COME_FROM           407  '407'

 L. 182       424  LOAD_FAST            11  'length'
              427  BUILD_TUPLE_1         1 
              430  LOAD_FAST            10  'fullshape'
              433  LOAD_CONST               1
              436  SLICE+1          
              437  BINARY_ADD       
              438  STORE_FAST            3  'shape'

 L. 184       441  LOAD_FAST             2  'dtype'
              444  LOAD_ATTR             6  'hasobject'
              447  POP_JUMP_IF_FALSE   471  'to 471'

 L. 185       450  LOAD_CONST               "Array can't be memory-mapped: Python objects in dtype."
              453  STORE_FAST            7  'msg'

 L. 186       456  LOAD_GLOBAL           2  'ValueError'
              459  LOAD_FAST             7  'msg'
              462  CALL_FUNCTION_1       1  None
              465  RAISE_VARARGS_1       1  None
              468  JUMP_FORWARD          0  'to 471'
            471_0  COME_FROM           468  '468'

 L. 188       471  LOAD_FAST             6  'offset'
              474  LOAD_GLOBAL           4  'np'
              477  LOAD_ATTR            19  'prod'
              480  LOAD_FAST            10  'fullshape'
              483  LOAD_CONST               1
              486  SLICE+1          
              487  LOAD_CONST               'dtype'
              490  LOAD_GLOBAL          20  'int'
              493  CALL_FUNCTION_257   257  None
              496  BINARY_MULTIPLY  
              497  STORE_FAST           12  'offset_items'

 L. 189       500  LOAD_FAST             9  'fp'
              503  LOAD_ATTR            13  'tell'
              506  CALL_FUNCTION_0       0  None
              509  LOAD_FAST            12  'offset_items'
              512  LOAD_FAST             2  'dtype'
              515  LOAD_ATTR            21  'itemsize'
              518  BINARY_MULTIPLY  
              519  BINARY_ADD       
              520  STORE_FAST           13  'offset_bytes'
              523  POP_BLOCK        
              524  LOAD_CONST               None
            527_0  COME_FROM_FINALLY   280  '280'

 L. 191       527  LOAD_FAST             9  'fp'
              530  LOAD_ATTR            14  'close'
              533  CALL_FUNCTION_0       0  None
              536  POP_TOP          
              537  END_FINALLY      
            538_0  COME_FROM           262  '262'

 L. 193       538  LOAD_FAST             4  'fortran_order'
              541  POP_JUMP_IF_FALSE   553  'to 553'

 L. 194       544  LOAD_CONST               'F'
              547  STORE_FAST           14  'order'
              550  JUMP_FORWARD          6  'to 559'

 L. 196       553  LOAD_CONST               'C'
              556  STORE_FAST           14  'order'
            559_0  COME_FROM           550  '550'

 L. 200       559  LOAD_FAST             1  'mode'
              562  LOAD_CONST               'w+'
              565  COMPARE_OP            2  ==
              568  POP_JUMP_IF_FALSE   580  'to 580'

 L. 201       571  LOAD_CONST               'r+'
              574  STORE_FAST            1  'mode'
              577  JUMP_FORWARD          0  'to 580'
            580_0  COME_FROM           577  '577'

 L. 203       580  LOAD_GLOBAL           4  'np'
              583  LOAD_ATTR            22  'memmap'
              586  LOAD_FAST             0  'filename'
              589  LOAD_CONST               'dtype'
              592  LOAD_FAST             2  'dtype'
              595  LOAD_CONST               'shape'
              598  LOAD_FAST             3  'shape'
              601  LOAD_CONST               'order'
              604  LOAD_FAST            14  'order'
              607  LOAD_CONST               'mode'

 L. 204       610  LOAD_FAST             1  'mode'
              613  LOAD_CONST               'offset'
              616  LOAD_FAST            13  'offset_bytes'
              619  CALL_FUNCTION_1281  1281  None
              622  STORE_FAST           15  'marray'

 L. 206       625  LOAD_FAST            15  'marray'
              628  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 523


def load(file, mmap_mode=None, offset=0, shape=None):
    """
    Load a pickled, ``.npy``, or ``.npz`` binary file.

    :param file file: The file to read. It must support ``seek()`` and 
        ``read()`` methods. If the filename extension is ``.gz``, the file is 
        first decompressed.
    :param str mmap_mode: {None, 'r+', 'r', 'w+', 'c'}
        If not None, then memory-map the file, using the given mode
        (see `numpy.memmap`).  The mode has no effect for pickled or
        zipped files.
        
        A memory-mapped array is stored on disk, and not directly loaded
        into memory.  However, it can be accessed and sliced like any
        ndarray.  Memory mapping is especially useful for accessing
        small fragments of large files without reading the entire file
        into memory.
    :return: array, tuple, dict, etc. data stored in the file.

    .. seealso::
       
       save, savez, loadtxt
       memmap : Create a memory-map to an array stored in a file on disk.

    .. note::
    
       * If the file contains pickle data, then whatever is stored in the
         pickle is returned.
       * If the file is a ``.npy`` file, then an array is returned.
       * If the file is a ``.npz`` file, then a dictionary-like object is
         returned, containing ``{filename: array}`` key-value pairs, one for
         each file in the archive.
    
    Examples:
    
    Store data to disk, and load it again:

    >>> np.save('/tmp/123', np.array([[1, 2, 3], [4, 5, 6]])) # doctest: +SKIP
    >>> np.load('/tmp/123.npy') # doctest: +SKIP
    array([[1, 2, 3],
           [4, 5, 6]])

    Mem-map the stored array, and then access the second row
    directly from disk:

    >>> X = np.load('/tmp/123.npy', mmap_mode='r') # doctest: +SKIP
    >>> X[1, :] # doctest: +SKIP
    memmap([4, 5, 6])
    """
    if not mmap_mode and (offset or shape):
        raise ValueError('Offset and shape should be used only with mmap_mode')
    import gzip
    if isinstance(file, basestring):
        fid = _file(file, 'rb')
    else:
        if isinstance(file, gzip.GzipFile):
            fid = np.lib.npyio.seek_gzip_factory(file)
        else:
            fid = file
        _ZIP_PREFIX = 'PK\x03\x04'
        N = len(np.lib.format.MAGIC_PREFIX)
        magic_ = fid.read(N)
        fid.seek(-N, 1)
        if magic_.startswith(_ZIP_PREFIX):
            return np.lib.npyio.NpzFile(fid)
        if magic_ == np.lib.format.MAGIC_PREFIX:
            if mmap_mode:
                return open_memmap(file, mode=mmap_mode, shape=shape, offset=offset)
            else:
                return np.lib.format.read_array(fid)

        else:
            try:
                return np.lib.npyio._cload(fid)
            except:
                raise IOError, 'Failed to interpret file %s as a pickle' % repr(file)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)