# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healsparse/healSparseMap.py
# Compiled at: 2020-05-04 20:14:02
# Size of source mod 2**32: 59881 bytes
from __future__ import division, absolute_import, print_function
import numpy as np, healpy as hp, os, numbers
from .utils import reduce_array, check_sentinel, _get_field_and_bitval, WIDE_NBIT, WIDE_MASK
from .utils import is_integer_value
from .fits_shim import HealSparseFits, _make_header, _write_filename

class HealSparseMap(object):
    __doc__ = '\n    Class to define a HealSparseMap\n    '

    def __init__(self, cov_index_map=None, sparse_map=None, nside_sparse=None, healpix_map=None, nside_coverage=None, primary=None, sentinel=None, nest=True, metadata=None):
        """
        Instantiate a HealSparseMap.

        Can be created with cov_index_map, sparse_map, and nside_sparse; or with
        healpix_map, nside_coverage.  Also see `HealSparseMap.read()`,
        `HealSparseMap.make_empty()`, `HealSparseMap.make_empty_like()`.

        Parameters
        ----------
        cov_index_map : `np.ndarray`, optional
           Coverage index map
        sparse_map : `np.ndarray`, optional
           Sparse map
        nside_sparse : `int`, optional
           Healpix nside for sparse map
        healpix_map : `np.ndarray`, optional
           Input healpix map to convert to a sparse map
        nside_coverage : `int`, optional
           Healpix nside for coverage map
        primary : `str`, optional
           Primary key for recarray, required if dtype has fields.
        sentinel : `int` or `float`, optional
           Sentinel value.  Default is `hp.UNSEEN` for floating-point types,
           and minimum int for int types.
        nest : `bool`, optional
           If input healpix map is in nest format.  Default is True.
        metadata : `dict`-like, optional
           Map metadata that can be stored in FITS header format.

        Returns
        -------
        healSparseMap : `HealSparseMap`
        """
        if cov_index_map is not None and sparse_map is not None and nside_sparse is not None:
            self._cov_index_map = cov_index_map
            self._sparse_map = sparse_map
        else:
            if healpix_map is not None:
                if nside_coverage is not None:
                    if sentinel is None:
                        sentinel = hp.UNSEEN
                    self._cov_index_map, self._sparse_map = self.convert_healpix_map(healpix_map, nside_coverage=nside_coverage,
                      nest=nest,
                      sentinel=sentinel)
                    nside_sparse = hp.npix2nside(healpix_map.size)
                else:
                    raise RuntimeError('Must specify either cov_index_map/sparse_map or healpix_map/nside_coverage')
            else:
                self._nside_coverage = hp.npix2nside(self._cov_index_map.size)
                self._nside_sparse = nside_sparse
                self._is_rec_array = False
                self._is_wide_mask = False
                self._wide_mask_width = 0
                self._primary = primary
                self.metadata = metadata
                if self._sparse_map.dtype.fields is not None:
                    self._is_rec_array = True
                    if self._primary is None:
                        raise RuntimeError('Must specify `primary` field when using a recarray for the sparse_map.')
                    self._sentinel = check_sentinel(self._sparse_map[self._primary].dtype.type, sentinel)
                else:
                    if self._sparse_map.dtype.type == WIDE_MASK:
                        if len(self._sparse_map.shape) == 2:
                            self._is_wide_mask = True
                            self._wide_mask_width = self._sparse_map.shape[1]
                            self._wide_mask_maxbits = WIDE_NBIT * self._wide_mask_width
                self._sentinel = check_sentinel(self._sparse_map.dtype.type, sentinel)
            self._bit_shift = 2 * int(np.round(np.log(self._nside_sparse / self._nside_coverage) / np.log(2)))

    @classmethod
    def read(cls, filename, nside_coverage=None, pixels=None, header=False):
        """
        Read in a HealSparseMap.

        Parameters
        ----------
        filename : `str`
           Name of the file to read.  May be either a regular HEALPIX
           map or a HealSparseMap
        nside_coverage : `int`, optional
           Nside of coverage map to generate if input file is healpix map.
        pixels : `list`, optional
           List of coverage map pixels to read.  Only used if input file
           is a HealSparseMap
        header : `bool`, optional
           Return the fits header as well as map?  Default is False.

        Returns
        -------
        healSparseMap : `HealSparseMap`
           HealSparseMap from file, covered by pixels
        header : `fitsio.FITSHDR` or `astropy.io.fits` (if header=True)
           Fits header for the map file.
        """
        with HealSparseFits(filename) as (fits):
            hdr = fits.read_ext_header(1)
        if 'PIXTYPE' in hdr and hdr['PIXTYPE'].rstrip() == 'HEALPIX':
            if nside_coverage is None:
                raise RuntimeError('Must specify nside_coverage when reading healpix map')
            elif hdr['OBJECT'].rstrip() == 'PARTIAL':
                with HealSparseFits(filename) as (fits):
                    row = fits.read_ext_data(1, row_range=[0, 1])
                    dtype = row[0]['SIGNAL'].dtype.type
            else:
                with HealSparseFits(filename) as (fits):
                    row = fits.read_ext_data(1, row_range=[0, 1])
                    dtype = row[0][0][0].dtype.type
            healpix_map = hp.read_map(filename, nest=True, verbose=False, dtype=dtype)
            if header:
                return (
                 cls(healpix_map=healpix_map, nside_coverage=nside_coverage, nest=True), hdr)
            return cls(healpix_map=healpix_map, nside_coverage=nside_coverage, nest=True)
        else:
            if 'PIXTYPE' in hdr and hdr['PIXTYPE'].rstrip() == 'HEALSPARSE':
                cov_index_map, sparse_map, nside_sparse, primary, sentinel = cls._read_healsparse_file(filename, pixels=pixels)
                if 'WIDEMASK' in hdr:
                    if hdr['WIDEMASK']:
                        sparse_map = sparse_map.reshape((sparse_map.size // hdr['WWIDTH'],
                         hdr['WWIDTH'])).astype(WIDE_MASK)
                if header:
                    return (
                     cls(cov_index_map=cov_index_map, sparse_map=sparse_map, nside_sparse=nside_sparse,
                       primary=primary,
                       sentinel=sentinel,
                       metadata=hdr), hdr)
                return cls(cov_index_map=cov_index_map, sparse_map=sparse_map, nside_sparse=nside_sparse,
                  primary=primary,
                  sentinel=sentinel,
                  metadata=hdr)
            else:
                raise RuntimeError('Filename %s not in healpix or healsparse format.' % filename)

    @classmethod
    def make_empty(cls, nside_coverage, nside_sparse, dtype, primary=None, sentinel=None, wide_mask_maxbits=None, metadata=None):
        """
        Make an empty map with nothing in it.

        Parameters
        ----------
        nside_coverage : `int`
           Nside for the coverage map
        nside_sparse : `int`
           Nside for the sparse map
        dtype : `str` or `list` or `np.dtype`
           Datatype, any format accepted by numpy.
        primary : `str`, optional
           Primary key for recarray, required if dtype has fields.
        sentinel : `int` or `float`, optional
           Sentinel value.  Default is `hp.UNSEEN` for floating-point types,
           and minimum int for int types.
        wide_mask_maxbits : `int`, optional
           Create a "wide bit mask" map, with this many bits.
        metadata : `dict`-like, optional
           Map metadata that can be stored in FITS header format.

        Returns
        -------
        healSparseMap : `HealSparseMap`
           HealSparseMap filled with sentinel values.
        """
        if wide_mask_maxbits is not None:
            test = np.zeros(1, dtype=dtype)
            if test.dtype != WIDE_MASK:
                raise ValueError('Must use dtype=healsparse.WIDE_MASK to use a wide_mask')
            if sentinel is not None:
                if sentinel != 0:
                    raise ValueError('Sentinel must be 0 for wide_mask')
            nbitfields = (wide_mask_maxbits - 1) // WIDE_NBIT + 1
        else:
            bit_shift = 2 * int(np.round(np.log(nside_sparse / nside_coverage) / np.log(2)))
            nfine_per_cov = 2 ** bit_shift
            cov_index_map = np.zeros((hp.nside2npix(nside_coverage)), dtype=(np.int64))
            cov_index_map[:] -= np.arange((hp.nside2npix(nside_coverage)), dtype=(np.int64)) * nfine_per_cov
            if wide_mask_maxbits is not None:
                sparse_map = np.zeros((nfine_per_cov, nbitfields), dtype=dtype)
            else:
                sparse_map = np.zeros(nfine_per_cov, dtype=dtype)
            if sparse_map.dtype.fields is not None:
                if primary is None:
                    raise RuntimeError("Must specify 'primary' field when using a recarray for the sparse_map.")
                primary_found = False
                for name in sparse_map.dtype.names:
                    if name == primary:
                        _sentinel = check_sentinel(sparse_map[name].dtype.type, sentinel)
                        sparse_map[name][:] = _sentinel
                        primary_found = True
                    else:
                        sparse_map[name][:] = check_sentinel(sparse_map[name].dtype.type, None)

                assert primary_found, 'Primary field not found in input dtype of recarray.'
            else:
                _sentinel = check_sentinel(sparse_map.dtype.type, sentinel)
                sparse_map[:] = _sentinel
        return cls(cov_index_map=cov_index_map, sparse_map=sparse_map, nside_sparse=nside_sparse,
          primary=primary,
          sentinel=_sentinel,
          metadata=metadata)

    @classmethod
    def make_empty_like(cls, sparsemap, nside_coverage=None, nside_sparse=None, dtype=None, primary=None, sentinel=None, wide_mask_maxbits=None, metadata=None):
        """
        Make an empty map with the same parameters as an existing map.

        Parameters
        ----------
        sparsemap : `HealSparseMap`
           Sparse map to use as basis for new empty map.
        nside_coverage : `int`, optional
           Coverage nside, default to sparsemap.nside_coverage
        nside_sparse : `int`, optional
           Sparse map nside, default to sparsemap.nside_sparse
        dtype : `str` or `list` or `np.dtype`, optional
           Datatype, any format accepted by numpy.  Default is sparsemap.dtype
        primary : `str`, optional
           Primary key for recarray.  Default is sparsemap.primary
        sentinel : `int` or `float`, optional
           Sentinel value.  Default is sparsemap._sentinel
        wide_mask_maxbits : `int`, optional
           Create a "wide bit mask" map, with this many bits.
        metadata : `dict`-like, optional
           Map metadata that can be stored in FITS header format.

        Returns
        -------
        healSparseMap : `HealSparseMap`
           HealSparseMap filled with sentinel values.
        """
        if nside_coverage is None:
            nside_coverage = sparsemap.nside_coverage
        else:
            if nside_sparse is None:
                nside_sparse = sparsemap.nside_sparse
            if dtype is None:
                dtype = sparsemap.dtype
            if primary is None:
                primary = sparsemap.primary
            if sentinel is None:
                sentinel = sparsemap._sentinel
            if wide_mask_maxbits is None and sparsemap._is_wide_mask:
                wide_mask_maxbits = sparsemap._wide_mask_maxbits
        if metadata is None:
            metadata = sparsemap._metadata
        return cls.make_empty(nside_coverage, nside_sparse, dtype, primary=primary, sentinel=sentinel,
          wide_mask_maxbits=wide_mask_maxbits,
          metadata=metadata)

    @staticmethod
    def _read_healsparse_file--- This code section failed: ---

 L. 308         0  LOAD_GLOBAL              HealSparseFits
                2  LOAD_FAST                'filename'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  SETUP_WITH           24  'to 24'
                8  STORE_FAST               'fits'

 L. 309        10  LOAD_FAST                'fits'
               12  LOAD_METHOD              read_ext_data
               14  LOAD_STR                 'COV'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  STORE_FAST               'cov_index_map'
               20  POP_BLOCK        
               22  LOAD_CONST               None
             24_0  COME_FROM_WITH        6  '6'
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  END_FINALLY      

 L. 310        30  LOAD_CONST               None
               32  STORE_FAST               'primary'

 L. 312        34  LOAD_FAST                'pixels'
               36  LOAD_CONST               None
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE   138  'to 138'

 L. 314        42  LOAD_GLOBAL              HealSparseFits
               44  LOAD_FAST                'filename'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  SETUP_WITH           76  'to 76'
               50  STORE_FAST               'fits'

 L. 315        52  LOAD_FAST                'fits'
               54  LOAD_METHOD              read_ext_data
               56  LOAD_STR                 'SPARSE'
               58  CALL_METHOD_1         1  '1 positional argument'
               60  STORE_FAST               'sparse_map'

 L. 316        62  LOAD_FAST                'fits'
               64  LOAD_METHOD              read_ext_header
               66  LOAD_STR                 'SPARSE'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  STORE_FAST               's_hdr'
               72  POP_BLOCK        
               74  LOAD_CONST               None
             76_0  COME_FROM_WITH       48  '48'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

 L. 317        82  LOAD_FAST                's_hdr'
               84  LOAD_STR                 'NSIDE'
               86  BINARY_SUBSCR    
               88  STORE_FAST               'nside_sparse'

 L. 318        90  LOAD_STR                 'PRIMARY'
               92  LOAD_FAST                's_hdr'
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 319        98  LOAD_FAST                's_hdr'
              100  LOAD_STR                 'PRIMARY'
              102  BINARY_SUBSCR    
              104  LOAD_METHOD              rstrip
              106  CALL_METHOD_0         0  '0 positional arguments'
              108  STORE_FAST               'primary'
            110_0  COME_FROM            96  '96'

 L. 321       110  LOAD_STR                 'SENTINEL'
              112  LOAD_FAST                's_hdr'
              114  COMPARE_OP               in
              116  POP_JUMP_IF_FALSE   128  'to 128'

 L. 322       118  LOAD_FAST                's_hdr'
              120  LOAD_STR                 'SENTINEL'
              122  BINARY_SUBSCR    
              124  STORE_FAST               'sentinel'
              126  JUMP_FORWARD        678  'to 678'
            128_0  COME_FROM           116  '116'

 L. 324       128  LOAD_GLOBAL              hp
              130  LOAD_ATTR                UNSEEN
              132  STORE_FAST               'sentinel'
          134_136  JUMP_FORWARD        678  'to 678'
            138_0  COME_FROM            40  '40'

 L. 326       138  LOAD_GLOBAL              np
              140  LOAD_METHOD              atleast_1d
              142  LOAD_FAST                'pixels'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  STORE_FAST               '_pixels'

 L. 327       148  LOAD_GLOBAL              len
              150  LOAD_GLOBAL              np
              152  LOAD_METHOD              unique
              154  LOAD_FAST                '_pixels'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                '_pixels'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  COMPARE_OP               <
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L. 328       170  LOAD_GLOBAL              RuntimeError
              172  LOAD_STR                 'Input list of pixels must be unique.'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  RAISE_VARARGS_1       1  'exception instance'
            178_0  COME_FROM           168  '168'

 L. 331       178  LOAD_GLOBAL              HealSparseFits
              180  LOAD_FAST                'filename'
              182  CALL_FUNCTION_1       1  '1 positional argument'
          184_186  SETUP_WITH          672  'to 672'
              188  STORE_FAST               'fits'

 L. 332       190  LOAD_FAST                'fits'
              192  LOAD_METHOD              read_ext_header
              194  LOAD_STR                 'SPARSE'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  STORE_FAST               's_hdr'

 L. 334       200  LOAD_FAST                's_hdr'
              202  LOAD_STR                 'NSIDE'
              204  BINARY_SUBSCR    
              206  STORE_FAST               'nside_sparse'

 L. 335       208  LOAD_GLOBAL              hp
              210  LOAD_METHOD              npix2nside
              212  LOAD_FAST                'cov_index_map'
              214  LOAD_ATTR                size
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'nside_coverage'

 L. 337       220  LOAD_STR                 'SENTINEL'
              222  LOAD_FAST                's_hdr'
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE   238  'to 238'

 L. 338       228  LOAD_FAST                's_hdr'
              230  LOAD_STR                 'SENTINEL'
              232  BINARY_SUBSCR    
              234  STORE_FAST               'sentinel'
              236  JUMP_FORWARD        244  'to 244'
            238_0  COME_FROM           226  '226'

 L. 340       238  LOAD_GLOBAL              hp
              240  LOAD_ATTR                UNSEEN
              242  STORE_FAST               'sentinel'
            244_0  COME_FROM           236  '236'

 L. 342       244  LOAD_CONST               2
              246  LOAD_GLOBAL              int
              248  LOAD_GLOBAL              np
              250  LOAD_METHOD              round
              252  LOAD_GLOBAL              np
              254  LOAD_METHOD              log
              256  LOAD_FAST                'nside_sparse'
              258  LOAD_FAST                'nside_coverage'
              260  BINARY_TRUE_DIVIDE
              262  CALL_METHOD_1         1  '1 positional argument'
              264  LOAD_GLOBAL              np
              266  LOAD_METHOD              log
              268  LOAD_CONST               2
              270  CALL_METHOD_1         1  '1 positional argument'
              272  BINARY_TRUE_DIVIDE
              274  CALL_METHOD_1         1  '1 positional argument'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  BINARY_MULTIPLY  
              280  STORE_FAST               'bit_shift'

 L. 343       282  LOAD_CONST               2
              284  LOAD_FAST                'bit_shift'
              286  BINARY_POWER     
              288  STORE_FAST               'nfine_per_cov'

 L. 345       290  LOAD_FAST                'fits'
              292  LOAD_METHOD              ext_is_image
              294  LOAD_STR                 'SPARSE'
              296  CALL_METHOD_1         1  '1 positional argument'
          298_300  POP_JUMP_IF_TRUE    314  'to 314'

 L. 347       302  LOAD_FAST                's_hdr'
              304  LOAD_STR                 'PRIMARY'
              306  BINARY_SUBSCR    
              308  LOAD_METHOD              rstrip
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               'primary'
            314_0  COME_FROM           298  '298'

 L. 350       314  LOAD_FAST                'cov_index_map'
              316  LOAD_GLOBAL              np
              318  LOAD_ATTR                arange
              320  LOAD_GLOBAL              hp
              322  LOAD_METHOD              nside2npix
              324  LOAD_FAST                'nside_coverage'
              326  CALL_METHOD_1         1  '1 positional argument'

 L. 351       328  LOAD_GLOBAL              np
              330  LOAD_ATTR                int64
              332  LOAD_CONST               ('dtype',)
              334  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              336  LOAD_FAST                'nfine_per_cov'
              338  BINARY_MULTIPLY  
              340  BINARY_ADD       
              342  STORE_FAST               'cov_index_map_temp'

 L. 352       344  LOAD_GLOBAL              np
              346  LOAD_METHOD              where
              348  LOAD_FAST                'cov_index_map_temp'
              350  LOAD_FAST                'nfine_per_cov'
              352  COMPARE_OP               >=
              354  CALL_METHOD_1         1  '1 positional argument'
              356  UNPACK_SEQUENCE_1     1 
              358  STORE_FAST               'cov_pix'

 L. 355       360  LOAD_GLOBAL              np
              362  LOAD_METHOD              clip
              364  LOAD_GLOBAL              np
              366  LOAD_METHOD              searchsorted
              368  LOAD_FAST                'cov_pix'
              370  LOAD_FAST                '_pixels'
              372  CALL_METHOD_2         2  '2 positional arguments'
              374  LOAD_CONST               0
              376  LOAD_FAST                'cov_pix'
              378  LOAD_ATTR                size
              380  LOAD_CONST               1
              382  BINARY_SUBTRACT  
              384  CALL_METHOD_3         3  '3 positional arguments'
              386  STORE_FAST               'sub'

 L. 356       388  LOAD_GLOBAL              np
              390  LOAD_METHOD              where
              392  LOAD_FAST                'cov_pix'
              394  LOAD_FAST                'sub'
              396  BINARY_SUBSCR    
              398  LOAD_FAST                '_pixels'
              400  COMPARE_OP               ==
              402  CALL_METHOD_1         1  '1 positional argument'
              404  UNPACK_SEQUENCE_1     1 
              406  STORE_FAST               'ok'

 L. 357       408  LOAD_FAST                'ok'
              410  LOAD_ATTR                size
              412  LOAD_CONST               0
              414  COMPARE_OP               ==
          416_418  POP_JUMP_IF_FALSE   428  'to 428'

 L. 358       420  LOAD_GLOBAL              RuntimeError
              422  LOAD_STR                 'None of the specified pixels are in the coverage map'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  RAISE_VARARGS_1       1  'exception instance'
            428_0  COME_FROM           416  '416'

 L. 359       428  LOAD_GLOBAL              np
              430  LOAD_METHOD              sort
              432  LOAD_FAST                'sub'
              434  LOAD_FAST                'ok'
              436  BINARY_SUBSCR    
              438  CALL_METHOD_1         1  '1 positional argument'
              440  STORE_FAST               'sub'

 L. 363       442  LOAD_GLOBAL              np
              444  LOAD_ATTR                zeros
              446  LOAD_FAST                'sub'
              448  LOAD_ATTR                size
              450  LOAD_CONST               1
              452  BINARY_ADD       
              454  LOAD_FAST                'nfine_per_cov'
              456  BINARY_MULTIPLY  
              458  LOAD_FAST                'fits'
              460  LOAD_METHOD              get_ext_dtype
              462  LOAD_STR                 'SPARSE'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  LOAD_CONST               ('dtype',)
              468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              470  STORE_FAST               'sparse_map'

 L. 365       472  LOAD_FAST                'fits'
              474  LOAD_ATTR                read_ext_data
              476  LOAD_STR                 'SPARSE'

 L. 366       478  LOAD_CONST               0
              480  LOAD_FAST                'nfine_per_cov'
              482  BUILD_LIST_2          2 
              484  LOAD_CONST               ('row_range',)
              486  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              488  LOAD_FAST                'sparse_map'
              490  LOAD_CONST               0
              492  LOAD_FAST                'nfine_per_cov'
              494  BUILD_SLICE_2         2 
              496  STORE_SUBSCR     

 L. 368       498  SETUP_LOOP          584  'to 584'
              500  LOAD_GLOBAL              enumerate
              502  LOAD_FAST                'cov_pix'
              504  LOAD_FAST                'sub'
              506  BINARY_SUBSCR    
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  GET_ITER         
              512  FOR_ITER            582  'to 582'
              514  UNPACK_SEQUENCE_2     2 
              516  STORE_FAST               'i'
              518  STORE_FAST               'pix'

 L. 369       520  LOAD_FAST                'cov_index_map_temp'
              522  LOAD_FAST                'pix'
              524  BINARY_SUBSCR    

 L. 370       526  LOAD_FAST                'cov_index_map_temp'
              528  LOAD_FAST                'pix'
              530  BINARY_SUBSCR    
              532  LOAD_FAST                'nfine_per_cov'
              534  BINARY_ADD       
              536  BUILD_LIST_2          2 
              538  STORE_FAST               'row_range'

 L. 372       540  LOAD_FAST                'fits'
              542  LOAD_ATTR                read_ext_data
              544  LOAD_STR                 'SPARSE'

 L. 373       546  LOAD_FAST                'row_range'
              548  LOAD_CONST               ('row_range',)
              550  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              552  LOAD_FAST                'sparse_map'
              554  LOAD_FAST                'i'
              556  LOAD_CONST               1
              558  BINARY_ADD       
              560  LOAD_FAST                'nfine_per_cov'
              562  BINARY_MULTIPLY  
              564  LOAD_FAST                'i'
              566  LOAD_CONST               2
              568  BINARY_ADD       
              570  LOAD_FAST                'nfine_per_cov'
              572  BINARY_MULTIPLY  
              574  BUILD_SLICE_2         2 
              576  STORE_SUBSCR     
          578_580  JUMP_BACK           512  'to 512'
              582  POP_BLOCK        
            584_0  COME_FROM_LOOP      498  '498'

 L. 376       584  LOAD_CONST               0
              586  LOAD_FAST                'cov_index_map'
              588  LOAD_CONST               None
              590  LOAD_CONST               None
              592  BUILD_SLICE_2         2 
              594  STORE_SUBSCR     

 L. 377       596  LOAD_GLOBAL              np
              598  LOAD_METHOD              arange
              600  LOAD_CONST               1
              602  LOAD_FAST                'sub'
              604  LOAD_ATTR                size
              606  LOAD_CONST               1
              608  BINARY_ADD       
              610  CALL_METHOD_2         2  '2 positional arguments'
              612  LOAD_FAST                'nfine_per_cov'
              614  BINARY_MULTIPLY  
              616  LOAD_FAST                'cov_index_map'
              618  LOAD_FAST                'cov_pix'
              620  LOAD_FAST                'sub'
              622  BINARY_SUBSCR    
              624  STORE_SUBSCR     

 L. 378       626  LOAD_FAST                'cov_index_map'
              628  LOAD_CONST               None
              630  LOAD_CONST               None
              632  BUILD_SLICE_2         2 
              634  DUP_TOP_TWO      
              636  BINARY_SUBSCR    
              638  LOAD_GLOBAL              np
              640  LOAD_ATTR                arange
              642  LOAD_GLOBAL              hp
              644  LOAD_METHOD              nside2npix
              646  LOAD_FAST                'nside_coverage'
              648  CALL_METHOD_1         1  '1 positional argument'
              650  LOAD_GLOBAL              np
              652  LOAD_ATTR                int64
              654  LOAD_CONST               ('dtype',)
              656  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              658  LOAD_FAST                'nfine_per_cov'
              660  BINARY_MULTIPLY  
              662  INPLACE_SUBTRACT 
              664  ROT_THREE        
              666  STORE_SUBSCR     
            668_0  COME_FROM           126  '126'
              668  POP_BLOCK        
              670  LOAD_CONST               None
            672_0  COME_FROM_WITH      184  '184'
              672  WITH_CLEANUP_START
              674  WITH_CLEANUP_FINISH
              676  END_FINALLY      
            678_0  COME_FROM           134  '134'

 L. 380       678  LOAD_FAST                'cov_index_map'
              680  LOAD_FAST                'sparse_map'
              682  LOAD_FAST                'nside_sparse'
              684  LOAD_FAST                'primary'
              686  LOAD_FAST                'sentinel'
              688  BUILD_TUPLE_5         5 
              690  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 668

    @staticmethod
    def convert_healpix_map(healpix_map, nside_coverage, nest=True, sentinel=hp.UNSEEN):
        """
        Convert a healpix map to a healsparsemap.

        Parameters
        ----------
        healpix_map : `np.array`
           Numpy array that describes a healpix map.
        nside_coverage : `int`
           Nside for the coverage map to construct
        nest : `bool`, optional
           Is the input map in nest format?  Default is True.
        sentinel : `float`, optional
           Sentinel value for null values in the sparse_map.
           Default is hp.UNSEEN

        Returns
        -------
        cov_index_map : `np.array`
           Coverage map with pixel indices
        sparse_map : `np.array`
           Sparse map of input values.
        """
        if not nest:
            healpix_map = hp.reorder(healpix_map, r2n=True)
        ipnest, = np.where(healpix_map > hp.UNSEEN)
        bit_shift = 2 * int(np.round(np.log(hp.npix2nside(healpix_map.size) / nside_coverage) / np.log(2)))
        ipnest_cov = np.right_shiftipnestbit_shift
        cov_pix = np.unique(ipnest_cov)
        nfine_per_cov = int(healpix_map.size / hp.nside2npix(nside_coverage))
        cov_index_map = np.zeros((hp.nside2npix(nside_coverage)), dtype=(np.int64))
        cov_index_map[cov_pix] = np.arange1(cov_pix.size + 1) * nfine_per_cov
        cov_index_map[:] -= np.arange((hp.nside2npix(nside_coverage)), dtype=(np.int64)) * nfine_per_cov
        sparse_map = np.zeros(((cov_pix.size + 1) * nfine_per_cov), dtype=(healpix_map.dtype)) + sentinel
        sparse_map[ipnest + cov_index_map[ipnest_cov]] = healpix_map[ipnest]
        return (
         cov_index_map, sparse_map)

    def write(self, filename, clobber=False):
        """
        Write heal HealSparseMap to filename.  Use the `metadata` property from
        the map to persist additional information in the fits header.

        Parameters
        ----------
        filename : `str`
           Name of file to save
        clobber : `bool`, optional
           Clobber existing file?  Default is False.
        """
        if os.path.isfile(filename):
            if not clobber:
                raise RuntimeError('Filename %s exists and clobber is False.' % filename)
        c_hdr = _make_header(self.metadata)
        c_hdr['PIXTYPE'] = 'HEALSPARSE'
        c_hdr['NSIDE'] = self._nside_coverage
        s_hdr = _make_header(self.metadata)
        s_hdr['PIXTYPE'] = 'HEALSPARSE'
        s_hdr['NSIDE'] = self._nside_sparse
        s_hdr['SENTINEL'] = self._sentinel
        if self._is_rec_array:
            s_hdr['PRIMARY'] = self._primary
        if self._is_wide_mask:
            s_hdr['WIDEMASK'] = self._is_wide_mask
            s_hdr['WWIDTH'] = self._wide_mask_width
        _write_filename(filename, c_hdr, s_hdr, self._cov_index_map, self._sparse_map)

    def update_values_pix(self, pixels, values, nest=True):
        """
        Update the values in the sparsemap for a list of pixels.

        Parameters
        ----------
        pixels : `np.ndarray`
           Integer array of sparse_map pixel values
        values : `np.ndarray`
           Value or Array of values.  Must be same type as sparse_map
        """
        if not isinstance(values, np.ndarray):
            raise RuntimeError('Values are not a numpy ndarray')
        else:
            if not nest:
                _pix = hp.ring2nestself._nside_sparsepixels
            else:
                _pix = pixels
            if self._sparse_map.dtype != values.dtype:
                raise RuntimeError('Data-type mismatch between sparse_map and values')
            if self._is_wide_mask:
                if len(values.shape) != 2:
                    raise RuntimeError('Values must be WideBits or equivalent array.')
                if values.shape[1] != self._wide_mask_width:
                    raise RuntimeError('Values must be WideBits or equivalent array with matched width.')
            if len(values) == 1:
                single_value = True
            else:
                single_value = False
                if len(values) != pixels.size:
                    raise RuntimeError('Length of values must be the same as pixels, or length 1.')
                else:
                    ipnest_cov = np.right_shift_pixself._bit_shift
                    cov_mask = self.coverage_mask
                    in_cov, = np.where(cov_mask[ipnest_cov])
                    out_cov, = np.where(~cov_mask[ipnest_cov])
                    if single_value:
                        self._sparse_map[_pix[in_cov] + self._cov_index_map[ipnest_cov[in_cov]]] = values[0]
                    else:
                        self._sparse_map[_pix[in_cov] + self._cov_index_map[ipnest_cov[in_cov]]] = values[in_cov]
                if out_cov.size > 0:
                    nfine_per_cov = 2 ** self._bit_shift
                    new_cov_pix = np.unique(ipnest_cov[out_cov])
                    if self._is_wide_mask:
                        sparse_append = np.zeros((new_cov_pix.size * nfine_per_cov, self._wide_mask_width), dtype=(self._sparse_map.dtype))
                    else:
                        sparse_append = np.zeros((new_cov_pix.size * nfine_per_cov), dtype=(self._sparse_map.dtype))
                    sparse_append[:] = self._sparse_map[0]
                    cov_index_map_temp = self._cov_index_map + np.arange((hp.nside2npix(self._nside_coverage)), dtype=(np.int64)) * nfine_per_cov
                    cov_index_map_temp[new_cov_pix] = np.arange(new_cov_pix.size) * nfine_per_cov + len(self._sparse_map)
                    cov_index_map_temp[:] -= np.arange((hp.nside2npix(self._nside_coverage)), dtype=(np.int64)) * nfine_per_cov
                    if single_value:
                        sparse_append[_pix[out_cov] + cov_index_map_temp[ipnest_cov[out_cov]] - len(self._sparse_map)] = values[0]
                    else:
                        sparse_append[_pix[out_cov] + cov_index_map_temp[ipnest_cov[out_cov]] - len(self._sparse_map)] = values[out_cov]
                    self._cov_index_map = cov_index_map_temp
                    if self._is_wide_mask:
                        self._sparse_map = np.reshapenp.appendself._sparse_mapsparse_append(
                         len(self._sparse_map) + len(sparse_append),
                         self._wide_mask_width)
                    else:
                        self._sparse_map = np.appendself._sparse_mapsparse_append

    def set_bits_pix(self, pixels, bits, nest=True):
        """
        Set bits of a wide_mask map.

        Parameters
        ----------
        pixels : `np.ndarray`
           Integer array of sparse_map pixel values
        bits : `list`
           List of bits to set
        """
        if not self._is_wide_mask:
            raise NotImplementedError('Can only use set_bits_pix on wide_mask map')
        if np.max(bits) >= self._wide_mask_maxbits:
            raise ValueError('Bit position %d too large (>= %d)' % (np.max(bits),
             self._wide_mask_maxbits))
        values = self.get_values_pix(pixels, nest=nest)
        for bit in bits:
            field, bitval = _get_field_and_bitval(bit)
            values[:, field] |= bitval

        self.update_values_pix(pixels, values, nest=nest)

    def clear_bits_pix(self, pixels, bits, nest=True):
        """
        Clear bits of a wide_mask map.

        Parameters
        ----------
        pixels : `np.ndarray`
           Integer array of sparse_map pixel values
        bits : `list`
           List of bits to clear
        """
        if not self._is_wide_mask:
            raise NotImplementedError('Can only use set_bits_pix on wide_mask map')
        if np.max(bits) >= self._wide_mask_maxbits:
            raise ValueError('Bit position %d too large (>= %d)' % (np.max(bits),
             self._wide_mask_maxbits))
        values = self.get_values_pix(pixels, nest=nest)
        for bit in bits:
            field, bitval = _get_field_and_bitval(bit)
            values[:, field] &= ~bitval

        self.update_values_pix(pixels, values, nest=nest)

    def get_values_pos(self, theta_or_ra, phi_or_dec, lonlat=False, valid_mask=False):
        """
        Get the map value for the position.  Positions may be theta/phi
        co-latitude and longitude in radians, or longitude and latitude in
        degrees.

        Parameters
        ----------
        theta_or_ra, phi_or_dec : float, array-like
           Angular coordinates of points on a sphere.
        lonlat : `bool`, optional
           If True, input angles are longitude and latitude in degrees.
           Otherwise, they are co-latitude and longitude in radians.
        valid_mask : `bool`, optional
           Return mask of True/False instead of values

        Returns
        -------
        values : `np.ndarray`
           Array of values/validity from the map.
        """
        return self.get_values_pix(hp.ang2pix((self._nside_sparse), theta_or_ra, phi_or_dec, lonlat=lonlat,
          nest=True),
          valid_mask=valid_mask)

    def get_values_pix(self, pixels, nest=True, valid_mask=False):
        """
        Get the map value for a set of pixelx.

        Parameters
        ----------
        pixel : `np.array`
           Integer array of healpix pixels.
        nest : `bool`, optional
           Are the pixels in nest scheme?  Default is True.
        valid_mask : `bool`, optional
           Return mask of True/False instead of values

        Returns
        -------
        values : `np.array`
           Array of values/validity from the map.
        """
        if not nest:
            _pix = hp.ring2nestself._nside_sparsepixels
        else:
            _pix = pixels
        ipnest_cov = np.right_shift_pixself._bit_shift
        if self._is_wide_mask:
            values = self._sparse_map[_pix + self._cov_index_map[ipnest_cov], :]
        else:
            values = self._sparse_map[(_pix + self._cov_index_map[ipnest_cov])]
        if valid_mask:
            if self._is_rec_array:
                return values[self._primary] > self._sentinel
            if self._is_wide_mask:
                return (values > 0).sum(axis=1, dtype=(np.bool))
            return values > self._sentinel
        else:
            return values

    def check_bits_pos(self, theta_or_ra, phi_or_dec, bits, lonlat=False):
        """
        Check the bits at the map for an array of positions.  Positions may be
        theta/phi co-latitude and longitude in radians, or longitude and
        latitude in degrees.

        Parameters
        ----------
        theta_or_ra, phi_or_dec : float, array-like
           Angular coordinates of points on a sphere.
        lonlat : `bool`, optional
           If True, input angles are longitude and latitude in degrees.
           Otherwise, they are co-latitude and longitude in radians.
        bits : `list`
           List of bits to check

        Returns
        -------
        bit_flags : `np.ndarray`
           Array of `np.bool` flags on whether any of the input bits were
           set
        """
        return self.check_bits_pixhp.ang2pix((self._nside_sparse), theta_or_ra,
          phi_or_dec, lonlat=lonlat,
          nest=True)bits

    def check_bits_pix(self, pixels, bits, nest=True):
        """
        Check the bits at the map for a set of pixels.

        Parameters
        ----------
        pixel : `np.array`
           Integer array of healpix pixels.
        nest : `bool`, optional
           Are the pixels in nest scheme?  Default is True.
        bits : `list`
           List of bits to check

        Returns
        -------
        bit_flags : `np.ndarray`
           Array of `np.bool` flags on whether any of the input bits were
           set
        """
        values = self.get_values_pix(pixels, nest=nest)
        bit_flags = None
        for bit in bits:
            field, bitval = _get_field_and_bitval(bit)
            if bit_flags is None:
                bit_flags = values[:, field] & bitval > 0
            else:
                bit_flags |= values[:, field] & bitval > 0

        return bit_flags

    @property
    def dtype(self):
        """
        get the dtype of the map
        """
        return self._sparse_map.dtype

    @property
    def coverage_map(self):
        """
        Get the fractional area covered by the sparse map
        in the resolution of the coverage map

        Returns
        -------
        cov_map : `np.array`
           Float array of fractional coverage of each pixel
        """
        cov_map = np.zeros_like((self.coverage_mask), dtype=(np.double))
        cov_mask = self.coverage_mask
        npop_pix = np.count_nonzero(cov_mask)
        if self._is_rec_array:
            spMap_T = self._sparse_map[self._primary].reshape((npop_pix + 1, -1))
        else:
            spMap_T = self._sparse_map.reshape((npop_pix + 1, -1))
        counts = np.sum((spMap_T > self._sentinel), axis=1).astype(np.double)
        cov_map[cov_mask] = counts[1:] / 2 ** self._bit_shift
        return cov_map

    @property
    def coverage_mask(self):
        """
        Get the boolean mask of the coverage map.

        Returns
        -------
        cov_mask : `np.array`
           Boolean array of coverage mask.
        """
        nfine = 2 ** self._bit_shift
        cov_mask = self._cov_index_map[:] + np.arange(hp.nside2npix(self._nside_coverage)) * nfine >= nfine
        return cov_mask

    @property
    def nside_coverage(self):
        """
        Get the nside of the coverage map

        Returns
        -------
        nside_coverage : `int`
        """
        return self._nside_coverage

    @property
    def nside_sparse(self):
        """
        Get the nside of the sparse map

        Returns
        -------
        nside_sparse : `int`
        """
        return self._nside_sparse

    @property
    def primary(self):
        """
        Get the primary field

        Returns
        -------
        primary : `str`
        """
        return self._primary

    @property
    def is_integer_map(self):
        """
        Check that the map is an integer map

        Returns
        -------
        is_integer_map : `bool`
        """
        if self._is_rec_array:
            return False
        return issubclass(self._sparse_map.dtype.type, np.integer)

    @property
    def is_unsigned_map(self):
        """
        Check that the map is an unsigned integer map

        Returns
        -------
        is_unsigned_map : `bool`
        """
        if self._is_rec_array:
            return False
        return issubclass(self._sparse_map.dtype.type, np.unsignedinteger)

    @property
    def is_wide_mask_map(self):
        """
        Check that the map is a wide mask

        Returns
        -------
        is_wide_mask_map : `bool`
        """
        return self._is_wide_mask

    @property
    def wide_mask_width(self):
        """
        Get the width of the wide mask

        Returns
        -------
        wide_mask_width : `int`
           Width of wide mask array.  0 if not wide mask.
        """
        return self._wide_mask_width

    @property
    def wide_mask_maxbits(self):
        """
        Get the maximum number of bits stored in the wide mask.

        Returns
        -------
        wide_mask_maxbits : `int`
           Maximum number of bits.  0 if not wide mask.
        """
        if self._is_wide_mask:
            return self._wide_mask_maxbits
        return 0

    @property
    def is_rec_array(self):
        """
        Check that the map is a recArray map.

        Returns
        -------
        is_rec_array : `bool`
        """
        return self._is_rec_array

    @property
    def metadata(self):
        """
        Return the metadata dict.

        Returns
        -------
        metadata : `dict`
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Set the metadata dict.

        This ensures that the keys conform to FITS standard (<=8 char string,
        all caps.)

        Parameters
        ----------
        metadata : `dict`
        """
        if metadata is None:
            self._metadata = metadata
        else:
            if not isinstance(metadata, dict):
                try:
                    metadata = dict(metadata)
                except ValueError:
                    raise ValueError('Could not convert metadata to dict')

            for key in metadata:
                if not isinstance(key, str):
                    raise ValueError('metadata key %s must be a string' % str(key))
                if not key.isupper():
                    raise ValueError('metadata key %s must be all upper case' % key)

            self._metadata = metadata

    def generate_healpix_map(self, nside=None, reduction='mean', key=None):
        """
        Generate the associated healpix map

        if nside is specified, then reduce to that nside

        Args:
        -----
        nside : `int`
            Output nside resolution parameter (should be a multiple of 2). If
            not specified the output resolution will be equal to the parent's
            sparsemap nside_sparse
        reduction : `str`
            If a change in resolution is requested, this controls the method to
            reduce the map computing the mean, median, std, max or min of the
            neighboring pixels to compute the "degraded" map.
        key : `str`
            If the parent HealSparseMap contains recarrays, key selects the
            field that will be transformed into a HEALPix map.

        Returns :
        --------
        hp_map : `np.array`
            Output HEALPix map with the requested resolution.
        """
        if nside is None:
            nside = self._nside_sparse
        elif self._is_rec_array:
            if key is None:
                raise ValueError('key should be specified for HealSparseMaps including `recarray`')
            else:
                single_map = self.get_single(key, copy=True)
        elif self._is_wide_mask:
            raise NotImplementedError('Cannot make healpix map out of wide_mask')
        else:
            single_map = self
        if nside < self._nside_sparse:
            single_map = single_map.degrade(nside, reduction=reduction)
        else:
            if nside > self._nside_sparse:
                raise ValueError('Cannot generate HEALPix map with higher resolution than the original.')
            elif issubclass(single_map._sparse_map.dtype.type, np.integer):
                dtypeOut = np.float64
            else:
                dtypeOut = single_map._sparse_map.dtype
            hp_map = np.zeros((hp.nside2npix(nside)), dtype=dtypeOut) + hp.UNSEEN
            valid_pixels = single_map.valid_pixels
            hp_map[valid_pixels] = single_map.get_values_pix(valid_pixels)
            return hp_map

    @property
    def valid_pixels(self):
        """
        Get an array of valid pixels in the sparse map.

        Returns
        -------
        valid_pixels : `np.array`
        """
        valid_coverage, = np.where(self.coverage_mask)
        nfine_per_cov = 2 ** self._bit_shift
        pixBase = np.left_shiftvalid_coverageself._bit_shift
        valid_pixels = np.tilenp.arange(nfine_per_cov)valid_coverage.size + np.repeatpixBasenfine_per_cov
        return valid_pixels[self.get_values_pix(valid_pixels, valid_mask=True)]

    def valid_pixels_pos(self, lonlat=False, return_pixels=False):
        """
        Get an array with the position of valid pixels in the sparse map.

        Parameters
        ----------
        lonlat: `bool`, optional
            If True, input angles are longitude and latitude in degrees.
            Otherwise, they are co-latitude and longitude in radians.
        return_pixels: `bool`, optional
            If true, return valid_pixels / co-lat / co-lon or
            valid_pixels / lat / lon instead of lat / lon

        Returns
        -------
        positions : `tuple`
            By default it will return a tuple of the form (`theta`, `phi`) in radians
            unless `lonlat = True`, for which it will return (`ra`, `dec`) in degrees.
            If `return_pixels = True`, valid_pixels will be returned as first element
            in tuple.
        """
        if return_pixels:
            valid_pixels = self.valid_pixels
            lon, lat = hp.pix2ang((self.nside_sparse), valid_pixels, lonlat=lonlat, nest=True)
            return (valid_pixels, lon, lat)
        return hp.pix2ang((self.nside_sparse), (self.valid_pixels), lonlat=lonlat, nest=True)

    def degrade(self, nside_out, reduction='mean'):
        """
        Reduce the resolution, i.e., increase the pixel size
        of a given sparse map.

        Parameters
        ----------
        nside_out : `int`
           Output Nside resolution parameter.
        reduction : `str`
           Reduction method (mean, median, std, max, min).

        Returns
        -------
        healSparseMap : `HealSparseMap`
           New map, at the desired resolution.
        """
        if self._nside_sparse < nside_out:
            raise ValueError('nside_out should be smaller than nside for the sparse_map')
        else:
            if self._is_wide_mask:
                raise NotImplementedError('Cannot degrade a wide_mask map')
            else:
                npop_pix = np.count_nonzero(self.coverage_mask)
                bit_shift = 2 * int(np.round(np.log(nside_out / self._nside_coverage) / np.log(2)))
                nfine_per_cov = 2 ** bit_shift
                if self._is_rec_array:
                    dtype = []
                    for key, value in self._sparse_map.dtype.fields.items():
                        if issubclass(self._sparse_map[key].dtype.type, np.integer):
                            dtype.append((key, np.float64))
                        else:
                            dtype.append((key, value[0]))

                    new_sparse_map = np.zeros(((npop_pix + 1) * nfine_per_cov), dtype=dtype)
                    for key, value in new_sparse_map.dtype.fields.items():
                        aux = self._sparse_map[key].astype(np.float64)
                        aux[self._sparse_map[self._primary] == self._sentinel] = np.nan
                        aux = aux.reshape((npop_pix + 1, (nside_out // self._nside_coverage) ** 2, -1))
                        aux = reduce_array(aux, reduction=reduction)
                        aux[np.isnan(aux)] = hp.UNSEEN
                        new_sparse_map[key] = aux

                else:
                    if issubclass(self._sparse_map.dtype.type, np.integer):
                        aux_dtype = np.float64
                    else:
                        aux_dtype = self._sparse_map.dtype
            aux = self._sparse_map.astype(aux_dtype)
            aux[self._sparse_map == self._sentinel] = np.nan
            aux = aux.reshape((npop_pix + 1, (nside_out // self._nside_coverage) ** 2, -1))
            aux = reduce_array(aux, reduction=reduction)
            aux[np.isnan(aux)] = hp.UNSEEN
            new_sparse_map = aux
        new_index_map = np.zeros((hp.nside2npix(self._nside_coverage)), dtype=(np.int64))
        new_index_map[self.coverage_mask] = np.arange1(npop_pix + 1) * nfine_per_cov
        new_index_map[:] -= np.arange((hp.nside2npix(self._nside_coverage)), dtype=(np.int64)) * nfine_per_cov
        return HealSparseMap(cov_index_map=new_index_map, sparse_map=new_sparse_map, nside_coverage=(self._nside_coverage),
          nside_sparse=nside_out,
          primary=(self._primary),
          sentinel=(hp.UNSEEN))

    def apply_mask(self, mask_map, mask_bits=None, mask_bit_arr=None, in_place=True):
        """
        Apply an integer mask to the map.  All pixels in the integer
        mask that have any bits in mask_bits set will be zeroed in the
        output map.  The default is that this operation will be done
        in place, but it may be set to return a copy with a masked map.

        Parameters
        ----------
        mask_map : `HealSparseMap`
           Integer mask to apply to the map.
        mask_bits : `int`, optional
           Bits to be treated as bad in the mask_map.
           Default is None (all non-zero pixels are masked)
        mask_bit_arr : `list` or `np.ndarray`, optional
           Array of bit values, used if mask_map is a wide_mask_map.
        in_place : `bool`, optional
           Apply operation in place.  Default is True

        Returns
        -------
        masked_map : `HealSparseMap`
           self if in_place is True, a new copy otherwise
        """
        if not mask_map.is_integer_map:
            raise RuntimeError('Can only apply a mask_map that is an integer map.')
        elif mask_bits is not None:
            if mask_map.is_wide_mask_map:
                raise RuntimeError('Cannot use mask_bits with wide_mask_map')
            else:
                valid_pixels = self.valid_pixels
                if mask_bits is None:
                    if mask_map.is_wide_mask_map:
                        if mask_bit_arr is None:
                            bad_pixels, = np.where(mask_map.get_values_pix(valid_pixels).sum(axis=1) > 0)
                        else:
                            mask_values = mask_map.get_values_pix(valid_pixels)
                            bad_pixel_flag = None
                            for bit in mask_bit_arr:
                                field, bitval = _get_field_and_bitval(bit)
                                if bad_pixel_flag is None:
                                    bad_pixel_flag = mask_values[:, field] & bitval > 0
                                else:
                                    bad_pixel_flag |= mask_values[:, field] & bitval > 0

                            bad_pixels, = np.where(bad_pixel_flag)
                    else:
                        bad_pixels, = np.where(mask_map.get_values_pix(valid_pixels) > 0)
                else:
                    bad_pixels, = np.where(mask_map.get_values_pix(valid_pixels) & mask_bits > 0)
                if in_place:
                    new_map = self
                else:
                    new_map = HealSparseMap(cov_index_map=(self._cov_index_map.copy()), sparse_map=(self._sparse_map.copy()),
                      nside_sparse=(self._nside_sparse),
                      primary=(self._primary),
                      sentinel=(self._sentinel))
                if new_map.is_wide_mask_map:
                    new_values = np.zeros((bad_pixels.size, new_map._wide_mask_width), dtype=(new_map._sparse_map.dtype))
                else:
                    new_values = np.zeros((bad_pixels.size), dtype=(new_map._sparse_map.dtype))
            if self.is_rec_array:
                new_values[new_map._primary] = new_map._sentinel
        else:
            new_values[:] = new_map._sentinel
        new_map.update_values_pixvalid_pixels[bad_pixels]new_values
        return new_map

    def __getitem__(self, key):
        """
        Get part of a healpix map.
        """
        if isinstance(key, str):
            if not self._is_rec_array:
                raise IndexError('HealSparseMap is not a recarray map, cannot use string index.')
            return self.get_single(key, sentinel=None)
            if isinstance(key, int):
                return self.get_values_pix(np.array([key]))[0]
            if isinstance(key, slice):
                start = key.start if key.start is not None else 0
                stop = key.stop if key.stop is not None else hp.nside2npix(self._nside_sparse)
                step = key.step if key.step is not None else 1
                return self.get_values_pix(np.arangestartstopstep)
            if isinstance(key, np.ndarray):
                if not is_integer_value(key[0]):
                    raise IndexError('Numpy array indices must be integers for __getitem__')
        else:
            return self.get_values_pix(key)
        if isinstance(key, list):
            arr = np.array(key)
            if not is_integer_value(arr[0]):
                raise IndexError('List array indices must be integers for __getitem__')
            return self.get_values_pix(arr)
        raise IndexError('Illegal index type (%s) for __getitem__ in HealSparseMap.' % key.__class__)

    def __setitem__(self, key, value):
        """
        Set part of a healpix map
        """
        if isinstance(key, int):
            return self.update_values_pixnp.array([key])np.array([value])
            if isinstance(key, slice):
                start = key.start if key.start is not None else 0
                stop = key.stop if key.stop is not None else hp.nside2npix(self._nside_sparse)
                step = key.step if key.step is not None else 1
                return self.update_values_pixnp.arangestartstopstepvalue
            if isinstance(key, np.ndarray):
                if not is_integer_value(key[0]):
                    raise IndexError('Numpy array indices must be integers for __setitem__')
        else:
            return self.update_values_pixkeyvalue
        if isinstance(key, list):
            arr = np.array(key)
            if not is_integer_value(arr[0]):
                raise IndexError('List/Tuple array indices must be integers for __setitem__')
            return self.update_values_pixarrvalue
        raise IndexError('Illegal index type (%s) for __setitem__ in HealSparseMap.' % key.__class__)

    def get_single(self, key, sentinel=None, copy=False):
        """
        Get a single healpix map out of a recarray map, with the ability to
        override a sentinel value.

        Parameters
        ----------
        key : `str`
           Field for the recarray
        sentinel : `int` or `float` or None, optional
           Override the default sentinel value.  Default is None (use default)
        """
        if not self._is_rec_array:
            raise TypeError('HealSparseMap is not a recarray map')
        else:
            return copy or HealSparseMap(cov_index_map=(self._cov_index_map), sparse_map=(self._sparse_map[key]),
              nside_sparse=(self._nside_sparse),
              sentinel=(self._sentinel))
        _sentinel = check_sentinel(self._sparse_map[key].dtype.type, sentinel)
        new_sparse_map = np.zeros_like(self._sparse_map[key]) + _sentinel
        valid_indices = self._sparse_map[self._primary] > self._sentinel
        new_sparse_map[valid_indices] = self._sparse_map[key][valid_indices]
        return HealSparseMap(cov_index_map=(self._cov_index_map), sparse_map=new_sparse_map, nside_sparse=(self._nside_sparse),
          sentinel=_sentinel)

    def __add__(self, other):
        """
        Add a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operationothernp.add

    def __iadd__(self, other):
        """
        Add a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.add), in_place=True)

    def __sub__(self, other):
        """
        Subtract a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operationothernp.subtract

    def __isub__(self, other):
        """
        Subtract a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.subtract), in_place=True)

    def __mul__(self, other):
        """
        Multiply a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operationothernp.multiply

    def __imul__(self, other):
        """
        Multiply a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.multiply), in_place=True)

    def __truediv__(self, other):
        """
        Divide a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operationothernp.divide

    def __itruediv__(self, other):
        """
        Divide a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.divide), in_place=True)

    def __pow__(self, other):
        """
        Raise the map to a power.

        Cannot be used with recarray maps.
        """
        return self._apply_operationothernp.power

    def __ipow__(self, other):
        """
        Divide a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.power), in_place=True)

    def __and__(self, other):
        """
        Perform a bitwise and with a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_and), int_only=True)

    def __iand__(self, other):
        """
        Perform a bitwise and with a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_and), int_only=True, in_place=True)

    def __xor__(self, other):
        """
        Perform a bitwise xor with a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_xor), int_only=True)

    def __ixor__(self, other):
        """
        Perform a bitwise xor with a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_xor), int_only=True, in_place=True)

    def __or__(self, other):
        """
        Perform a bitwise or with a constant.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_or), int_only=True)

    def __ior__(self, other):
        """
        Perform a bitwise or with a constant, in place.

        Cannot be used with recarray maps.
        """
        return self._apply_operation(other, (np.bitwise_or), int_only=True, in_place=True)

    def _apply_operation(self, other, func, int_only=False, in_place=False):
        """
        Apply a generic arithmetic function.

        Cannot be used with recarray maps.

        Parameters
        ----------
        other : `int` or `float` (or numpy equivalents)
           The other item to perform the operator on.
        func : `np.ufunc`
           The numpy universal function to apply.
        int_only : `bool`, optional
           Only accept integer types.  Default is False.
        in_place : `bool`, optional
           Perform operation in-place.  Default is False.

        Returns
        -------
        result : `HealSparseMap`
           Resulting map
        """
        name = func.__str__()
        if self._is_rec_array:
            raise NotImplementedError('Cannot use %s with recarray maps' % name)
        elif int_only and not self.is_integer_map:
            raise NotImplementedError('Can only apply %s to integer maps' % name)
        else:
            if self._is_wide_mask:
                raise NotImplementedError('Cannot use %s with wide mask maps' % name)
        other_int = False
        other_float = False
        other_bits = False
        if isinstance(other, numbers.Integral):
            other_int = True
        else:
            if isinstance(other, numbers.Real):
                other_float = True
            else:
                if isinstance(other, (tuple, list)):
                    if not self._is_wide_mask:
                        raise NotImplementedError('Must use a wide mask to operate with a bit list')
                    else:
                        other_bits = True
                        for elt in other:
                            if not isinstance(elt, numbers.Integral):
                                raise NotImplementedError('Can only use an integer list of bits with %s operation' % name)

                        if np.max(other) >= self._wide_mask_maxbits:
                            raise ValueError('Bit position %d too large (>= %d)' % (np.max(other),
                             self._wide_mask_maxbits))
                        elif self._is_wide_mask:
                            if not other_bits:
                                raise NotImplementedError('Must use a bit list with the %s operation with a wide mask' % name)
                        else:
                            if not (other_int or other_float):
                                raise NotImplementedError('Can only use a constant with the %s operation' % name)
                        if not other_int:
                            if int_only:
                                raise NotImplementedError('Can only use an integer constant with the %s operation' % name)
                            if self._is_wide_mask:
                                valid_sparse_pixels = (self._sparse_map > self._sentinel).sum(axis=1, dtype=(np.bool))
                                other_value = np.zerosself._wide_mask_widthself._sparse_map.dtype
                                for bit in other:
                                    field, bitval = _get_field_and_bitval(bit)
                                    other_value[field] |= bitval

                            else:
                                valid_sparse_pixels = self._sparse_map > self._sentinel
                            if in_place:
                                if self._is_wide_mask:
                                    for i in range(self._wide_mask_width):
                                        col = self._sparse_map[:, i]
                                        func(col, (other_value[i]), out=col, where=valid_sparse_pixels)

                        else:
                            func((self._sparse_map), other, out=(self._sparse_map), where=valid_sparse_pixels)
                        return self
                    combinedSparseMap = self._sparse_map.copy()
                    if self._is_wide_mask:
                        for i in range(self._wide_mask_width):
                            col = combinedSparseMap[:, i]
                            func(col, (other_value[i]), out=col, where=valid_sparse_pixels)

                else:
                    func(combinedSparseMap, other, out=combinedSparseMap, where=valid_sparse_pixels)
                return HealSparseMap(cov_index_map=(self._cov_index_map), sparse_map=combinedSparseMap, nside_sparse=(self._nside_sparse),
                  sentinel=(self._sentinel))

    def __copy__(self):
        return HealSparseMap(cov_index_map=(self._cov_index_map.copy()), sparse_map=(self._sparse_map.copy()),
          nside_sparse=(self._nside_sparse),
          sentinel=(self._sentinel),
          primary=(self._primary))

    def copy(self):
        return self.__copy__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        descr = 'HealSparseMap: nside_coverage = %d, nside_sparse = %d' % (self._nside_coverage,
         self._nside_sparse)
        if self._is_rec_array:
            descr += ', record array type.\n'
            descr += self._sparse_map.dtype.descr.__str__()
        else:
            if self._is_wide_mask:
                descr += ', %d bit wide mask' % self._wide_mask_maxbits
            else:
                descr += ', ' + self._sparse_map.dtype.name
        return descr