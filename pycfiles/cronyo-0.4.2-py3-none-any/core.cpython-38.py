# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/idna/core.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 11733 bytes
from . import idnadata
import bisect, unicodedata, re, sys
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_unicode_dots_re = re.compile('[.。．｡]')
if sys.version_info[0] == 3:
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


def check_bidi(label, check_ltr=False):
    bidi_label = False
    for idx, cp in enumerate(label, 1):
        direction = unicodedata.bidirectional(cp)
        if direction == '':
            raise IDNABidiError('Unknown directionality in label {0} at position {1}'.format(repr(label), idx))
        if direction in ('R', 'AL', 'AN'):
            bidi_label = True
        if not bidi_label:
            if not check_ltr:
                return True
            else:
                direction = unicodedata.bidirectional(label[0])
                if direction in ('R', 'AL'):
                    rtl = True
                else:
                    if direction == 'L':
                        rtl = False
                    else:
                        raise IDNABidiError('First codepoint in label {0} must be directionality L, R or AL'.format(repr(label)))
            valid_ending = False
            number_type = False
            for idx, cp in enumerate(label, 1):
                direction = unicodedata.bidirectional(cp)
                if rtl:
                    if direction not in ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON',
                                         'BN', 'NSM'):
                        raise IDNABidiError('Invalid direction for codepoint at position {0} in a right-to-left label'.format(idx))
                    elif direction in ('R', 'AL', 'EN', 'AN'):
                        valid_ending = True
                    else:
                        if direction != 'NSM':
                            valid_ending = False
                    if direction in ('AN', 'EN'):
                        if not number_type:
                            number_type = direction

        else:
            pass
        if number_type != direction:
            raise IDNABidiError('Can not mix numeral types in a right-to-left label')
        else:
            if direction not in ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM'):
                raise IDNABidiError('Invalid direction for codepoint at position {0} in a left-to-right label'.format(idx))
            if direction in ('L', 'EN'):
                valid_ending = True
            elif direction != 'NSM':
                valid_ending = False

    if not valid_ending:
        raise IDNABidiError('Label ends with illegal codepoint directionality')
    return True


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
    if unicodedata.normalize('NFC', label) != label:
        raise IDNAError('Label must be in Normalization Form C')


def valid_contextj(label, pos):
    cp_value = ord(label[pos])
    if cp_value == 8204:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                pass
            elif joining_type in (ord('L'), ord('D')):
                ok = True
                break
        else:
            if not ok:
                return False
            ok = False
            for i in range(pos + 1, len(label)):
                joining_type = idnadata.joining_types.get(ord(label[i]))

        if joining_type == ord('T'):
            pass
        else:
            if joining_type in (ord('R'), ord('D')):
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
                pass
            else:
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

        elif intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTO']):
            if not valid_contexto(label, pos):
                raise InvalidCodepointContext('Codepoint {0} not allowed at position {1} in {2}'.format(_unot(cp_value), pos + 1, repr(label)))
            else:
                raise InvalidCodepoint('Codepoint {0} at position {1} of {2} not allowed'.format(_unot(cp_value), pos + 1, repr(label)))
        else:
            check_bidi(label)


def alabel--- This code section failed: ---

 L. 268         0  SETUP_FINALLY        42  'to 42'

 L. 269         2  LOAD_FAST                'label'
                4  LOAD_METHOD              encode
                6  LOAD_STR                 'ascii'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'label'

 L. 270        12  LOAD_GLOBAL              ulabel
               14  LOAD_FAST                'label'
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 271        20  LOAD_GLOBAL              valid_label_length
               22  LOAD_FAST                'label'
               24  CALL_FUNCTION_1       1  ''
               26  POP_JUMP_IF_TRUE     36  'to 36'

 L. 272        28  LOAD_GLOBAL              IDNAError
               30  LOAD_STR                 'Label too long'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 273        36  LOAD_FAST                'label'
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 274        42  DUP_TOP          
               44  LOAD_GLOBAL              UnicodeEncodeError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    60  'to 60'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 275        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            48  '48'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

 L. 277        62  LOAD_FAST                'label'
               64  POP_JUMP_IF_TRUE     74  'to 74'

 L. 278        66  LOAD_GLOBAL              IDNAError
               68  LOAD_STR                 'No Input'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L. 280        74  LOAD_GLOBAL              unicode
               76  LOAD_FAST                'label'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'label'

 L. 281        82  LOAD_GLOBAL              check_label
               84  LOAD_FAST                'label'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          

 L. 282        90  LOAD_GLOBAL              _punycode
               92  LOAD_FAST                'label'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'label'

 L. 283        98  LOAD_GLOBAL              _alabel_prefix
              100  LOAD_FAST                'label'
              102  BINARY_ADD       
              104  STORE_FAST               'label'

 L. 285       106  LOAD_GLOBAL              valid_label_length
              108  LOAD_FAST                'label'
              110  CALL_FUNCTION_1       1  ''
              112  POP_JUMP_IF_TRUE    122  'to 122'

 L. 286       114  LOAD_GLOBAL              IDNAError
              116  LOAD_STR                 'Label too long'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 288       122  LOAD_FAST                'label'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 52


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
    else:
        check_label(label)
        return label.decode('ascii')
        label = label.decode('punycode')
        check_label(label)
        return label


def uts46_remap--- This code section failed: ---

 L. 314         0  LOAD_CONST               1
                2  LOAD_CONST               ('uts46data',)
                4  IMPORT_NAME              uts46data
                6  IMPORT_FROM              uts46data
                8  STORE_FAST               'uts46data'
               10  POP_TOP          

 L. 315        12  LOAD_STR                 ''
               14  STORE_FAST               'output'

 L. 316        16  SETUP_FINALLY       240  'to 240'

 L. 317        18  LOAD_GLOBAL              enumerate
               20  LOAD_FAST                'domain'
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
             26_0  COME_FROM           216  '216'
               26  FOR_ITER            226  'to 226'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'pos'
               32  STORE_FAST               'char'

 L. 318        34  LOAD_GLOBAL              ord
               36  LOAD_FAST                'char'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'code_point'

 L. 319        42  LOAD_FAST                'uts46data'
               44  LOAD_FAST                'code_point'
               46  LOAD_CONST               256
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    56  'to 56'
               52  LOAD_FAST                'code_point'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            50  '50'

 L. 320        56  LOAD_GLOBAL              bisect
               58  LOAD_METHOD              bisect_left
               60  LOAD_FAST                'uts46data'
               62  LOAD_FAST                'code_point'
               64  LOAD_STR                 'Z'
               66  BUILD_TUPLE_2         2 
               68  CALL_METHOD_2         2  ''
               70  LOAD_CONST               1
               72  BINARY_SUBTRACT  
             74_0  COME_FROM            54  '54'

 L. 319        74  BINARY_SUBSCR    
               76  STORE_FAST               'uts46row'

 L. 321        78  LOAD_FAST                'uts46row'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  STORE_FAST               'status'

 L. 322        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'uts46row'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_CONST               3
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   106  'to 106'
               98  LOAD_FAST                'uts46row'
              100  LOAD_CONST               2
              102  BINARY_SUBSCR    
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            96  '96'
              106  LOAD_CONST               None
            108_0  COME_FROM           104  '104'
              108  STORE_FAST               'replacement'

 L. 323       110  LOAD_FAST                'status'
              112  LOAD_STR                 'V'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    150  'to 150'

 L. 324       118  LOAD_FAST                'status'
              120  LOAD_STR                 'D'
              122  COMPARE_OP               ==

 L. 323       124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 324       126  LOAD_FAST                'transitional'

 L. 323       128  POP_JUMP_IF_FALSE   150  'to 150'
            130_0  COME_FROM           124  '124'

 L. 325       130  LOAD_FAST                'status'
              132  LOAD_STR                 '3'
              134  COMPARE_OP               ==

 L. 323       136  POP_JUMP_IF_FALSE   160  'to 160'

 L. 325       138  LOAD_FAST                'std3_rules'

 L. 323       140  POP_JUMP_IF_TRUE    160  'to 160'

 L. 325       142  LOAD_FAST                'replacement'
              144  LOAD_CONST               None
              146  COMPARE_OP               is

 L. 323       148  POP_JUMP_IF_FALSE   160  'to 160'
            150_0  COME_FROM           128  '128'
            150_1  COME_FROM           116  '116'

 L. 326       150  LOAD_FAST                'output'
              152  LOAD_FAST                'char'
              154  INPLACE_ADD      
              156  STORE_FAST               'output'
              158  JUMP_BACK            26  'to 26'
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           140  '140'
            160_2  COME_FROM           136  '136'

 L. 327       160  LOAD_FAST                'replacement'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   210  'to 210'
              168  LOAD_FAST                'status'
              170  LOAD_STR                 'M'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_TRUE    200  'to 200'

 L. 328       176  LOAD_FAST                'status'
              178  LOAD_STR                 '3'
              180  COMPARE_OP               ==

 L. 327       182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 328       184  LOAD_FAST                'std3_rules'

 L. 327       186  POP_JUMP_IF_FALSE   200  'to 200'
            188_0  COME_FROM           182  '182'

 L. 329       188  LOAD_FAST                'status'
              190  LOAD_STR                 'D'
              192  COMPARE_OP               ==

 L. 327       194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 329       196  LOAD_FAST                'transitional'

 L. 327       198  POP_JUMP_IF_FALSE   210  'to 210'
            200_0  COME_FROM           186  '186'
            200_1  COME_FROM           174  '174'

 L. 330       200  LOAD_FAST                'output'
              202  LOAD_FAST                'replacement'
              204  INPLACE_ADD      
              206  STORE_FAST               'output'
              208  JUMP_BACK            26  'to 26'
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           194  '194'
            210_2  COME_FROM           166  '166'

 L. 331       210  LOAD_FAST                'status'
              212  LOAD_STR                 'I'
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_FALSE    26  'to 26'

 L. 332       218  LOAD_GLOBAL              IndexError
              220  CALL_FUNCTION_0       0  ''
              222  RAISE_VARARGS_1       1  'exception instance'
              224  JUMP_BACK            26  'to 26'

 L. 333       226  LOAD_GLOBAL              unicodedata
              228  LOAD_METHOD              normalize
              230  LOAD_STR                 'NFC'
              232  LOAD_FAST                'output'
              234  CALL_METHOD_2         2  ''
              236  POP_BLOCK        
              238  RETURN_VALUE     
            240_0  COME_FROM_FINALLY    16  '16'

 L. 334       240  DUP_TOP          
              242  LOAD_GLOBAL              IndexError
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   290  'to 290'
              250  POP_TOP          
              252  POP_TOP          
              254  POP_TOP          

 L. 335       256  LOAD_GLOBAL              InvalidCodepoint

 L. 336       258  LOAD_STR                 'Codepoint {0} not allowed at position {1} in {2}'
              260  LOAD_METHOD              format

 L. 337       262  LOAD_GLOBAL              _unot
              264  LOAD_FAST                'code_point'
              266  CALL_FUNCTION_1       1  ''

 L. 337       268  LOAD_FAST                'pos'
              270  LOAD_CONST               1
              272  BINARY_ADD       

 L. 337       274  LOAD_GLOBAL              repr
              276  LOAD_FAST                'domain'
              278  CALL_FUNCTION_1       1  ''

 L. 336       280  CALL_METHOD_3         3  ''

 L. 335       282  CALL_FUNCTION_1       1  ''
              284  RAISE_VARARGS_1       1  'exception instance'
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           246  '246'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'

Parse error at or near `POP_TOP' instruction at offset 252


def encode(s, strict=False, uts46=False, std3_rules=False, transitional=False):
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    else:
        if uts46:
            s = uts46_remap(s, std3_rules, transitional)
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
    else:
        if trailing_dot:
            result.append(b'')
        s = (b'.').join(result)
        if not valid_string_length(s, trailing_dot):
            raise IDNAError('Domain too long')
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
    else:
        if trailing_dot:
            result.append('')
        return '.'.join(result)


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break (2)
#      0.  L. 178       236  POP_TOP          
#      1.               238  BREAK_LOOP          242  'to 242'