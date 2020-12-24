# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/idna/core.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 11844 bytes
from . import idnadata
import bisect, unicodedata, re, sys
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_unicode_dots_re = re.compile('[.。．｡]')
if sys.version_info[0] >= 3:
    unicode = str
    unichr = chr

class IDNAError(UnicodeError):
    __doc__ = ' Base exception for all IDNA-encoding related problems '


class IDNABidiError(IDNAError):
    __doc__ = ' Exception when bidirectional requirements are not satisfied '


class InvalidCodepoint(IDNAError):
    __doc__ = ' Exception when a disallowed or unallocated codepoint is used '


class InvalidCodepointContext(IDNAError):
    __doc__ = ' Exception when the codepoint is not valid in the context it is used '


def _combining_class(cp):
    v = unicodedata.combining(unichr(cp))
    if v == 0:
        if not unicodedata.name(unichr(cp)):
            raise ValueError('Unknown character in unicodedata')
    return v


def _is_script(cp, script):
    return intranges_contain(ord(cp), idnadata.scripts[script])


def _punycode(s):
    return s.encode('punycode')


def _unot(s):
    return 'U+{0:04X}'.format(s)


def valid_label_length(label):
    if len(label) > 63:
        return False
    return True


def valid_string_length(label, trailing_dot):
    if len(label) > (254 if trailing_dot else 253):
        return False
    return True


def check_bidi--- This code section failed: ---

 L.  70         0  LOAD_CONST               False
                2  STORE_FAST               'bidi_label'

 L.  71         4  SETUP_LOOP           78  'to 78'
                6  LOAD_GLOBAL              enumerate
                8  LOAD_FAST                'label'
               10  LOAD_CONST               1
               12  CALL_FUNCTION_2       2  '2 positional arguments'
               14  GET_ITER         
             16_0  COME_FROM            68  '68'
               16  FOR_ITER             76  'to 76'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'idx'
               22  STORE_FAST               'cp'

 L.  72        24  LOAD_GLOBAL              unicodedata
               26  LOAD_METHOD              bidirectional
               28  LOAD_FAST                'cp'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  STORE_FAST               'direction'

 L.  73        34  LOAD_FAST                'direction'
               36  LOAD_STR                 ''
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L.  75        42  LOAD_GLOBAL              IDNABidiError
               44  LOAD_STR                 'Unknown directionality in label {0} at position {1}'
               46  LOAD_METHOD              format
               48  LOAD_GLOBAL              repr
               50  LOAD_FAST                'label'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  LOAD_FAST                'idx'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            40  '40'

 L.  76        62  LOAD_FAST                'direction'
               64  LOAD_CONST               ('R', 'AL', 'AN')
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE    16  'to 16'

 L.  77        70  LOAD_CONST               True
               72  STORE_FAST               'bidi_label'
               74  JUMP_BACK            16  'to 16'
               76  POP_BLOCK        
             78_0  COME_FROM_LOOP        4  '4'

 L.  78        78  LOAD_FAST                'bidi_label'
               80  POP_JUMP_IF_TRUE     90  'to 90'
               82  LOAD_FAST                'check_ltr'
               84  POP_JUMP_IF_TRUE     90  'to 90'

 L.  79        86  LOAD_CONST               True
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            80  '80'

 L.  82        90  LOAD_GLOBAL              unicodedata
               92  LOAD_METHOD              bidirectional
               94  LOAD_FAST                'label'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  CALL_METHOD_1         1  '1 positional argument'
              102  STORE_FAST               'direction'

 L.  83       104  LOAD_FAST                'direction'
              106  LOAD_CONST               ('R', 'AL')
              108  COMPARE_OP               in
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L.  84       112  LOAD_CONST               True
              114  STORE_FAST               'rtl'
              116  JUMP_FORWARD        150  'to 150'
            118_0  COME_FROM           110  '110'

 L.  85       118  LOAD_FAST                'direction'
              120  LOAD_STR                 'L'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   132  'to 132'

 L.  86       126  LOAD_CONST               False
              128  STORE_FAST               'rtl'
              130  JUMP_FORWARD        150  'to 150'
            132_0  COME_FROM           124  '124'

 L.  88       132  LOAD_GLOBAL              IDNABidiError
              134  LOAD_STR                 'First codepoint in label {0} must be directionality L, R or AL'
              136  LOAD_METHOD              format
              138  LOAD_GLOBAL              repr
              140  LOAD_FAST                'label'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           130  '130'
            150_1  COME_FROM           116  '116'

 L.  90       150  LOAD_CONST               False
              152  STORE_FAST               'valid_ending'

 L.  91       154  LOAD_CONST               False
              156  STORE_FAST               'number_type'

 L.  92       158  SETUP_LOOP          340  'to 340'
              160  LOAD_GLOBAL              enumerate
              162  LOAD_FAST                'label'
              164  LOAD_CONST               1
              166  CALL_FUNCTION_2       2  '2 positional arguments'
              168  GET_ITER         
            170_0  COME_FROM           330  '330'
              170  FOR_ITER            338  'to 338'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               'idx'
              176  STORE_FAST               'cp'

 L.  93       178  LOAD_GLOBAL              unicodedata
              180  LOAD_METHOD              bidirectional
              182  LOAD_FAST                'cp'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  STORE_FAST               'direction'

 L.  95       188  LOAD_FAST                'rtl'
          190_192  POP_JUMP_IF_FALSE   284  'to 284'

 L.  97       194  LOAD_FAST                'direction'
              196  LOAD_CONST               ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              198  COMPARE_OP               not-in
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.  98       202  LOAD_GLOBAL              IDNABidiError
              204  LOAD_STR                 'Invalid direction for codepoint at position {0} in a right-to-left label'
              206  LOAD_METHOD              format
              208  LOAD_FAST                'idx'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           200  '200'

 L. 100       216  LOAD_FAST                'direction'
              218  LOAD_CONST               ('R', 'AL', 'EN', 'AN')
              220  COMPARE_OP               in
              222  POP_JUMP_IF_FALSE   230  'to 230'

 L. 101       224  LOAD_CONST               True
              226  STORE_FAST               'valid_ending'
              228  JUMP_FORWARD        242  'to 242'
            230_0  COME_FROM           222  '222'

 L. 102       230  LOAD_FAST                'direction'
              232  LOAD_STR                 'NSM'
              234  COMPARE_OP               !=
              236  POP_JUMP_IF_FALSE   242  'to 242'

 L. 103       238  LOAD_CONST               False
              240  STORE_FAST               'valid_ending'
            242_0  COME_FROM           236  '236'
            242_1  COME_FROM           228  '228'

 L. 105       242  LOAD_FAST                'direction'
              244  LOAD_CONST               ('AN', 'EN')
              246  COMPARE_OP               in
          248_250  POP_JUMP_IF_FALSE   336  'to 336'

 L. 106       252  LOAD_FAST                'number_type'
          254_256  POP_JUMP_IF_TRUE    264  'to 264'

 L. 107       258  LOAD_FAST                'direction'
              260  STORE_FAST               'number_type'
              262  JUMP_FORWARD        282  'to 282'
            264_0  COME_FROM           254  '254'

 L. 109       264  LOAD_FAST                'number_type'
              266  LOAD_FAST                'direction'
              268  COMPARE_OP               !=
          270_272  POP_JUMP_IF_FALSE   336  'to 336'

 L. 110       274  LOAD_GLOBAL              IDNABidiError
              276  LOAD_STR                 'Can not mix numeral types in a right-to-left label'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           262  '262'
              282  JUMP_BACK           170  'to 170'
            284_0  COME_FROM           190  '190'

 L. 113       284  LOAD_FAST                'direction'
              286  LOAD_CONST               ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              288  COMPARE_OP               not-in
          290_292  POP_JUMP_IF_FALSE   308  'to 308'

 L. 114       294  LOAD_GLOBAL              IDNABidiError
              296  LOAD_STR                 'Invalid direction for codepoint at position {0} in a left-to-right label'
              298  LOAD_METHOD              format
              300  LOAD_FAST                'idx'
              302  CALL_METHOD_1         1  '1 positional argument'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           290  '290'

 L. 116       308  LOAD_FAST                'direction'
              310  LOAD_CONST               ('L', 'EN')
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE   324  'to 324'

 L. 117       318  LOAD_CONST               True
              320  STORE_FAST               'valid_ending'
              322  JUMP_BACK           170  'to 170'
            324_0  COME_FROM           314  '314'

 L. 118       324  LOAD_FAST                'direction'
              326  LOAD_STR                 'NSM'
              328  COMPARE_OP               !=
              330  POP_JUMP_IF_FALSE   170  'to 170'

 L. 119       332  LOAD_CONST               False
              334  STORE_FAST               'valid_ending'
            336_0  COME_FROM           270  '270'
            336_1  COME_FROM           248  '248'
              336  JUMP_BACK           170  'to 170'
              338  POP_BLOCK        
            340_0  COME_FROM_LOOP      158  '158'

 L. 121       340  LOAD_FAST                'valid_ending'
          342_344  POP_JUMP_IF_TRUE    354  'to 354'

 L. 122       346  LOAD_GLOBAL              IDNABidiError
              348  LOAD_STR                 'Label ends with illegal codepoint directionality'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  RAISE_VARARGS_1       1  'exception instance'
            354_0  COME_FROM           342  '342'

 L. 124       354  LOAD_CONST               True
              356  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 338


def check_initial_combiner(label):
    if unicodedata.category(label[0])[0] == 'M':
        raise IDNAError('Label begins with an illegal combining character')
    return True


def check_hyphen_ok(label):
    if label[2:4] == '--':
        raise IDNAError('Label has disallowed hyphens in 3rd and 4th position')
    if label[0] == '-' or label[(-1)] == '-':
        raise IDNAError('Label must not start or end with a hyphen')
    return True


def check_nfc(label):
    if unicodedata.normalize'NFC'label != label:
        raise IDNAError('Label must be in Normalization Form C')


def valid_contextj(label, pos):
    cp_value = ord(label[pos])
    if cp_value == 8204:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        else:
            ok = False
            for i in range(pos - 1, -1, -1):
                joining_type = idnadata.joining_types.get(ord(label[i]))
                if joining_type == ord('T'):
                    continue
                if joining_type in [ord('L'), ord('D')]:
                    ok = True
                    break

            return ok or False
        ok = False
        for i in range(pos + 1, len(label)):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                continue
            if joining_type in [ord('R'), ord('D')]:
                ok = True
                break

        return ok
    if cp_value == 8205:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        return False
    return False


def valid_contexto(label, pos, exception=False):
    cp_value = ord(label[pos])
    if cp_value == 183:
        if 0 < pos < len(label) - 1:
            if ord(label[(pos - 1)]) == 108:
                if ord(label[(pos + 1)]) == 108:
                    return True
        return False
    if cp_value == 885:
        if pos < len(label) - 1:
            if len(label) > 1:
                return _is_script(label[(pos + 1)], 'Greek')
        return False
    if cp_value == 1523 or cp_value == 1524:
        if pos > 0:
            return _is_script(label[(pos - 1)], 'Hebrew')
        return False
    if cp_value == 12539:
        for cp in label:
            if cp == '・':
                continue
            if _is_script(cp, 'Hiragana') or _is_script(cp, 'Katakana') or _is_script(cp, 'Han'):
                return True

        return False
    if 1632 <= cp_value <= 1641:
        for cp in label:
            if 1776 <= ord(cp) <= 1785:
                return False

        return True
    if 1776 <= cp_value <= 1785:
        for cp in label:
            if 1632 <= ord(cp) <= 1641:
                return False

        return True


def check_label(label):
    if isinstance(label, (bytes, bytearray)):
        label = label.decode('utf-8')
    if len(label) == 0:
        raise IDNAError('Empty Label')
    check_nfc(label)
    check_hyphen_ok(label)
    check_initial_combiner(label)
    for pos, cp in enumerate(label):
        cp_value = ord(cp)
        if intranges_contain(cp_value, idnadata.codepoint_classes['PVALID']):
            continue
        elif intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTJ']):
            try:
                if not valid_contextj(label, pos):
                    raise InvalidCodepointContext('Joiner {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
            except ValueError:
                raise IDNAError('Unknown codepoint adjacent to joiner {0} at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))

        elif intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTO']) and not valid_contexto(label, pos):
            raise InvalidCodepointContext('Codepoint {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
        else:
            raise InvalidCodepoint('Codepoint {0} at position {1} of {2} not allowed'.format(_unot(cp_value), pos + 1, repr(label)))

    check_bidi(label)


def alabel(label):
    try:
        label = label.encode('ascii')
        ulabel(label)
        if not valid_label_length(label):
            raise IDNAError('Label too long')
        return label
    except UnicodeEncodeError:
        pass

    if not label:
        raise IDNAError('No Input')
    label = unicode(label)
    check_label(label)
    label = _punycode(label)
    label = _alabel_prefix + label
    if not valid_label_length(label):
        raise IDNAError('Label too long')
    return label


def ulabel(label):
    if not isinstance(label, (bytes, bytearray)):
        try:
            label = label.encode('ascii')
        except UnicodeEncodeError:
            check_label(label)
            return label

    else:
        label = label.lower()
        if label.startswith(_alabel_prefix):
            label = label[len(_alabel_prefix):]
            if label.decode('ascii')[(-1)] == '-':
                raise IDNAError('A-label must not end with a hyphen')
        else:
            check_label(label)
            return label.decode('ascii')
    label = label.decode('punycode')
    check_label(label)
    return label


def uts46_remap(domain, std3_rules=True, transitional=False):
    """Re-map the characters in the string according to UTS46 processing."""
    from .uts46data import uts46data
    output = ''
    try:
        for pos, char in enumerate(domain):
            code_point = ord(char)
            uts46row = uts46data[(code_point if code_point < 256 else bisect.bisect_leftuts46data(code_point, 'Z') - 1)]
            status = uts46row[1]
            replacement = uts46row[2] if len(uts46row) == 3 else None
            if not status == 'V':
                if not status == 'D' or transitional:
                    if not status == '3' or (std3_rules or replacement) is None:
                        output += char
                if replacement is not None:
                    if not status == 'M':
                        if not status == '3' or std3_rules:
                            if not status == 'D' or transitional:
                                output += replacement
                if status != 'I':
                    raise IndexError()

        return unicodedata.normalize'NFC'output
    except IndexError:
        raise InvalidCodepoint('Codepoint {0} not allowed at position {1} in {2}'.format(_unot(code_point), pos + 1, repr(domain)))


def encode(s, strict=False, uts46=False, std3_rules=False, transitional=False):
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    else:
        if uts46:
            s = uts46_remap(s, std3_rules, transitional)
        else:
            trailing_dot = False
            result = []
            if strict:
                labels = s.split('.')
            else:
                labels = _unicode_dots_re.split(s)
        if not labels or labels == ['']:
            raise IDNAError('Empty domain')
        if labels[(-1)] == '':
            del labels[-1]
            trailing_dot = True
        for label in labels:
            s = alabel(label)
            if s:
                result.append(s)
            else:
                raise IDNAError('Empty label')

        if trailing_dot:
            result.append(b'')
        s = (b'.').join(result)
        assert valid_string_length(s, trailing_dot), 'Domain too long'
    return s


def decode(s, strict=False, uts46=False, std3_rules=False):
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    else:
        if uts46:
            s = uts46_remap(s, std3_rules, False)
        else:
            trailing_dot = False
            result = []
            if not strict:
                labels = _unicode_dots_re.split(s)
            else:
                labels = s.split('.')
        if not labels or labels == ['']:
            raise IDNAError('Empty domain')
        del (labels[(-1)] or labels)[-1]
        trailing_dot = True
    for label in labels:
        s = ulabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError('Empty label')

    if trailing_dot:
        result.append('')
    return '.'.join(result)