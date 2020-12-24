# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_object.py
# Compiled at: 2020-02-18 04:13:44
# Size of source mod 2**32: 19725 bytes
from collections import OrderedDict
import uuid, struct
from pytwig.src.lib import util
from pytwig.src.lib.luts import names, non_overlap, field_lists
from pytwig import color, route
serialized = [
 None]
passed = []
import json

class BW_Object:
    __doc__ = 'Anything that can be in the device contents, including atoms, types, and panels. Any object with the form {class, object_id, data}.\n\n\tBW_Objects can be printed and serialized, and their data can be set or get (got?).\n\t'
    classname = ''
    data = {}

    def __init__(self, classnum=None, fields=None):
        self.data = OrderedDict()
        if classnum == None:
            return
        if isinstance(classnum, int):
            if classnum in names.class_names:
                self.classname = '{}({})'.format(names.class_names[classnum], classnum)
            else:
                if classnum in non_overlap.potential_names and classnum not in non_overlap.confirmed_names:
                    self.classname = '{}({})'.format(non_overlap.potential_names[classnum], classnum)
                    non_overlap.confirmed_names[classnum] = non_overlap.potential_names[classnum]
                else:
                    self.classname = 'missing class (' + str(classnum) + ')'
            self.classnum = classnum
        else:
            if isinstance(classnum, str):
                self.classname = classnum
                self.classnum = util.extract_num(classnum)
            else:
                if self.classnum in field_lists.class_type_list:
                    for each_field in field_lists.class_type_list[self.classnum]:
                        if each_field in names.field_names:
                            fieldname = names.field_names[each_field] + '(' + str(each_field) + ')'
                            self.data[fieldname] = util.get_field_default(each_field)
                        else:
                            fieldname = 'missing_field({})'.format(each_field)
                            self.data[fieldname] = None

            if not fields == None:
                for each_field in fields:
                    if each_field in self.data:
                        self.data[each_field] = fields[each_field]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.classname)

    def __dict__(self):
        return {'class':self.classname, 
         'data':dict(self.data)}

    def show(self):
        print(str(self.__dict__()).replace(', ', ',\n').replace('{', '{\n').replace('}', '\n}'))

    def set(self, key, val):
        """Sets a field in the object's data dictionary

                Args:
                        key (str): The key of the data field that is being set.
                        key (int): The classnum to be converted to the key of the data field that is being set.
                        val (any): The data value that the field is being set to.

                Returns:
                        Abstract_Serializable_BW_Object: self is returned so the function can be daisy-chained
                """
        if isinstance(key, int):
            key = names.field_names[key] + '(' + str(key) + ')'
        if key not in self.data:
            raise KeyError('{}, {}'.format(self.data, key))
        self.data[key] = val
        return self

    def set_default(self, key):
        """Sets a field in the object's data dictionary to its type's default value

                Args:
                        key (str): The key of the data field that is being set.
                        key (int): The classnum to be converted to the key of the data field that is being set.

                Returns:
                        Abstract_Serializable_BW_Object: self is returned so the function can be daisy-chained
                """
        if isinstance(key, int):
            key = names.field_names[key] + '(' + str(key) + ')'
        if key not in self.data:
            raise KeyError()
        self.data[key] = get_field_default(util.extract_num(key))
        return self

    def set_multi(self, dict):
        """Sets multiple fields in the object's data dictionary.

                Calls the set function once for each key-value pair input.

                Args:
                        dict (dict): The set of key-value pairs that are being set

                Returns:
                        Abstract_Serializable_BW_Object: self is returned so the function can be daisy-chained
                """
        for each_key in dict:
            self.set(each_key, dict[each_key])
        else:
            return self

    def get(self, key):
        """Gets the value at a data field in the object's data dictionary.

                Usually used to get a Bitwig object nested inside the self object's data.

                Args:
                        key (str): The key of the data field that the data is fetched from.
                        key (int): The classnum to be converted to the key of the data field that the data is fetched from.

                Returns:
                        Any: Returns the value inside the object's data dictionary, which can be any encodeable/decodable value
                """
        if isinstance(key, int):
            key = '{}({})'.format(names.field_names[key], key)
        return self.data[key]

    def get_referenced_ids(self, output=[], visited=[]):
        if self in visited:
            return output
        visited.append(self)
        for each_field in self.data:
            each_value = self.data[each_field]
            if util.extract_num(each_field) in (153, ):
                if each_value not in output:
                    output.append(each_value)
            elif isinstance(each_value, BW_Object):
                each_value.get_referenced_ids(output, visited)
            elif isinstance(each_value, list) and len(each_value) > 0 and isinstance(each_value[0], BW_Object):
                for each_object in each_value:
                    each_object.get_referenced_ids(output, visited)

            else:
                return output

    def check(self, key):
        """Checks whether the key is in the object's data dictionary.

                Args:
                        key (str): The key that is checked.
                        key (int): The classnum to be converted to the key that is checked.

                Returns:
                        bool: Returns true if the key exists in the data directory and false otherwise
                """
        if isinstance(key, int):
            key = '{}({})'.format(names.field_names[key], key)
        return key in self.data

    def clean(self, visited=[]):
        if self in visited:
            return output
        visited.append(self)
        if self.check(6093):
            self.set(6093, None)
        for each_field in self.data:
            each_value = self.data[each_field]
            if isinstance(each_value, BW_Object):
                each_value.clean(visited)
            elif isinstance(each_value, list) and len(each_value) > 0 and isinstance(each_value[0], BW_Object):
                for each_object in each_value:
                    each_object.clean(visited)

    def parse_field--- This code section failed: ---

 L. 198         0  LOAD_FAST                'bytecode'
                2  LOAD_METHOD              increment_position
                4  LOAD_CONST               -4
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 199        10  LOAD_FAST                'bytecode'
               12  LOAD_METHOD              read_int
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'field_num'

 L. 200        18  LOAD_FAST                'field_num'
               20  LOAD_GLOBAL              field_lists
               22  LOAD_ATTR                field_type_list
               24  COMPARE_OP               not-in
               26  POP_JUMP_IF_FALSE   150  'to 150'
               28  LOAD_FAST                'field_num'
               30  LOAD_GLOBAL              non_overlap
               32  LOAD_ATTR                confirmed_fields
               34  COMPARE_OP               not-in
               36  POP_JUMP_IF_FALSE   150  'to 150'

 L. 201        38  LOAD_CONST               False
               40  STORE_FAST               'pass_over'

 L. 202        42  LOAD_GLOBAL              util
               44  LOAD_METHOD              btoi
               46  LOAD_FAST                'bytecode'
               48  LOAD_METHOD              peek
               50  LOAD_CONST               1
               52  CALL_METHOD_1         1  ''
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'value'

 L. 203        58  LOAD_FAST                'value'
               60  LOAD_CONST               (1, 5, 7, 8, 9, 13, 18, 21, 25)
               62  COMPARE_OP               not-in
               64  POP_JUMP_IF_FALSE   136  'to 136'

 L. 204        66  LOAD_FAST                'value'
               68  LOAD_CONST               (2, 3, 4)
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L. 205        74  LOAD_CONST               1
               76  STORE_FAST               'value'
               78  JUMP_FORWARD        136  'to 136'
             80_0  COME_FROM            72  '72'

 L. 206        80  LOAD_FAST                'value'
               82  LOAD_CONST               6
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    94  'to 94'

 L. 207        88  LOAD_CONST               7
               90  STORE_FAST               'value'
               92  JUMP_FORWARD        136  'to 136'
             94_0  COME_FROM            86  '86'

 L. 208        94  LOAD_FAST                'value'
               96  LOAD_CONST               11
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   108  'to 108'

 L. 209       102  LOAD_CONST               9
              104  STORE_FAST               'value'
              106  JUMP_FORWARD        136  'to 136'
            108_0  COME_FROM           100  '100'

 L. 210       108  LOAD_FAST                'value'
              110  LOAD_CONST               10
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   122  'to 122'

 L. 211       116  LOAD_CONST               True
              118  STORE_FAST               'pass_over'
              120  JUMP_FORWARD        136  'to 136'
            122_0  COME_FROM           114  '114'

 L. 213       122  LOAD_GLOBAL              TypeError
              124  LOAD_STR                 "So I was writing a new field default type, right? but out of nowhere, there's this weird number I've never seen before: {}"
              126  LOAD_METHOD              format
              128  LOAD_FAST                'value'
              130  CALL_METHOD_1         1  ''
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           120  '120'
            136_1  COME_FROM           106  '106'
            136_2  COME_FROM            92  '92'
            136_3  COME_FROM            78  '78'
            136_4  COME_FROM            64  '64'

 L. 214       136  LOAD_FAST                'pass_over'
              138  POP_JUMP_IF_TRUE    150  'to 150'

 L. 215       140  LOAD_FAST                'value'
              142  LOAD_GLOBAL              non_overlap
              144  LOAD_ATTR                confirmed_fields
              146  LOAD_FAST                'field_num'
              148  STORE_SUBSCR     
            150_0  COME_FROM           138  '138'
            150_1  COME_FROM            36  '36'
            150_2  COME_FROM            26  '26'

 L. 218       150  LOAD_FAST                'bytecode'
              152  LOAD_METHOD              read_int
              154  LOAD_CONST               1
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'parse_type'

 L. 219       160  LOAD_FAST                'parse_type'
              162  LOAD_CONST               1
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   198  'to 198'

 L. 220       168  LOAD_FAST                'bytecode'
              170  LOAD_METHOD              read_int
              172  LOAD_CONST               1
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'val'

 L. 221       178  LOAD_FAST                'val'
              180  LOAD_CONST               128
              182  BINARY_AND       
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 222       186  LOAD_FAST                'val'
              188  LOAD_CONST               256
              190  INPLACE_SUBTRACT 
              192  STORE_FAST               'val'
            194_0  COME_FROM           184  '184'
          194_196  JUMP_FORWARD       1320  'to 1320'
            198_0  COME_FROM           166  '166'

 L. 223       198  LOAD_FAST                'parse_type'
              200  LOAD_CONST               2
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   236  'to 236'

 L. 224       206  LOAD_FAST                'bytecode'
              208  LOAD_METHOD              read_int
              210  LOAD_CONST               2
              212  CALL_METHOD_1         1  ''
              214  STORE_FAST               'val'

 L. 225       216  LOAD_FAST                'val'
              218  LOAD_CONST               32768
              220  BINARY_AND       
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L. 226       224  LOAD_FAST                'val'
              226  LOAD_CONST               65536
              228  INPLACE_SUBTRACT 
              230  STORE_FAST               'val'
            232_0  COME_FROM           222  '222'
          232_234  JUMP_FORWARD       1320  'to 1320'
            236_0  COME_FROM           204  '204'

 L. 227       236  LOAD_FAST                'parse_type'
              238  LOAD_CONST               3
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   278  'to 278'

 L. 228       246  LOAD_FAST                'bytecode'
              248  LOAD_METHOD              read_int
              250  LOAD_CONST               4
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'val'

 L. 229       256  LOAD_FAST                'val'
              258  LOAD_CONST               2147483648
              260  BINARY_AND       
          262_264  POP_JUMP_IF_FALSE  1320  'to 1320'

 L. 230       266  LOAD_FAST                'val'
              268  LOAD_CONST               4294967296
              270  INPLACE_SUBTRACT 
              272  STORE_FAST               'val'
          274_276  JUMP_FORWARD       1320  'to 1320'
            278_0  COME_FROM           242  '242'

 L. 231       278  LOAD_FAST                'parse_type'
              280  LOAD_CONST               4
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   320  'to 320'

 L. 232       288  LOAD_FAST                'bytecode'
              290  LOAD_METHOD              read_int
              292  LOAD_CONST               8
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'val'

 L. 233       298  LOAD_FAST                'val'
              300  LOAD_CONST               9223372036854775808
              302  BINARY_AND       
          304_306  POP_JUMP_IF_FALSE  1320  'to 1320'

 L. 234       308  LOAD_FAST                'val'
              310  LOAD_CONST               18446744073709551616
              312  INPLACE_SUBTRACT 
              314  STORE_FAST               'val'
          316_318  JUMP_FORWARD       1320  'to 1320'
            320_0  COME_FROM           284  '284'

 L. 235       320  LOAD_FAST                'parse_type'
              322  LOAD_CONST               5
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   350  'to 350'

 L. 236       330  LOAD_GLOBAL              bool
              332  LOAD_FAST                'bytecode'
              334  LOAD_METHOD              read
              336  CALL_METHOD_0         0  ''
              338  LOAD_CONST               b'\x00'
              340  COMPARE_OP               !=
              342  CALL_FUNCTION_1       1  ''
              344  STORE_FAST               'val'
          346_348  JUMP_FORWARD       1320  'to 1320'
            350_0  COME_FROM           326  '326'

 L. 237       350  LOAD_FAST                'parse_type'
              352  LOAD_CONST               6
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_FALSE   386  'to 386'

 L. 238       360  LOAD_GLOBAL              struct
              362  LOAD_METHOD              unpack
              364  LOAD_STR                 '>f'
              366  LOAD_FAST                'bytecode'
              368  LOAD_METHOD              read
              370  LOAD_CONST               4
              372  CALL_METHOD_1         1  ''
              374  CALL_METHOD_2         2  ''
              376  LOAD_CONST               0
              378  BINARY_SUBSCR    
              380  STORE_FAST               'val'
          382_384  JUMP_FORWARD       1320  'to 1320'
            386_0  COME_FROM           356  '356'

 L. 239       386  LOAD_FAST                'parse_type'
              388  LOAD_CONST               7
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   422  'to 422'

 L. 240       396  LOAD_GLOBAL              struct
              398  LOAD_METHOD              unpack
              400  LOAD_STR                 '>d'
              402  LOAD_FAST                'bytecode'
              404  LOAD_METHOD              read
              406  LOAD_CONST               8
              408  CALL_METHOD_1         1  ''
              410  CALL_METHOD_2         2  ''
              412  LOAD_CONST               0
              414  BINARY_SUBSCR    
              416  STORE_FAST               'val'
          418_420  JUMP_FORWARD       1320  'to 1320'
            422_0  COME_FROM           392  '392'

 L. 241       422  LOAD_FAST                'parse_type'
              424  LOAD_CONST               8
              426  COMPARE_OP               ==
          428_430  POP_JUMP_IF_FALSE   444  'to 444'

 L. 242       432  LOAD_FAST                'bytecode'
              434  LOAD_METHOD              read_str
              436  CALL_METHOD_0         0  ''
              438  STORE_FAST               'val'
          440_442  JUMP_FORWARD       1320  'to 1320'
            444_0  COME_FROM           428  '428'

 L. 243       444  LOAD_FAST                'parse_type'
              446  LOAD_CONST               9
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_FALSE   468  'to 468'

 L. 244       454  LOAD_GLOBAL              BW_Object
              456  LOAD_METHOD              decode
              458  LOAD_FAST                'bytecode'
              460  CALL_METHOD_1         1  ''
              462  STORE_FAST               'val'
          464_466  JUMP_FORWARD       1320  'to 1320'
            468_0  COME_FROM           450  '450'

 L. 245       468  LOAD_FAST                'parse_type'
              470  LOAD_CONST               10
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   486  'to 486'

 L. 246       478  LOAD_CONST               None
              480  STORE_FAST               'val'
          482_484  JUMP_FORWARD       1320  'to 1320'
            486_0  COME_FROM           474  '474'

 L. 247       486  LOAD_FAST                'parse_type'
              488  LOAD_CONST               11
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE   554  'to 554'

 L. 248       496  LOAD_FAST                'bytecode'
              498  LOAD_METHOD              read_int
              500  CALL_METHOD_0         0  ''
              502  STORE_FAST               'obj_num'

 L. 249       504  LOAD_FAST                'obj_num'
              506  LOAD_GLOBAL              len
              508  LOAD_FAST                'bytecode'
              510  LOAD_ATTR                obj_list
              512  CALL_FUNCTION_1       1  ''
              514  COMPARE_OP               >=
          516_518  POP_JUMP_IF_FALSE   540  'to 540'

 L. 250       520  LOAD_GLOBAL              ReferenceError
              522  LOAD_STR                 'Referenced object before decode'
              524  CALL_FUNCTION_1       1  ''
              526  RAISE_VARARGS_1       1  'exception instance'

 L. 251       528  LOAD_FAST                'bytecode'
              530  LOAD_ATTR                obj_list
              532  LOAD_CONST               -1
              534  BINARY_SUBSCR    
              536  STORE_FAST               'val'
              538  JUMP_FORWARD       1320  'to 1320'
            540_0  COME_FROM           516  '516'

 L. 253       540  LOAD_FAST                'bytecode'
              542  LOAD_ATTR                obj_list
              544  LOAD_FAST                'obj_num'
              546  BINARY_SUBSCR    
              548  STORE_FAST               'val'
          550_552  JUMP_FORWARD       1320  'to 1320'
            554_0  COME_FROM           492  '492'

 L. 254       554  LOAD_FAST                'parse_type'
              556  LOAD_CONST               13
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_FALSE   652  'to 652'

 L. 255       564  LOAD_FAST                'bytecode'
              566  LOAD_METHOD              read_int
              568  CALL_METHOD_0         0  ''
              570  STORE_FAST               'file_len'

 L. 256       572  LOAD_FAST                'file_len'
              574  LOAD_CONST               16
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE   594  'to 594'

 L. 257       582  LOAD_FAST                'bytecode'
              584  LOAD_METHOD              read
              586  LOAD_CONST               16
              588  CALL_METHOD_1         1  ''
              590  STORE_FAST               'val'
              592  JUMP_FORWARD       1320  'to 1320'
            594_0  COME_FROM           578  '578'

 L. 260       594  LOAD_CONST               0
              596  LOAD_CONST               ('bw_file',)
              598  IMPORT_NAME              pytwig
              600  IMPORT_FROM              bw_file
              602  STORE_FAST               'bw_file'
              604  POP_TOP          

 L. 261       606  LOAD_FAST                'bw_file'
              608  LOAD_METHOD              BW_File
              610  CALL_METHOD_0         0  ''
              612  STORE_FAST               'val'

 L. 262       614  LOAD_FAST                'bw_file'
              616  LOAD_METHOD              BW_Bytecode
              618  CALL_METHOD_0         0  ''
              620  STORE_FAST               'sub_bytecode'

 L. 263       622  LOAD_FAST                'sub_bytecode'
              624  LOAD_METHOD              set_contents
              626  LOAD_FAST                'bytecode'
              628  LOAD_METHOD              read
              630  LOAD_FAST                'file_len'
              632  CALL_METHOD_1         1  ''
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          

 L. 264       638  LOAD_FAST                'val'
              640  LOAD_METHOD              decode
              642  LOAD_FAST                'sub_bytecode'
              644  CALL_METHOD_1         1  ''
              646  POP_TOP          
          648_650  JUMP_FORWARD       1320  'to 1320'
            652_0  COME_FROM           560  '560'

 L. 265       652  LOAD_FAST                'parse_type'
              654  LOAD_CONST               18
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   718  'to 718'

 L. 266       662  BUILD_LIST_0          0 
              664  STORE_FAST               'val'

 L. 267       666  LOAD_FAST                'bytecode'
              668  LOAD_METHOD              peek_int
              670  CALL_METHOD_0         0  ''
              672  LOAD_CONST               3
              674  COMPARE_OP               !=
          676_678  POP_JUMP_IF_FALSE   704  'to 704'

 L. 268       680  LOAD_GLOBAL              BW_Object
              682  LOAD_METHOD              decode
              684  LOAD_FAST                'bytecode'
              686  CALL_METHOD_1         1  ''
              688  STORE_FAST               'each_object'

 L. 269       690  LOAD_FAST                'val'
              692  LOAD_METHOD              append
              694  LOAD_FAST                'each_object'
              696  CALL_METHOD_1         1  ''
              698  POP_TOP          
          700_702  JUMP_BACK           666  'to 666'
            704_0  COME_FROM           676  '676'

 L. 270       704  LOAD_FAST                'bytecode'
              706  LOAD_METHOD              increment_position
              708  LOAD_CONST               4
              710  CALL_METHOD_1         1  ''
              712  POP_TOP          
          714_716  JUMP_FORWARD       1320  'to 1320'
            718_0  COME_FROM           658  '658'

 L. 271       718  LOAD_FAST                'parse_type'
              720  LOAD_CONST               20
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   844  'to 844'

 L. 272       728  LOAD_STR                 ''
              730  BUILD_MAP_0           0 
              732  LOAD_CONST               ('type', 'data')
              734  BUILD_CONST_KEY_MAP_2     2 
              736  STORE_FAST               'val'

 L. 273       738  LOAD_STR                 ''
              740  STORE_FAST               'string'

 L. 274       742  LOAD_STR                 'map<string,object>'
              744  LOAD_FAST                'val'
              746  LOAD_STR                 'type'
              748  STORE_SUBSCR     

 L. 275       750  LOAD_FAST                'bytecode'
              752  LOAD_METHOD              read_int
              754  LOAD_CONST               1
              756  CALL_METHOD_1         1  ''
              758  STORE_FAST               'sub_parse_type'

 L. 276       760  LOAD_FAST                'sub_parse_type'
          762_764  POP_JUMP_IF_FALSE  1320  'to 1320'

 L. 277       766  LOAD_FAST                'sub_parse_type'
              768  LOAD_CONST               1
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE   804  'to 804'

 L. 278       776  LOAD_FAST                'bytecode'
              778  LOAD_METHOD              read_str
              780  CALL_METHOD_0         0  ''
              782  STORE_FAST               'string'

 L. 279       784  LOAD_GLOBAL              BW_Object
              786  LOAD_METHOD              decode
              788  LOAD_FAST                'bytecode'
              790  CALL_METHOD_1         1  ''
              792  LOAD_FAST                'val'
              794  LOAD_STR                 'data'
              796  BINARY_SUBSCR    
              798  LOAD_FAST                'string'
              800  STORE_SUBSCR     
              802  JUMP_FORWARD        826  'to 826'
            804_0  COME_FROM           772  '772'

 L. 281       804  LOAD_GLOBAL              TypeError
              806  LOAD_STR                 'Unknown type in map<string,?>: {}'
              808  LOAD_METHOD              format
              810  LOAD_FAST                'sub_parse_type'
              812  CALL_METHOD_1         1  ''
              814  CALL_FUNCTION_1       1  ''
              816  RAISE_VARARGS_1       1  'exception instance'

 L. 282       818  LOAD_STR                 'unknown'
              820  LOAD_FAST                'val'
              822  LOAD_STR                 'type'
              824  STORE_SUBSCR     
            826_0  COME_FROM           802  '802'

 L. 283       826  LOAD_FAST                'bytecode'
              828  LOAD_METHOD              read_int
              830  LOAD_CONST               1
              832  CALL_METHOD_1         1  ''
              834  STORE_FAST               'sub_parse_type'
          836_838  JUMP_BACK           760  'to 760'
          840_842  JUMP_FORWARD       1320  'to 1320'
            844_0  COME_FROM           724  '724'

 L. 284       844  LOAD_FAST                'parse_type'
              846  LOAD_CONST               21
              848  COMPARE_OP               ==
          850_852  POP_JUMP_IF_FALSE   880  'to 880'

 L. 285       854  LOAD_GLOBAL              str
              856  LOAD_GLOBAL              uuid
              858  LOAD_ATTR                UUID
              860  LOAD_FAST                'bytecode'
              862  LOAD_METHOD              read
              864  LOAD_CONST               16
              866  CALL_METHOD_1         1  ''
              868  LOAD_CONST               ('bytes',)
              870  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              872  CALL_FUNCTION_1       1  ''
              874  STORE_FAST               'val'
          876_878  JUMP_FORWARD       1320  'to 1320'
            880_0  COME_FROM           850  '850'

 L. 286       880  LOAD_FAST                'parse_type'
              882  LOAD_CONST               22
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_FALSE   922  'to 922'

 L. 287       890  LOAD_GLOBAL              struct
              892  LOAD_METHOD              unpack
              894  LOAD_STR                 '>ffff'
              896  LOAD_FAST                'bytecode'
              898  LOAD_METHOD              read
              900  LOAD_CONST               16
              902  CALL_METHOD_1         1  ''
              904  CALL_METHOD_2         2  ''
              906  STORE_FAST               'flVals'

 L. 288       908  LOAD_GLOBAL              color
              910  LOAD_ATTR                Color
              912  LOAD_FAST                'flVals'
              914  CALL_FUNCTION_EX      0  'positional arguments only'
              916  STORE_FAST               'val'
          918_920  JUMP_FORWARD       1320  'to 1320'
            922_0  COME_FROM           886  '886'

 L. 289       922  LOAD_FAST                'parse_type'
              924  LOAD_CONST               23
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_FALSE   992  'to 992'

 L. 290       932  LOAD_FAST                'bytecode'
              934  LOAD_METHOD              read_int
              936  CALL_METHOD_0         0  ''
              938  STORE_FAST               'arr_len'

 L. 291       940  BUILD_LIST_0          0 
              942  STORE_FAST               'val'

 L. 292       944  LOAD_GLOBAL              range
              946  LOAD_FAST                'arr_len'
              948  CALL_FUNCTION_1       1  ''
              950  GET_ITER         
              952  FOR_ITER            988  'to 988'
              954  STORE_FAST               'i'

 L. 293       956  LOAD_FAST                'val'
              958  LOAD_METHOD              append
              960  LOAD_GLOBAL              struct
              962  LOAD_METHOD              unpack
              964  LOAD_STR                 '>f'
              966  LOAD_FAST                'bytecode'
              968  LOAD_METHOD              read
              970  LOAD_CONST               4
              972  CALL_METHOD_1         1  ''
              974  CALL_METHOD_2         2  ''
              976  LOAD_CONST               0
              978  BINARY_SUBSCR    
              980  CALL_METHOD_1         1  ''
              982  POP_TOP          
          984_986  JUMP_BACK           952  'to 952'
          988_990  JUMP_FORWARD       1320  'to 1320'
            992_0  COME_FROM           928  '928'

 L. 294       992  LOAD_FAST                'parse_type'
              994  LOAD_CONST               25
              996  COMPARE_OP               ==
         998_1000  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 295      1002  LOAD_FAST                'bytecode'
             1004  LOAD_METHOD              read_int
             1006  CALL_METHOD_0         0  ''
             1008  STORE_FAST               'arr_len'

 L. 296      1010  BUILD_LIST_0          0 
             1012  STORE_FAST               'val'

 L. 297      1014  LOAD_GLOBAL              range
             1016  LOAD_FAST                'arr_len'
             1018  CALL_FUNCTION_1       1  ''
             1020  GET_ITER         
             1022  FOR_ITER           1044  'to 1044'
             1024  STORE_FAST               'i'

 L. 298      1026  LOAD_FAST                'val'
             1028  LOAD_METHOD              append
             1030  LOAD_FAST                'bytecode'
             1032  LOAD_METHOD              read_str
             1034  CALL_METHOD_0         0  ''
             1036  CALL_METHOD_1         1  ''
             1038  POP_TOP          
         1040_1042  JUMP_BACK          1022  'to 1022'
         1044_1046  JUMP_FORWARD       1320  'to 1320'
           1048_0  COME_FROM           998  '998'

 L. 299      1048  LOAD_FAST                'parse_type'
             1050  LOAD_CONST               26
             1052  COMPARE_OP               ==
         1054_1056  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 300      1058  LOAD_FAST                'bytecode'
             1060  LOAD_METHOD              read_int
             1062  CALL_METHOD_0         0  ''
             1064  STORE_FAST               'sub_parse'

 L. 301      1066  LOAD_FAST                'sub_parse'
             1068  LOAD_CONST               144
             1070  COMPARE_OP               ==
         1072_1074  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 302      1076  LOAD_FAST                'bytecode'
             1078  LOAD_METHOD              increment_position
             1080  LOAD_CONST               -4
             1082  CALL_METHOD_1         1  ''
             1084  POP_TOP          

 L. 303      1086  LOAD_GLOBAL              route
             1088  LOAD_METHOD              Route
             1090  CALL_METHOD_0         0  ''
             1092  STORE_FAST               'val'

 L. 304      1094  LOAD_GLOBAL              BW_Object
             1096  LOAD_METHOD              decode
             1098  LOAD_FAST                'bytecode'
             1100  CALL_METHOD_1         1  ''
             1102  STORE_FAST               'obj'

 L. 305      1104  LOAD_FAST                'obj'
             1106  LOAD_FAST                'val'
             1108  LOAD_ATTR                data
             1110  LOAD_STR                 'obj'
             1112  STORE_SUBSCR     

 L. 306      1114  LOAD_FAST                'bytecode'
             1116  LOAD_METHOD              read_str
             1118  CALL_METHOD_0         0  ''
             1120  LOAD_FAST                'val'
             1122  LOAD_ATTR                data
             1124  LOAD_STR                 'str'
             1126  STORE_SUBSCR     
             1128  JUMP_FORWARD       1186  'to 1186'
           1130_0  COME_FROM          1072  '1072'

 L. 307      1130  LOAD_FAST                'sub_parse'
             1132  LOAD_CONST               1
             1134  COMPARE_OP               ==
         1136_1138  POP_JUMP_IF_FALSE  1178  'to 1178'

 L. 308      1140  LOAD_GLOBAL              route
             1142  LOAD_METHOD              Route
             1144  CALL_METHOD_0         0  ''
             1146  STORE_FAST               'val'

 L. 309      1148  LOAD_FAST                'bytecode'
             1150  LOAD_METHOD              read_int
             1152  CALL_METHOD_0         0  ''
             1154  LOAD_FAST                'val'
             1156  LOAD_ATTR                data
             1158  LOAD_STR                 'int'
             1160  STORE_SUBSCR     

 L. 310      1162  LOAD_FAST                'bytecode'
             1164  LOAD_METHOD              read_str
             1166  CALL_METHOD_0         0  ''
             1168  LOAD_FAST                'val'
             1170  LOAD_ATTR                data
             1172  LOAD_STR                 'str'
             1174  STORE_SUBSCR     
             1176  JUMP_FORWARD       1186  'to 1186'
           1178_0  COME_FROM          1136  '1136'

 L. 312      1178  LOAD_GLOBAL              TypeError
             1180  LOAD_STR                 'unparsable value in route'
             1182  CALL_FUNCTION_1       1  ''
             1184  RAISE_VARARGS_1       1  'exception instance'
           1186_0  COME_FROM          1176  '1176'
           1186_1  COME_FROM          1128  '1128'
             1186  JUMP_FORWARD       1320  'to 1320'
           1188_0  COME_FROM          1054  '1054'

 L. 313      1188  LOAD_FAST                'parse_type'
             1190  LOAD_CONST               51
             1192  COMPARE_OP               ==
         1194_1196  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 314      1198  LOAD_GLOBAL              print
             1200  LOAD_STR                 'position: '
             1202  LOAD_GLOBAL              hex
             1204  LOAD_FAST                'bytecode'
             1206  LOAD_ATTR                position
             1208  CALL_FUNCTION_1       1  ''
             1210  BINARY_ADD       
             1212  CALL_FUNCTION_1       1  ''
             1214  POP_TOP          

 L. 315      1216  LOAD_GLOBAL              TypeError
             1218  LOAD_STR                 'this bug should be gone'
             1220  CALL_FUNCTION_1       1  ''
             1222  RAISE_VARARGS_1       1  'exception instance'

 L. 316      1224  LOAD_FAST                'bytecode'
             1226  LOAD_METHOD              increment_position
             1228  LOAD_CONST               -2
             1230  CALL_METHOD_1         1  ''
             1232  POP_TOP          

 L. 317      1234  LOAD_GLOBAL              BW_Object
             1236  LOAD_METHOD              decode
             1238  LOAD_FAST                'bytecode'
             1240  CALL_METHOD_1         1  ''
             1242  STORE_FAST               'val'
             1244  JUMP_FORWARD       1320  'to 1320'
           1246_0  COME_FROM          1194  '1194'

 L. 319      1246  LOAD_GLOBAL              print
             1248  LOAD_FAST                'bytecode'
             1250  LOAD_ATTR                obj_list
             1252  LOAD_CONST               -1
             1254  BINARY_SUBSCR    
             1256  LOAD_ATTR                data
             1258  CALL_FUNCTION_1       1  ''
             1260  POP_TOP          
           1262_0  COME_FROM           592  '592'

 L. 320      1262  LOAD_GLOBAL              print
             1264  LOAD_STR                 'position: '
             1266  LOAD_GLOBAL              hex
             1268  LOAD_FAST                'bytecode'
             1270  LOAD_ATTR                position
             1272  CALL_FUNCTION_1       1  ''
             1274  BINARY_ADD       
             1276  CALL_FUNCTION_1       1  ''
             1278  POP_TOP          

 L. 321      1280  LOAD_FAST                'bytecode'
             1282  LOAD_METHOD              increment_position
             1284  LOAD_CONST               -4
             1286  CALL_METHOD_1         1  ''
             1288  POP_TOP          

 L. 322      1290  LOAD_GLOBAL              print
             1292  LOAD_FAST                'bytecode'
             1294  LOAD_METHOD              peek
             1296  LOAD_CONST               80
             1298  CALL_METHOD_1         1  ''
             1300  CALL_FUNCTION_1       1  ''
             1302  POP_TOP          

 L. 323      1304  LOAD_GLOBAL              TypeError
           1306_0  COME_FROM           538  '538'
             1306  LOAD_STR                 'unknown type '
             1308  LOAD_GLOBAL              str
             1310  LOAD_FAST                'parse_type'
             1312  CALL_FUNCTION_1       1  ''
             1314  BINARY_ADD       
             1316  CALL_FUNCTION_1       1  ''
             1318  RAISE_VARARGS_1       1  'exception instance'
           1320_0  COME_FROM          1244  '1244'
           1320_1  COME_FROM          1186  '1186'
           1320_2  COME_FROM          1044  '1044'
           1320_3  COME_FROM           988  '988'
           1320_4  COME_FROM           918  '918'
           1320_5  COME_FROM           876  '876'
           1320_6  COME_FROM           840  '840'
           1320_7  COME_FROM           762  '762'
           1320_8  COME_FROM           714  '714'
           1320_9  COME_FROM           648  '648'
          1320_10  COME_FROM           550  '550'
          1320_11  COME_FROM           482  '482'
          1320_12  COME_FROM           464  '464'
          1320_13  COME_FROM           440  '440'
          1320_14  COME_FROM           418  '418'
          1320_15  COME_FROM           382  '382'
          1320_16  COME_FROM           346  '346'
          1320_17  COME_FROM           316  '316'
          1320_18  COME_FROM           304  '304'
          1320_19  COME_FROM           274  '274'
          1320_20  COME_FROM           262  '262'
          1320_21  COME_FROM           232  '232'
          1320_22  COME_FROM           194  '194'

 L. 324      1320  LOAD_FAST                'val'
             1322  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1306_0

    def encode_field(self, bytecode, field):
        """Helper function for recursively serializing Bitwig objects into Bitwig bytecode.

                Args:
                        bytecode (BW_Bytecode): Current bytecode to add the encoded field onto
                        field (str): Key of the field of this object's data dictionary to be encoded into Bitwig bytecode
                """
        value = self.data[field]
        fieldNum = util.extract_num(field)
        if value == None:
            bytecode.write('0a')
        else:
            if fieldNum in field_lists.field_type_list:
                if field_lists.field_type_list[fieldNum] == 1:
                    if value <= 127:
                        if value >= -128:
                            bytecode.write('01')
                            if value < 0:
                                bytecode.write(hex(255 + value + 1)[2:])
                            else:
                                bytecode.write_int(value, 2)
                        elif value <= 32767 and value >= -32768:
                            bytecode.write('02')
                            if value < 0:
                                bytecode.write(hex(65535 + value + 1)[2:])
                            else:
                                bytecode.write_int(value, 4)
                        elif value <= 2147483647:
                            if value >= -2147483648:
                                bytecode.write('03')
                                if value < 0:
                                    bytecode.write(hex(4294967295 + value + 1)[2:])
                                else:
                                    bytecode.write_int(value, 8)
                            else:
                                bytecode.write('04')
                                if value < 0:
                                    bytecode.write(hex(18446744073709551615 + value + 1)[2:])
                                else:
                                    bytecode.write_int(value, 16)
                        elif field_lists.field_type_list[fieldNum] == 5:
                            bytecode.write('05')
                            bytecode.write('01' if value else '00')
                        elif field_lists.field_type_list[fieldNum] == 6:
                            flVal = struct.unpack('<I', struct.pack('<f', value))[0]
                            bytecode.write('06')
                            bytecode.write_int(flVal, 8)
                        elif field_lists.field_type_list[fieldNum] == 7:
                            dbVal = struct.unpack('<Q', struct.pack('<d', value))[0]
                            bytecode.write('07')
                            bytecode.write_int(dbVal, 16)
                        elif field_lists.field_type_list[fieldNum] == 8:
                            bytecode.write('08')
                            value = value.replace('\\n', '\n')
                            bytecode.write_str(value)
                        elif field_lists.field_type_list[fieldNum] in (9, 20):
                            if isinstance(value, BW_Object):
                                if value in bytecode.obj_list:
                                    bytecode.write('0b')
                                    bytecode.write_int(bytecode.obj_list.index(value), 8)
                                else:
                                    bytecode.write('09')
                                    value.encode_to(bytecode)
                            elif value is None:
                                print('untested portion: NoneType')
                                bytecode.write('0a')
                            elif isinstance(value, dict):
                                bytecode.write('14')
                                if len(value['data']):
                                    bytecode.write('01')
                                    for key in value['data']:
                                        bytecode.write_str(key)
                                        value['data'][key].encode_to(bytecode)

                            else:
                                bytecode.write('00')
                        elif field_lists.field_type_list[fieldNum] == 13:
                            bytecode.write('0d')
                            from pytwig import bw_file
                            if isinstance(value, bw_file.BW_File):
                                sub_bytecode = bw_file.BW_Bytecode()
                                value.encode_to(sub_bytecode)
                                bytecode.write_int(sub_bytecode.contents_len)
                                bytecode.write(sub_bytecode.contents)
                            elif isinstance(value, bytes):
                                bytecode.write_int(len(value))
                                bytecode.write(value)
                            else:
                                raise TypeError('invalid structure type')
                        elif field_lists.field_type_list[fieldNum] == 18:
                            bytecode.write('12')
                            for item in value:
                                if isinstance(item, BW_Object):
                                    if item in bytecode.obj_list:
                                        bytecode.write('00000001')
                                        bytecode.write_int(bytecode.obj_list.index(item), 8)
                                    else:
                                        item.encode_to(bytecode)
                                else:
                                    print("something went wrong in objects.py: 'not object list'")
                            else:
                                bytecode.write('00000003')

                        elif field_lists.field_type_list[fieldNum] == 21:
                            bytecode.write('15')
                            if isinstance(value, str):
                                value = uuid.UUID(value)
                            else:
                                if not isinstance(value, uuid.UUID):
                                    raise TypeError('encoding a non-uuid value as a uuid: {}'.format(value))
                            bytecode.write(value.bytes)
                        elif field_lists.field_type_list[fieldNum] == 22:
                            bytecode.write('16')
                            bytecode.write(value.encode())
                        elif field_lists.field_type_list[fieldNum] == 23:
                            bytecode.write('17')
                            bytecode.write_int(len(value), 8)
                            for item in value:
                                flVal = struct.unpack('<I', struct.pack('<f', item))[0]
                                bytecode.write_int(flVal, 8)

                        elif field_lists.field_type_list[fieldNum] == 25:
                            bytecode.write('19')
                            bytecode.write_int(len(value), 8)
                            for each_str in value:
                                each_str = each_str.replace('\\n', '\n')
                                bytecode.write_str(each_str)

                else:
                    if field_lists.field_type_list[fieldNum] == 26:
                        bytecode.write('1a')
                        if 'obj' in value.data:
                            value.data['obj'].encode_to(bytecode)
                        if 'int' in value.data:
                            bytecode.write_int(1)
                            bytecode.write_int(value.data['int'])
                        if 'str' in value.data:
                            bytecode.write_str(value.data['str'])
                    elif field_lists.field_type_list[fieldNum] == None:
                        print('skipped in binary serialization: {}'.format(fieldNum))
                        break
                    else:
                        print('jaxter stop being a lazy nerd and ' + hex(field_lists.field_type_list[fieldNum]) + ' to the atom encoder. obj: ' + str(fieldNum))
            else:
                print('missing type in field_lists.field_type_list: {}'.format(fieldNum))

    def decode_fields(self, bytecode):
        """Helper function for iteratively reading all of an object's fields from Bitwig bytecode

                Args:
                        bytecode (BW_Bytecode): Bytecode to be parsed
                        obj_list (list): List of objects that are currently in the file. Used to pass on to self.decode_object() so it can parse references.

                Returns:
                        bytes: Passes back the remaining bytecode to be parsed
                """
        field_num = bytecode.read_int()
        while field_num:
            if field_num in names.field_names:
                field_name = names.field_names[field_num] + '(' + str(field_num) + ')'
            else:
                field_name = 'missing_field(' + str(field_num) + ')'
                print('missing field: ' + str(field_num))
            value = self.parse_field(bytecode)
            self.data[field_name] = value
            field_num = bytecode.read_int()

    @staticmethod
    def decode(bytecode):
        """Helper function for recursively reading Bitwig objects from Bitwig bytecode.

                Args:
                        bytecode (BW_Bytecode): Bytecode to be parsed.

                Returns:
                        BW_Object: Result of parsing
                """
        obj_num = bytecode.read_int()
        if obj_num == 1:
            return bytecode.obj_list[bytecode.read_int()]
        elif bytecode.raw:
            obj = BW_Object()
            obj.data = OrderedDict()
            from pytwig.src.lib.luts import names
            if obj_num in names.class_names:
                obj.classname = '{}({})'.format(names.class_names[obj_num], obj_num)
            else:
                print('problematic missing class {}'.format(obj_num))
                obj.classname = 'missing_class({})'.format(obj_num)
            obj.classnum = obj_num
        else:
            obj = BW_Object(obj_num)
        bytecode.obj_list.append(obj)
        obj.decode_fields(bytecode)
        return obj

    def encode_to(self, bytecode):
        bytecode.obj_list.append(self)
        bytecode.write(util.hex_pad(self.classnum, 8))
        for each_field in self.data:
            bytecode.write(util.hex_pad(util.extract_num(each_field), 8))
            self.encode_field(bytecode, each_field)
        else:
            bytecode.write('00000000')

    def iter_helper(self, obj):
        from pytwig import bw_file
        if isinstance(obj, BW_Object) or isinstance(obj, color.Color) or isinstance(obj, route.Route):
            return dict(obj)
        if isinstance(obj, bw_file.BW_File) or isinstance(obj, bytes):
            return str(obj)
        if isinstance(obj, list):
            output = []
            for i in obj:
                output.append(self.iter_helper(i))
            else:
                return output

        if isinstance(obj, dict):
            output = {}
            for key in obj:
                output[key] = self.iter_helper(obj[key])
            else:
                return output

        if isinstance(obj, uuid.UUID):
            return str(obj)
        return obj

    def __iter__(self):
        if self in serialized:
            (yield (
             'object_ref', serialized.index(self)))
        else:
            serialized.append(self)
            (yield ('class', self.classname))
            (yield ('object_id', len(serialized) - 1))
            data_output = {}
            for each_field in self.data:
                data_output[each_field] = self.iter_helper(self.data[each_field])
            else:
                print(str(data_output).replace(', ', '\n'))
                print(json.dumps(data_output, indent=2))
                (yield ('data', data_output))

    def serialize(self):
        serialized = [
         None]
        return json.dumps((dict(self)), indent=2)

    def debug_list_fields(self):
        """Debug function for listing all the data fields of a Bitwig object
                """
        output = ''
        output += 'class : ' + str(self.classname) + '\n'
        for each_field in self.data:
            output += each_field + '\n'
        else:
            return output


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 460      1582  BREAK_LOOP         1618  'to 1618'