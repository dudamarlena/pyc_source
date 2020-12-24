# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cs/prj/quantumcore/src/quantumcore.contenttypes/quantumcore/contenttypes/pymagic/magic.py
# Compiled at: 2010-04-21 06:17:08
import os, re, string, cStringIO, pkg_resources, convert

class Failed(Exception):
    pass


class Magic(object):
    """the main magic detection class"""
    data_size = {'byte': 1, 'short': 2, 'long': 4, 'string': 1, 'pstring': 1, 'date': 4, 'ldate': 4}
    type_size = {'b': 1, 'B': 1, 's': 2, 'S': 2, 'l': 4, 'L': 5}
    se_offset_abs = '^\\(([0\\\\][xX][\\dA-Fa-f]+|[0\\\\][0-7]*|\\d+)(\\.[bslBSL])*\\)'
    se_offset_add = '^\\(([0\\\\][xX][\\dA-Fa-f]+|[0\\\\][0-7]*|\\d+)(\\.[bslBSL])*([-+])([0\\\\][xX][\\dA-Fa-f]+|[0\\\\][0-7]*|\\d+)\\)'

    def __init__(self, fp=None, cachename=None):
        """initialize the magic object with a ``fp`` from which the magic data to load and a ``cachename`` in which to store
                the parsed data to make it load faster next time. """
        if fp is None:
            fp = pkg_resources.resource_stream(__name__, 'magic.mime')
        self.entries = 0
        self._level = {}
        self._direct = {}
        self._offset_relatif = {}
        self._offset_type = {}
        self._offset_delta = {}
        self._endian = {}
        self._kind = {}
        self._oper = {}
        self._mask = {}
        self._test = {}
        self._data = {}
        self._length = {}
        self._mime = {}
        if not os.path.isfile(cachename):
            self.read_magic(fp)
            self.write_cache(cachename)
        self.read_cache(cachename)
        return

    def __split(self, line):
        result = ''
        split = line.split()
        again = 1
        while again:
            again = 0
            pos = 0
            part = []
            top = len(split)
            while pos < top:
                if convert.is_final_dash(split[pos]):
                    result = split[pos] + ' '
                    index = line.find(result)
                    if index != -1:
                        char = line[(index + len(result))]
                        if char != ' ' and char != '\t':
                            pos += 1
                            result += split[pos]
                            again = 1
                else:
                    result = split[pos]
                part.append(result)
                pos += 1

            split = part

        return part

    def __level(self, text):
        return string.count(text, '>')

    def __strip_start(self, char, text):
        if text[0] == char:
            return text[1:]
        return text

    def __direct_offset(self, text):
        if text[0] == '(' and text[(-1)] == ')':
            return 0
        return 1

    def __offset(self, text):
        direct = self.__direct_offset(text)
        offset_type = 'l'
        offset_delta = 0
        offset_relatif = 0
        if direct:
            offset_delta = convert.convert(text)
        else:
            match_abs = re.compile(self.se_offset_abs).match(text)
            match_add = re.compile(self.se_offset_add).match(text)
            if match_abs:
                offset_relatif = convert.convert(match_abs.group(1))
                if match_abs.group(2) != None:
                    offset_type = match_abs.group(2)[1]
            elif match_add:
                offset_relatif = convert.convert(match_add.group(1))
                if match_add.group(2) != None:
                    offset_type = match_add.group(2)[1]
                if match_add.group(3) == '-':
                    offset_delta = 0 - match_add.group(4)
                else:
                    offset_delta = convert.convert(match_add.group(4))
        return (
         direct, offset_type, offset_delta, offset_relatif)

    def __oper_mask(self, text):
        type_mask_and = string.split(text, '&')
        type_mask_or = string.split(text, '^')
        if len(type_mask_and) > 1:
            oper = '&'
            mask = convert.convert(type_mask_and[1])
            rest = type_mask_and[0]
            return (oper, mask, rest)
        elif len(type_mask_or) > 1:
            oper = '^'
            mask = convert.convert(type_mask_or[1])
            rest = type_mask_or[0]
            return (oper, mask, rest)
        else:
            return (
             '', 0, text)

    def __endian(self, full_type):
        if full_type.startswith('be'):
            return 'big'
        elif full_type.startswith('le'):
            return 'little'
        return 'local'

    def __kind(self, full_type, endian):
        if endian == 'local':
            kind = full_type
        else:
            kind = full_type[2:]
        if kind.startswith('string/'):
            NOT_DONE_YET = kind[7:]
            kind = 'string'
        if kind.startswith('ldate-'):
            NOT_DONE_YET = kind[6:]
            kind = 'ldate'
        return kind

    def __test_result(self, test_result):
        if test_result[0] in '=><&!^':
            test = test_result[0]
            result = test_result[1:]
            return (test, result)
        elif test_result == 'x':
            test = 'x'
            result = 'x'
            return (test, result)
        else:
            test = '='
            result = test_result
            return (test, result)

    def __string(self, list):
        r = []
        for s in list:
            if type(s) is str:
                if s == '\\0':
                    r.append(chr(0))
                else:
                    r.append(s)
            elif s < 10:
                r.append(ord(str(s)))
            else:
                r.append(s)

        return r

    def __data(self, kind, result):
        pos = 0
        data = list('')
        prev = ''
        while pos < len(result):
            if convert.is_c_escape(result[pos:]):
                if result[(pos + 1)] == '0':
                    data.append(result[pos])
                    data.append(0)
                else:
                    data.append(result[pos:pos + 2])
                pos += 2
            elif kind == 'string' and (result[pos] in string.ascii_letters or result[pos] in string.digits):
                data.append(ord(result[pos]) * 1)
                pos += 1
            else:
                base = convert.which_base(result[pos:])
                if base == 0:
                    data.append(ord(result[pos]) * 1)
                    pos += 1
                else:
                    size_base = convert.size_base(base)
                    size_number = convert.size_number(result[pos:])
                    start = pos + size_base
                    end = pos + size_number
                    nb = convert.base10(result[start:end], base)
                    pos += size_number
                    data.append(nb * 1)

        return data

    def __length(self, kind, data):
        if kind == 'string':
            replace = ''
            for i in data:
                try:
                    replace += chr(i)
                except:
                    replace += '*'

            replace = replace.replace('*\x00', '*')
            replace = replace.replace('\\\\', '*')
            replace = replace.replace('\\', '')
            length = len(replace)
        else:
            length = self.data_size[kind]
        return length

    def __mime(self, list):
        mime = ''
        for name in list:
            mime += name + ' '

        mime = mime.rstrip()
        mime = mime.replace('\\a', '\x07')
        mime = mime.replace('\\b', '\x08')
        mime = mime.replace('\\f', '\x0c')
        mime = mime.replace('\\n', '\n')
        mime = mime.replace('\\r', '\r')
        mime = mime.replace('\\t', '\t')
        mime = mime.replace('\\v', '\x0b')
        mime = mime.replace('\\0', '\x00')
        return mime

    def read_magic(self, f):
        """read the magic file given in filepointer ``f``"""
        self.magic = []
        index = 0
        for line in f.readlines():
            line = line.strip()
            if line and not line.startswith('#'):
                part = self.__split(line)
                while len(part) < 4:
                    part.append('\x08')

                level = self.__level(part[0])
                offset_string = self.__strip_start('&', part[0][level:])
                (direct, offset_type, offset_delta, offset_relatif) = self.__offset(offset_string)
                (oper, mask, rest) = self.__oper_mask(part[1])
                full_type = self.__strip_start('u', rest)
                endian = self.__endian(full_type)
                kind = self.__kind(full_type, endian)
                (test, result) = self.__test_result(part[2])
                data = self.__data(kind, result)
                length = self.__length(kind, data)
                mime = self.__mime(part[3:])
                self._level[index] = level
                self._direct[index] = direct
                self._offset_type[index] = offset_type
                self._offset_delta[index] = offset_delta
                self._offset_relatif[index] = offset_relatif
                self._endian[index] = endian
                self._kind[index] = kind
                self._oper[index] = oper
                self._mask[index] = mask
                self._test[index] = test
                self._data[index] = data
                self._length[index] = length
                self._mime[index] = mime
                self.entries = index
                index += 1

        f.close()

    def write_cache(self, name):
        f = open(name, 'wb')
        import cPickle
        cPickle.dump(self._level, f, 1)
        cPickle.dump(self._direct, f, 1)
        cPickle.dump(self._offset_relatif, f, 1)
        cPickle.dump(self._offset_type, f, 1)
        cPickle.dump(self._offset_delta, f, 1)
        cPickle.dump(self._endian, f, 1)
        cPickle.dump(self._kind, f, 1)
        cPickle.dump(self._oper, f, 1)
        cPickle.dump(self._mask, f, 1)
        cPickle.dump(self._test, f, 1)
        cPickle.dump(self._data, f, 1)
        cPickle.dump(self._length, f, 1)
        cPickle.dump(self._mime, f, 1)
        f.close()

    def read_cache(self, name):
        f = open(name, 'rb')
        import cPickle
        self._level = cPickle.load(f)
        self._direct = cPickle.load(f)
        self._offset_relatif = cPickle.load(f)
        self._offset_type = cPickle.load(f)
        self._offset_delta = cPickle.load(f)
        self._endian = cPickle.load(f)
        self._kind = cPickle.load(f)
        self._oper = cPickle.load(f)
        self._mask = cPickle.load(f)
        self._test = cPickle.load(f)
        self._data = cPickle.load(f)
        self._length = cPickle.load(f)
        self._mime = cPickle.load(f)
        self.entries = len(self._level)
        f.close()

    def __indirect_offset(self, file, type, offset):
        f.seek(offset)
        if type == 'l':
            delta = convert.little4(self.__read(f, 4))
        elif type == 'L':
            delta = convert.big4(self.__read(f, 4))
        elif type == 's':
            delta = convert.little2(self.__read(f, 2))
        elif type == 'S':
            delta = convert.big2(self.__read(f, 2))
        elif type == 'b':
            delta = ord(self.__read(f, 1))
        elif type == 'B':
            delta = ord(self.__read(f, 1))
        return offset + delta

    def __read(self, file, number):
        data = file.read(number)
        if not data:
            raise IOError, 'out of file access'
        return data

    def __convert(self, kind, endian, data):
        value = 0
        if kind == 'byte':
            if len(data) < 1:
                raise StandardError, 'Should never happen, not enough data'
            value = ord(data[0])
        elif kind == 'short':
            if len(data) < 2:
                raise StandardError, 'Should never happen, not enough data'
            if endian == 'local':
                value = convert.local2(data)
            elif endian == 'little':
                value = convert.little2(data)
            elif endian == 'big':
                value = convert.big2(data)
            else:
                raise StandardError, 'Endian type unknown'
        elif kind == 'long':
            if len(data) < 4:
                raise StandardError, 'Should never happen, not enough data'
            if endian == 'local':
                value = convert.local4(data)
            elif endian == 'little':
                value = convert.little4(data)
            elif endian == 'big':
                value = convert.big4(data)
            else:
                raise StandardError, 'Endian type unknown'
        elif kind == 'date':
            pass
        elif kind == 'ldate':
            pass
        elif kind == 'string':
            pass
        elif kind == 'pstring':
            pass
        else:
            raise StandardError, 'Type ' + str(kind) + ' not recognised'
        return value

    def __binary_mask(self, oper, value, mask):
        if oper == '&':
            value &= mask
        elif oper == '^':
            value ^= mask
        elif oper == '':
            pass
        else:
            raise StandardError, 'Binary operator unknown ' + str(oper)
        return value

    def __read_string(self, file):
        limit = 0
        result = ''
        while limit < 100:
            char = self.__read(file, 1)
            if char == '\x00' or char == '\n':
                break
            result += char
            limit += 1

        if limit == 100:
            raise Failed()
        return result

    def __is_null_string(self, data):
        return len(data) == 2 and data[0] == '\\' and data[1] == 0

    def classify(self, buffer):
        """classify the buffer contents"""
        if not self.entries:
            raise StandardError, 'Not initialised properly'
        found_rule = 0
        in_level = 0
        allow_next = 0
        result = ''
        f = cStringIO.StringIO(buffer)
        f.seek(0, 2)
        file_length = f.tell()
        for i in range(self.entries):
            level = self._level[i]
            if not found_rule and level > 0:
                continue
            if found_rule:
                if level == 0:
                    break
                if level > allow_next:
                    continue
            direct = self._direct[i]
            offset_type = self._offset_type[i]
            offset_delta = self._offset_delta[i]
            offset_relatif = self._offset_relatif[i]
            endian = self._endian[i]
            kind = self._kind[i]
            oper = self._oper[i]
            mask = self._mask[i]
            test = self._test[i]
            data = self._data[i]
            leng = self._length[i]
            mime = self._mime[i]
            value = 0
            success = 0
            replace = None
            try:
                if direct == 1:
                    offset = offset_delta
                else:
                    offset = self.__indirect_offset(file, offset_type, offset_delta)
                if file_length < offset:
                    raise Failed()
                f.seek(offset)
                extract = self.__read(f, leng)
                if not extract:
                    raise Failed()
                value = self.__convert(kind, endian, extract)
                value = self.__binary_mask(oper, value, mask)
                if test == '=':
                    if kind == 'string':
                        if self.__is_null_string(data):
                            success = 1
                        elif len(data) == len(extract):
                            success = 1
                            for index in range(len(data)):
                                if ord(extract[index]) != data[index]:
                                    success = 0

                    elif kind == 'pstring':
                        raise Failed, 'pstring not implemented'
                    else:
                        success = data[0] == value
                        replace = value
                elif test == '>':
                    if kind == 'string':
                        if self.__is_null_string(data):
                            if ord(extract[0]) != 0:
                                replace = extract + self.__read_string(f)
                                success = 1
                        else:
                            raise Failed, '>[^0] Not implemented'
                    elif kind == 'pstring':
                        raise Failed, 'pstring not implemented'
                    else:
                        success = value > data[0]
                        replace = value
                elif test == '<':
                    if kind == 'string':
                        success = 1
                        minimum = min(len(data), len(extract))
                        if len(extract) > minimum:
                            success = 0
                        else:
                            for index in range(minimum):
                                if data[index] > extract[index]:
                                    success = 0
                                    break

                    elif kind == 'pstring':
                        raise Failed, 'pstring not implemented'
                    else:
                        success = value < data[0]
                        replace = value
                elif test == '&':
                    success = value & data[0] == data[0]
                    replace = value
                elif test == '^':
                    success = value ^ data[0] == 0
                    replace = value
                elif test == '!':
                    success = 0
                    replace = value
                elif test == 'x':
                    if kind == 'string':
                        limit = 0
                        while 1:
                            if ord(extract[0]) == 0 or limit > 100:
                                break
                            replace += extract
                            extract = self.__read(f, 1)
                            limit += 1

                        if limit <= 100:
                            success = 1
                    elif kind == 'pstring':
                        raise Failed, 'pstring not implemented'
                    else:
                        success = 1
                        replace = value
                else:
                    raise StandardError, "test used '" + test + "' is not defined"
                if success:
                    found_rule = 1
                    in_level = level
                    allow_next = level + 1
                    if replace is not None:
                        try:
                            mime = mime % replace
                        except:
                            pass

                    if mime != []:
                        result += mime
                        result += ' '
                else:
                    raise Failed()
            except Failed, IOError:
                allow_next = level
            except:
                pass

        f.close()
        if found_rule == 0:
            return
        return result.rstrip().lstrip('').replace(' \x08', '')
        return result.rstrip().lstrip('\x08').replace(' \x08', '')


if __name__ == '__main__':
    import sys
    try:
        binname = sys.argv[1]
    except:
        binname = sys.argv[0]

    try:
        filename = sys.argv[2]
    except:
        filename = 'magic.mime'

    try:
        cachename = sys.argv[3]
    except:
        cachename = 'delete-me'

    magic = Magic(filename, cachename)
    classify = magic.classify(binname)
    if classify:
        print binname + ': ' + classify
    else:
        print binname + ': Can not recognise file type'