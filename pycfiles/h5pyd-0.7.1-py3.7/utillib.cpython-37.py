# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_apps/utillib.py
# Compiled at: 2020-02-03 14:26:53
# Size of source mod 2**32: 25647 bytes
import sys, logging
try:
    import h5py, h5pyd, numpy as np
except ImportError as e:
    try:
        sys.stderr.write('ERROR : %s : install it to use this utility...\n' % str(e))
        sys.exit(1)
    finally:
        e = None
        del e

if __name__ == 'utillib':
    from chunkiter import ChunkIterator
else:
    from .chunkiter import ChunkIterator

def dump_dtype(dt):
    if not isinstance(dt, np.dtype):
        raise TypeError('expected np.dtype, but got: {}'.format(type(dt)))
    elif len(dt) > 0:
        out = '{'
        for name in dt.fields:
            subdt = dt.fields[name][0]
            out += '{}: {} |'.format(name, dump_dtype(subdt))

        out = out[:-1] + '}'
    else:
        ref = h5py.check_dtype(ref=dt)
        if ref:
            out = str(ref)
        else:
            vlen = h5py.check_dtype(vlen=dt)
            if vlen:
                out = 'VLEN: ' + dump_dtype(vlen)
            else:
                out = str(dt)
    return out


def is_h5py(obj):
    if isinstance(obj, object):
        if isinstance(obj.id.id, int):
            return True
    return False


def is_reference(val):
    try:
        if isinstance(val, object):
            if val.__class__.__name__ == 'Reference':
                return True
        if isinstance(val, type):
            if val.__name__ == 'Reference':
                return True
    except AttributeError as ae:
        try:
            msg = 'is_reference for {} error: {}'.format(val, ae)
            logging.error(msg)
        finally:
            ae = None
            del ae

    return False


def is_regionreference(val):
    try:
        if isinstance(val, object):
            if val.__class__.__name__ == 'RegionReference':
                return True
        if isinstance(val, type):
            if val.__name__ == 'RegionReference':
                return True
    except AttributeError as ae:
        try:
            msg = 'is_reference for {} error: {}'.format(val, ae)
            logging.error(msg)
        finally:
            ae = None
            del ae

    return False


def has_reference(dtype):
    has_ref = False
    if not isinstance(dtype, np.dtype):
        return False
        if len(dtype) > 0:
            for name in dtype.fields:
                item = dtype.fields[name]
                if has_reference(item[0]):
                    has_ref = True
                    break

    elif dtype.metadata and 'ref' in dtype.metadata:
        basedt = dtype.metadata['ref']
        has_ref = is_reference(basedt)
    else:
        if dtype.metadata:
            if 'vlen' in dtype.metadata:
                basedt = dtype.metadata['vlen']
                has_ref = has_reference(basedt)
    return has_ref


def convert_dtype(srcdt, ctx):
    """ Return a dtype based on input dtype, converting any Reference types from
    h5py style to h5pyd and vice-versa.
    """
    msg = 'convert dtype: {}, type: {},'.format(srcdt, type(srcdt))
    logging.info(msg)
    if len(srcdt) > 0:
        fields = []
        for name in srcdt.fields:
            item = srcdt.fields[name]
            field_dt = convert_dtype(item[0], ctx)
            fields.append((name, field_dt))

        tgt_dt = np.dtype(fields)
    else:
        if srcdt.metadata and 'ref' in srcdt.metadata:
            ref = srcdt.metadata['ref']
            if is_reference(ref):
                if is_h5py(ctx['fout']):
                    tgt_dt = h5py.special_dtype(ref=(h5py.Reference))
                else:
                    tgt_dt = h5pyd.special_dtype(ref=(h5pyd.Reference))
            else:
                if is_regionreference(ref):
                    if is_h5py(ctx['fout']):
                        tgt_dt = h5py.special_dtype(ref=(h5py.RegionReference))
                    else:
                        tgt_dt = h5py.special_dtype(ref=(h5py.RegionReference))
                else:
                    msg = 'Unexpected ref type: {}'.format(srcdt)
                    logging.error(msg)
                    raise TypeError(msg)
        else:
            if srcdt.metadata:
                if 'vlen' in srcdt.metadata:
                    src_vlen = srcdt.metadata['vlen']
                    if isinstance(src_vlen, np.dtype):
                        tgt_base = convert_dtype(src_vlen, ctx)
                    else:
                        tgt_base = src_vlen
                elif is_h5py(ctx['fout']):
                    tgt_dt = h5py.special_dtype(vlen=tgt_base)
                else:
                    tgt_dt = h5pyd.special_dtype(vlen=tgt_base)
            else:
                tgt_dt = srcdt
    return tgt_dt


def copy_element--- This code section failed: ---

 L. 151         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'copy_element, val: '
                6  LOAD_GLOBAL              str
                8  LOAD_FAST                'val'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  BINARY_ADD       
               14  LOAD_STR                 ' val type: '
               16  BINARY_ADD       
               18  LOAD_GLOBAL              str
               20  LOAD_GLOBAL              type
               22  LOAD_FAST                'val'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  BINARY_ADD       
               30  LOAD_STR                 'src_dt: '
               32  BINARY_ADD       
               34  LOAD_GLOBAL              dump_dtype
               36  LOAD_FAST                'src_dt'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  BINARY_ADD       
               42  LOAD_STR                 ' tgt_dt: '
               44  BINARY_ADD       
               46  LOAD_GLOBAL              dump_dtype
               48  LOAD_FAST                'tgt_dt'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  BINARY_ADD       
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_TOP          

 L. 153        58  LOAD_FAST                'ctx'
               60  LOAD_STR                 'fin'
               62  BINARY_SUBSCR    
               64  STORE_FAST               'fin'

 L. 154        66  LOAD_FAST                'ctx'
               68  LOAD_STR                 'fout'
               70  BINARY_SUBSCR    
               72  STORE_FAST               'fout'

 L. 155        74  LOAD_CONST               None
               76  STORE_FAST               'out'

 L. 156        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'src_dt'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  LOAD_CONST               0
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE   194  'to 194'

 L. 157        90  BUILD_LIST_0          0 
               92  STORE_FAST               'out_fields'

 L. 158        94  LOAD_CONST               0
               96  STORE_FAST               'i'

 L. 159        98  SETUP_LOOP          190  'to 190'
              100  LOAD_FAST                'src_dt'
              102  LOAD_ATTR                fields
              104  GET_ITER         
              106  FOR_ITER            188  'to 188'
              108  STORE_FAST               'name'

 L. 160       110  LOAD_FAST                'src_dt'
              112  LOAD_ATTR                fields
              114  LOAD_FAST                'name'
              116  BINARY_SUBSCR    
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  STORE_FAST               'field_src_dt'

 L. 161       124  LOAD_FAST                'tgt_dt'
              126  LOAD_ATTR                fields
              128  LOAD_FAST                'name'
              130  BINARY_SUBSCR    
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  STORE_FAST               'field_tgt_dt'

 L. 162       138  LOAD_FAST                'val'
              140  LOAD_FAST                'i'
              142  BINARY_SUBSCR    
              144  STORE_FAST               'field_val'

 L. 163       146  LOAD_FAST                'i'
              148  LOAD_CONST               1
              150  INPLACE_ADD      
              152  STORE_FAST               'i'

 L. 164       154  LOAD_GLOBAL              copy_element
              156  LOAD_FAST                'field_val'
              158  LOAD_FAST                'field_src_dt'
              160  LOAD_FAST                'field_tgt_dt'
              162  LOAD_FAST                'ctx'
              164  CALL_FUNCTION_4       4  '4 positional arguments'
              166  STORE_FAST               'out_field'

 L. 165       168  LOAD_FAST                'out_fields'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'out_field'
              174  CALL_METHOD_1         1  '1 positional argument'
              176  POP_TOP          

 L. 166       178  LOAD_GLOBAL              tuple
              180  LOAD_FAST                'out_fields'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  STORE_FAST               'out'
              186  JUMP_BACK           106  'to 106'
              188  POP_BLOCK        
            190_0  COME_FROM_LOOP       98  '98'
          190_192  JUMP_FORWARD        796  'to 796'
            194_0  COME_FROM            88  '88'

 L. 167       194  LOAD_FAST                'src_dt'
              196  LOAD_ATTR                metadata
          198_200  POP_JUMP_IF_FALSE   502  'to 502'
              202  LOAD_STR                 'ref'
              204  LOAD_FAST                'src_dt'
              206  LOAD_ATTR                metadata
              208  COMPARE_OP               in
          210_212  POP_JUMP_IF_FALSE   502  'to 502'

 L. 168       214  LOAD_FAST                'tgt_dt'
              216  LOAD_ATTR                metadata
              218  POP_JUMP_IF_FALSE   230  'to 230'
              220  LOAD_STR                 'ref'
              222  LOAD_FAST                'tgt_dt'
              224  LOAD_ATTR                metadata
              226  COMPARE_OP               not-in
              228  POP_JUMP_IF_FALSE   244  'to 244'
            230_0  COME_FROM           218  '218'

 L. 169       230  LOAD_GLOBAL              TypeError
              232  LOAD_STR                 'Expected tgt dtype to be ref, but got: {}'
              234  LOAD_METHOD              format
              236  LOAD_FAST                'tgt_dt'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  RAISE_VARARGS_1       1  'exception instance'
            244_0  COME_FROM           228  '228'

 L. 170       244  LOAD_FAST                'tgt_dt'
              246  LOAD_ATTR                metadata
              248  LOAD_STR                 'ref'
              250  BINARY_SUBSCR    
              252  STORE_FAST               'ref'

 L. 171       254  LOAD_GLOBAL              is_reference
              256  LOAD_FAST                'ref'
              258  CALL_FUNCTION_1       1  '1 positional argument'
          260_262  POP_JUMP_IF_FALSE   464  'to 464'

 L. 173       264  LOAD_GLOBAL              is_h5py
              266  LOAD_FAST                'ctx'
              268  LOAD_STR                 'fout'
              270  BINARY_SUBSCR    
              272  CALL_FUNCTION_1       1  '1 positional argument'
          274_276  POP_JUMP_IF_FALSE   288  'to 288'

 L. 174       278  LOAD_GLOBAL              h5py
              280  LOAD_METHOD              Reference
              282  CALL_METHOD_0         0  '0 positional arguments'
              284  STORE_FAST               'out'
              286  JUMP_FORWARD        292  'to 292'
            288_0  COME_FROM           274  '274'

 L. 176       288  LOAD_STR                 ''
              290  STORE_FAST               'out'
            292_0  COME_FROM           286  '286'

 L. 178       292  LOAD_FAST                'ref'
          294_296  POP_JUMP_IF_FALSE   498  'to 498'

 L. 179       298  SETUP_EXCEPT        312  'to 312'

 L. 180       300  LOAD_FAST                'fin'
              302  LOAD_FAST                'val'
              304  BINARY_SUBSCR    
              306  STORE_FAST               'fin_obj'
              308  POP_BLOCK        
              310  JUMP_FORWARD        376  'to 376'
            312_0  COME_FROM_EXCEPT    298  '298'

 L. 181       312  DUP_TOP          
              314  LOAD_GLOBAL              AttributeError
              316  COMPARE_OP               exception-match
          318_320  POP_JUMP_IF_FALSE   374  'to 374'
              322  POP_TOP          
              324  STORE_FAST               'ae'
              326  POP_TOP          
              328  SETUP_FINALLY       362  'to 362'

 L. 182       330  LOAD_STR                 'Unable able to get obj for ref value: {}'
              332  LOAD_METHOD              format
              334  LOAD_FAST                'ae'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  STORE_FAST               'msg'

 L. 183       340  LOAD_GLOBAL              logging
              342  LOAD_METHOD              error
              344  LOAD_FAST                'msg'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          

 L. 184       350  LOAD_GLOBAL              print
              352  LOAD_FAST                'msg'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  POP_TOP          

 L. 185       358  LOAD_CONST               None
              360  RETURN_VALUE     
            362_0  COME_FROM_FINALLY   328  '328'
              362  LOAD_CONST               None
              364  STORE_FAST               'ae'
              366  DELETE_FAST              'ae'
              368  END_FINALLY      
              370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
            374_0  COME_FROM           318  '318'
              374  END_FINALLY      
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           310  '310'

 L. 188       376  LOAD_FAST                'fin_obj'
              378  LOAD_ATTR                name
              380  STORE_FAST               'h5path'

 L. 189       382  LOAD_FAST                'h5path'
          384_386  POP_JUMP_IF_TRUE    422  'to 422'

 L. 190       388  LOAD_STR                 'No path found for ref object'
              390  STORE_FAST               'msg'

 L. 191       392  LOAD_GLOBAL              logging
              394  LOAD_METHOD              warn
              396  LOAD_FAST                'msg'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          

 L. 192       402  LOAD_FAST                'ctx'
              404  LOAD_STR                 'verbose'
              406  BINARY_SUBSCR    
          408_410  POP_JUMP_IF_FALSE   462  'to 462'

 L. 193       412  LOAD_GLOBAL              print
              414  LOAD_FAST                'msg'
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  POP_TOP          
              420  JUMP_FORWARD        462  'to 462'
            422_0  COME_FROM           384  '384'

 L. 195       422  LOAD_FAST                'fout'
              424  LOAD_FAST                'h5path'
              426  BINARY_SUBSCR    
              428  STORE_FAST               'fout_obj'

 L. 196       430  LOAD_GLOBAL              is_h5py
              432  LOAD_FAST                'ctx'
              434  LOAD_STR                 'fout'
              436  BINARY_SUBSCR    
              438  CALL_FUNCTION_1       1  '1 positional argument'
          440_442  POP_JUMP_IF_FALSE   452  'to 452'

 L. 197       444  LOAD_FAST                'fout_obj'
              446  LOAD_ATTR                ref
              448  STORE_FAST               'out'
              450  JUMP_FORWARD        462  'to 462'
            452_0  COME_FROM           440  '440'

 L. 199       452  LOAD_GLOBAL              str
              454  LOAD_FAST                'fout_obj'
              456  LOAD_ATTR                ref
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  STORE_FAST               'out'
            462_0  COME_FROM           450  '450'
            462_1  COME_FROM           420  '420'
            462_2  COME_FROM           408  '408'
              462  JUMP_FORWARD        796  'to 796'
            464_0  COME_FROM           260  '260'

 L. 202       464  LOAD_GLOBAL              is_regionreference
              466  LOAD_FAST                'ref'
              468  CALL_FUNCTION_1       1  '1 positional argument'
          470_472  POP_JUMP_IF_FALSE   480  'to 480'

 L. 203       474  LOAD_STR                 'tbd'
              476  STORE_FAST               'out'
              478  JUMP_FORWARD        796  'to 796'
            480_0  COME_FROM           470  '470'

 L. 205       480  LOAD_GLOBAL              TypeError
              482  LOAD_STR                 'Unexpected ref type: {}'
              484  LOAD_METHOD              format
              486  LOAD_GLOBAL              type
              488  LOAD_FAST                'ref'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  RAISE_VARARGS_1       1  'exception instance'
            498_0  COME_FROM           294  '294'
          498_500  JUMP_FORWARD        796  'to 796'
            502_0  COME_FROM           210  '210'
            502_1  COME_FROM           198  '198'

 L. 206       502  LOAD_FAST                'src_dt'
              504  LOAD_ATTR                metadata
          506_508  POP_JUMP_IF_FALSE   792  'to 792'
              510  LOAD_STR                 'vlen'
              512  LOAD_FAST                'src_dt'
              514  LOAD_ATTR                metadata
              516  COMPARE_OP               in
          518_520  POP_JUMP_IF_FALSE   792  'to 792'

 L. 207       522  LOAD_GLOBAL              logging
              524  LOAD_METHOD              debug
              526  LOAD_STR                 'copy_elment, got vlen element, dt: {}'
              528  LOAD_METHOD              format
              530  LOAD_FAST                'src_dt'
              532  LOAD_ATTR                metadata
              534  LOAD_STR                 'vlen'
              536  BINARY_SUBSCR    
              538  CALL_METHOD_1         1  '1 positional argument'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  POP_TOP          

 L. 208       544  LOAD_GLOBAL              isinstance
              546  LOAD_FAST                'val'
              548  LOAD_GLOBAL              np
              550  LOAD_ATTR                ndarray
              552  CALL_FUNCTION_2       2  '2 positional arguments'
          554_556  POP_JUMP_IF_TRUE    576  'to 576'

 L. 209       558  LOAD_GLOBAL              TypeError
              560  LOAD_STR                 'Expecting ndarray or vlen element, but got: {}'
              562  LOAD_METHOD              format
              564  LOAD_GLOBAL              type
              566  LOAD_FAST                'val'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  CALL_METHOD_1         1  '1 positional argument'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  RAISE_VARARGS_1       1  'exception instance'
            576_0  COME_FROM           554  '554'

 L. 210       576  LOAD_FAST                'tgt_dt'
              578  LOAD_ATTR                metadata
          580_582  POP_JUMP_IF_FALSE   596  'to 596'
              584  LOAD_STR                 'vlen'
              586  LOAD_FAST                'tgt_dt'
              588  LOAD_ATTR                metadata
              590  COMPARE_OP               not-in
          592_594  POP_JUMP_IF_FALSE   610  'to 610'
            596_0  COME_FROM           580  '580'

 L. 211       596  LOAD_GLOBAL              TypeError
              598  LOAD_STR                 'Expected tgt dtype to be vlen, but got: {}'
              600  LOAD_METHOD              format
              602  LOAD_FAST                'tgt_dt'
              604  CALL_METHOD_1         1  '1 positional argument'
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  RAISE_VARARGS_1       1  'exception instance'
            610_0  COME_FROM           592  '592'

 L. 212       610  LOAD_FAST                'src_dt'
              612  LOAD_ATTR                metadata
              614  LOAD_STR                 'vlen'
              616  BINARY_SUBSCR    
              618  STORE_FAST               'src_vlen_dt'

 L. 213       620  LOAD_FAST                'tgt_dt'
              622  LOAD_ATTR                metadata
              624  LOAD_STR                 'vlen'
              626  BINARY_SUBSCR    
              628  STORE_FAST               'tgt_vlen_dt'

 L. 214       630  LOAD_GLOBAL              has_reference
              632  LOAD_FAST                'src_vlen_dt'
              634  CALL_FUNCTION_1       1  '1 positional argument'
          636_638  POP_JUMP_IF_FALSE   762  'to 762'

 L. 215       640  LOAD_GLOBAL              len
              642  LOAD_FAST                'val'
              644  LOAD_ATTR                shape
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  LOAD_CONST               0
              650  COMPARE_OP               ==
          652_654  POP_JUMP_IF_FALSE   694  'to 694'

 L. 217       656  LOAD_FAST                'val'
              658  LOAD_CONST               ()
              660  BINARY_SUBSCR    
              662  STORE_FAST               'e'

 L. 218       664  LOAD_GLOBAL              copy_element
              666  LOAD_FAST                'e'
              668  LOAD_FAST                'src_vlen_dt'
              670  LOAD_FAST                'tgt_vlen_dt'
              672  LOAD_FAST                'ctx'
              674  CALL_FUNCTION_4       4  '4 positional arguments'
              676  STORE_FAST               'v'

 L. 219       678  LOAD_GLOBAL              np
              680  LOAD_ATTR                array
              682  LOAD_FAST                'v'
              684  LOAD_FAST                'tgt_dt'
              686  LOAD_CONST               ('dtype',)
              688  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              690  STORE_FAST               'out'
              692  JUMP_FORWARD        760  'to 760'
            694_0  COME_FROM           652  '652'

 L. 222       694  LOAD_GLOBAL              np
              696  LOAD_ATTR                zeros
              698  LOAD_FAST                'val'
              700  LOAD_ATTR                shape
              702  LOAD_FAST                'tgt_dt'
              704  LOAD_CONST               ('dtype',)
              706  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              708  STORE_FAST               'out'

 L. 223       710  SETUP_LOOP          790  'to 790'
              712  LOAD_GLOBAL              range
              714  LOAD_GLOBAL              len
              716  LOAD_FAST                'out'
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  GET_ITER         
              724  FOR_ITER            758  'to 758'
              726  STORE_FAST               'i'

 L. 224       728  LOAD_FAST                'val'
              730  LOAD_FAST                'i'
              732  BINARY_SUBSCR    
              734  STORE_FAST               'e'

 L. 225       736  LOAD_GLOBAL              copy_element
              738  LOAD_FAST                'e'
              740  LOAD_FAST                'src_vlen_dt'
              742  LOAD_FAST                'tgt_vlen_dt'
              744  LOAD_FAST                'ctx'
              746  CALL_FUNCTION_4       4  '4 positional arguments'
              748  LOAD_FAST                'out'
              750  LOAD_FAST                'i'
              752  STORE_SUBSCR     
          754_756  JUMP_BACK           724  'to 724'
            758_0  COME_FROM           462  '462'
              758  POP_BLOCK        
            760_0  COME_FROM           692  '692'
              760  JUMP_FORWARD        790  'to 790'
            762_0  COME_FROM           636  '636'

 L. 228       762  LOAD_GLOBAL              np
              764  LOAD_ATTR                zeros
              766  LOAD_FAST                'val'
              768  LOAD_ATTR                shape
              770  LOAD_FAST                'tgt_dt'
              772  LOAD_CONST               ('dtype',)
            774_0  COME_FROM           478  '478'
              774  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              776  STORE_FAST               'out'

 L. 229       778  LOAD_FAST                'val'
              780  LOAD_CONST               Ellipsis
              782  BINARY_SUBSCR    
              784  LOAD_FAST                'out'
              786  LOAD_CONST               Ellipsis
              788  STORE_SUBSCR     
            790_0  COME_FROM           760  '760'
            790_1  COME_FROM_LOOP      710  '710'
              790  JUMP_FORWARD        796  'to 796'
            792_0  COME_FROM           518  '518'
            792_1  COME_FROM           506  '506'

 L. 231       792  LOAD_FAST                'val'
              794  STORE_FAST               'out'
            796_0  COME_FROM           790  '790'
            796_1  COME_FROM           498  '498'
            796_2  COME_FROM           190  '190'

 L. 232       796  LOAD_FAST                'out'
              798  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 758_0


def copy_array(src_arr, ctx):
    """ Copy the numpy array to a new array.
    Convert any reference type to point to item in the target's hierarchy.
    """
    if not isinstance(src_arr, np.ndarray):
        raise TypeError('Expecting ndarray, but got: {}'.format(src_arr))
    else:
        tgt_dt = convert_dtype(src_arr.dtype, ctx)
        tgt_arr = np.zeros((src_arr.shape), dtype=tgt_dt)
        if has_reference(src_arr.dtype):
            count = np.product(src_arr.shape)
            tgt_arr_flat = tgt_arr.reshape((count,))
            src_arr_flat = src_arr.reshape((count,))
            for i in range(count):
                e = src_arr_flat[i]
                element = copy_elementesrc_arr.dtypetgt_dtctx
                tgt_arr_flat[i] = element

            tgt_arr = tgt_arr_flat.reshape(src_arr.shape)
        else:
            tgt_arr[...] = src_arr[...]
    return tgt_arr


def copy_attribute(desobj, name, srcobj, ctx):
    msg = 'creating attribute {} in {}'.format(name, srcobj.name)
    logging.debug(msg)
    if ctx['verbose']:
        print(msg)
    tgtarr = None
    data = srcobj.attrs[name]
    src_dt = None
    try:
        src_dt = data.dtype
    except AttributeError:
        pass

    srcarr = np.asarray(data, order='C', dtype=src_dt)
    tgtarr = copy_array(srcarr, ctx)
    try:
        desobj.attrs.create(name, tgtarr)
    except (IOError, TypeError) as e:
        try:
            msg = 'ERROR: failed to create attribute {} of object {} -- {}'.format(name, desobj.name, str(e))
            logging.error(msg)
            print(msg)
        finally:
            e = None
            del e


def create_dataset(dobj, ctx):
    """ create a dataset using the properties of the passed in h5py dataset.
        If successful, proceed to copy attributes and data.
    """
    msg = 'creating dataset {}, shape: {}, type: {}'.format(dobj.name, dobj.shape, dobj.dtype)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)
    else:
        fout = ctx['fout']
        deflate = ctx['deflate']
        fillvalue = None
        try:
            fillvalue = dobj.fillvalue
        except RuntimeError:
            pass

        chunks = None
        if ctx['dataload'] == 's3link':
            dset_dims = dobj.shape
            logging.debug('dset_dims: {}'.format(dset_dims))
            rank = len(dset_dims)
            chunk_dims = dobj.chunks
            logging.debug('chunk_dims: {}'.format(chunk_dims))
            num_chunks = 0
            dsetid = dobj.id
            spaceid = dsetid.get_space
            if chunk_dims:
                num_chunks = dsetid.get_num_chunks(spaceid)
            chunks = {}
            if num_chunks == 0:
                chunks['class'] = 'H5D_CONTIGUOUS_REF'
                chunks['file_uri'] = ctx['s3path']
                chunks['offset'] = dsetid.get_offset
                chunks['size'] = dsetid.get_storage_size
                logging.info(f"using chunk layout: {chunks}")
            else:
                if num_chunks < 10:
                    chunk_map = {}
                    for i in range(num_chunks):
                        chunk_info = dsetid.get_chunk_info(i, spaceid)
                        index = chunk_info.chunk_offset
                        logging.debug(f"got chunk_info: {chunk_info} for chunk: {i}")
                        if not isinstance(index, tuple) or len(index) != rank:
                            msg = f"Unexpected array_offset: {index} for dataset with rank: {rank}"
                            logging.error(msg)
                            raise IOError(msg)
                        chunk_key = ''
                        for dim in range(rank):
                            chunk_key += str(index[dim] // chunk_dims[dim])
                            if dim < rank - 1:
                                chunk_key += '_'

                        logging.debug('adding chunk_key: {}'.format(chunk_key))
                        chunk_map[chunk_key] = (chunk_info.byte_offset, chunk_info.size)

                    chunks['class'] = 'H5D_CHUNKED_REF'
                    chunks['file_uri'] = ctx['s3path']
                    chunks['dims'] = dobj.chunks
                    chunks['chunks'] = chunk_map
                    logging.info('using chunk layout: {}'.format(chunks))
                else:
                    dt = np.dtype([('offset', np.int64), ('size', np.int32)])
                    chunkinfo_arr_dims = []
                    for dim in range(rank):
                        chunkinfo_arr_dims.append(int(np.ceil(dset_dims[dim] / chunk_dims[dim])))

                    chunkinfo_arr_dims = tuple(chunkinfo_arr_dims)
                    logging.debug('creating chunkinfo array of shape: {}'.format(chunkinfo_arr_dims))
                    chunkinfo_arr = np.zeros((np.prod(chunkinfo_arr_dims)), dtype=dt)
                    for i in range(num_chunks):
                        chunk_info = dsetid.get_chunk_info(i, spaceid)
                        index = chunk_info.chunk_offset
                        if not isinstance(index, tuple) or len(index) != rank:
                            msg = f"Unexpected array_offset: {index} for dataset with rank: {rank}"
                            logging.error(msg)
                            raise IOError(msg)
                        offset = 0
                        stride = 1
                        for i in range(rank):
                            dim = rank - i - 1
                            offset += index[dim] // chunk_dims[dim] * stride
                            stride *= chunkinfo_arr_dims[dim]

                        chunkinfo_arr[offset] = (
                         chunk_info.byte_offset, chunk_info.size)

                    anon_dset = fout.create_dataset(None, shape=chunkinfo_arr_dims, dtype=dt)
                    anon_dset[...] = chunkinfo_arr
                    logging.debug('anon_dset: {}'.format(anon_dset))
                    logging.debug('annon_values: {}'.format(anon_dset[...]))
                    chunks['class'] = 'H5D_CHUNKED_REF_INDIRECT'
                    chunks['file_uri'] = ctx['s3path']
                    chunks['dims'] = dobj.chunks
                    chunks['chunk_table'] = anon_dset.id.id
                    logging.info('using chunk layout: {}'.format(chunks))
    if chunks is None:
        if dobj.chunks:
            chunks = tuple(dobj.chunks)
    try:
        tgt_dtype = convert_dtype(dobj.dtype, ctx)
        if len(dobj.shape) == 0:
            compression_filter = None
            compression_opts = None
            chunks = None
            shuffle = None
            fletcher32 = None
            maxshape = None
            scaleoffset = None
        else:
            compression_filter = dobj.compression
            compression_opts = dobj.compression_opts
            if deflate is not None:
                if compression_filter is None:
                    compression_filter = 'gzip'
                    compression_opts = deflate
                    if ctx['verbose']:
                        print('applying gzip filter with level: {}'.format(deflate))
            shuffle = dobj.shuffle
            fletcher32 = dobj.fletcher32
            maxshape = dobj.maxshape
            scaleoffset = dobj.scaleoffset
        dset = fout.create_dataset((dobj.name), shape=(dobj.shape), dtype=tgt_dtype, chunks=chunks, compression=compression_filter,
          shuffle=shuffle,
          fletcher32=fletcher32,
          maxshape=maxshape,
          compression_opts=compression_opts,
          fillvalue=fillvalue,
          scaleoffset=scaleoffset)
        msg = 'dataset created, uuid: {}, chunk_size: {}'.format(dset.id.id, str(dset.chunks))
        logging.info(msg)
        if ctx['verbose']:
            print(msg)
        logging.debug('adding dataset id {} to {} in srcid_desobj_map'.format(dobj.id.id, dset))
        srcid_desobj_map = ctx['srcid_desobj_map']
        srcid_desobj_map[dobj.id.__hash__] = dset
    except (IOError, TypeError, KeyError) as e:
        try:
            msg = 'ERROR: failed to create dataset: {}'.format(str(e))
            logging.error(msg)
            print(msg)
            return
        finally:
            e = None
            del e


def write_dataset(src, tgt, ctx):
    """ write values from src dataset to target dataset.
    """
    msg = 'write_dataset src: {} to tgt: {}, shape: {}, type: {}'.format(src.name, tgt.name, src.shape, src.dtype)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)
    if src.shape is None:
        msg = 'no data for null space dataset: {}'.format(src.name)
        logging.info(msg)
        if ctx['verbose']:
            print(msg)
        return
    if len(src.shape) == 0:
        x = src[()]
        msg = 'writing for scalar dataset: {}'.format(src.name)
        logging.info(msg)
        if ctx['verbose']:
            print(msg)
        tgt[()] = x
        return
    fillvalue = None
    try:
        fillvalue = src.fillvalue
    except RuntimeError:
        pass

    msg = 'iterating over chunks for {}'.format(src.name)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)
    try:
        it = ChunkIterator(tgt)
        logging.debug('src dtype: {}'.format(src.dtype))
        logging.debug('des dtype: {}'.format(tgt.dtype))
        for s in it:
            arr = src[s]
            empty_arr = np.zeros((arr.shape), dtype=(arr.dtype))
            if fillvalue:
                empty_arr.fill(fillvalue)
            elif np.array_equal(arr, empty_arr):
                msg = 'skipping chunk for slice: {}'.format(str(s))
            else:
                msg = 'writing dataset data for slice: {}'.format(s)
                tgt[s] = arr
            logging.info(msg)
            if ctx['verbose']:
                print(msg)

    except (IOError, TypeError) as e:
        try:
            msg = 'ERROR : failed to copy dataset data : {}'.format(str(e))
            logging.error(msg)
            print(msg)
        finally:
            e = None
            del e

    msg = 'done with dataload for {}'.format(src.name)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)


def create_links(gsrc, gdes, ctx):
    srcid_desobj_map = ctx['srcid_desobj_map']
    if ctx['verbose']:
        print('create_links: {}'.format(gsrc.name))
    for title in gsrc:
        if ctx['verbose']:
            print('got link: {}'.format(title))
        lnk = gsrc.get(title, getlink=True)
        link_classname = lnk.__class__.__name__
        if link_classname == 'HardLink':
            logging.debug('Got hardlink: {} gsrc: {} gdes: {}'.format(title, gsrc, gdes))
            if title not in gdes:
                msg = 'creating multilink {} with title: {}'.format(gdes, title)
                if ctx['verbose']:
                    print(msg)
                logging.info(msg)
                src_obj_id = gsrc[title].id
                src_obj_id_hash = src_obj_id.__hash__
                logging.debug('got src_obj_id hash: {}'.format(src_obj_id_hash))
                if src_obj_id_hash in srcid_desobj_map:
                    des_obj = srcid_desobj_map[src_obj_id_hash]
                    logging.debug('creating hardlink to {}'.format(des_obj.id.id))
                    gdes[title] = des_obj
                else:
                    msg = 'could not find map item to src id: {}'.format(src_obj_id_hash)
                    logging.warn(msg)
                if ctx['verbose']:
                    print('WARNING: ' + msg)
                elif link_classname == 'SoftLink':
                    msg = 'creating SoftLink({}) with title: {}'.format(lnk.path, title)
                    if ctx['verbose']:
                        print(msg)
                    else:
                        logging.info(msg)
                        if is_h5py(gdes):
                            soft_link = h5py.SoftLink(lnk.path)
                        else:
                            soft_link = h5pyd.SoftLink(lnk.path)
                    gdes[title] = soft_link
                elif link_classname == 'ExternalLink':
                    msg = 'creating ExternalLink({}, {}) with title: {}'.format(lnk.filename, lnk.path, title)
                    if ctx['verbose']:
                        print(msg)
                    else:
                        logging.info(msg)
                        if is_h5py(gdes):
                            ext_link = h5py.ExternalLink(lnk.filename, lnk.path)
                        else:
                            ext_link = h5pyd.ExternalLink(lnk.filename, lnk.path)
                    gdes[title] = ext_link
                else:
                    msg = 'Unexpected link type: {}'.format(lnk.__class__.__name__)
                    logging.warning(msg)
                    if ctx['verbose']:
                        print(msg)


def create_group(gobj, ctx):
    msg = 'creating group {}'.format(gobj.name)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)
    fout = ctx['fout']
    grp = fout.create_group(gobj.name)
    srcid_desobj_map = ctx['srcid_desobj_map']
    logging.debug('adding group id {} to {} in srcid_desobj_map'.format(gobj.id.id, grp))
    srcid_desobj_map[gobj.id.__hash__] = grp
    create_links(gobj, grp, ctx)


def create_datatype(obj, ctx):
    msg = 'creating datatype {}'.format(obj.name)
    logging.info(msg)
    if ctx['verbose']:
        print(msg)
    fout = ctx['fout']
    fout[obj.name] = obj.dtype
    srcid_desobj_map = ctx['srcid_desobj_map']
    logging.debug('adding datatype id {} to {} in srcid_desobj_map'.format(obj.id.id, fout[obj.name]))
    srcid_desobj_map[obj.id.__hash__] = fout[obj.name]


def load_file(fin, fout, verbose=False, dataload='ingest', s3path=None, deflate=None):
    logging.info('input file: {}'.format(fin.filename))
    logging.info('output file: {}'.format(fout.filename))
    if dataload != 'ingest':
        if dataload == 'nodata':
            logging.info('no data load')
        else:
            if dataload == 's3link':
                if not s3path:
                    logging.error('s3path expected to be set')
                    sys.exit(1)
                logging.info('using s3path')
            else:
                logging.error('unexpected dataload value')
                sys.exit(1)
    ctx = {}
    ctx['fin'] = fin
    ctx['fout'] = fout
    ctx['verbose'] = verbose
    ctx['dataload'] = dataload
    ctx['deflate'] = deflate
    ctx['s3path'] = s3path
    ctx['dataload'] = dataload
    ctx['srcid_desobj_map'] = {}
    for ga in fin.attrs:
        copy_attributefoutgafinctx

    create_links(fin, fout, ctx)

    def object_create_helper(name, obj):
        class_name = obj.__class__.__name__
        if class_name in ('Dataset', 'Table'):
            create_dataset(obj, ctx)
        else:
            if class_name == 'Group':
                create_group(obj, ctx)
            else:
                if class_name == 'Datatype':
                    create_datatype(obj, ctx)
                else:
                    logging.error('no handler for object class: {}'.format(type(obj)))

    def object_copy_helper(name, obj):
        class_name = obj.__class__.__name__
        if class_name in ('Dataset', 'Table'):
            if ctx['dataload'] == 's3link':
                logging.info('skip datacopy for s3 reference')
            else:
                tgt = fout[obj.name]
                write_dataset(obj, tgt, ctx)
        elif class_name == 'Group':
            logging.debug('skip copy for group: {}'.format(obj.name))
        else:
            if class_name == 'Datatype':
                logging.debug('skip copy for datatype: {}'.format(obj.name))
            else:
                logging.error('no handler for object class: {}'.format(type(obj)))

    def object_attribute_helper(name, obj):
        tgt = fout[obj.name]
        for ga in obj.attrs:
            copy_attributetgtgaobjctx

    fin.visititems(object_create_helper)
    fin.visititems(object_attribute_helper)
    if dataload:
        fin.visititems(object_copy_helper)
    fout.close
    fin.close
    msg = 'load_file complete'
    logging.info(msg)
    if verbose:
        print(msg)
    return 0