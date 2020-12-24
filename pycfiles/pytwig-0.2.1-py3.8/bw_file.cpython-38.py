# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_file.py
# Compiled at: 2020-02-18 03:37:49
# Size of source mod 2**32: 13819 bytes
from collections import OrderedDict
from pytwig.src.lib import util
from pytwig import bw_object
from pytwig import bw_track

class BW_File:

    def __init__(self, type=None):
        self.bytecode = None
        if type == None:
            self.header = ''
            self.meta = BW_Meta(None)
            self.contents = None
            return
        self.header = 'BtWgXXXXX'
        self.meta = BW_Meta('application/bitwig-' + type)
        self.contents = None

    def __str__(self):
        return 'File'

    def __iter__(self):
        (yield (
         'header', self.header))
        (yield ('meta', self.meta))
        (yield ('contents', self.contents))

    def show(self):
        print(str(self.__dict__()).replace(', ', ',\n').replace('{', '{\n').replace('}', '\n}'))

    def set_header(self, value):
        """Sets self.header, checking for validity before doing so.

                Args:
                        value (str): Header string to be checked and written

                Returns:
                        BW_File: self is returned so the function can be daisy-chained
                """
        if not (value[:4] == 'BtWg' and int(value[4:], 16) and len(value) == 40):
            raise TypeError('"{}" is not a valid header'.format(value))
        else:
            self.header = value
        return self

    def set_contents(self, value):
        """Sets self.contents, checking very superficially for validity before doing so.

                Args:
                        value (BW_Object): Bitwig object to be set as this object's contents

                Returns:
                        BW_File: self is returned so the function can be daisy-chained
                """
        if not isinstance(value, BW_Object):
            raise TypeError('"{}" is not an atom'.format(value))
        else:
            self.contents = value
        return self

    def get_contents(self):
        return self.contents

    def set_uuid(self, value):
        self.contents.data['device_UUID'] = value
        self.meta.data['device_uuid'] = value
        self.meta.data['device_id'] = value
        return self

    def set_description(self, value):
        self.meta.data['device_description'] = value
        return self

    def set_version(self, value):
        self.meta.data['application_version_name'] = value
        return self

    def serialize(self):
        bw_object.serialized = [
         None]
        output = self.header[:11] + '1' + self.header[12:]
        output += self.meta.serialize()
        output += '\n'
        bw_object.serialized = [None]
        output += self.contents.serialize()
        return output

    def encode_to(self, bytecode):
        if bytecode.string_mode == 'PREPEND_LEN':
            str_byte = '2'
        else:
            if bytecode.string_mode == 'NULL_TERMINATED':
                str_byte = '0'
            else:
                if bytecode.string_mode == None:
                    str_byte = self.header[11]
                    bytecode.set_string_mode(str_byte)
                else:
                    raise SyntaxError('Invalid string mode')
        bytecode.write(bytes(self.header[:11] + str_byte + self.header[12:], 'utf-8'))
        self.meta.encode_to(bytecode)
        bytecode.write(bytes('\n', 'utf-8'))
        self.contents.encode_to(bytecode)

    def decode(self, bytecode, meta_only=False):
        if bytecode.contents_len < 40:
            return
            bytecode.set_string_mode()
            self.header = bytecode.read_str(40)
            if not self.header[:4] == 'BtWg' and int(self.header[4:40], 16) or self.header[11] == '2' or self.header[11] == '0':
                bytecode.set_string_mode(self.header[11])
                self.meta.decode(bytecode)
                if bytecode.read_int(1) != 10:
                    pass
                elif meta_only:
                    return
                    self.contents = bw_object.BW_Object.decode(bytecode)
                elif self.header[11] == '1':
                    raise TypeError('"' + self.header + '" is a json typed file')
                else:
                    raise TypeError('"' + self.header + '" is not a valid type')
        else:
            print(self.header)
            raise TypeError('"' + self.header + '" is not a valid header')

    def set_meta(self):
        pass

    def write(self, path, json=False):
        self.set_meta()
        from pytwig.src.lib import fs
        bytecode = BW_Bytecode()
        self.encode_to(bytecode)
        fs.write_binary(path, bytecode.contents)

    def export(self, path):
        self.set_meta()
        from pytwig.src.lib import fs
        fs.write(path, self.serialize().replace('":', '" :'))

    def read(self, path, raw=True, meta_only=False):
        from pytwig.src.lib import fs
        bytecode = BW_Bytecode().set_contents(fs.read_binary(path))
        bytecode.raw = raw
        bytecode.debug_obj = self
        self.decode(bytecode, meta_only=meta_only)


BW_VERSION = '2.4.2'
BW_FILE_META_TEMPLATE = [
 'application_version_name', 'branch', 'creator',
 'revision_id', 'revision_no', 'tags', 'type']
BW_DEVICE_META_TEMPLATE = [
 'comment', 'device_category', 'device_id', 'device_name',
 'additional_device_types', 'device_description', 'device_type', 'device_uuid',
 'has_audio_input', 'has_audio_output', 'has_note_input', 'has_note_output',
 'suggest_for_audio_input', 'suggest_for_note_input']
BW_MODULATOR_META_TEMPLATE = [
 'comment', 'device_category', 'device_id', 'device_name',
 'device_creator', 'device_type', 'preset_category', 'referenced_device_ids', 'referenced_packaged_file_ids']
BW_PRESET_META_TEMPLATE = [
 'comment', 'device_category', 'device_id', 'device_name',
 'device_creator', 'device_type', 'preset_category',
 'referenced_device_ids', 'referenced_modulator_ids', 'referenced_module_ids', 'referenced_packaged_file_ids']
BW_CLIP_META_TEMPLATE = [
 'beat_length', 'bpm', 'referenced_packaged_file_ids']

class BW_Meta(bw_object.BW_Object):

    def __init__(self, type=None):
        self.data = OrderedDict()
        if type == None:
            return
        self.classname = 'meta'
        for each_field in BW_FILE_META_TEMPLATE:
            self.data[each_field] = util.get_field_default(each_field)
        else:
            if type == 'application/bitwig-device':
                for each_field in BW_DEVICE_META_TEMPLATE:
                    self.data[each_field] = util.get_field_default(each_field)

            else:
                if type == 'application/bitwig-modulator':
                    for each_field in BW_MODULATOR_META_TEMPLATE:
                        self.data[each_field] = util.get_field_default(each_field)

                else:
                    if type == 'application/bitwig-preset':
                        for each_field in BW_PRESET_META_TEMPLATE:
                            self.data[each_field] = util.get_field_default(each_field)

                    else:
                        if type == 'application/bitwig-note-clip':
                            for each_field in BW_CLIP_META_TEMPLATE:
                                self.data[each_field] = util.get_field_default(each_field)

                        else:
                            raise TypeError('Type "' + type + '" is an invalid application type')
            self.data['application_version_name'] = BW_VERSION
            self.data['type'] = type
            self.data = OrderedDict(sorted((self.data.items()), key=(lambda t: t[0])))

    def encode_to(self, bytecode):
        bytecode.write('00000004')
        bytecode.write_str('meta')
        for each_field in self.data:
            bytecode.write('00000001')
            bytecode.write_str(each_field)
            self.encode_field(bytecode, each_field)
        else:
            bytecode.write('00000000')

    def decode(self, bytecode):
        if not bytecode.reading_meta:
            raise SyntaxError('BW_Bytecode in wrong read mode')
        else:
            if bytecode.read(4) != bytes([0, 0, 0, 4]):
                raise TypeError()
            self.classname = bytecode.read_str()
            while True:
                if bytecode.peek(4) != bytes([0, 0, 0, 0]):
                    type = bytecode.read_int()
                    if type == 1:
                        key = bytecode.read_str()
                        self.data[key] = self.parse_field(bytecode)
                    elif type == 4:
                        raise TypeError('No objects should be in root of metadata')
                        str_len = util.btoi(bytecode[:4])
                        bytecode = bytecode[4:]
                        name = str(bytecode[:length], 'utf-8')
                        bytecode = bytecode[str_len:]
                    else:
                        bytecode.increment_position(-48)
                        print(bytecode.peek(40))
                        raise TypeError('mystery type?!?')

        bytecode.increment_position(4)


class BW_Collection:

    def __init__(self):
        self.header = 0
        self.packaged_items = []
        self.unpackaged_items = []

    def read(self, path):
        from pytwig.src.lib import fs
        bytecode = BW_Bytecode().set_contents(fs.read_binary(path))
        bytecode.raw = True
        bytecode.set_string_mode('PREPEND_LEN')
        bytecode.debug_obj = self
        self.decode(bytecode)

    def decode(self, bytecode):
        self.header = bytecode.read(16)
        num_unpackaged = bytecode.read_int()
        for i in range(num_unpackaged):
            self.unpackaged_items.append(bytecode.read_str())
            bytecode.increment_position(4)
        else:
            num_packaged = bytecode.read_int()
            for i in range(num_packaged):
                self.packaged_items.append(bytecode.read_str())

    def encode_to(self, bytecode):
        bytecode.write(self.header)
        bytecode.write_int(len(self.unpackaged_items))
        for each_entry in self.unpackaged_items:
            bytecode.write_str(each_entry)
            bytecode.write_int(0)
        else:
            bytecode.write_int(len(self.packaged_items))
            for each_entry in self.packaged_items:
                bytecode.write_str(each_entry)

    def write(self, path):
        bytecode = BW_Bytecode()
        bytecode.set_string_mode('PREPEND_LEN')
        bytecode.raw = True
        bytecode.debug_obj = self
        self.encode_to(bytecode)
        from pytwig.src.lib import fs
        fs.write_binary(path, bytecode.contents)

    def __str__(self):
        return str(self.unpackaged_items + self.packaged_items)

    def __dict__(self):
        return {'header':self.header, 
         'meta':self.meta,  'contents':self.contents}


class BW_Bytecode:

    def __init__(self, contents=''):
        self.debug_obj = None
        self.contents = ''
        self.contents_len = 0
        if contents != '':
            self.contents = contents
        self.position = 0
        self.reading_meta = True
        self.obj_list = [None]
        self.meta_only = False
        self.raw = False
        self.string_mode = None

    def set_contents(self, contents):
        self.contents = contents
        self.contents_len = len(contents)
        self.position = 0
        if self.contents_len >= 40:
            if self.contents[11] == b'2':
                self.string_mode = 'PREPEND_LEN'
            else:
                if self.contents[11] == b'0':
                    self.string_mode = 'NULL_TERMINATED'
        return self

    def set_string_mode(self, new_string_mode=None):
        if new_string_mode == None:
            new_string_mode = str(self.contents[11])
        elif len(new_string_mode) == 1:
            if new_string_mode == '0':
                self.string_mode = 'NULL_TERMINATED'
            elif new_string_mode == '2':
                self.string_mode = 'PREPEND_LEN'
            elif new_string_mode == '1':
                raise SyntaxError('invalid string mode: header is json typed')
            else:
                raise SyntaxError('invalid string mode: ' + new_string_mode)
        else:
            self.string_mode = new_string_mode

    def reset_pos(self):
        self.position = 0

    def peek(self, length=1):
        return self.contents[self.position:self.position + length]

    def read(self, length=1):
        output = self.peek(length)
        self.position += length
        return output

    def read_str--- This code section failed: ---

 L. 340         0  LOAD_FAST                'length'
                2  LOAD_CONST               None
                4  COMPARE_OP               !=
                6  POP_JUMP_IF_FALSE    72  'to 72'

 L. 341         8  LOAD_FAST                'self'
               10  LOAD_METHOD              peek
               12  LOAD_FAST                'length'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'output'

 L. 342        18  LOAD_FAST                'self'
               20  DUP_TOP          
               22  LOAD_ATTR                position
               24  LOAD_FAST                'length'
               26  INPLACE_ADD      
               28  ROT_TWO          
               30  STORE_ATTR               position

 L. 343        32  SETUP_FINALLY        46  'to 46'

 L. 344        34  LOAD_GLOBAL              str
               36  LOAD_FAST                'output'
               38  LOAD_STR                 'utf-8'
               40  CALL_FUNCTION_2       2  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    32  '32'

 L. 345        46  DUP_TOP          
               48  LOAD_GLOBAL              UnicodeDecodeError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    68  'to 68'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 346        60  LOAD_FAST                'output'
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM            52  '52'

 L. 347        68  END_FINALLY      
               70  JUMP_FORWARD        250  'to 250'
             72_0  COME_FROM             6  '6'

 L. 349        72  LOAD_FAST                'self'
               74  LOAD_ATTR                string_mode
               76  LOAD_STR                 'PREPEND_LEN'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   172  'to 172'

 L. 350        82  LOAD_FAST                'self'
               84  LOAD_METHOD              read_int
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'str_len'

 L. 351        90  LOAD_FAST                'str_len'
               92  LOAD_CONST               2147483648
               94  BINARY_AND       
               96  POP_JUMP_IF_FALSE   116  'to 116'

 L. 352        98  LOAD_FAST                'str_len'
              100  LOAD_CONST               2147483647
              102  INPLACE_AND      
              104  STORE_FAST               'str_len'

 L. 353       106  LOAD_STR                 'utf-16'
              108  STORE_FAST               'char_enc'

 L. 354       110  LOAD_CONST               2
              112  STORE_FAST               'char_len'
              114  JUMP_FORWARD        124  'to 124'
            116_0  COME_FROM            96  '96'

 L. 356       116  LOAD_STR                 'utf-8'
              118  STORE_FAST               'char_enc'

 L. 357       120  LOAD_CONST               1
              122  STORE_FAST               'char_len'
            124_0  COME_FROM           114  '114'

 L. 358       124  LOAD_FAST                'str_len'
              126  LOAD_CONST               100000
              128  COMPARE_OP               >
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L. 359       132  LOAD_GLOBAL              TypeError
              134  LOAD_STR                 'String is too long'
              136  CALL_FUNCTION_1       1  ''
              138  RAISE_VARARGS_1       1  'exception instance'
              140  JUMP_FORWARD        162  'to 162'
            142_0  COME_FROM           130  '130'

 L. 361       142  LOAD_FAST                'self'
              144  LOAD_METHOD              read
              146  LOAD_FAST                'str_len'
              148  LOAD_FAST                'char_len'
              150  BINARY_MULTIPLY  
              152  CALL_METHOD_1         1  ''
              154  LOAD_METHOD              decode
              156  LOAD_FAST                'char_enc'
              158  CALL_METHOD_1         1  ''
              160  RETURN_VALUE     
            162_0  COME_FROM           140  '140'

 L. 362       162  LOAD_FAST                'self'
              164  LOAD_METHOD              read_str
              166  LOAD_FAST                'str_len'
              168  CALL_METHOD_1         1  ''
              170  RETURN_VALUE     
            172_0  COME_FROM            80  '80'

 L. 363       172  LOAD_FAST                'self'
              174  LOAD_ATTR                string_mode
              176  LOAD_STR                 'NULL_TERMINATED'
              178  COMPARE_OP               ==
          180_182  POP_JUMP_IF_FALSE   232  'to 232'

 L. 364       184  LOAD_STR                 ''
              186  STORE_FAST               'output'

 L. 365       188  LOAD_FAST                'self'
              190  LOAD_METHOD              peek_int
              192  LOAD_CONST               1
              194  CALL_METHOD_1         1  ''
              196  POP_JUMP_IF_FALSE   212  'to 212'

 L. 366       198  LOAD_FAST                'output'
              200  LOAD_FAST                'self'
              202  LOAD_METHOD              read
              204  CALL_METHOD_0         0  ''
              206  INPLACE_ADD      
              208  STORE_FAST               'output'
              210  JUMP_BACK           188  'to 188'
            212_0  COME_FROM           196  '196'

 L. 367       212  LOAD_FAST                'self'
              214  LOAD_METHOD              increment_position
              216  LOAD_CONST               1
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          

 L. 368       222  LOAD_GLOBAL              str
              224  LOAD_FAST                'output'
              226  LOAD_STR                 'utf-8'
              228  CALL_FUNCTION_2       2  ''
              230  RETURN_VALUE     
            232_0  COME_FROM           180  '180'

 L. 370       232  LOAD_GLOBAL              print
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                string_mode
              238  CALL_FUNCTION_1       1  ''
              240  POP_TOP          

 L. 371       242  LOAD_GLOBAL              SyntaxError
              244  LOAD_STR                 'Invalid string mode'
              246  CALL_FUNCTION_1       1  ''
              248  RAISE_VARARGS_1       1  'exception instance'
            250_0  COME_FROM            70  '70'

Parse error at or near `POP_TOP' instruction at offset 56

    def read_int(self, len=4):
        return util.btoi(self.read(len))

    def peek_int(self, len=4):
        return util.btoi(self.peek(len))

    def write(self, append):
        if isinstance(append, bytes):
            self.contents += append
        else:
            if isinstance(append, str):
                self.contents += bytes.fromhex(append)
            else:
                raise TypeError('Cannot write a non-bytes file')
        self.contents_len = len(self.contents)

    def write_str(self, string):
        if self.string_mode == 'PREPEND_LEN':
            try:
                string.encode('ascii')
            except UnicodeEncodeError:
                self.contents += bytes.fromhex(hex(2147483648 + len(string))[2:])
                self.contents += string.encode('utf-16be')
            else:
                self.contents += util.hex_pad(len(string), 8)
                self.contents += string.encode('utf-8')
        else:
            if self.string_mode == 'NULL_TERMINATED':
                self.contents += string.encode('utf-8')
                self.contents += bytes([0])
            else:
                raise SyntaxError('Invalid string mode')

    def write_int(self, num, pad=8):
        self.contents += util.hex_pad(num, pad)
        self.contents_len = len(self.contents)

    def increment_position(self, amt):
        if self.position + amt > self.contents_len:
            raise EOFError('End of file')
        self.position = self.position + amt


class BW_Clip_File(BW_File):

    def __init__(self, track=None):
        super().__init__('note-clip')
        document = bw_object.BW_Object(46)
        if track == None:
            document.get('track_group(1245)').get('main_tracks(1246)').append(bw_track.Track())
        else:
            document.get('track_group(1245)').get('main_tracks(1246)').append(track)
        self.contents = bw_object.BW_Object('clip_document(479)').set('document(2409)', document)

    def set_meta(self):
        self.meta.data['beat_length'] = 1.0

    def get_main_track(self):
        if len(self.contents.get(2409).get(1245).get(1246)) == 0:
            print('No main tracks in clip file')
            return None
        return self.contents.get(2409).get(1245).get(1246)[0]

    def set_main_track(self, track):
        self.contents.get(2409).get(1245).get(1246).insert(0, track)
        return self


class BW_Device(BW_File):

    def __init__(self, track=None):
        super().__init__('device')
        self.contents = bw_object.BW_Object(151)

    def get_atoms(self):
        return self.contents.get(173) + self.contents.get(177) + self.contents.get(178)

    def get_panels(self):
        return self.contents.get(6213)