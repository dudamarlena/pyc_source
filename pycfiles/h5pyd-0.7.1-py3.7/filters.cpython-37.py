# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/filters.py
# Compiled at: 2019-12-23 13:45:07
# Size of source mod 2**32: 13668 bytes
"""
    Implements support for HDF5 compression filters via the high-level
    interface.  The following types of filter are available:

    "gzip"
        Standard DEFLATE-based compression, at integer levels from 0 to 9.
        Built-in to all public versions of HDF5.  Use this if you want a
        decent-to-good ratio, good portability, and don't mind waiting.

    "lzf"
        Custom compression filter for h5py.  This filter is much, much faster
        than gzip (roughly 10x in compression vs. gzip level 4, and 3x faster
        in decompressing), but at the cost of a worse compression ratio.  Use
        this if you want cheap compression and portability is not a concern.

    "szip"
        Access to the HDF5 SZIP encoder.  SZIP is a non-mainstream compression
        format used in space science on integer and float datasets.  SZIP is
        subject to license requirements, which means the encoder is not
        guaranteed to be always available.  However, it is also much faster
        than gzip.

    The following constants in this module are also useful:

    decode
        Tuple of available filter names for decoding

    encode
        Tuple of available filter names for encoding
"""
from __future__ import absolute_import, division
import numpy as np
_COMP_FILTERS = {'gzip':'H5Z_FILTER_DEFLATE', 
 'szip':'H5Z_FILTER_SZIP', 
 'lzf':'H5Z_FILTER_LZF', 
 'shuffle':'H5Z_FILTER_SHUFFLE', 
 'fletcher32':'H5Z_FILTER_FLETCHER32', 
 'scaleoffset':'H5Z_FILTER_SCALEOFFSET'}
DEFAULT_GZIP = 4
DEFAULT_SZIP = ('nn', 8)
SO_INT_MINBITS_DEFAULT = 0

def _gen_filter_tuples():
    """ Bootstrap function to figure out what filters are available. """
    dec = []
    enc = []
    for name, code in _COMP_FILTERS.items():
        enc.append(name)
        dec.append(name)

    return (tuple(dec), tuple(enc))


decode, encode = _gen_filter_tuples()

def generate_dcpl--- This code section failed: ---

 L.  82         0  BUILD_MAP_0           0 
                2  STORE_FAST               'plist'

 L.  84         4  LOAD_DEREF               'shape'
                6  LOAD_CONST               ()
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    68  'to 68'

 L.  85        12  LOAD_GLOBAL              any
               14  LOAD_FAST                'chunks'
               16  LOAD_FAST                'compression'
               18  LOAD_FAST                'compression_opts'
               20  LOAD_FAST                'shuffle'
               22  LOAD_FAST                'fletcher32'

 L.  86        24  LOAD_FAST                'scaleoffset'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  BUILD_TUPLE_6         6 
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L.  87        36  LOAD_GLOBAL              TypeError
               38  LOAD_STR                 "Scalar datasets don't support chunk/filter options"
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'

 L.  88        44  LOAD_FAST                'maxshape'
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_FAST                'maxshape'
               50  LOAD_CONST               ()
               52  COMPARE_OP               !=
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L.  89        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 'Scalar datasets cannot be extended'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            46  '46'

 L.  90        64  LOAD_FAST                'plist'
               66  RETURN_VALUE     
             68_0  COME_FROM            10  '10'

 L.  92        68  LOAD_CLOSURE             'shape'
               70  BUILD_TUPLE_1         1 
               72  LOAD_CODE                <code_object rq_tuple>
               74  LOAD_STR                 'generate_dcpl.<locals>.rq_tuple'
               76  MAKE_FUNCTION_8          'closure'
               78  STORE_FAST               'rq_tuple'

 L. 103        80  LOAD_FAST                'rq_tuple'
               82  LOAD_FAST                'chunks'
               84  LOAD_STR                 'chunks'
               86  CALL_FUNCTION_2       2  '2 positional arguments'
               88  POP_TOP          

 L. 104        90  LOAD_FAST                'rq_tuple'
               92  LOAD_FAST                'maxshape'
               94  LOAD_STR                 'maxshape'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_TOP          

 L. 106       100  LOAD_FAST                'compression'
              102  LOAD_CONST               None
              104  COMPARE_OP               is-not
          106_108  POP_JUMP_IF_FALSE   360  'to 360'

 L. 108       110  LOAD_FAST                'compression'
              112  LOAD_GLOBAL              encode
              114  COMPARE_OP               not-in
              116  POP_JUMP_IF_FALSE   140  'to 140'
              118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'compression'
              122  LOAD_GLOBAL              int
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_JUMP_IF_TRUE    140  'to 140'

 L. 109       128  LOAD_GLOBAL              ValueError
              130  LOAD_STR                 'Compression filter "%s" is unavailable'
              132  LOAD_FAST                'compression'
              134  BINARY_MODULO    
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM           126  '126'
            140_1  COME_FROM           116  '116'

 L. 111       140  LOAD_FAST                'compression'
              142  LOAD_STR                 'gzip'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   194  'to 194'

 L. 112       148  LOAD_FAST                'compression_opts'
              150  LOAD_CONST               None
              152  COMPARE_OP               is
              154  POP_JUMP_IF_FALSE   162  'to 162'

 L. 113       156  LOAD_GLOBAL              DEFAULT_GZIP
              158  STORE_FAST               'gzip_level'
              160  JUMP_FORWARD        192  'to 192'
            162_0  COME_FROM           154  '154'

 L. 114       162  LOAD_FAST                'compression_opts'
              164  LOAD_GLOBAL              range
              166  LOAD_CONST               10
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   180  'to 180'

 L. 115       174  LOAD_FAST                'compression_opts'
              176  STORE_FAST               'gzip_level'
              178  JUMP_FORWARD        192  'to 192'
            180_0  COME_FROM           172  '172'

 L. 117       180  LOAD_GLOBAL              ValueError
              182  LOAD_STR                 'GZIP setting must be an integer from 0-9, not %r'
              184  LOAD_FAST                'compression_opts'
              186  BINARY_MODULO    
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           178  '178'
            192_1  COME_FROM           160  '160'
              192  JUMP_FORWARD        358  'to 358'
            194_0  COME_FROM           146  '146'

 L. 119       194  LOAD_FAST                'compression'
              196  LOAD_STR                 'lzf'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   220  'to 220'

 L. 120       202  LOAD_FAST                'compression_opts'
              204  LOAD_CONST               None
              206  COMPARE_OP               is-not
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L. 121       210  LOAD_GLOBAL              ValueError
              212  LOAD_STR                 'LZF compression filter accepts no options'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           208  '208'
              218  JUMP_FORWARD        358  'to 358'
            220_0  COME_FROM           200  '200'

 L. 123       220  LOAD_FAST                'compression'
              222  LOAD_STR                 'szip'
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_FALSE   378  'to 378'

 L. 124       230  LOAD_FAST                'compression_opts'
              232  LOAD_CONST               None
              234  COMPARE_OP               is
              236  POP_JUMP_IF_FALSE   242  'to 242'

 L. 125       238  LOAD_GLOBAL              DEFAULT_SZIP
              240  STORE_FAST               'compression_opts'
            242_0  COME_FROM           236  '236'

 L. 127       242  LOAD_STR                 "SZIP options must be a 2-tuple ('ec'|'nn', even integer 0-32)"
              244  STORE_FAST               'err'

 L. 128       246  SETUP_EXCEPT        260  'to 260'

 L. 129       248  LOAD_FAST                'compression_opts'
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'szmethod'
              254  STORE_FAST               'szpix'
              256  POP_BLOCK        
              258  JUMP_FORWARD        290  'to 290'
            260_0  COME_FROM_EXCEPT    246  '246'

 L. 130       260  DUP_TOP          
              262  LOAD_GLOBAL              TypeError
              264  COMPARE_OP               exception-match
          266_268  POP_JUMP_IF_FALSE   288  'to 288'
              270  POP_TOP          
              272  POP_TOP          
              274  POP_TOP          

 L. 131       276  LOAD_GLOBAL              TypeError
              278  LOAD_FAST                'err'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  RAISE_VARARGS_1       1  'exception instance'
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           266  '266'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           258  '258'

 L. 132       290  LOAD_FAST                'szmethod'
              292  LOAD_CONST               ('ec', 'nn')
              294  COMPARE_OP               not-in
          296_298  POP_JUMP_IF_FALSE   308  'to 308'

 L. 133       300  LOAD_GLOBAL              ValueError
              302  LOAD_FAST                'err'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           296  '296'

 L. 134       308  LOAD_CONST               0
              310  LOAD_FAST                'szpix'
              312  DUP_TOP          
              314  ROT_THREE        
              316  COMPARE_OP               <
          318_320  POP_JUMP_IF_FALSE   332  'to 332'
              322  LOAD_CONST               32
              324  COMPARE_OP               <=
          326_328  POP_JUMP_IF_FALSE   350  'to 350'
              330  JUMP_FORWARD        336  'to 336'
            332_0  COME_FROM           318  '318'
              332  POP_TOP          
              334  JUMP_FORWARD        350  'to 350'
            336_0  COME_FROM           330  '330'
              336  LOAD_FAST                'szpix'
              338  LOAD_CONST               2
              340  BINARY_MODULO    
              342  LOAD_CONST               0
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_TRUE    378  'to 378'
            350_0  COME_FROM           334  '334'
            350_1  COME_FROM           326  '326'

 L. 135       350  LOAD_GLOBAL              ValueError
              352  LOAD_FAST                'err'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           218  '218'
            358_1  COME_FROM           192  '192'
              358  JUMP_FORWARD        378  'to 378'
            360_0  COME_FROM           106  '106'

 L. 137       360  LOAD_FAST                'compression_opts'
              362  LOAD_CONST               None
              364  COMPARE_OP               is-not
          366_368  POP_JUMP_IF_FALSE   378  'to 378'

 L. 139       370  LOAD_GLOBAL              TypeError
              372  LOAD_STR                 'Compression method must be specified'
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           366  '366'
            378_1  COME_FROM           358  '358'
            378_2  COME_FROM           346  '346'
            378_3  COME_FROM           226  '226'

 L. 141       378  LOAD_FAST                'scaleoffset'
              380  LOAD_CONST               None
              382  COMPARE_OP               is-not
          384_386  POP_JUMP_IF_FALSE   488  'to 488'

 L. 146       388  LOAD_FAST                'scaleoffset'
              390  LOAD_CONST               0
              392  COMPARE_OP               <
          394_396  POP_JUMP_IF_FALSE   406  'to 406'

 L. 147       398  LOAD_GLOBAL              ValueError
              400  LOAD_STR                 'scale factor must be >= 0'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  RAISE_VARARGS_1       1  'exception instance'
            406_0  COME_FROM           394  '394'

 L. 149       406  LOAD_FAST                'dtype'
              408  LOAD_ATTR                kind
              410  LOAD_STR                 'f'
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   438  'to 438'

 L. 150       418  LOAD_FAST                'scaleoffset'
              420  LOAD_CONST               True
              422  COMPARE_OP               is
          424_426  POP_JUMP_IF_FALSE   474  'to 474'

 L. 151       428  LOAD_GLOBAL              ValueError
              430  LOAD_STR                 'integer scaleoffset must be provided for floating point types'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  RAISE_VARARGS_1       1  'exception instance'
              436  JUMP_FORWARD        474  'to 474'
            438_0  COME_FROM           414  '414'

 L. 153       438  LOAD_FAST                'dtype'
              440  LOAD_ATTR                kind
              442  LOAD_CONST               ('u', 'i')
              444  COMPARE_OP               in
          446_448  POP_JUMP_IF_FALSE   466  'to 466'

 L. 154       450  LOAD_FAST                'scaleoffset'
              452  LOAD_CONST               True
              454  COMPARE_OP               is
          456_458  POP_JUMP_IF_FALSE   474  'to 474'

 L. 155       460  LOAD_GLOBAL              SO_INT_MINBITS_DEFAULT
              462  STORE_FAST               'scaleoffset'
              464  JUMP_FORWARD        474  'to 474'
            466_0  COME_FROM           446  '446'

 L. 157       466  LOAD_GLOBAL              TypeError
              468  LOAD_STR                 'scale/offset filter only supported for integer and floating-point types'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  RAISE_VARARGS_1       1  'exception instance'
            474_0  COME_FROM           464  '464'
            474_1  COME_FROM           456  '456'
            474_2  COME_FROM           436  '436'
            474_3  COME_FROM           424  '424'

 L. 164       474  LOAD_FAST                'fletcher32'
          476_478  POP_JUMP_IF_FALSE   488  'to 488'

 L. 165       480  LOAD_GLOBAL              ValueError
              482  LOAD_STR                 'fletcher32 cannot be used with potentially lossy scale/offset filter'
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  RAISE_VARARGS_1       1  'exception instance'
            488_0  COME_FROM           476  '476'
            488_1  COME_FROM           384  '384'

 L. 169       488  LOAD_FAST                'chunks'
              490  LOAD_CONST               True
              492  COMPARE_OP               is
          494_496  POP_JUMP_IF_TRUE    542  'to 542'

 L. 170       498  LOAD_FAST                'chunks'
              500  LOAD_CONST               None
              502  COMPARE_OP               is
          504_506  POP_JUMP_IF_FALSE   556  'to 556'
              508  LOAD_FAST                'layout'
              510  LOAD_CONST               None
              512  COMPARE_OP               is-not
          514_516  POP_JUMP_IF_FALSE   556  'to 556'
              518  LOAD_GLOBAL              any
              520  LOAD_FAST                'shuffle'
              522  LOAD_FAST                'fletcher32'
              524  LOAD_FAST                'compression'
              526  LOAD_FAST                'maxshape'

 L. 171       528  LOAD_FAST                'scaleoffset'
              530  LOAD_CONST               None
              532  COMPARE_OP               is-not
              534  BUILD_TUPLE_5         5 
              536  CALL_FUNCTION_1       1  '1 positional argument'
          538_540  POP_JUMP_IF_FALSE   556  'to 556'
            542_0  COME_FROM           494  '494'

 L. 172       542  LOAD_GLOBAL              guess_chunk
              544  LOAD_DEREF               'shape'
              546  LOAD_FAST                'maxshape'
              548  LOAD_FAST                'dtype'
              550  LOAD_ATTR                itemsize
              552  CALL_FUNCTION_3       3  '3 positional arguments'
              554  STORE_FAST               'chunks'
            556_0  COME_FROM           538  '538'
            556_1  COME_FROM           514  '514'
            556_2  COME_FROM           504  '504'

 L. 174       556  LOAD_FAST                'maxshape'
              558  LOAD_CONST               True
              560  COMPARE_OP               is
          562_564  POP_JUMP_IF_FALSE   578  'to 578'

 L. 175       566  LOAD_CONST               (None,)
              568  LOAD_GLOBAL              len
              570  LOAD_DEREF               'shape'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  BINARY_MULTIPLY  
              576  STORE_FAST               'maxshape'
            578_0  COME_FROM           562  '562'

 L. 177       578  LOAD_FAST                'layout'
              580  LOAD_CONST               None
              582  COMPARE_OP               is-not
          584_586  POP_JUMP_IF_FALSE   598  'to 598'

 L. 178       588  LOAD_FAST                'layout'
              590  LOAD_FAST                'plist'
              592  LOAD_STR                 'layout'
              594  STORE_SUBSCR     
              596  JUMP_FORWARD        640  'to 640'
            598_0  COME_FROM           584  '584'

 L. 179       598  LOAD_FAST                'chunks'
              600  LOAD_CONST               None
              602  COMPARE_OP               is-not
          604_606  POP_JUMP_IF_FALSE   640  'to 640'

 L. 182       608  LOAD_STR                 'class'
              610  LOAD_STR                 'H5D_CHUNKED'
              612  BUILD_MAP_1           1 
              614  STORE_FAST               'layout'

 L. 183       616  LOAD_FAST                'chunks'
              618  LOAD_FAST                'layout'
              620  LOAD_STR                 'dims'
              622  STORE_SUBSCR     

 L. 184       624  LOAD_FAST                'layout'
              626  LOAD_FAST                'plist'
              628  LOAD_STR                 'layout'
              630  STORE_SUBSCR     

 L. 185       632  LOAD_STR                 'H5D_FILL_TIME_ALLOC'
              634  LOAD_FAST                'plist'
              636  LOAD_STR                 'fillTime'
              638  STORE_SUBSCR     
            640_0  COME_FROM           604  '604'
            640_1  COME_FROM           596  '596'

 L. 187       640  BUILD_LIST_0          0 
              642  STORE_FAST               'filters'

 L. 189       644  LOAD_FAST                'fletcher32'
          646_648  POP_JUMP_IF_FALSE   676  'to 676'

 L. 190       650  LOAD_STR                 'class'
              652  LOAD_STR                 'H5Z_FLETCHER_DEFLATE'
              654  BUILD_MAP_1           1 
              656  STORE_FAST               'filter_fletcher32'

 L. 191       658  LOAD_CONST               3
              660  LOAD_FAST                'filter_fletcher32'
              662  LOAD_STR                 'id'
              664  STORE_SUBSCR     

 L. 192       666  LOAD_FAST                'filters'
              668  LOAD_METHOD              append
              670  LOAD_FAST                'filter_fletcher32'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  POP_TOP          
            676_0  COME_FROM           646  '646'

 L. 195       676  LOAD_FAST                'scaleoffset'
              678  LOAD_CONST               None
              680  COMPARE_OP               is-not
          682_684  POP_JUMP_IF_FALSE   750  'to 750'

 L. 196       686  LOAD_STR                 'class'
              688  LOAD_STR                 'H5Z_FILTER_SCALEOFFSET'
              690  BUILD_MAP_1           1 
              692  STORE_FAST               'filter_scaleoffset'

 L. 197       694  LOAD_CONST               6
              696  LOAD_FAST                'filter_scaleoffset'
              698  LOAD_STR                 'id'
              700  STORE_SUBSCR     

 L. 198       702  LOAD_FAST                'scaleoffset'
              704  LOAD_FAST                'filter_scaleoffset'
              706  LOAD_STR                 'scaleOffset'
              708  STORE_SUBSCR     

 L. 199       710  LOAD_FAST                'dtype'
              712  LOAD_ATTR                kind
              714  LOAD_CONST               ('u', 'i')
              716  COMPARE_OP               in
          718_720  POP_JUMP_IF_FALSE   732  'to 732'

 L. 201       722  LOAD_STR                 'H5Z_SO_INT'
              724  LOAD_FAST                'filter_scaleoffset'
              726  LOAD_STR                 'scaleType'
              728  STORE_SUBSCR     
              730  JUMP_FORWARD        740  'to 740'
            732_0  COME_FROM           718  '718'

 L. 204       732  LOAD_STR                 'H5Z_SO_FLOAT_DSCALE'
              734  LOAD_FAST                'filter_scaleoffset'
              736  LOAD_STR                 'scaleType'
              738  STORE_SUBSCR     
            740_0  COME_FROM           730  '730'

 L. 205       740  LOAD_FAST                'filters'
              742  LOAD_METHOD              append
              744  LOAD_FAST                'filter_scaleoffset'
              746  CALL_METHOD_1         1  '1 positional argument'
              748  POP_TOP          
            750_0  COME_FROM           682  '682'

 L. 207       750  LOAD_FAST                'shuffle'
          752_754  POP_JUMP_IF_FALSE   782  'to 782'

 L. 208       756  LOAD_STR                 'class'
              758  LOAD_STR                 'H5Z_FILTER_SHUFFLE'
              760  BUILD_MAP_1           1 
              762  STORE_FAST               'filter_shuffle'

 L. 209       764  LOAD_CONST               2
              766  LOAD_FAST                'filter_shuffle'
              768  LOAD_STR                 'id'
              770  STORE_SUBSCR     

 L. 210       772  LOAD_FAST                'filters'
              774  LOAD_METHOD              append
              776  LOAD_FAST                'filter_shuffle'
              778  CALL_METHOD_1         1  '1 positional argument'
              780  POP_TOP          
            782_0  COME_FROM           752  '752'

 L. 212       782  LOAD_FAST                'compression'
              784  LOAD_STR                 'gzip'
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   828  'to 828'

 L. 214       792  LOAD_STR                 'class'
              794  LOAD_STR                 'H5Z_FILTER_DEFLATE'
              796  BUILD_MAP_1           1 
              798  STORE_FAST               'filter_gzip'

 L. 215       800  LOAD_CONST               1
              802  LOAD_FAST                'filter_gzip'
              804  LOAD_STR                 'id'
              806  STORE_SUBSCR     

 L. 216       808  LOAD_FAST                'gzip_level'
              810  LOAD_FAST                'filter_gzip'
              812  LOAD_STR                 'level'
              814  STORE_SUBSCR     

 L. 217       816  LOAD_FAST                'filters'
              818  LOAD_METHOD              append
              820  LOAD_FAST                'filter_gzip'
              822  CALL_METHOD_1         1  '1 positional argument'
              824  POP_TOP          
              826  JUMP_FORWARD        984  'to 984'
            828_0  COME_FROM           788  '788'

 L. 218       828  LOAD_FAST                'compression'
              830  LOAD_STR                 'lzf'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   866  'to 866'

 L. 220       838  LOAD_STR                 'class'
              840  LOAD_STR                 'H5Z_FILTER_LZF'
              842  BUILD_MAP_1           1 
              844  STORE_FAST               'filter_lzf'

 L. 221       846  LOAD_CONST               32000
              848  LOAD_FAST                'filter_lzf'
              850  LOAD_STR                 'id'
              852  STORE_SUBSCR     

 L. 222       854  LOAD_FAST                'filters'
              856  LOAD_METHOD              append
              858  LOAD_FAST                'filter_lzf'
              860  CALL_METHOD_1         1  '1 positional argument'
              862  POP_TOP          
              864  JUMP_FORWARD        984  'to 984'
            866_0  COME_FROM           834  '834'

 L. 224       866  LOAD_FAST                'compression'
              868  LOAD_STR                 'szip'
              870  COMPARE_OP               ==
          872_874  POP_JUMP_IF_FALSE   958  'to 958'

 L. 225       876  LOAD_STR                 'H5Z_SZIP_EC_OPTION_MASK'
              878  LOAD_STR                 'H5Z_SZIP_NN_OPTION_MASK'
              880  LOAD_CONST               ('ec', 'nn')
              882  BUILD_CONST_KEY_MAP_2     2 
              884  STORE_FAST               'opts'

 L. 227       886  LOAD_STR                 'class'
              888  LOAD_STR                 'H5Z_FILTER_SZIP'
              890  BUILD_MAP_1           1 
              892  STORE_FAST               'filter_szip'

 L. 228       894  LOAD_CONST               4
              896  LOAD_FAST                'filter_szip'
              898  LOAD_STR                 'id'
              900  STORE_SUBSCR     

 L. 229       902  LOAD_FAST                'opts'
              904  LOAD_FAST                'filter_szip'
              906  LOAD_STR                 'coding'
              908  STORE_SUBSCR     

 L. 230       910  LOAD_FAST                'szmethod'
              912  LOAD_STR                 'ec'
              914  COMPARE_OP               ==
          916_918  POP_JUMP_IF_FALSE   930  'to 930'

 L. 231       920  LOAD_STR                 'H5_SZIP_EC_OPTION_MASK'
              922  LOAD_FAST                'filter_szip'
              924  LOAD_STR                 'coding'
              926  STORE_SUBSCR     
              928  JUMP_FORWARD        938  'to 938'
            930_0  COME_FROM           916  '916'

 L. 233       930  LOAD_STR                 'H5_SZIP_NN_OPTION_MASK'
              932  LOAD_FAST                'filter_szip'
              934  LOAD_STR                 'coding'
              936  STORE_SUBSCR     
            938_0  COME_FROM           928  '928'

 L. 234       938  LOAD_FAST                'szpix'
              940  LOAD_FAST                'filter_szip'
              942  LOAD_STR                 'bitsPerPixel'
              944  STORE_SUBSCR     

 L. 235       946  LOAD_FAST                'filters'
              948  LOAD_METHOD              append
              950  LOAD_FAST                'filter_szip'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  POP_TOP          
              956  JUMP_FORWARD        984  'to 984'
            958_0  COME_FROM           872  '872'

 L. 237       958  LOAD_GLOBAL              isinstance
              960  LOAD_FAST                'compression'
              962  LOAD_GLOBAL              int
              964  CALL_FUNCTION_2       2  '2 positional arguments'
          966_968  POP_JUMP_IF_FALSE   984  'to 984'

 L. 240       970  LOAD_GLOBAL              ValueError
              972  LOAD_STR                 'Unsupported compression filter: {}'
              974  LOAD_METHOD              format
              976  LOAD_FAST                'compression'
              978  CALL_METHOD_1         1  '1 positional argument'
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  RAISE_VARARGS_1       1  'exception instance'
            984_0  COME_FROM           966  '966'
            984_1  COME_FROM           956  '956'
            984_2  COME_FROM           864  '864'
            984_3  COME_FROM           826  '826'

 L. 251       984  LOAD_GLOBAL              len
              986  LOAD_FAST                'filters'
              988  CALL_FUNCTION_1       1  '1 positional argument'
              990  LOAD_CONST               0
              992  COMPARE_OP               >
          994_996  POP_JUMP_IF_FALSE  1006  'to 1006'

 L. 252       998  LOAD_FAST                'filters'
             1000  LOAD_FAST                'plist'
             1002  LOAD_STR                 'filters'
             1004  STORE_SUBSCR     
           1006_0  COME_FROM           994  '994'

 L. 254      1006  LOAD_FAST                'plist'
             1008  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 358_0


def get_filters(plist):
    """ Extract a dictionary of active filters from a DCPL, along with
    their settings.

    Undocumented and subject to change without warning.
    """
    filter_names = {'H5Z_FILTER_DEFLATE':'gzip', 
     'H5Z_FILTER_SZIP':'szip', 
     'H5Z_FILTER_SHUFFLE':'shuffle', 
     'H5Z_FILTER_FLETCHER32':'fletcher32', 
     'H5Z_FILTER_LZF':'lzf', 
     'H5Z_FILTER_SCALEOFFSET':'scaleoffset'}
    vals = None
    pipeline = {}
    if 'filters' not in plist:
        return pipeline
    filters = plist['filters']
    for filter in filters:
        if filter['class'] == 'H5Z_FILTER_DEFLATE':
            vals = filter['level']
        else:
            if filter['class'] == 'H5Z_FILTER_SZIP':
                mask = None
                if filter['coding'] == 'H5Z_SZIP_EC_OPTION_MASK':
                    mask = 'ec'
                else:
                    if filter['coding'] == 'H5Z_SZIP_NN_OPTION_MASK':
                        mask = 'nn'
                    else:
                        raise TypeError('Unknown SZIP configuration')
                pixels = filter['bitsPerPixel']
                vals = (mask, pixels)
            else:
                if filter['class'] == 'H5Z_FILTER_LZF':
                    vals = None
                else:
                    if vals:
                        if len(vals) == 0:
                            vals = None
        filter_name = 'Extension'
        if filter['class'] in filter_names:
            filter_name = filter_names[filter['class']]
        if filter['class'] in filter_names.keys():
            filter_name = filter_names[filter['class']]
            pipeline[filter_name] = vals

    return pipeline


CHUNK_BASE = 16384
CHUNK_MIN = 8192
CHUNK_MAX = 1048576

def guess_chunk(shape, maxshape, typesize):
    """ Guess an appropriate chunk layout for a dataset, given its shape and
    the size of each element in bytes.  Will allocate chunks only as large
    as MAX_SIZE.  Chunks are generally close to some power-of-2 fraction of
    each axis, slightly favoring bigger values for the last index.

    Undocumented and subject to change without warning.
    """
    shape = tuple(((x if x != 0 else 1024) for i, x in enumerate(shape)))
    ndims = len(shape)
    if ndims == 0:
        raise ValueError('Chunks not allowed for scalar datasets.')
    else:
        chunks = np.array(shape, dtype='=f8')
        if not np.all(np.isfinite(chunks)):
            raise ValueError('Illegal value in chunk tuple')
        dset_size = np.product(chunks) * typesize
        target_size = CHUNK_BASE * 2 ** np.log10(dset_size / 1048576.0)
        if target_size > CHUNK_MAX:
            target_size = CHUNK_MAX
        else:
            if target_size < CHUNK_MIN:
                target_size = CHUNK_MIN
    idx = 0
    while 1:
        chunk_bytes = np.product(chunks) * typesize
        if not chunk_bytes < target_size:
            if abs(chunk_bytes - target_size) / target_size < 0.5:
                if chunk_bytes < CHUNK_MAX:
                    break
            if np.product(chunks) == 1:
                break
            chunks[idx % ndims] = np.ceil(chunks[(idx % ndims)] / 2.0)
            idx += 1

    return tuple((int(x) for x in chunks))