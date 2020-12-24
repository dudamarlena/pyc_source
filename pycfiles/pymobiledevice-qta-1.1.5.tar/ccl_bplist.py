# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/ccl_bplist.py
# Compiled at: 2019-02-24 18:45:28
__doc__ = '\nCopyright (c) 2012, CCL Forensics\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are met:\n    * Redistributions of source code must retain the above copyright\n      notice, this list of conditions and the following disclaimer.\n    * Redistributions in binary form must reproduce the above copyright\n      notice, this list of conditions and the following disclaimer in the\n      documentation and/or other materials provided with the distribution.\n    * Neither the name of the CCL Forensics nor the\n      names of its contributors may be used to endorse or promote products\n      derived from this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\nWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL CCL FORENSICS BE LIABLE FOR ANY\nDIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\nLOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\nON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
import sys, os, struct, datetime
__version__ = '0.11'
__description__ = 'Converts Apple binary PList files into a native Python data structure'
__contact__ = 'Alex Caithness'

class BplistError(Exception):
    pass


class BplistUID:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return ('UID: {0}').format(self.value)

    def __str__(self):
        return self.__repr__()


def __decode_multibyte_int(b, signed=True):
    if len(b) == 1:
        fmt = '>B'
    elif len(b) == 2:
        fmt = '>h'
    elif len(b) == 3:
        if signed:
            return (b[0] << 16 | struct.unpack('>H', b[1:])[0]) - (b[0] >> 7) * 2 * 8388608
        else:
            return b[0] << 16 | struct.unpack('>H', b[1:])[0]

    elif len(b) == 4:
        fmt = '>i'
    elif len(b) == 8:
        fmt = '>q'
    else:
        raise BplistError(('Cannot decode multibyte int of length {0}').format(len(b)))
    if signed and len(b) > 1:
        return struct.unpack(fmt.lower(), b)[0]
    else:
        return struct.unpack(fmt.upper(), b)[0]


def __decode_float(b, signed=True):
    if len(b) == 4:
        fmt = '>f'
    elif len(b) == 8:
        fmt = '>d'
    else:
        raise BplistError(('Cannot decode float of length {0}').format(len(b)))
    if signed:
        return struct.unpack(fmt.lower(), b)[0]
    else:
        return struct.unpack(fmt.upper(), b)[0]


def __decode_object(f, offset, collection_offset_size, offset_table):
    f.seek(offset)
    if sys.version_info[0] < 3:
        type_byte = ord(f.read(1)[0])
    else:
        type_byte = f.read(1)[0]
    if type_byte == 0:
        return
    else:
        if type_byte == 8:
            return False
        if type_byte == 9:
            return True
        if type_byte == 15:
            raise BplistError(('Fill type not currently supported at offset {0}').format(f.tell()))
        else:
            if type_byte & 240 == 16:
                int_length = 2 ** (type_byte & 15)
                int_bytes = f.read(int_length)
                return __decode_multibyte_int(int_bytes)
            if type_byte & 240 == 32:
                float_length = 2 ** (type_byte & 15)
                float_bytes = f.read(float_length)
                return __decode_float(float_bytes)
            if type_byte & 255 == 51:
                date_bytes = f.read(8)
                date_value = __decode_float(date_bytes)
                return datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=date_value)
            if type_byte & 240 == 64:
                if type_byte & 15 != 15:
                    data_length = type_byte & 15
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long Data field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    data_length = __decode_multibyte_int(int_bytes, False)
                return f.read(data_length)
            if type_byte & 240 == 80:
                if type_byte & 15 != 15:
                    ascii_length = type_byte & 15
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long ASCII field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    ascii_length = __decode_multibyte_int(int_bytes, False)
                return f.read(ascii_length).decode('ascii')
            if type_byte & 240 == 96:
                if type_byte & 15 != 15:
                    utf16_length = (type_byte & 15) * 2
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long UTF-16 field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    utf16_length = __decode_multibyte_int(int_bytes, False) * 2
                return f.read(utf16_length).decode('utf_16_be')
            if type_byte & 240 == 128:
                uid_length = (type_byte & 15) + 1
                uid_bytes = f.read(uid_length)
                return BplistUID(__decode_multibyte_int(uid_bytes, signed=False))
            if type_byte & 240 == 160:
                if type_byte & 15 != 15:
                    array_count = type_byte & 15
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long Array field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    array_count = __decode_multibyte_int(int_bytes, signed=False)
                array_refs = []
                for i in range(array_count):
                    array_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))

                return [ __decode_object(f, offset_table[obj_ref], collection_offset_size, offset_table) for obj_ref in array_refs ]
            if type_byte & 240 == 192:
                if type_byte & 15 != 15:
                    set_count = type_byte & 15
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long Set field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    set_count = __decode_multibyte_int(int_bytes, signed=False)
                set_refs = []
                for i in range(set_count):
                    set_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))

                return [ __decode_object(f, offset_table[obj_ref], collection_offset_size, offset_table) for obj_ref in set_refs ]
            if type_byte & 240 == 208:
                if type_byte & 15 != 15:
                    dict_count = type_byte & 15
                else:
                    if sys.version_info[0] < 3:
                        int_type_byte = ord(f.read(1)[0])
                    else:
                        int_type_byte = f.read(1)[0]
                    if int_type_byte & 240 != 16:
                        raise BplistError(('Long Dict field definition not followed by int type at offset {0}').format(f.tell()))
                    int_length = 2 ** (int_type_byte & 15)
                    int_bytes = f.read(int_length)
                    dict_count = __decode_multibyte_int(int_bytes, signed=False)
                key_refs = []
                for i in range(dict_count):
                    key_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))

                value_refs = []
                for i in range(dict_count):
                    value_refs.append(__decode_multibyte_int(f.read(collection_offset_size), False))

                dict_result = {}
                for i in range(dict_count):
                    key = __decode_object(f, offset_table[key_refs[i]], collection_offset_size, offset_table)
                    val = __decode_object(f, offset_table[value_refs[i]], collection_offset_size, offset_table)
                    dict_result[key] = val

                return dict_result
        return


def load(f):
    """
    Reads and converts a file-like object containing a binary property list.
    Takes a file-like object (must support reading and seeking) as an argument
    Returns a data structure representing the data in the property list
    """
    if f.read(8) != 'bplist00':
        raise BplistError('Bad file header')
    f.seek(-32, os.SEEK_END)
    trailer = f.read(32)
    offset_int_size, collection_offset_size, object_count, top_level_object_index, offest_table_offset = struct.unpack('>6xbbQQQ', trailer)
    f.seek(offest_table_offset)
    offset_table = []
    for i in range(object_count):
        offset_table.append(__decode_multibyte_int(f.read(offset_int_size), False))

    return __decode_object(f, offset_table[top_level_object_index], collection_offset_size, offset_table)


def NSKeyedArchiver_convert(o, object_table):
    if isinstance(o, list):
        return NsKeyedArchiverList(o, object_table)
    else:
        if isinstance(o, dict):
            return NsKeyedArchiverDictionary(o, object_table)
        if isinstance(o, BplistUID):
            return NSKeyedArchiver_convert(object_table[o.value], object_table)
        return o


class NsKeyedArchiverDictionary(dict):

    def __init__(self, original_dict, object_table):
        super(NsKeyedArchiverDictionary, self).__init__(original_dict)
        self.object_table = object_table

    def __getitem__(self, index):
        o = super(NsKeyedArchiverDictionary, self).__getitem__(index)
        return NSKeyedArchiver_convert(o, self.object_table)


class NsKeyedArchiverList(list):

    def __init__(self, original_iterable, object_table):
        super(NsKeyedArchiverList, self).__init__(original_iterable)
        self.object_table = object_table

    def __getitem__(self, index):
        o = super(NsKeyedArchiverList, self).__getitem__(index)
        return NSKeyedArchiver_convert(o, self.object_table)

    def __iter__(self):
        for o in super(NsKeyedArchiverList, self).__iter__():
            yield NSKeyedArchiver_convert(o, self.object_table)


def deserialise_NsKeyedArchiver(obj):
    """Deserialises an NSKeyedArchiver bplist rebuilding the structure.
       obj should usually be the top-level object returned by the load()
       function."""
    if not isinstance(obj, dict):
        raise TypeError('obj must be a dict')
    if '$archiver' not in obj or obj['$archiver'] != 'NSKeyedArchiver':
        raise ValueError("obj does not contain an '$archiver' key or the '$archiver' is unrecognised")
    if '$version' not in obj or obj['$version'] != 100000:
        raise ValueError("obj does not contain a '$version' key or the '$version' is unrecognised")
    object_table = obj['$objects']
    if 'root' in obj['$top']:
        return NSKeyedArchiver_convert(obj['$top']['root'], object_table)
    else:
        return NSKeyedArchiver_convert(obj['$top'], object_table)


def is_nsmutabledictionary(obj):
    if not isinstance(obj, dict):
        return False
    if '$class' not in obj.keys():
        return False
    if obj['$class'].get('$classname') != 'NSMutableDictionary':
        return False
    if 'NS.keys' not in obj.keys():
        return False
    if 'NS.objects' not in obj.keys():
        return False
    return True


def convert_NSMutableDictionary(obj):
    """Converts a NSKeyedArchiver serialised NSMutableDictionary into
       a straight dictionary (rather than two lists as it is serialised
       as)"""
    if not is_nsmutabledictionary(obj):
        raise ValueError('obj does not have the correct structure for a NSMutableDictionary serialised to a NSKeyedArchiver')
    keys = obj['NS.keys']
    vals = obj['NS.objects']
    if not isinstance(keys, list):
        raise TypeError(("The 'NS.keys' value is an unexpected type (expected list; actual: {0}").format(type(keys)))
    if not isinstance(vals, list):
        raise TypeError(("The 'NS.objects' value is an unexpected type (expected list; actual: {0}").format(type(vals)))
    if len(keys) != len(vals):
        raise ValueError(("The length of the 'NS.keys' list ({0}) is not equal to that of the 'NS.objects ({1})").format(len(keys), len(vals)))
    result = {}
    for i, k in enumerate(keys):
        if 'k' in result:
            raise ValueError("The 'NS.keys' list contains duplicate entries")
        result[k] = vals[i]

    return result