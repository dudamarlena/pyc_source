# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/attrs.py
# Compiled at: 2019-12-23 12:02:32
# Size of source mod 2**32: 13777 bytes
"""
    Implements high-level operations for attributes.

    Provides the AttributeManager class, available on high-level objects
    as <obj>.attrs.
"""
from __future__ import absolute_import
import numpy, json
from . import base
from .base import jsonToArray
from .datatype import Datatype
from .objectid import GroupID, DatasetID, TypeID
from .h5type import getTypeItem, createDataType, special_dtype, Reference

class AttributeManager(base.MutableMappingHDF5, base.CommonStateObject):
    __doc__ = "\n        Allows dictionary-style access to an HDF5 object's attributes.\n\n        These are created exclusively by the library and are available as\n        a Python attribute at <object>.attrs\n\n        Like Group objects, attributes provide a minimal dictionary-\n        style interface.  Anything which can be reasonably converted to a\n        Numpy array or Numpy scalar can be stored.\n\n        Attributes are automatically created on assignment with the\n        syntax <obj>.attrs[name] = value, with the HDF5 type automatically\n        deduced from the value.  Existing attributes are overwritten.\n\n        To modify an existing attribute while preserving its type, use the\n        method modify().  To specify an attribute of a particular type and\n        shape, use create().\n    "

    def __init__(self, parent):
        """ Private constructor.
        """
        self._parent = parent
        if isinstance(parent.id, GroupID):
            self._req_prefix = '/groups/' + parent.id.uuid + '/attributes/'
        else:
            if isinstance(parent.id, TypeID):
                self._req_prefix = '/datatypes/' + parent.id.uuid + '/attributes/'
            else:
                if isinstance(parent.id, DatasetID):
                    self._req_prefix = '/datasets/' + parent.id.uuid + '/attributes/'
                else:
                    self._req_prefix = '<unknown>'
        objdb = self._parent.id.http_conn.getObjDb()
        if objdb:
            objid = self._parent.id.uuid
            if objid not in objdb:
                raise IOError('Expected to find {} in objdb'.format(objid))
            obj_json = objdb[objid]
            self._objdb_attributes = obj_json['attributes']
        else:
            self._objdb_attributes = None

    def _bytesArrayToList(self, data):
        """
        Convert list that may contain bytes type elements to list of string
        elements
        """
        text_types = (
         bytes, str)
        if isinstance(data, text_types):
            is_list = False
        else:
            if isinstance(data, (numpy.ndarray, numpy.generic)):
                if len(data.shape) == 0:
                    is_list = False
                    data = data.tolist()
                    if type(data) in (list, tuple):
                        is_list = True
                    else:
                        is_list = False
                else:
                    is_list = True
            elif isinstance(data, list) or isinstance(data, tuple):
                is_list = True
            else:
                is_list = False
        if is_list:
            out = []
            for item in data:
                out.append(self._bytesArrayToList(item))

        else:
            if isinstance(data, bytes):
                out = data.decode('utf-8')
            else:
                out = data
        return out

    def __getitem__(self, name):
        """ Read the value of an attribute.
        """
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if self._objdb_attributes is not None:
            if name not in self._objdb_attributes:
                raise KeyError
            attr_json = self._objdb_attributes[name]
        else:
            req = self._req_prefix + name
            try:
                attr_json = self._parent.GET(req)
            except IOError:
                raise KeyError

            shape_json = attr_json['shape']
            type_json = attr_json['type']
            if shape_json['class'] == 'H5S_NULL':
                raise IOError('Empty attributes cannot be read')
            else:
                value_json = attr_json['value']
                dtype = createDataType(type_json)
                if 'dims' in shape_json:
                    shape = shape_json['dims']
                else:
                    shape = ()
            htype = dtype
            if dtype.subdtype is not None:
                subdtype, subshape = dtype.subdtype
                shape = shape + subshape
                dtype = subdtype
            arr = jsonToArray(shape, htype, value_json)
            if len(arr.shape) == 0:
                return arr[()]
            return arr

    def __setitem__(self, name, value):
        """ Set a new attribute, overwriting any existing attribute.

        The type and shape of the attribute are determined from the data.  To
        use a specific type or shape, or to preserve the type of an attribute,
        use the methods create() and modify().
        """
        self.create(name, data=value, dtype=(base.guess_dtype(value)))

    def __delitem__(self, name):
        """ Delete an attribute (which must already exist). """
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        req = self._req_prefix + name
        self._parent.DELETE(req)

    def create--- This code section failed: ---

 L. 192         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _parent
                4  LOAD_ATTR                log
                6  LOAD_METHOD              info
                8  LOAD_STR                 'attrs.create({})'
               10  LOAD_METHOD              format
               12  LOAD_FAST                'name'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L. 196        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'data'
               24  LOAD_GLOBAL              Reference
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 197        30  LOAD_GLOBAL              special_dtype
               32  LOAD_GLOBAL              Reference
               34  LOAD_CONST               ('ref',)
               36  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               38  STORE_FAST               'dtype'
             40_0  COME_FROM            28  '28'

 L. 198        40  LOAD_GLOBAL              numpy
               42  LOAD_ATTR                asarray
               44  LOAD_FAST                'data'
               46  LOAD_FAST                'dtype'
               48  LOAD_STR                 'C'
               50  LOAD_CONST               ('dtype', 'order')
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'data'

 L. 200        56  LOAD_FAST                'shape'
               58  LOAD_CONST               None
               60  COMPARE_OP               is
               62  POP_JUMP_IF_FALSE    70  'to 70'

 L. 201        64  LOAD_FAST                'data'
               66  LOAD_ATTR                shape
               68  STORE_FAST               'shape'
             70_0  COME_FROM            62  '62'

 L. 203        70  LOAD_CONST               None
               72  STORE_FAST               'use_htype'

 L. 206        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'dtype'
               78  LOAD_GLOBAL              Datatype
               80  CALL_FUNCTION_2       2  '2 positional arguments'
               82  POP_JUMP_IF_FALSE   196  'to 196'

 L. 207        84  LOAD_FAST                'dtype'
               86  LOAD_ATTR                id
               88  STORE_FAST               'use_htype'

 L. 208        90  LOAD_FAST                'dtype'
               92  LOAD_ATTR                dtype
               94  STORE_FAST               'dtype'

 L. 211        96  LOAD_FAST                'data'
               98  LOAD_ATTR                dtype
              100  LOAD_ATTR                kind
              102  LOAD_STR                 'c'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   246  'to 246'

 L. 212       108  LOAD_FAST                'dtype'
              110  LOAD_ATTR                names
              112  LOAD_CONST               None
              114  COMPARE_OP               is
              116  POP_JUMP_IF_TRUE    180  'to 180'

 L. 213       118  LOAD_FAST                'dtype'
              120  LOAD_ATTR                names
              122  LOAD_CONST               ('r', 'i')
              124  COMPARE_OP               !=
              126  POP_JUMP_IF_TRUE    180  'to 180'

 L. 214       128  LOAD_GLOBAL              any
              130  LOAD_GENEXPR             '<code_object <genexpr>>'
              132  LOAD_STR                 'AttributeManager.create.<locals>.<genexpr>'
              134  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              136  LOAD_FAST                'dtype'
              138  LOAD_ATTR                fields
              140  LOAD_METHOD              values
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  GET_ITER         
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  POP_JUMP_IF_TRUE    180  'to 180'

 L. 215       152  LOAD_FAST                'dtype'
              154  LOAD_ATTR                fields
              156  LOAD_STR                 'r'
              158  BINARY_SUBSCR    
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'dtype'
              166  LOAD_ATTR                fields
              168  LOAD_STR                 'i'
              170  BINARY_SUBSCR    
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   246  'to 246'
            180_0  COME_FROM           150  '150'
            180_1  COME_FROM           126  '126'
            180_2  COME_FROM           116  '116'

 L. 216       180  LOAD_GLOBAL              TypeError

 L. 217       182  LOAD_STR                 'Wrong committed datatype for complex numbers: %s'

 L. 218       184  LOAD_FAST                'dtype'
              186  LOAD_ATTR                name
              188  BINARY_MODULO    
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  RAISE_VARARGS_1       1  'exception instance'
              194  JUMP_FORWARD        246  'to 246'
            196_0  COME_FROM            82  '82'

 L. 219       196  LOAD_FAST                'dtype'
              198  LOAD_CONST               None
              200  COMPARE_OP               is
              202  POP_JUMP_IF_FALSE   236  'to 236'

 L. 220       204  LOAD_FAST                'data'
              206  LOAD_ATTR                dtype
              208  LOAD_ATTR                kind
              210  LOAD_STR                 'U'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L. 222       216  LOAD_GLOBAL              special_dtype
              218  LOAD_GLOBAL              str
              220  LOAD_CONST               ('vlen',)
              222  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              224  STORE_FAST               'dtype'
              226  JUMP_ABSOLUTE       246  'to 246'
            228_0  COME_FROM           214  '214'

 L. 224       228  LOAD_FAST                'data'
              230  LOAD_ATTR                dtype
              232  STORE_FAST               'dtype'
              234  JUMP_FORWARD        246  'to 246'
            236_0  COME_FROM           202  '202'

 L. 226       236  LOAD_GLOBAL              numpy
              238  LOAD_METHOD              dtype
              240  LOAD_FAST                'dtype'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               'dtype'
            246_0  COME_FROM           234  '234'
            246_1  COME_FROM           194  '194'
            246_2  COME_FROM           178  '178'
            246_3  COME_FROM           106  '106'

 L. 231       246  LOAD_FAST                'dtype'
              248  LOAD_ATTR                subdtype
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   338  'to 338'

 L. 233       258  LOAD_FAST                'dtype'
              260  LOAD_ATTR                subdtype
              262  UNPACK_SEQUENCE_2     2 
              264  STORE_FAST               'subdtype'
              266  STORE_FAST               'subshape'

 L. 236       268  LOAD_FAST                'shape'
              270  LOAD_GLOBAL              len
              272  LOAD_FAST                'subshape'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  UNARY_NEGATIVE   
              278  LOAD_CONST               None
              280  BUILD_SLICE_2         2 
              282  BINARY_SUBSCR    
              284  LOAD_FAST                'subshape'
              286  COMPARE_OP               !=
          288_290  POP_JUMP_IF_FALSE   308  'to 308'

 L. 237       292  LOAD_GLOBAL              ValueError
              294  LOAD_STR                 'Array dtype shape %s is incompatible with data shape %s'
              296  LOAD_FAST                'subshape'
              298  LOAD_FAST                'shape'
              300  BUILD_TUPLE_2         2 
              302  BINARY_MODULO    
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           288  '288'

 L. 240       308  LOAD_FAST                'shape'
              310  LOAD_CONST               0
              312  LOAD_GLOBAL              len
              314  LOAD_FAST                'shape'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  LOAD_GLOBAL              len
              320  LOAD_FAST                'subshape'
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  BINARY_SUBTRACT  
              326  BUILD_SLICE_2         2 
              328  BINARY_SUBSCR    
              330  STORE_FAST               'shape'

 L. 241       332  LOAD_FAST                'subdtype'
              334  STORE_FAST               'dtype'
              336  JUMP_FORWARD        392  'to 392'
            338_0  COME_FROM           254  '254'

 L. 246       338  LOAD_GLOBAL              numpy
              340  LOAD_METHOD              product
              342  LOAD_FAST                'shape'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  LOAD_GLOBAL              numpy
              348  LOAD_METHOD              product
              350  LOAD_FAST                'data'
              352  LOAD_ATTR                shape
              354  CALL_METHOD_1         1  '1 positional argument'
              356  COMPARE_OP               !=
          358_360  POP_JUMP_IF_FALSE   370  'to 370'

 L. 247       362  LOAD_GLOBAL              ValueError
              364  LOAD_STR                 'Shape of new attribute conflicts with shape of data'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  RAISE_VARARGS_1       1  'exception instance'
            370_0  COME_FROM           358  '358'

 L. 249       370  LOAD_FAST                'shape'
              372  LOAD_FAST                'data'
              374  LOAD_ATTR                shape
              376  COMPARE_OP               !=
          378_380  POP_JUMP_IF_FALSE   392  'to 392'

 L. 250       382  LOAD_FAST                'data'
              384  LOAD_METHOD              reshape
              386  LOAD_FAST                'shape'
              388  CALL_METHOD_1         1  '1 positional argument'
              390  STORE_FAST               'data'
            392_0  COME_FROM           378  '378'
            392_1  COME_FROM           336  '336'

 L. 253       392  LOAD_GLOBAL              numpy
              394  LOAD_ATTR                asarray
              396  LOAD_FAST                'data'
              398  LOAD_FAST                'dtype'
              400  LOAD_CONST               ('dtype',)
              402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              404  STORE_FAST               'data'

 L. 256       406  LOAD_FAST                'use_htype'
              408  LOAD_CONST               None
              410  COMPARE_OP               is
          412_414  POP_JUMP_IF_FALSE   444  'to 444'

 L. 257       416  LOAD_GLOBAL              getTypeItem
              418  LOAD_FAST                'dtype'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  STORE_FAST               'type_json'

 L. 258       424  LOAD_FAST                'self'
              426  LOAD_ATTR                _parent
              428  LOAD_ATTR                log
              430  LOAD_METHOD              debug
              432  LOAD_STR                 'attrs.create type_json: {}'
              434  LOAD_METHOD              format
              436  LOAD_FAST                'type_json'
              438  CALL_METHOD_1         1  '1 positional argument'
              440  CALL_METHOD_1         1  '1 positional argument'
              442  POP_TOP          
            444_0  COME_FROM           412  '412'

 L. 263       444  LOAD_FAST                'self'
              446  LOAD_ATTR                _req_prefix
              448  LOAD_FAST                'name'
              450  BINARY_ADD       
              452  STORE_FAST               'req'

 L. 264       454  BUILD_MAP_0           0 
              456  STORE_FAST               'body'

 L. 265       458  LOAD_FAST                'type_json'
              460  LOAD_FAST                'body'
              462  LOAD_STR                 'type'
              464  STORE_SUBSCR     

 L. 266       466  LOAD_FAST                'shape'
              468  LOAD_FAST                'body'
              470  LOAD_STR                 'shape'
              472  STORE_SUBSCR     

 L. 267       474  LOAD_FAST                'data'
              476  LOAD_ATTR                dtype
              478  LOAD_ATTR                kind
              480  LOAD_STR                 'c'
              482  COMPARE_OP               !=
          484_486  POP_JUMP_IF_FALSE   504  'to 504'

 L. 268       488  LOAD_FAST                'self'
              490  LOAD_METHOD              _bytesArrayToList
              492  LOAD_FAST                'data'
              494  CALL_METHOD_1         1  '1 positional argument'
              496  LOAD_FAST                'body'
              498  LOAD_STR                 'value'
              500  STORE_SUBSCR     
              502  JUMP_FORWARD        572  'to 572'
            504_0  COME_FROM           484  '484'

 L. 271       504  LOAD_GLOBAL              createDataType
              506  LOAD_FAST                'type_json'
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  STORE_FAST               'special_dt'

 L. 272       512  LOAD_GLOBAL              numpy
              514  LOAD_ATTR                empty
              516  LOAD_FAST                'data'
              518  LOAD_ATTR                shape
              520  LOAD_FAST                'special_dt'
              522  LOAD_CONST               ('shape', 'dtype')
              524  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              526  STORE_FAST               'tmp'

 L. 273       528  LOAD_FAST                'data'
              530  LOAD_ATTR                real
              532  LOAD_FAST                'tmp'
              534  LOAD_STR                 'r'
              536  STORE_SUBSCR     

 L. 274       538  LOAD_FAST                'data'
              540  LOAD_ATTR                imag
              542  LOAD_FAST                'tmp'
              544  LOAD_STR                 'i'
              546  STORE_SUBSCR     

 L. 275       548  LOAD_GLOBAL              json
              550  LOAD_METHOD              loads
              552  LOAD_GLOBAL              json
              554  LOAD_METHOD              dumps
              556  LOAD_FAST                'tmp'
              558  LOAD_METHOD              tolist
              560  CALL_METHOD_0         0  '0 positional arguments'
              562  CALL_METHOD_1         1  '1 positional argument'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  LOAD_FAST                'body'
              568  LOAD_STR                 'value'
              570  STORE_SUBSCR     
            572_0  COME_FROM           502  '502'

 L. 277       572  SETUP_EXCEPT        594  'to 594'

 L. 278       574  LOAD_FAST                'self'
              576  LOAD_ATTR                _parent
              578  LOAD_ATTR                PUT
              580  LOAD_FAST                'req'
              582  LOAD_FAST                'body'
              584  LOAD_CONST               ('body',)
              586  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              588  POP_TOP          
              590  POP_BLOCK        
              592  JUMP_FORWARD        664  'to 664'
            594_0  COME_FROM_EXCEPT    572  '572'

 L. 279       594  DUP_TOP          
              596  LOAD_GLOBAL              RuntimeError
              598  COMPARE_OP               exception-match
          600_602  POP_JUMP_IF_FALSE   662  'to 662'
              604  POP_TOP          
              606  POP_TOP          
              608  POP_TOP          

 L. 281       610  LOAD_FAST                'self'
              612  LOAD_ATTR                _parent
              614  LOAD_ATTR                log
              616  LOAD_METHOD              info
              618  LOAD_STR                 'Update to existing attribute ({}), deleting it'
              620  LOAD_METHOD              format
              622  LOAD_FAST                'name'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  POP_TOP          

 L. 282       630  LOAD_FAST                'self'
              632  LOAD_ATTR                _parent
              634  LOAD_METHOD              DELETE
              636  LOAD_FAST                'req'
              638  CALL_METHOD_1         1  '1 positional argument'
              640  POP_TOP          

 L. 284       642  LOAD_FAST                'self'
              644  LOAD_ATTR                _parent
              646  LOAD_ATTR                PUT
              648  LOAD_FAST                'req'
              650  LOAD_FAST                'body'
              652  LOAD_CONST               ('body',)
              654  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              656  POP_TOP          
              658  POP_EXCEPT       
              660  JUMP_FORWARD        664  'to 664'
            662_0  COME_FROM           600  '600'
              662  END_FINALLY      
            664_0  COME_FROM           660  '660'
            664_1  COME_FROM           592  '592'

Parse error at or near `JUMP_FORWARD' instruction at offset 194

    def modify(self, name, value):
        """ Change the value of an attribute while preserving its type.

        Differs from __setitem__ in that if the attribute already exists, its
        type is preserved.  This can be very useful for interacting with
        externally generated files.

        If the attribute doesn't exist, it will be automatically created.
        """
        pass

    def __len__(self):
        """ Number of attributes attached to the object. """
        if self._objdb_attributes is not None:
            count = len(self._objdb_attributes)
        else:
            req = self._req_prefix
            req = req[:-len('/attributes/')]
            rsp = self._parent.GET(req)
            count = rsp['attributeCount']
        return count

    def __iter__(self):
        """ Iterate over the names of attributes. """
        if self._objdb_attributes is not None:
            for name in self._objdb_attributes:
                yield name

        else:
            req = self._req_prefix
            req = req[:-1]
            rsp = self._parent.GET(req)
            attributes = rsp['attributes']
            attrlist = []
            for attr in attributes:
                attrlist.append(attr['name'])

            for name in attrlist:
                yield name

    def __contains__(self, name):
        """ Determine if an attribute exists, by name. """
        exists = True
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if self._objdb_attributes is not None:
            exists = name in self._objdb_attributes
        else:
            req = self._req_prefix + name
            try:
                self._parent.GET(req)
            except IOError:
                exists = False

            return exists

    def __repr__(self):
        if not self._parent.id.id:
            return '<Attributes of closed HDF5 object>'
        return '<Attributes of HDF5 object at %s>' % id(self._parent.id)