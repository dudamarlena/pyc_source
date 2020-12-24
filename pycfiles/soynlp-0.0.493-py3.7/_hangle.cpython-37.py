# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/hangle/_hangle.py
# Compiled at: 2019-03-07 20:33:51
# Size of source mod 2**32: 8318 bytes
import sys
if sys.version_info <= (2, 7):
    reload(sys)
    sys.setdefaultencoding('utf-8')
import warnings, re, numpy as np
kor_begin = 44032
kor_end = 55203
chosung_base = 588
jungsung_base = 28
jaum_begin = 12593
jaum_end = 12622
moum_begin = 12623
moum_end = 12643
chosung_list = [
 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jungsung_list = [
 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
 'ㅡ', 'ㅢ', 'ㅣ']
jongsung_list = [
 ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ',
 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
jaum_list = [
 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ',
 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
moum_list = [
 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
doublespace_pattern = re.compile('\\s+')
repeatchars_pattern = re.compile('(\\w)\\1{3,}')

def normalize--- This code section failed: ---

 L.  45         0  LOAD_STR                 'normalize func will be moved soynlp.normalizer at ver 0.1\nargument remains will be removed at ver 0.1'
                2  STORE_FAST               'message'

 L.  46         4  LOAD_GLOBAL              warnings
                6  LOAD_ATTR                warn
                8  LOAD_FAST                'message'
               10  LOAD_GLOBAL              DeprecationWarning
               12  LOAD_CONST               2
               14  LOAD_CONST               ('stacklevel',)
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  48        20  LOAD_FAST                'remove_repeat'
               22  LOAD_CONST               0
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    44  'to 44'

 L.  49        28  LOAD_GLOBAL              repeatchars_pattern
               30  LOAD_METHOD              sub
               32  LOAD_STR                 '\\1'
               34  LOAD_FAST                'remove_repeat'
               36  BINARY_MULTIPLY  
               38  LOAD_FAST                'doc'
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  STORE_FAST               'doc'
             44_0  COME_FROM            26  '26'

 L.  51        44  BUILD_LIST_0          0 
               46  STORE_FAST               'f'

 L.  52     48_50  SETUP_LOOP          376  'to 376'
               52  LOAD_FAST                'doc'
               54  GET_ITER         
            56_58  FOR_ITER            374  'to 374'
               60  STORE_FAST               'c'

 L.  53        62  LOAD_FAST                'c'
               64  LOAD_STR                 ' '
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L.  54        70  LOAD_FAST                'f'
               72  LOAD_METHOD              append
               74  LOAD_FAST                'c'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  POP_TOP          

 L.  55        80  CONTINUE             56  'to 56'
             82_0  COME_FROM            68  '68'

 L.  56        82  LOAD_GLOBAL              to_base
               84  LOAD_FAST                'c'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'i'

 L.  57        90  LOAD_GLOBAL              kor_begin
               92  LOAD_FAST                'i'
               94  DUP_TOP          
               96  ROT_THREE        
               98  COMPARE_OP               <=
              100  POP_JUMP_IF_FALSE   110  'to 110'
              102  LOAD_GLOBAL              kor_end
              104  COMPARE_OP               <=
              106  POP_JUMP_IF_TRUE    158  'to 158'
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM           100  '100'
              110  POP_TOP          
            112_0  COME_FROM           108  '108'
              112  LOAD_GLOBAL              jaum_begin
              114  LOAD_FAST                'i'
              116  DUP_TOP          
              118  ROT_THREE        
              120  COMPARE_OP               <=
              122  POP_JUMP_IF_FALSE   132  'to 132'
              124  LOAD_GLOBAL              jaum_end
              126  COMPARE_OP               <=
              128  POP_JUMP_IF_TRUE    158  'to 158'
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM           122  '122'
              132  POP_TOP          
            134_0  COME_FROM           130  '130'
              134  LOAD_GLOBAL              moum_begin
              136  LOAD_FAST                'i'
              138  DUP_TOP          
              140  ROT_THREE        
              142  COMPARE_OP               <=
              144  POP_JUMP_IF_FALSE   154  'to 154'
              146  LOAD_GLOBAL              moum_end
              148  COMPARE_OP               <=
              150  POP_JUMP_IF_FALSE   170  'to 170'
              152  JUMP_FORWARD        158  'to 158'
            154_0  COME_FROM           144  '144'
              154  POP_TOP          
              156  JUMP_FORWARD        170  'to 170'
            158_0  COME_FROM           152  '152'
            158_1  COME_FROM           128  '128'
            158_2  COME_FROM           106  '106'

 L.  58       158  LOAD_FAST                'f'
              160  LOAD_METHOD              append
              162  LOAD_FAST                'c'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          

 L.  59       168  CONTINUE             56  'to 56'
            170_0  COME_FROM           156  '156'
            170_1  COME_FROM           150  '150'

 L.  60       170  LOAD_FAST                'english'
              172  POP_JUMP_IF_FALSE   218  'to 218'
              174  LOAD_FAST                'i'
              176  LOAD_CONST               97
              178  COMPARE_OP               >=
              180  POP_JUMP_IF_FALSE   190  'to 190'
              182  LOAD_FAST                'i'
              184  LOAD_CONST               122
              186  COMPARE_OP               <=
              188  POP_JUMP_IF_TRUE    206  'to 206'
            190_0  COME_FROM           180  '180'
              190  LOAD_FAST                'i'
              192  LOAD_CONST               65
              194  COMPARE_OP               >=
              196  POP_JUMP_IF_FALSE   218  'to 218'
              198  LOAD_FAST                'i'
              200  LOAD_CONST               90
              202  COMPARE_OP               <=
              204  POP_JUMP_IF_FALSE   218  'to 218'
            206_0  COME_FROM           188  '188'

 L.  61       206  LOAD_FAST                'f'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'c'
              212  CALL_METHOD_1         1  '1 positional argument'
              214  POP_TOP          

 L.  62       216  CONTINUE             56  'to 56'
            218_0  COME_FROM           204  '204'
            218_1  COME_FROM           196  '196'
            218_2  COME_FROM           172  '172'

 L.  63       218  LOAD_FAST                'number'
              220  POP_JUMP_IF_FALSE   250  'to 250'
              222  LOAD_FAST                'i'
              224  LOAD_CONST               48
              226  COMPARE_OP               >=
              228  POP_JUMP_IF_FALSE   250  'to 250'
              230  LOAD_FAST                'i'
              232  LOAD_CONST               57
              234  COMPARE_OP               <=
              236  POP_JUMP_IF_FALSE   250  'to 250'

 L.  64       238  LOAD_FAST                'f'
              240  LOAD_METHOD              append
              242  LOAD_FAST                'c'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  POP_TOP          

 L.  65       248  CONTINUE             56  'to 56'
            250_0  COME_FROM           236  '236'
            250_1  COME_FROM           228  '228'
            250_2  COME_FROM           220  '220'

 L.  66       250  LOAD_FAST                'punctuation'
          252_254  POP_JUMP_IF_FALSE   338  'to 338'
              256  LOAD_FAST                'i'
              258  LOAD_CONST               33
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_TRUE    326  'to 326'
              266  LOAD_FAST                'i'
              268  LOAD_CONST               34
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_TRUE    326  'to 326'
              276  LOAD_FAST                'i'
              278  LOAD_CONST               39
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_TRUE    326  'to 326'
              286  LOAD_FAST                'i'
              288  LOAD_CONST               44
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_TRUE    326  'to 326'
              296  LOAD_FAST                'i'
              298  LOAD_CONST               46
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_TRUE    326  'to 326'
              306  LOAD_FAST                'i'
              308  LOAD_CONST               63
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_TRUE    326  'to 326'
              316  LOAD_FAST                'i'
              318  LOAD_CONST               96
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   338  'to 338'
            326_0  COME_FROM           312  '312'
            326_1  COME_FROM           302  '302'
            326_2  COME_FROM           292  '292'
            326_3  COME_FROM           282  '282'
            326_4  COME_FROM           272  '272'
            326_5  COME_FROM           262  '262'

 L.  67       326  LOAD_FAST                'f'
              328  LOAD_METHOD              append
              330  LOAD_FAST                'c'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  POP_TOP          

 L.  68       336  CONTINUE             56  'to 56'
            338_0  COME_FROM           322  '322'
            338_1  COME_FROM           252  '252'

 L.  69       338  LOAD_FAST                'c'
              340  LOAD_FAST                'remains'
              342  COMPARE_OP               in
          344_346  POP_JUMP_IF_FALSE   362  'to 362'

 L.  70       348  LOAD_FAST                'f'
              350  LOAD_METHOD              append
              352  LOAD_FAST                'c'
              354  CALL_METHOD_1         1  '1 positional argument'
              356  POP_TOP          

 L.  71       358  CONTINUE             56  'to 56'
              360  JUMP_BACK            56  'to 56'
            362_0  COME_FROM           344  '344'

 L.  73       362  LOAD_FAST                'f'
              364  LOAD_METHOD              append
              366  LOAD_STR                 ' '
              368  CALL_METHOD_1         1  '1 positional argument'
              370  POP_TOP          
              372  JUMP_BACK            56  'to 56'
              374  POP_BLOCK        
            376_0  COME_FROM_LOOP       48  '48'

 L.  74       376  LOAD_GLOBAL              doublespace_pattern
              378  LOAD_METHOD              sub
              380  LOAD_STR                 ' '
              382  LOAD_STR                 ''
              384  LOAD_METHOD              join
              386  LOAD_FAST                'f'
              388  CALL_METHOD_1         1  '1 positional argument'
              390  CALL_METHOD_2         2  '2 positional arguments'
              392  LOAD_METHOD              strip
              394  CALL_METHOD_0         0  '0 positional arguments'
              396  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 170_0


def compose(chosung, jungsung, jongsung):
    return chr(kor_begin + chosung_base * chosung_list.index(chosung) + jungsung_base * jungsung_list.index(jungsung) + jongsung_list.index(jongsung))


def decompose(c):
    if not character_is_korean(c):
        return
    else:
        i = to_base(c)
        if jaum_begin <= i <= jaum_end:
            return (
             c, ' ', ' ')
        if moum_begin <= i <= moum_end:
            return (
             ' ', c, ' ')
    i -= kor_begin
    cho = i // chosung_base
    jung = (i - cho * chosung_base) // jungsung_base
    jong = i - cho * chosung_base - jung * jungsung_base
    return (chosung_list[cho], jungsung_list[jung], jongsung_list[jong])


def character_is_korean(c):
    i = to_base(c)
    return kor_begin <= i <= kor_end or jaum_begin <= i <= jaum_end or moum_begin <= i <= moum_end


def character_is_complete_korean(c):
    return kor_begin <= to_base(c) <= kor_end


def character_is_jaum(c):
    return jaum_begin <= to_base(c) <= jaum_end


def character_is_moum(c):
    return moum_begin <= to_base(c) <= moum_end


def to_base(c):
    if sys.version_info.major == 2 and not type(c) == str:
        if type(c) == unicode:
            return ord(c)
        raise TypeError
    else:
        if type(c) == str or type(c) == int:
            return ord(c)
        raise TypeError


def character_is_number(i):
    i = to_base(i)
    return i >= 48 and i <= 57


def character_is_english(i):
    i = to_base(i)
    return i >= 97 and i <= 122 or i >= 65 and i <= 90


def character_is_punctuation(i):
    i = to_base(i)
    return i == 33 or i == 34 or i == 39 or i == 44 or i == 46 or i == 63 or i == 96


class ConvolutionHangleEncoder:
    __doc__ = '초/중/종성을 구성하는 자음/모음과 띄어쓰기만 인코딩\n    one hot vector [ㄱ, ㄴ, ㄷ, ... ㅎ, ㅏ, ㅐ, .. ㅢ, ㅣ,"  ", ㄱ, ㄲ, ... ㅍ, ㅎ,"  ", 0, 1, 2, .. 9]\n    '

    def __init__(self):
        self.jung_begin = 19
        self.jong_begin = 40
        self.number_begin = 68
        self.space = 78
        self.unk = 79
        self.dim = 80
        num = [str(i) for i in range(10)]
        space = ' '
        unk = '<unk>'
        idx_to_char = chosung_list + jungsung_list + jongsung_list + num + [space] + [unk]
        self.idx_to_char = np.asarray(idx_to_char)
        self.jamo_to_idx = {'ㄱ':0, 
         'ㄲ':1,  'ㄴ':2,  'ㄷ':3,  'ㄸ':4,  'ㄹ':5,  'ㅁ':6,  'ㅂ':7,  'ㅃ':8, 
         'ㅅ':9,  'ㅆ':10,  'ㅇ':11,  'ㅈ':12,  'ㅉ':13,  'ㅊ':14,  'ㅋ':15,  'ㅌ':16, 
         'ㅍ':17,  'ㅎ':18,  'ㅏ':19,  'ㅐ':20,  'ㅑ':21,  'ㅒ':22,  'ㅓ':23,  'ㅔ':24, 
         'ㅕ':25,  'ㅖ':26,  'ㅗ':27,  'ㅘ':28,  'ㅙ':29,  'ㅚ':30,  'ㅛ':31,  'ㅜ':32, 
         'ㅝ':33,  'ㅞ':34,  'ㅟ':35,  'ㅠ':36,  'ㅡ':37,  'ㅢ':38,  'ㅣ':39,  ' ':40, 
         'ㄳ':43,  'ㄵ':45,  'ㄶ':46,  'ㄺ':49,  'ㄻ':50,  'ㄼ':51,  'ㄽ':52,  'ㄾ':53, 
         'ㄿ':54,  'ㅀ':55,  'ㅄ':58}

    def encode(self, sent):
        onehot = self.sent_to_onehot(sent)
        x = np.zeros((len(onehot), self.dim))
        for i, xi in enumerate(onehot):
            for j in xi:
                x[(i, j)] = 1

        return x

    def sent_to_onehot(self, sent):
        chars = self._normalize(sent)
        ords = [ord(c) for c in chars]
        onehot = []
        for char, idx in zip(chars, ords):
            if idx == 32:
                onehot.append((self.space,))
            elif 48 <= idx <= 57:
                onehot.append((idx - 48 + self.number_begin,))
            else:
                onehot.append(self._decomposecharidx)

        return onehot

    def onehot_to_sent(self, encoded_sent):

        def check_cjj(c):
            cho, jung, jong = c
            if not 0 <= cho < self.jung_begin:
                raise ValueError('Chosung %d is out of index' % cho)
            if not self.jung_begin <= jung < self.jong_begin:
                raise ValueError('Jungsung %d is out of index' % jung)
            if not self.jong_begin <= jong < self.number_begin:
                raise ValueError('Jongsung %d is out of index' % jong)

        chars = []
        for c in encoded_sent:
            if len(c) == 1:
                if not 0 <= c[0] < self.dim:
                    raise ValueError('character index %d is out of index [0, %d]' % (c[0], self.dim))
                chars.append(self.idx_to_char[c[0]])
            elif len(c) == 3:
                check_cjj(c)
                cho, jung, jong = tuple((self.idx_to_char[ci] for ci in c))
                chars.append(compose(cho, jung, jong))
            else:
                chars.append(self.idx_to_char[(-1)])

        return ''.join(chars)

    def _normalize(self, sent):
        import re
        regex = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣 0-9]')
        sent = regex.sub' 'sent
        sent = doublespace_pattern.sub' 'sent.strip
        return sent

    def _compose(self, cho, jung, jong):
        return chr(kor_begin + chosung_base * cho + jungsung_base * jung + jong)

    def _decompose(self, c, i):
        if kor_begin <= i <= kor_end:
            i -= kor_begin
            cho = i // chosung_base
            jung = (i - cho * chosung_base) // jungsung_base
            jong = i - cho * chosung_base - jung * jungsung_base
            return (cho, self.jung_begin + jung, self.jong_begin + jong)
        return (self.jamo_to_idx.getcself.unk,)