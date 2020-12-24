# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/h5type.py
# Compiled at: 2019-12-23 13:59:38
# Size of source mod 2**32: 27453 bytes
from __future__ import absolute_import
import numpy as np, weakref

def is_reference(val):
    try:
        if val.__class__.__name__ == 'Reference':
            return True
    except AttributeError:
        pass

    try:
        if val.__name__ == 'Reference':
            return True
    except AttributeError:
        pass

    return False


def is_regionreference(val):
    try:
        if val.__class__.__name__ == 'RegionReference':
            return True
    except AttributeError:
        pass

    try:
        if val.__name__ == 'RegionReference':
            return True
    except AttributeError:
        pass

    return False


class Reference:
    __doc__ = '\n        Represents an HDF5 object reference\n    '

    @property
    def id(self):
        """ Low-level identifier appropriate for this object """
        return self._id

    @property
    def objref(self):
        """ Weak reference to object """
        return self._objref

    def __init__(self, bind):
        """ Create a new reference by binding to a group/dataset/committed type
        """
        self._id = bind._id
        self._objref = weakref.ref(bind)

    def __repr__(self):
        if not isinstance(self._id.id, str):
            raise TypeError('Expected string id')
        else:
            item = None
            if self._id.objtype_code == 'd':
                item = 'datasets/' + self._id.id
            else:
                if self._id.objtype_code == 'g':
                    item = 'groups/' + self._id.id
                else:
                    if self._id.objtype_code == 't':
                        item = 'datatypes/' + self._id.id
                    else:
                        raise TypeError('Unexpected id type')
        return item

    def tolist(self):
        return [
         self.__repr__()]


class RegionReference:
    __doc__ = '\n        Represents an HDF5 region reference\n    '

    @property
    def id(self):
        """ Low-level identifier appropriate for this object """
        return self._id

    @property
    def objref(self):
        """ Weak reference to object """
        return self._objref

    def __init__(self, bind):
        """ Create a new reference by binding to a group/dataset/committed type
        """
        self._id = bind._id
        self._objref = weakref.ref(bind)

    def __repr__(self):
        return '<HDF5 region reference>'


def special_dtype(**kwds):
    """ Create a new h5py "special" type.  Only one keyword may be given.

    Legal keywords are:

    vlen = basetype
        Base type for HDF5 variable-length datatype. This can be Python
        str type or instance of np.dtype.
        Example: special_dtype( vlen=str )

    enum = (basetype, values_dict)
        Create a NumPy representation of an HDF5 enumerated type.  Provide
        a 2-tuple containing an (integer) base dtype and a dict mapping
        string names to integer values.

    ref = Reference | RegionReference
        Create a NumPy representation of an HDF5 object or region reference
        type.    """
    if len(kwds) != 1:
        raise TypeError('Exactly one keyword may be provided')
    else:
        name, val = kwds.popitem()
        if name == 'vlen':
            return np.dtype('O', metadata={'vlen': val})
        elif name == 'enum':
            try:
                dt, enum_vals = val
            except TypeError:
                raise TypeError('Enums must be created from a 2-tuple (basetype, values_dict)')

            dt = np.dtype(dt)
            if dt.kind not in 'iu':
                raise TypeError('Only integer types can be used as enums')
            return np.dtype(dt, metadata={'enum': enum_vals})
            if name == 'ref':
                dt = None
                if is_reference(val):
                    dt = np.dtype('S48', metadata={'ref': val})
        elif is_regionreference(val):
            dt = np.dtype('S48', metadata={'ref': val})
        else:
            raise ValueError('Ref class must be Reference or RegionReference')
        return dt
    raise TypeError('Unknown special type "%s"' % name)


def check_dtype(**kwds):
    """ Check a dtype for h5py special type "hint" information.  Only one
    keyword may be given.

    vlen = dtype
        If the dtype represents an HDF5 vlen, returns the Python base class.
        Currently only builting string vlens (str) are supported.  Returns
        None if the dtype does not represent an HDF5 vlen.

    enum = dtype
        If the dtype represents an HDF5 enumerated type, returns the dictionary
        mapping string names to integer values.  Returns None if the dtype does
        not represent an HDF5 enumerated type.

    ref = dtype
        If the dtype represents an HDF5 reference type, returns the reference
        class (either Reference or RegionReference).  Returns None if the dtype
        does not represent an HDF5 reference type.
    """
    if len(kwds) != 1:
        raise TypeError('Exactly one keyword may be provided')
    name, dt = kwds.popitem()
    if name not in ('vlen', 'enum', 'ref'):
        raise TypeError('Unknown special type "%s"' % name)
    try:
        return dt.metadata[name]
    except TypeError:
        return
    except KeyError:
        return


def getTypeResponse(typeItem):
    response = None
    if 'uuid' in typeItem:
        response = 'datatypes/' + typeItem['uuid']
    else:
        if typeItem['class'] == 'H5T_INTEGER' or typeItem['class'] == 'H5T_FLOAT':
            response = {}
            response['class'] = typeItem['class']
            response['base'] = typeItem['base']
        else:
            if typeItem['class'] == 'H5T_OPAQUE':
                response = {}
                response['class'] = 'H5T_OPAQUE'
                response['size'] = typeItem['size']
            else:
                if typeItem['class'] == 'H5T_REFERENCE':
                    response = {}
                    response['class'] = 'H5T_REFERENCE'
                    response['base'] = typeItem['base']
                else:
                    if typeItem['class'] == 'H5T_COMPOUND':
                        response = {}
                        response['class'] = 'H5T_COMPOUND'
                        fieldList = []
                        for field in typeItem['fields']:
                            fieldItem = {}
                            fieldItem['name'] = field['name']
                            fieldItem['type'] = getTypeResponse(field['type'])
                            fieldList.append(fieldItem)

                        response['fields'] = fieldList
                    else:
                        response = {}
                        for k in typeItem.keys():
                            if k == 'base':
                                if isinstance(typeItem[k], dict):
                                    response[k] = getTypeResponse(typeItem[k])
                                else:
                                    response[k] = typeItem[k]

    return response


def getTypeItem--- This code section failed: ---

 L. 258         0  LOAD_STR                 'H5T_STD_I8'

 L. 259         2  LOAD_STR                 'H5T_STD_U8'

 L. 260         4  LOAD_STR                 'H5T_STD_I16'

 L. 261         6  LOAD_STR                 'H5T_STD_U16'

 L. 262         8  LOAD_STR                 'H5T_STD_I32'

 L. 263        10  LOAD_STR                 'H5T_STD_U32'

 L. 264        12  LOAD_STR                 'H5T_STD_I64'

 L. 265        14  LOAD_STR                 'H5T_STD_U64'
               16  LOAD_CONST               ('int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64')
               18  BUILD_CONST_KEY_MAP_8     8 
               20  STORE_FAST               'predefined_int_types'

 L. 268        22  LOAD_STR                 'H5T_IEEE_F16'

 L. 269        24  LOAD_STR                 'H5T_IEEE_F32'

 L. 270        26  LOAD_STR                 'H5T_IEEE_F64'
               28  LOAD_CONST               ('float16', 'float32', 'float64')
               30  BUILD_CONST_KEY_MAP_3     3 
               32  STORE_FAST               'predefined_float_types'

 L. 273        34  BUILD_MAP_0           0 
               36  STORE_FAST               'type_info'

 L. 274        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'dt'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  LOAD_CONST               1
               46  COMPARE_OP               >
               48  POP_JUMP_IF_FALSE   128  'to 128'

 L. 276        50  LOAD_FAST                'dt'
               52  LOAD_ATTR                names
               54  STORE_FAST               'names'

 L. 277        56  LOAD_STR                 'H5T_COMPOUND'
               58  LOAD_FAST                'type_info'
               60  LOAD_STR                 'class'
               62  STORE_SUBSCR     

 L. 278        64  BUILD_LIST_0          0 
               66  STORE_FAST               'fields'

 L. 279        68  SETUP_LOOP          124  'to 124'
               70  LOAD_FAST                'names'
               72  GET_ITER         
               74  FOR_ITER            122  'to 122'
               76  STORE_FAST               'name'

 L. 280        78  LOAD_STR                 'name'
               80  LOAD_FAST                'name'
               82  BUILD_MAP_1           1 
               84  STORE_FAST               'field'

 L. 281        86  LOAD_GLOBAL              getTypeItem
               88  LOAD_FAST                'dt'
               90  LOAD_FAST                'name'
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_FAST                'field'
               98  LOAD_STR                 'type'
              100  STORE_SUBSCR     

 L. 282       102  LOAD_FAST                'fields'
              104  LOAD_METHOD              append
              106  LOAD_FAST                'field'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          

 L. 283       112  LOAD_FAST                'fields'
              114  LOAD_FAST                'type_info'
              116  LOAD_STR                 'fields'
              118  STORE_SUBSCR     
              120  JUMP_BACK            74  'to 74'
              122  POP_BLOCK        
            124_0  COME_FROM_LOOP       68  '68'
          124_126  JUMP_FORWARD       1232  'to 1232'
            128_0  COME_FROM            48  '48'

 L. 284       128  LOAD_FAST                'dt'
              130  LOAD_ATTR                shape
              132  POP_JUMP_IF_FALSE   188  'to 188'

 L. 286       134  LOAD_FAST                'dt'
              136  LOAD_ATTR                base
              138  LOAD_FAST                'dt'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   152  'to 152'

 L. 287       144  LOAD_GLOBAL              TypeError
              146  LOAD_STR                 'Expected base type to be different than parent'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           142  '142'

 L. 289       152  LOAD_FAST                'dt'
              154  LOAD_ATTR                shape
              156  LOAD_FAST                'type_info'
              158  LOAD_STR                 'dims'
              160  STORE_SUBSCR     

 L. 290       162  LOAD_STR                 'H5T_ARRAY'
              164  LOAD_FAST                'type_info'
              166  LOAD_STR                 'class'
              168  STORE_SUBSCR     

 L. 291       170  LOAD_GLOBAL              getTypeItem
              172  LOAD_FAST                'dt'
              174  LOAD_ATTR                base
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  LOAD_FAST                'type_info'
              180  LOAD_STR                 'base'
              182  STORE_SUBSCR     
          184_186  JUMP_FORWARD       1232  'to 1232'
            188_0  COME_FROM           132  '132'

 L. 292       188  LOAD_FAST                'dt'
              190  LOAD_ATTR                kind
              192  LOAD_STR                 'O'
              194  COMPARE_OP               ==
          196_198  POP_JUMP_IF_FALSE   500  'to 500'

 L. 296       200  LOAD_GLOBAL              check_dtype
              202  LOAD_FAST                'dt'
              204  LOAD_ATTR                base
              206  LOAD_CONST               ('vlen',)
              208  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              210  STORE_FAST               'vlen_check'

 L. 297       212  LOAD_FAST                'vlen_check'
              214  LOAD_CONST               None
              216  COMPARE_OP               is-not
              218  POP_JUMP_IF_FALSE   242  'to 242'
              220  LOAD_GLOBAL              isinstance
              222  LOAD_FAST                'vlen_check'
              224  LOAD_GLOBAL              np
              226  LOAD_ATTR                dtype
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  POP_JUMP_IF_FALSE   242  'to 242'

 L. 298       232  LOAD_GLOBAL              np
              234  LOAD_METHOD              dtype
              236  LOAD_FAST                'vlen_check'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               'vlen_check'
            242_0  COME_FROM           230  '230'
            242_1  COME_FROM           218  '218'

 L. 299       242  LOAD_GLOBAL              check_dtype
              244  LOAD_FAST                'dt'
              246  LOAD_ATTR                base
              248  LOAD_CONST               ('ref',)
              250  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              252  STORE_FAST               'ref_check'

 L. 300       254  LOAD_FAST                'vlen_check'
              256  LOAD_GLOBAL              bytes
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   298  'to 298'

 L. 301       264  LOAD_STR                 'H5T_STRING'
              266  LOAD_FAST                'type_info'
              268  LOAD_STR                 'class'
              270  STORE_SUBSCR     

 L. 302       272  LOAD_STR                 'H5T_VARIABLE'
              274  LOAD_FAST                'type_info'
              276  LOAD_STR                 'length'
              278  STORE_SUBSCR     

 L. 303       280  LOAD_STR                 'H5T_CSET_ASCII'
              282  LOAD_FAST                'type_info'
              284  LOAD_STR                 'charSet'
              286  STORE_SUBSCR     

 L. 304       288  LOAD_STR                 'H5T_STR_NULLTERM'
              290  LOAD_FAST                'type_info'
              292  LOAD_STR                 'strPad'
              294  STORE_SUBSCR     
              296  JUMP_FORWARD       1232  'to 1232'
            298_0  COME_FROM           260  '260'

 L. 305       298  LOAD_FAST                'vlen_check'
              300  LOAD_GLOBAL              str
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   342  'to 342'

 L. 306       308  LOAD_STR                 'H5T_STRING'
              310  LOAD_FAST                'type_info'
              312  LOAD_STR                 'class'
              314  STORE_SUBSCR     

 L. 307       316  LOAD_STR                 'H5T_VARIABLE'
              318  LOAD_FAST                'type_info'
              320  LOAD_STR                 'length'
              322  STORE_SUBSCR     

 L. 308       324  LOAD_STR                 'H5T_CSET_UTF8'
              326  LOAD_FAST                'type_info'
              328  LOAD_STR                 'charSet'
              330  STORE_SUBSCR     

 L. 309       332  LOAD_STR                 'H5T_STR_NULLTERM'
              334  LOAD_FAST                'type_info'
              336  LOAD_STR                 'strPad'
              338  STORE_SUBSCR     
              340  JUMP_FORWARD       1232  'to 1232'
            342_0  COME_FROM           304  '304'

 L. 310       342  LOAD_GLOBAL              isinstance
              344  LOAD_FAST                'vlen_check'
              346  LOAD_GLOBAL              np
              348  LOAD_ATTR                dtype
              350  CALL_FUNCTION_2       2  '2 positional arguments'
          352_354  POP_JUMP_IF_FALSE   386  'to 386'

 L. 312       356  LOAD_STR                 'H5T_VLEN'
              358  LOAD_FAST                'type_info'
              360  LOAD_STR                 'class'
              362  STORE_SUBSCR     

 L. 313       364  LOAD_STR                 'H5T_VARIABLE'
              366  LOAD_FAST                'type_info'
              368  LOAD_STR                 'size'
              370  STORE_SUBSCR     

 L. 314       372  LOAD_GLOBAL              getTypeItem
              374  LOAD_FAST                'vlen_check'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  LOAD_FAST                'type_info'
              380  LOAD_STR                 'base'
              382  STORE_SUBSCR     
              384  JUMP_FORWARD       1232  'to 1232'
            386_0  COME_FROM           352  '352'

 L. 315       386  LOAD_FAST                'vlen_check'
              388  LOAD_CONST               None
              390  COMPARE_OP               is-not
          392_394  POP_JUMP_IF_FALSE   414  'to 414'

 L. 317       396  LOAD_GLOBAL              TypeError
              398  LOAD_STR                 'Unknown h5py vlen type: '
              400  LOAD_GLOBAL              str
              402  LOAD_FAST                'vlen_check'
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  BINARY_ADD       
              408  CALL_FUNCTION_1       1  '1 positional argument'
              410  RAISE_VARARGS_1       1  'exception instance'
              412  JUMP_FORWARD       1232  'to 1232'
            414_0  COME_FROM           392  '392'

 L. 318       414  LOAD_FAST                'ref_check'
              416  LOAD_CONST               None
              418  COMPARE_OP               is-not
          420_422  POP_JUMP_IF_FALSE   488  'to 488'

 L. 320       424  LOAD_STR                 'H5T_REFERENCE'
              426  LOAD_FAST                'type_info'
              428  LOAD_STR                 'class'
              430  STORE_SUBSCR     

 L. 323       432  LOAD_GLOBAL              is_reference
              434  LOAD_FAST                'ref_check'
              436  CALL_FUNCTION_1       1  '1 positional argument'
          438_440  POP_JUMP_IF_FALSE   452  'to 452'

 L. 324       442  LOAD_STR                 'H5T_STD_REF_OBJ'
              444  LOAD_FAST                'type_info'
              446  LOAD_STR                 'base'
              448  STORE_SUBSCR     
              450  JUMP_FORWARD        486  'to 486'
            452_0  COME_FROM           438  '438'

 L. 325       452  LOAD_GLOBAL              is_regionreference
              454  LOAD_FAST                'ref_check'
              456  CALL_FUNCTION_1       1  '1 positional argument'
          458_460  POP_JUMP_IF_FALSE   472  'to 472'

 L. 326       462  LOAD_STR                 'H5T_STD_REF_DSETREG'
              464  LOAD_FAST                'type_info'
              466  LOAD_STR                 'base'
              468  STORE_SUBSCR     
              470  JUMP_FORWARD        486  'to 486'
            472_0  COME_FROM           458  '458'

 L. 328       472  LOAD_GLOBAL              TypeError
              474  LOAD_STR                 'unexpected reference type: {}'
              476  LOAD_METHOD              format
              478  LOAD_FAST                'ref_check'
              480  CALL_METHOD_1         1  '1 positional argument'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  RAISE_VARARGS_1       1  'exception instance'
            486_0  COME_FROM           470  '470'
            486_1  COME_FROM           450  '450'
              486  JUMP_FORWARD       1232  'to 1232'
            488_0  COME_FROM           420  '420'

 L. 330       488  LOAD_GLOBAL              TypeError
              490  LOAD_STR                 'unknown object type'
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  RAISE_VARARGS_1       1  'exception instance'
          496_498  JUMP_FORWARD       1232  'to 1232'
            500_0  COME_FROM           196  '196'

 L. 331       500  LOAD_FAST                'dt'
              502  LOAD_ATTR                kind
              504  LOAD_STR                 'V'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   542  'to 542'

 L. 333       512  LOAD_STR                 'H5T_OPAQUE'
              514  LOAD_FAST                'type_info'
              516  LOAD_STR                 'class'
              518  STORE_SUBSCR     

 L. 334       520  LOAD_FAST                'dt'
              522  LOAD_ATTR                itemsize
              524  LOAD_FAST                'type_info'
              526  LOAD_STR                 'size'
              528  STORE_SUBSCR     

 L. 335       530  LOAD_STR                 ''
              532  LOAD_FAST                'type_info'
              534  LOAD_STR                 'tag'
              536  STORE_SUBSCR     
          538_540  JUMP_FORWARD       1232  'to 1232'
            542_0  COME_FROM           508  '508'

 L. 336       542  LOAD_FAST                'dt'
              544  LOAD_ATTR                base
              546  LOAD_ATTR                kind
              548  LOAD_STR                 'S'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   674  'to 674'

 L. 337       556  LOAD_GLOBAL              check_dtype
              558  LOAD_FAST                'dt'
              560  LOAD_ATTR                base
              562  LOAD_CONST               ('ref',)
              564  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              566  STORE_FAST               'ref_check'

 L. 338       568  LOAD_FAST                'ref_check'
              570  LOAD_CONST               None
              572  COMPARE_OP               is-not
          574_576  POP_JUMP_IF_FALSE   636  'to 636'

 L. 340       578  LOAD_STR                 'H5T_REFERENCE'
              580  LOAD_FAST                'type_info'
              582  LOAD_STR                 'class'
              584  STORE_SUBSCR     

 L. 342       586  LOAD_GLOBAL              is_reference
              588  LOAD_FAST                'ref_check'
              590  CALL_FUNCTION_1       1  '1 positional argument'
          592_594  POP_JUMP_IF_FALSE   606  'to 606'

 L. 343       596  LOAD_STR                 'H5T_STD_REF_OBJ'
              598  LOAD_FAST                'type_info'
              600  LOAD_STR                 'base'
              602  STORE_SUBSCR     
              604  JUMP_FORWARD        634  'to 634'
            606_0  COME_FROM           592  '592'

 L. 344       606  LOAD_GLOBAL              is_regionreference
              608  LOAD_FAST                'ref_check'
              610  CALL_FUNCTION_1       1  '1 positional argument'
          612_614  POP_JUMP_IF_FALSE   626  'to 626'

 L. 345       616  LOAD_STR                 'H5T_STD_REF_DSETREG'
              618  LOAD_FAST                'type_info'
              620  LOAD_STR                 'base'
              622  STORE_SUBSCR     
              624  JUMP_FORWARD        634  'to 634'
            626_0  COME_FROM           612  '612'

 L. 347       626  LOAD_GLOBAL              TypeError
              628  LOAD_STR                 'unexpected reference type'
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  RAISE_VARARGS_1       1  'exception instance'
            634_0  COME_FROM           624  '624'
            634_1  COME_FROM           604  '604'
              634  JUMP_FORWARD        644  'to 644'
            636_0  COME_FROM           574  '574'

 L. 350       636  LOAD_STR                 'H5T_STRING'
              638  LOAD_FAST                'type_info'
              640  LOAD_STR                 'class'
              642  STORE_SUBSCR     
            644_0  COME_FROM           634  '634'

 L. 353       644  LOAD_STR                 'H5T_CSET_ASCII'
              646  LOAD_FAST                'type_info'
              648  LOAD_STR                 'charSet'
              650  STORE_SUBSCR     

 L. 354       652  LOAD_FAST                'dt'
              654  LOAD_ATTR                itemsize
              656  LOAD_FAST                'type_info'
              658  LOAD_STR                 'length'
              660  STORE_SUBSCR     

 L. 355       662  LOAD_STR                 'H5T_STR_NULLPAD'
              664  LOAD_FAST                'type_info'
              666  LOAD_STR                 'strPad'
              668  STORE_SUBSCR     
          670_672  JUMP_FORWARD       1232  'to 1232'
            674_0  COME_FROM           552  '552'

 L. 356       674  LOAD_FAST                'dt'
              676  LOAD_ATTR                base
              678  LOAD_ATTR                kind
              680  LOAD_STR                 'U'
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   700  'to 700'

 L. 358       688  LOAD_GLOBAL              TypeError
              690  LOAD_STR                 'Fixed length unicode type is not supported'
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  RAISE_VARARGS_1       1  'exception instance'
          696_698  JUMP_FORWARD       1232  'to 1232'
            700_0  COME_FROM           684  '684'

 L. 360       700  LOAD_FAST                'dt'
              702  LOAD_ATTR                kind
              704  LOAD_STR                 'b'
              706  COMPARE_OP               ==
          708_710  POP_JUMP_IF_FALSE   792  'to 792'

 L. 363       712  LOAD_STR                 'LE'
              714  STORE_FAST               'byteorder'

 L. 364       716  LOAD_FAST                'dt'
              718  LOAD_ATTR                base
              720  LOAD_ATTR                byteorder
              722  LOAD_STR                 '>'
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_FALSE   734  'to 734'

 L. 365       730  LOAD_STR                 'BE'
              732  STORE_FAST               'byteorder'
            734_0  COME_FROM           726  '726'

 L. 368       734  LOAD_CONST               0

 L. 369       736  LOAD_CONST               1
              738  LOAD_CONST               ('FALSE', 'TRUE')
              740  BUILD_CONST_KEY_MAP_2     2 
              742  STORE_FAST               'mapping'

 L. 371       744  LOAD_STR                 'H5T_ENUM'
              746  LOAD_FAST                'type_info'
              748  LOAD_STR                 'class'
              750  STORE_SUBSCR     

 L. 372       752  LOAD_FAST                'mapping'
              754  LOAD_FAST                'type_info'
              756  LOAD_STR                 'mapping'
              758  STORE_SUBSCR     

 L. 373       760  LOAD_STR                 'class'
              762  LOAD_STR                 'H5T_INTEGER'
              764  BUILD_MAP_1           1 
              766  STORE_FAST               'base_info'

 L. 374       768  LOAD_STR                 'H5T_STD_I8'
              770  LOAD_FAST                'byteorder'
              772  BINARY_ADD       
              774  LOAD_FAST                'base_info'
              776  LOAD_STR                 'base'
              778  STORE_SUBSCR     

 L. 375       780  LOAD_FAST                'base_info'
              782  LOAD_FAST                'type_info'
              784  LOAD_STR                 'base'
              786  STORE_SUBSCR     
          788_790  JUMP_FORWARD       1232  'to 1232'
            792_0  COME_FROM           708  '708'

 L. 376       792  LOAD_FAST                'dt'
              794  LOAD_ATTR                kind
              796  LOAD_STR                 'f'
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   884  'to 884'

 L. 378       804  LOAD_STR                 'H5T_FLOAT'
              806  LOAD_FAST                'type_info'
              808  LOAD_STR                 'class'
              810  STORE_SUBSCR     

 L. 379       812  LOAD_STR                 'LE'
              814  STORE_FAST               'byteorder'

 L. 380       816  LOAD_FAST                'dt'
              818  LOAD_ATTR                byteorder
              820  LOAD_STR                 '>'
              822  COMPARE_OP               ==
          824_826  POP_JUMP_IF_FALSE   832  'to 832'

 L. 381       828  LOAD_STR                 'BE'
              830  STORE_FAST               'byteorder'
            832_0  COME_FROM           824  '824'

 L. 382       832  LOAD_FAST                'dt'
              834  LOAD_ATTR                name
              836  LOAD_FAST                'predefined_float_types'
              838  COMPARE_OP               in
          840_842  POP_JUMP_IF_FALSE   866  'to 866'

 L. 384       844  LOAD_FAST                'predefined_float_types'
              846  LOAD_FAST                'dt'
              848  LOAD_ATTR                base
              850  LOAD_ATTR                name
              852  BINARY_SUBSCR    
              854  LOAD_FAST                'byteorder'
              856  BINARY_ADD       
              858  LOAD_FAST                'type_info'
              860  LOAD_STR                 'base'
              862  STORE_SUBSCR     
              864  JUMP_FORWARD       1232  'to 1232'
            866_0  COME_FROM           840  '840'

 L. 386       866  LOAD_GLOBAL              TypeError
              868  LOAD_STR                 'Unexpected floating point type: '
              870  LOAD_FAST                'dt'
              872  LOAD_ATTR                name
              874  BINARY_ADD       
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  RAISE_VARARGS_1       1  'exception instance'
          880_882  JUMP_FORWARD       1232  'to 1232'
            884_0  COME_FROM           800  '800'

 L. 387       884  LOAD_FAST                'dt'
              886  LOAD_ATTR                kind
              888  LOAD_STR                 'i'
              890  COMPARE_OP               ==
          892_894  POP_JUMP_IF_TRUE    908  'to 908'
              896  LOAD_FAST                'dt'
              898  LOAD_ATTR                kind
              900  LOAD_STR                 'u'
              902  COMPARE_OP               ==
          904_906  POP_JUMP_IF_FALSE  1082  'to 1082'
            908_0  COME_FROM           892  '892'

 L. 391       908  LOAD_STR                 'LE'
              910  STORE_FAST               'byteorder'

 L. 392       912  LOAD_FAST                'dt'
              914  LOAD_ATTR                base
              916  LOAD_ATTR                byteorder
              918  LOAD_STR                 '>'
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   930  'to 930'

 L. 393       926  LOAD_STR                 'BE'
              928  STORE_FAST               'byteorder'
            930_0  COME_FROM           922  '922'

 L. 397       930  LOAD_GLOBAL              check_dtype
              932  LOAD_FAST                'dt'
              934  LOAD_CONST               ('enum',)
              936  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              938  STORE_FAST               'mapping'

 L. 399       940  LOAD_FAST                'mapping'
          942_944  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 401       946  LOAD_STR                 'H5T_ENUM'
              948  LOAD_FAST                'type_info'
              950  LOAD_STR                 'class'
              952  STORE_SUBSCR     

 L. 402       954  LOAD_FAST                'mapping'
              956  LOAD_FAST                'type_info'
              958  LOAD_STR                 'mapping'
              960  STORE_SUBSCR     

 L. 403       962  LOAD_FAST                'dt'
              964  LOAD_ATTR                name
              966  LOAD_FAST                'predefined_int_types'
              968  COMPARE_OP               not-in
          970_972  POP_JUMP_IF_FALSE   988  'to 988'

 L. 404       974  LOAD_GLOBAL              TypeError
              976  LOAD_STR                 'Unexpected integer type: '
              978  LOAD_FAST                'dt'
              980  LOAD_ATTR                name
              982  BINARY_ADD       
              984  CALL_FUNCTION_1       1  '1 positional argument'
              986  RAISE_VARARGS_1       1  'exception instance'
            988_0  COME_FROM           970  '970'

 L. 406       988  LOAD_STR                 'class'
              990  LOAD_STR                 'H5T_INTEGER'
              992  BUILD_MAP_1           1 
              994  STORE_FAST               'base_info'

 L. 407       996  LOAD_FAST                'predefined_int_types'
              998  LOAD_FAST                'dt'
             1000  LOAD_ATTR                name
             1002  BINARY_SUBSCR    
             1004  LOAD_FAST                'byteorder'
             1006  BINARY_ADD       
             1008  LOAD_FAST                'base_info'
             1010  LOAD_STR                 'base'
             1012  STORE_SUBSCR     

 L. 408      1014  LOAD_FAST                'base_info'
             1016  LOAD_FAST                'type_info'
             1018  LOAD_STR                 'base'
             1020  STORE_SUBSCR     
             1022  JUMP_FORWARD       1080  'to 1080'
           1024_0  COME_FROM           942  '942'

 L. 410      1024  LOAD_STR                 'H5T_INTEGER'
             1026  LOAD_FAST                'type_info'
             1028  LOAD_STR                 'class'
           1030_0  COME_FROM           296  '296'
             1030  STORE_SUBSCR     

 L. 411      1032  LOAD_FAST                'dt'
             1034  LOAD_ATTR                name
             1036  STORE_FAST               'base_name'

 L. 413      1038  LOAD_FAST                'dt'
             1040  LOAD_ATTR                name
             1042  LOAD_FAST                'predefined_int_types'
             1044  COMPARE_OP               not-in
         1046_1048  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 414      1050  LOAD_GLOBAL              TypeError
             1052  LOAD_STR                 'Unexpected integer type: '
             1054  LOAD_FAST                'dt'
             1056  LOAD_ATTR                name
             1058  BINARY_ADD       
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  RAISE_VARARGS_1       1  'exception instance'
           1064_0  COME_FROM          1046  '1046'

 L. 416      1064  LOAD_FAST                'predefined_int_types'
             1066  LOAD_FAST                'base_name'
             1068  BINARY_SUBSCR    
             1070  LOAD_FAST                'byteorder'
             1072  BINARY_ADD       
           1074_0  COME_FROM           340  '340'
             1074  LOAD_FAST                'type_info'
             1076  LOAD_STR                 'base'
             1078  STORE_SUBSCR     
           1080_0  COME_FROM          1022  '1022'
             1080  JUMP_FORWARD       1232  'to 1232'
           1082_0  COME_FROM           904  '904'

 L. 418      1082  LOAD_FAST                'dt'
             1084  LOAD_ATTR                kind
             1086  LOAD_STR                 'c'
             1088  COMPARE_OP               ==
         1090_1092  POP_JUMP_IF_FALSE  1218  'to 1218'

 L. 419      1094  LOAD_STR                 'H5T_COMPOUND'
             1096  LOAD_FAST                'type_info'
             1098  LOAD_STR                 'class'
             1100  STORE_SUBSCR     

 L. 420      1102  LOAD_FAST                'dt'
             1104  LOAD_ATTR                name
             1106  LOAD_STR                 'complex64'
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 421      1114  LOAD_STR                 'H5T_IEEE_F32'
             1116  STORE_FAST               'base_type'
           1118_0  COME_FROM           384  '384'
             1118  JUMP_FORWARD       1152  'to 1152'
           1120_0  COME_FROM          1110  '1110'

 L. 422      1120  LOAD_FAST                'dt'
             1122  LOAD_ATTR                name
             1124  LOAD_STR                 'complex128'
             1126  COMPARE_OP               ==
         1128_1130  POP_JUMP_IF_FALSE  1138  'to 1138'

 L. 423      1132  LOAD_STR                 'H5T_IEEE_F64'
             1134  STORE_FAST               'base_type'
             1136  JUMP_FORWARD       1152  'to 1152'
           1138_0  COME_FROM          1128  '1128'

 L. 425      1138  LOAD_GLOBAL              TypeError
             1140  LOAD_STR                 'Unexpected complex type: '
             1142  LOAD_FAST                'dt'
             1144  LOAD_ATTR                name
           1146_0  COME_FROM           412  '412'
             1146  BINARY_ADD       
             1148  CALL_FUNCTION_1       1  '1 positional argument'
             1150  RAISE_VARARGS_1       1  'exception instance'
           1152_0  COME_FROM          1136  '1136'
           1152_1  COME_FROM          1118  '1118'

 L. 426      1152  LOAD_STR                 'LE'
             1154  STORE_FAST               'byteorder'

 L. 427      1156  LOAD_FAST                'dt'
             1158  LOAD_ATTR                byteorder
             1160  LOAD_STR                 '>'
             1162  COMPARE_OP               ==
         1164_1166  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 428      1168  LOAD_STR                 'BE'
             1170  STORE_FAST               'byteorder'
           1172_0  COME_FROM          1164  '1164'

 L. 429      1172  LOAD_STR                 'r'

 L. 430      1174  LOAD_STR                 'H5T_FLOAT'

 L. 431      1176  LOAD_FAST                'base_type'
             1178  LOAD_FAST                'byteorder'
             1180  BINARY_ADD       
             1182  LOAD_CONST               ('class', 'base')
             1184  BUILD_CONST_KEY_MAP_2     2 
             1186  LOAD_CONST               ('name', 'type')
             1188  BUILD_CONST_KEY_MAP_2     2 

 L. 432      1190  LOAD_STR                 'i'

 L. 433      1192  LOAD_STR                 'H5T_FLOAT'

 L. 434      1194  LOAD_FAST                'base_type'
             1196  LOAD_FAST                'byteorder'
             1198  BINARY_ADD       
             1200  LOAD_CONST               ('class', 'base')
             1202  BUILD_CONST_KEY_MAP_2     2 
             1204  LOAD_CONST               ('name', 'type')
             1206  BUILD_CONST_KEY_MAP_2     2 
             1208  BUILD_LIST_2          2 
             1210  LOAD_FAST                'type_info'
             1212  LOAD_STR                 'fields'
           1214_0  COME_FROM           864  '864'
             1214  STORE_SUBSCR     
             1216  JUMP_FORWARD       1232  'to 1232'
           1218_0  COME_FROM          1090  '1090'

 L. 438      1218  LOAD_GLOBAL              TypeError
           1220_0  COME_FROM           486  '486'
             1220  LOAD_STR                 'unexpected dtype kind: '
             1222  LOAD_FAST                'dt'
             1224  LOAD_ATTR                kind
             1226  BINARY_ADD       
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  RAISE_VARARGS_1       1  'exception instance'
           1232_0  COME_FROM          1216  '1216'
           1232_1  COME_FROM          1080  '1080'
           1232_2  COME_FROM           880  '880'
           1232_3  COME_FROM           788  '788'
           1232_4  COME_FROM           696  '696'
           1232_5  COME_FROM           670  '670'
           1232_6  COME_FROM           538  '538'
           1232_7  COME_FROM           496  '496'
           1232_8  COME_FROM           184  '184'
           1232_9  COME_FROM           124  '124'

 L. 440      1232  LOAD_FAST                'type_info'
             1234  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1030_0


def getItemSize(typeItem):
    if isinstance(typeItem, str) or isinstance(typeItem, bytes):
        for type_prefix in ('H5T_STD_I', 'H5T_STD_U', 'H5T_IEEE_F'):
            if typeItem.startswith(type_prefix):
                num_bits = typeItem[len(type_prefix):]
                if num_bits[-2:] in ('LE', 'BE'):
                    num_bits = num_bits[:-2]
                try:
                    return int(num_bits) // 8
                except ValueError:
                    raise TypeError('Invalid Type')

        raise TypeError('Invalid Type')
    elif not isinstance(typeItem, dict):
        raise TypeError('invalid type')
    else:
        item_size = 0
        if 'class' not in typeItem:
            raise KeyError("'class' not provided")
        else:
            typeClass = typeItem['class']
            if typeClass == 'H5T_INTEGER':
                if 'base' not in typeItem:
                    raise KeyError("'base' not provided")
                item_size = getItemSize(typeItem['base'])
            else:
                if typeClass == 'H5T_FLOAT':
                    if 'base' not in typeItem:
                        raise KeyError("'base' not provided")
                    item_size = getItemSize(typeItem['base'])
                else:
                    if typeClass == 'H5T_STRING':
                        if 'length' not in typeItem:
                            raise KeyError("'length' not provided")
                        item_size = typeItem['length']
                    else:
                        if typeClass == 'H5T_VLEN':
                            item_size = 'H5T_VARIABLE'
                        else:
                            if typeClass == 'H5T_OPAQUE':
                                if 'size' not in typeItem:
                                    raise KeyError("'size' not provided")
                                item_size = int(typeItem['size'])
                            else:
                                if typeClass == 'H5T_ARRAY':
                                    if 'dims' not in typeItem:
                                        raise KeyError("'dims' must be provided for array types")
                                    if 'base' not in typeItem:
                                        raise KeyError("'base' not provided")
                                    item_size = getItemSize(typeItem['base'])
                                else:
                                    if typeClass == 'H5T_ENUM':
                                        if 'base' not in typeItem:
                                            raise KeyError("'base' must be provided for enum types")
                                        item_size = getItemSize(typeItem['base'])
                                    else:
                                        if typeClass == 'H5T_REFERENCE':
                                            item_size = 'H5T_VARIABLE'
                                        else:
                                            if typeClass == 'H5T_COMPOUND':
                                                if 'fields' not in typeItem:
                                                    raise KeyError("'fields' not provided for compound type")
                                                else:
                                                    fields = typeItem['fields']
                                                    if not isinstance(fields, list):
                                                        raise TypeError("Type Error: expected list type for 'fields'")
                                                    assert fields, "no 'field' elements provided"
                                                for field in fields:
                                                    if not isinstance(field, dict):
                                                        raise TypeError('Expected dictionary type for field')
                                                    if 'type' not in field:
                                                        raise KeyError("'type' missing from field")
                                                    subtype_size = getItemSize(field['type'])
                                                    if subtype_size == 'H5T_VARIABLE':
                                                        item_size = 'H5T_VARIABLE'
                                                        break
                                                    item_size += subtype_size

                                            else:
                                                raise TypeError('Invalid type class')
    if 'dims' in typeItem:
        if isinstance(item_size, int):
            dims = typeItem['dims']
            for dim in dims:
                item_size *= dim

    return item_size


def getNumpyTypename(hdf5TypeName, typeClass=None):
    predefined_int_types = {'H5T_STD_I8':'i1', 
     'H5T_STD_U8':'u1', 
     'H5T_STD_I16':'i2', 
     'H5T_STD_U16':'u2', 
     'H5T_STD_I32':'i4', 
     'H5T_STD_U32':'u4', 
     'H5T_STD_I64':'i8', 
     'H5T_STD_U64':'u8'}
    predefined_float_types = {'H5T_IEEE_F16':'f2', 
     'H5T_IEEE_F32':'f4', 
     'H5T_IEEE_F64':'f8'}
    if len(hdf5TypeName) < 3:
        raise Exception('Type Error: invalid typename: ')
    endian = '<'
    key = hdf5TypeName
    if hdf5TypeName.endswith('LE'):
        key = hdf5TypeName[:-2]
    else:
        if hdf5TypeName.endswith('BE'):
            key = hdf5TypeName[:-2]
            endian = '>'
        elif not key in predefined_int_types or typeClass == None or typeClass == 'H5T_INTEGER':
            return endian + predefined_int_types[key]
        if key in predefined_float_types:
            if typeClass == None or typeClass == 'H5T_FLOAT':
                return endian + predefined_float_types[key]
        raise TypeError('Type Error: invalid type')


def createBaseDataType(typeItem):
    dtRet = None
    if type(typeItem) == str or type(typeItem) == str:
        dtName = getNumpyTypename(typeItem)
        dtRet = np.dtype(dtName)
        return dtRet
    if not isinstance(typeItem, dict):
        raise TypeError('Type Error: invalid type')
    if 'class' not in typeItem:
        raise KeyError("'class' not provided")
    typeClass = typeItem['class']
    dims = ''
    if 'dims' in typeItem:
        dims = None
        if isinstance(typeItem['dims'], int):
            dims = typeItem['dims']
        else:
            if not (isinstance(typeItem['dims'], list) or isinstance(typeItem['dims'], tuple)):
                raise TypeError('expected list or integer for dims')
            else:
                dims = typeItem['dims']
        dims = str(tuple(dims))
    if typeClass == 'H5T_INTEGER':
        if 'base' not in typeItem:
            raise KeyError("'base' not provided")
        baseType = getNumpyTypename((typeItem['base']), typeClass='H5T_INTEGER')
        dtRet = np.dtype(dims + baseType)
    else:
        if typeClass == 'H5T_FLOAT':
            if 'base' not in typeItem:
                raise KeyError("'base' not provided")
            baseType = getNumpyTypename((typeItem['base']), typeClass='H5T_FLOAT')
            dtRet = np.dtype(dims + baseType)
        else:
            if typeClass == 'H5T_STRING':
                if 'length' not in typeItem:
                    raise KeyError("'length' not provided")
                if 'charSet' not in typeItem:
                    raise KeyError("'charSet' not provided")
                if typeItem['length'] == 'H5T_VARIABLE':
                    if dims:
                        raise TypeError('ArrayType is not supported for variable len types')
                    elif typeItem['charSet'] == 'H5T_CSET_ASCII':
                        dtRet = special_dtype(vlen=bytes)
                    else:
                        if typeItem['charSet'] == 'H5T_CSET_UTF8':
                            dtRet = special_dtype(vlen=str)
                        else:
                            raise TypeError("unexpected 'charSet' value")
                else:
                    nStrSize = typeItem['length']
                    if not isinstance(nStrSize, int):
                        raise TypeError("expecting integer value for 'length'")
                    else:
                        type_code = None
                        if typeItem['charSet'] == 'H5T_CSET_ASCII':
                            type_code = 'S'
                        else:
                            if typeItem['charSet'] == 'H5T_CSET_UTF8':
                                raise TypeError('fixed-width unicode strings are not supported')
                            else:
                                raise TypeError("unexpected 'charSet' value")
                    dtRet = np.dtype(dims + type_code + str(nStrSize))
            else:
                if typeClass == 'H5T_VLEN':
                    if dims:
                        raise TypeError('ArrayType is not supported for variable len types')
                    if 'base' not in typeItem:
                        raise KeyError("'base' not provided")
                    baseType = createBaseDataType(typeItem['base'])
                    dtRet = special_dtype(vlen=(np.dtype(baseType)))
                else:
                    if typeClass == 'H5T_OPAQUE':
                        if dims:
                            raise TypeError('Opaque Type is not supported for variable len types')
                        if 'size' not in typeItem:
                            raise KeyError("'size' not provided")
                        nSize = int(typeItem['size'])
                        if nSize <= 0:
                            raise TypeError("'size' must be non-negative")
                        dtRet = np.dtype('V' + str(nSize))
                    else:
                        if typeClass == 'H5T_ARRAY':
                            if not dims:
                                raise KeyError("'dims' must be provided for array types")
                            else:
                                if 'base' not in typeItem:
                                    raise KeyError("'base' not provided")
                                arrayBaseType = typeItem['base']
                                if isinstance(arrayBaseType, dict):
                                    if 'class' not in arrayBaseType:
                                        raise KeyError("'class' not provided for array base type")
                                    if arrayBaseType['class'] not in ('H5T_INTEGER',
                                                                      'H5T_FLOAT',
                                                                      'H5T_STRING'):
                                        raise TypeError('Array Type base type must be integer, float, or string')
                                    baseType = createDataType(arrayBaseType)
                                    metadata = None
                                    if baseType.metadata:
                                        metadata = dict(baseType.metadata)
                                        dtRet = np.dtype((dims + baseType.str), metadata=metadata)
                                else:
                                    dtRet = np.dtype(dims + baseType.str)
                            return dtRet
                        if typeClass == 'H5T_REFERENCE':
                            if 'base' not in typeItem:
                                raise KeyError("'base' not provided")
                            elif typeItem['base'] == 'H5T_STD_REF_OBJ':
                                dtRet = special_dtype(ref=Reference)
                            else:
                                if typeItem['base'] == 'H5T_STD_REF_DSETREG':
                                    dtRet = special_dtype(ref=RegionReference)
                                else:
                                    raise TypeError('Invalid base type for reference type')
                        else:
                            if typeClass == 'H5T_ENUM':
                                if 'base' not in typeItem:
                                    raise KeyError("Expected 'base' to be provided for enum type")
                                else:
                                    base_json = typeItem['base']
                                    if 'class' not in base_json:
                                        raise KeyError('Expected class field in base type')
                                    if base_json['class'] != 'H5T_INTEGER':
                                        raise TypeError('Only integer base types can be used with enum type')
                                    if 'mapping' not in typeItem:
                                        raise KeyError("'mapping' not provided for enum type")
                                    mapping = typeItem['mapping']
                                    if len(mapping) == 0:
                                        raise KeyError('empty enum map')
                                    dt = createBaseDataType(base_json)
                                    if dt.kind == 'i' and dt.name == 'int8' and len(mapping) == 2 and 'TRUE' in mapping and 'FALSE' in mapping:
                                        dtRet = np.dtype('bool')
                                    else:
                                        dtRet = special_dtype(enum=(dt, mapping))
                            else:
                                raise TypeError('Invalid type class')
    return dtRet


def createDataType(typeItem):
    dtRet = None
    if type(typeItem) in [str, bytes]:
        dtName = getNumpyTypename(typeItem)
        dtRet = np.dtype(dtName)
        return dtRet
    if type(typeItem) != dict:
        raise TypeError('invalid type')
    else:
        if 'class' not in typeItem:
            raise KeyError("'class' not provided")
        typeClass = typeItem['class']
        if typeClass == 'H5T_COMPOUND':
            if 'fields' not in typeItem:
                raise KeyError("'fields' not provided for compound type")
            else:
                fields = typeItem['fields']
                if type(fields) is not list:
                    raise TypeError("Type Error: expected list type for 'fields'")
                assert fields, "no 'field' elements provided"
            subtypes = []
            for field in fields:
                if type(field) != dict:
                    raise TypeError('Expected dictionary type for field')
                if 'name' not in field:
                    raise KeyError("'name' missing from field")
                if 'type' not in field:
                    raise KeyError("'type' missing from field")
                field_name = field['name']
                if isinstance(field_name, str):
                    try:
                        field_name.encode('ascii')
                    except UnicodeDecodeError:
                        raise TypeError('non-ascii field name not allowed')

                dt = createDataType(field['type'])
                if dt is None:
                    raise Exception('unexpected error')
                subtypes.append((field['name'], dt))

            dtRet = np.dtype(subtypes)
        else:
            dtRet = createBaseDataType(typeItem)
    return dtRet