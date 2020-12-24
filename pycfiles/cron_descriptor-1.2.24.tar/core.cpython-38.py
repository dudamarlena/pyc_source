# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """IDNAError"""
    pass


class IDNABidiError(IDNAError):
    """IDNABidiError"""
    pass


class InvalidCodepoint(IDNAError):
    """InvalidCodepoint"""
    pass


class InvalidCodepointContext(IDNAError):
    """InvalidCodepointContext"""
    pass


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

 L.  71         4  LOAD_GLOBAL              enumerate
                6  LOAD_FAST                'label'
                8  LOAD_CONST               1
               10  CALL_FUNCTION_2       2  ''
               12  GET_ITER         
             14_0  COME_FROM            66  '66'
               14  FOR_ITER             74  'to 74'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'idx'
               20  STORE_FAST               'cp'

 L.  72        22  LOAD_GLOBAL              unicodedata
               24  LOAD_METHOD              bidirectional
               26  LOAD_FAST                'cp'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'direction'

 L.  73        32  LOAD_FAST                'direction'
               34  LOAD_STR                 ''
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    60  'to 60'

 L.  75        40  LOAD_GLOBAL              IDNABidiError
               42  LOAD_STR                 'Unknown directionality in label {0} at position {1}'
               44  LOAD_METHOD              format
               46  LOAD_GLOBAL              repr
               48  LOAD_FAST                'label'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'idx'
               54  CALL_METHOD_2         2  ''
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  ''
             60_0  COME_FROM            38  '38'

 L.  76        60  LOAD_FAST                'direction'
               62  LOAD_CONST               ('R', 'AL', 'AN')
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE    14  'to 14'

 L.  77        68  LOAD_CONST               True
               70  STORE_FAST               'bidi_label'
               72  JUMP_BACK            14  'to 14'

 L.  78        74  LOAD_FAST                'bidi_label'
               76  POP_JUMP_IF_TRUE     86  'to 86'
               78  LOAD_FAST                'check_ltr'
               80  POP_JUMP_IF_TRUE     86  'to 86'

 L.  79        82  LOAD_CONST               True
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            76  '76'

 L.  82        86  LOAD_GLOBAL              unicodedata
               88  LOAD_METHOD              bidirectional
               90  LOAD_FAST                'label'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'direction'

 L.  83       100  LOAD_FAST                'direction'
              102  LOAD_CONST               ('R', 'AL')
              104  COMPARE_OP               in
              106  POP_JUMP_IF_FALSE   114  'to 114'

 L.  84       108  LOAD_CONST               True
              110  STORE_FAST               'rtl'
              112  JUMP_FORWARD        146  'to 146'
            114_0  COME_FROM           106  '106'

 L.  85       114  LOAD_FAST                'direction'
              116  LOAD_STR                 'L'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   128  'to 128'

 L.  86       122  LOAD_CONST               False
              124  STORE_FAST               'rtl'
              126  JUMP_FORWARD        146  'to 146'
            128_0  COME_FROM           120  '120'

 L.  88       128  LOAD_GLOBAL              IDNABidiError
              130  LOAD_STR                 'First codepoint in label {0} must be directionality L, R or AL'
              132  LOAD_METHOD              format
              134  LOAD_GLOBAL              repr
              136  LOAD_FAST                'label'
              138  CALL_FUNCTION_1       1  ''
              140  CALL_METHOD_1         1  ''
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  ''
            146_0  COME_FROM           126  '126'
            146_1  COME_FROM           112  '112'

 L.  90       146  LOAD_CONST               False
              148  STORE_FAST               'valid_ending'

 L.  91       150  LOAD_CONST               False
              152  STORE_FAST               'number_type'

 L.  92       154  LOAD_GLOBAL              enumerate
              156  LOAD_FAST                'label'
              158  LOAD_CONST               1
              160  CALL_FUNCTION_2       2  ''
              162  GET_ITER         
            164_0  COME_FROM           324  '324'
              164  FOR_ITER            332  'to 332'
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'idx'
              170  STORE_FAST               'cp'

 L.  93       172  LOAD_GLOBAL              unicodedata
              174  LOAD_METHOD              bidirectional
              176  LOAD_FAST                'cp'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'direction'

 L.  95       182  LOAD_FAST                'rtl'
          184_186  POP_JUMP_IF_FALSE   278  'to 278'

 L.  97       188  LOAD_FAST                'direction'
              190  LOAD_CONST               ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              192  COMPARE_OP               not-in
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L.  98       196  LOAD_GLOBAL              IDNABidiError
              198  LOAD_STR                 'Invalid direction for codepoint at position {0} in a right-to-left label'
              200  LOAD_METHOD              format
              202  LOAD_FAST                'idx'
              204  CALL_METHOD_1         1  ''
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  ''
            210_0  COME_FROM           194  '194'

 L. 100       210  LOAD_FAST                'direction'
              212  LOAD_CONST               ('R', 'AL', 'EN', 'AN')
              214  COMPARE_OP               in
              216  POP_JUMP_IF_FALSE   224  'to 224'

 L. 101       218  LOAD_CONST               True
              220  STORE_FAST               'valid_ending'
              222  JUMP_FORWARD        236  'to 236'
            224_0  COME_FROM           216  '216'

 L. 102       224  LOAD_FAST                'direction'
              226  LOAD_STR                 'NSM'
              228  COMPARE_OP               !=
              230  POP_JUMP_IF_FALSE   236  'to 236'

 L. 103       232  LOAD_CONST               False
              234  STORE_FAST               'valid_ending'
            236_0  COME_FROM           230  '230'
            236_1  COME_FROM           222  '222'

 L. 105       236  LOAD_FAST                'direction'
              238  LOAD_CONST               ('AN', 'EN')
              240  COMPARE_OP               in
          242_244  POP_JUMP_IF_FALSE   330  'to 330'

 L. 106       246  LOAD_FAST                'number_type'
          248_250  POP_JUMP_IF_TRUE    258  'to 258'

 L. 107       252  LOAD_FAST                'direction'
              254  STORE_FAST               'number_type'
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM           248  '248'

 L. 109       258  LOAD_FAST                'number_type'
              260  LOAD_FAST                'direction'
              262  COMPARE_OP               !=
          264_266  POP_JUMP_IF_FALSE   330  'to 330'

 L. 110       268  LOAD_GLOBAL              IDNABidiError
              270  LOAD_STR                 'Can not mix numeral types in a right-to-left label'
              272  CALL_FUNCTION_1       1  ''
              274  RAISE_VARARGS_1       1  ''
            276_0  COME_FROM           256  '256'
              276  JUMP_BACK           164  'to 164'
            278_0  COME_FROM           184  '184'

 L. 113       278  LOAD_FAST                'direction'
              280  LOAD_CONST               ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM')
              282  COMPARE_OP               not-in
          284_286  POP_JUMP_IF_FALSE   302  'to 302'

 L. 114       288  LOAD_GLOBAL              IDNABidiError
              290  LOAD_STR                 'Invalid direction for codepoint at position {0} in a left-to-right label'
              292  LOAD_METHOD              format
              294  LOAD_FAST                'idx'
              296  CALL_METHOD_1         1  ''
              298  CALL_FUNCTION_1       1  ''
              300  RAISE_VARARGS_1       1  ''
            302_0  COME_FROM           284  '284'

 L. 116       302  LOAD_FAST                'direction'
              304  LOAD_CONST               ('L', 'EN')
              306  COMPARE_OP               in
          308_310  POP_JUMP_IF_FALSE   318  'to 318'

 L. 117       312  LOAD_CONST               True
              314  STORE_FAST               'valid_ending'
              316  JUMP_BACK           164  'to 164'
            318_0  COME_FROM           308  '308'

 L. 118       318  LOAD_FAST                'direction'
              320  LOAD_STR                 'NSM'
              322  COMPARE_OP               !=
              324  POP_JUMP_IF_FALSE   164  'to 164'

 L. 119       326  LOAD_CONST               False
              328  STORE_FAST               'valid_ending'
            330_0  COME_FROM           264  '264'
            330_1  COME_FROM           242  '242'
              330  JUMP_BACK           164  'to 164'

 L. 121       332  LOAD_FAST                'valid_ending'
          334_336  POP_JUMP_IF_TRUE    346  'to 346'

 L. 122       338  LOAD_GLOBAL              IDNABidiError
              340  LOAD_STR                 'Label ends with illegal codepoint directionality'
              342  CALL_FUNCTION_1       1  ''
              344  RAISE_VARARGS_1       1  ''
            346_0  COME_FROM           334  '334'

 L. 124       346  LOAD_CONST               True
              348  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 332


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
        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                pass
            else:
                if joining_type in (ord('L'), ord('D')):
                    ok = True
                    break
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
                _is_script(cp, 'Hiragana') or _is_script(cp, 'Katakana') or _is_script(cp, 'Han')
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
               34  RAISE_VARARGS_1       1  ''
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
               72  RAISE_VARARGS_1       1  ''
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
              120  RAISE_VARARGS_1       1  ''
            122_0  COME_FROM           112  '112'

 L. 288       122  LOAD_FAST                'label'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 38


def ulabel--- This code section failed: ---

 L. 293         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'label'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     62  'to 62'

 L. 294        14  SETUP_FINALLY        30  'to 30'

 L. 295        16  LOAD_FAST                'label'
               18  LOAD_METHOD              encode
               20  LOAD_STR                 'ascii'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'label'
               26  POP_BLOCK        
               28  JUMP_FORWARD         62  'to 62'
             30_0  COME_FROM_FINALLY    14  '14'

 L. 296        30  DUP_TOP          
               32  LOAD_GLOBAL              UnicodeEncodeError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    60  'to 60'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 297        44  LOAD_GLOBAL              check_label
               46  LOAD_FAST                'label'
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          

 L. 298        52  LOAD_FAST                'label'
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            36  '36'
               60  END_FINALLY      
             62_0  COME_FROM            28  '28'
             62_1  COME_FROM            12  '12'

 L. 300        62  LOAD_FAST                'label'
               64  LOAD_METHOD              lower
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'label'

 L. 301        70  LOAD_FAST                'label'
               72  LOAD_METHOD              startswith
               74  LOAD_GLOBAL              _alabel_prefix
               76  CALL_METHOD_1         1  ''
               78  POP_JUMP_IF_FALSE    98  'to 98'

 L. 302        80  LOAD_FAST                'label'
               82  LOAD_GLOBAL              len
               84  LOAD_GLOBAL              _alabel_prefix
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               None
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  STORE_FAST               'label'
               96  JUMP_FORWARD        116  'to 116'
             98_0  COME_FROM            78  '78'

 L. 304        98  LOAD_GLOBAL              check_label
              100  LOAD_FAST                'label'
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          

 L. 305       106  LOAD_FAST                'label'
              108  LOAD_METHOD              decode
              110  LOAD_STR                 'ascii'
              112  CALL_METHOD_1         1  ''
              114  RETURN_VALUE     
            116_0  COME_FROM            96  '96'

 L. 307       116  LOAD_FAST                'label'
              118  LOAD_METHOD              decode
              120  LOAD_STR                 'punycode'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'label'

 L. 308       126  LOAD_GLOBAL              check_label
              128  LOAD_FAST                'label'
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          

 L. 309       134  LOAD_FAST                'label'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 54


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
              222  RAISE_VARARGS_1       1  ''
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
              284  RAISE_VARARGS_1       1  ''
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           246  '246'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'

Parse error at or near `RETURN_VALUE' instruction at offset 238


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


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break (2)
#      0.  L. 178       236  POP_TOP          
#      1.               238  BREAK_LOOP          242  'to 242'