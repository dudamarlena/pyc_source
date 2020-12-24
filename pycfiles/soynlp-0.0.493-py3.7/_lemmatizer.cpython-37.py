# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/lemmatizer/_lemmatizer.py
# Compiled at: 2019-02-17 12:03:10
# Size of source mod 2**32: 9957 bytes
from soynlp.hangle import compose, decompose
from ._conjugation import conjugate, conjugate_chat

class Lemmatizer:

    def __init__(self, stems, endings, predefined=None):
        self._stems = stems
        self._endings = endings
        self._initialize()
        if predefined:
            self._predefined.update(predefined)

    def _initialize(self):
        self._predefined = {'불어':('붇다', '불다'),  '그래':('그렇다', )}

    def lemmatize(self, word, check_only_stem=False):
        candidates = set()
        for i in range(1, len(word) + 1):
            l, r = word[:i], word[i:]
            for stem, ending in lemma_candidate(l, r, self._predefined):
                if stem in self._stems:
                    if check_only_stem:
                        candidates.add((stem, ending))
                    elif ending in self._endings:
                        candidates.add((stem, ending))

        return candidates

    def candidates(self, word):
        candidates = set()
        for i in range(1, len(word) + 1):
            l = word[:i]
            r = word[i:]
            candidates.update(self.lemma_candidate(l, r, self._predefined))

        return candidates


def debug_message(message, l, r):
    print('{}: {} + {}'.format(message, l, r))


def lemma_candidate_chat(l, r, predefined=None, debug=False):

    def add_lemma(stem, ending):
        candidates.add((stem, ending))

    def character_is_emoticon(c):
        return c in set('ㄷㅂㅅㅇㅋㅎ')

    candidates = lemma_candidate(l, r, predefined, debug)
    l_last = decompose(l[(-1)])
    if not r:
        if character_is_emoticon(l_last[2]):
            l_ = l[:-1] + compose(l_last[0], l_last[1], ' ')
            if debug:
                debug_message('마지막 종성이 이모티콘으로 의심되는 경우', l_, '()')
            candidates.update(lemma_candidate(l_, r, predefined, debug))
    return candidates


def lemma_candidate--- This code section failed: ---

 L.  64         0  LOAD_CLOSURE             'candidates'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object add_lemma>
                6  LOAD_STR                 'lemma_candidate.<locals>.add_lemma'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'add_lemma'

 L.  67        12  LOAD_FAST                'l'
               14  LOAD_FAST                'r'
               16  BUILD_TUPLE_2         2 
               18  BUILD_SET_1           1 
               20  STORE_DEREF              'candidates'

 L.  68        22  LOAD_FAST                'l'
               24  LOAD_FAST                'r'
               26  BINARY_ADD       
               28  STORE_FAST               'word'

 L.  70        30  LOAD_GLOBAL              decompose
               32  LOAD_FAST                'l'
               34  LOAD_CONST               -1
               36  BINARY_SUBSCR    
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  STORE_FAST               'l_last'

 L.  71        42  LOAD_GLOBAL              compose
               44  LOAD_FAST                'l_last'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'l_last'
               52  LOAD_CONST               1
               54  BINARY_SUBSCR    
               56  LOAD_STR                 ' '
               58  CALL_FUNCTION_3       3  '3 positional arguments'
               60  STORE_FAST               'l_last_'

 L.  72        62  LOAD_FAST                'l'
               64  LOAD_CONST               None
               66  LOAD_CONST               -1
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  STORE_FAST               'l_front'

 L.  73        74  LOAD_FAST                'r'
               76  POP_JUMP_IF_FALSE    90  'to 90'
               78  LOAD_GLOBAL              decompose
               80  LOAD_FAST                'r'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            76  '76'
               90  LOAD_CONST               ('', '', '')
             92_0  COME_FROM            88  '88'
               92  STORE_FAST               'r_first'

 L.  74        94  LOAD_FAST                'r'
               96  POP_JUMP_IF_FALSE   118  'to 118'
               98  LOAD_GLOBAL              compose
              100  LOAD_FAST                'r_first'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'r_first'
              108  LOAD_CONST               1
              110  BINARY_SUBSCR    
              112  LOAD_STR                 ' '
              114  CALL_FUNCTION_3       3  '3 positional arguments'
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            96  '96'
              118  LOAD_STR                 ' '
            120_0  COME_FROM           116  '116'
              120  STORE_FAST               'r_first_'

 L.  75       122  LOAD_FAST                'r'
              124  LOAD_CONST               1
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  STORE_FAST               'r_end'

 L.  78       134  LOAD_FAST                'l_last'
              136  LOAD_CONST               2
              138  BINARY_SUBSCR    
              140  LOAD_STR                 'ㄹ'
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   208  'to 208'
              146  LOAD_FAST                'r_first'
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  LOAD_STR                 'ㅇ'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   208  'to 208'

 L.  79       158  LOAD_FAST                'l_front'
              160  LOAD_GLOBAL              compose
              162  LOAD_FAST                'l_last'
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'l_last'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  LOAD_STR                 'ㄷ'
              176  CALL_FUNCTION_3       3  '3 positional arguments'
              178  BINARY_ADD       
              180  STORE_FAST               'l_stem'

 L.  80       182  LOAD_FAST                'add_lemma'
              184  LOAD_FAST                'l_stem'
              186  LOAD_FAST                'r'
              188  CALL_FUNCTION_2       2  '2 positional arguments'
              190  POP_TOP          

 L.  81       192  LOAD_FAST                'debug'
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L.  82       196  LOAD_GLOBAL              debug_message
              198  LOAD_STR                 'ㄷ 불규칙 활용'
              200  LOAD_FAST                'l_stem'
              202  LOAD_FAST                'r'
              204  CALL_FUNCTION_3       3  '3 positional arguments'
              206  POP_TOP          
            208_0  COME_FROM           194  '194'
            208_1  COME_FROM           156  '156'
            208_2  COME_FROM           144  '144'

 L.  85       208  LOAD_FAST                'l_last'
              210  LOAD_CONST               2
              212  BINARY_SUBSCR    
              214  LOAD_STR                 'ㄹ'
              216  COMPARE_OP               ==
          218_220  POP_JUMP_IF_FALSE   320  'to 320'
              222  LOAD_FAST                'r_first_'
              224  LOAD_STR                 '러'
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_TRUE    240  'to 240'
              230  LOAD_FAST                'r_first_'
              232  LOAD_STR                 '라'
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   320  'to 320'
            240_0  COME_FROM           228  '228'

 L.  86       240  LOAD_FAST                'l_front'
              242  LOAD_GLOBAL              compose
              244  LOAD_FAST                'l_last'
              246  LOAD_CONST               0
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'l_last'
              252  LOAD_CONST               1
              254  BINARY_SUBSCR    
              256  LOAD_STR                 ' '
              258  CALL_FUNCTION_3       3  '3 positional arguments'
              260  BINARY_ADD       
              262  LOAD_STR                 '르'
              264  BINARY_ADD       
              266  STORE_FAST               'l_stem'

 L.  87       268  LOAD_GLOBAL              compose
              270  LOAD_STR                 'ㅇ'
              272  LOAD_FAST                'r_first'
              274  LOAD_CONST               1
              276  BINARY_SUBSCR    
              278  LOAD_FAST                'r_first'
              280  LOAD_CONST               2
              282  BINARY_SUBSCR    
              284  CALL_FUNCTION_3       3  '3 positional arguments'
              286  LOAD_FAST                'r_end'
              288  BINARY_ADD       
              290  STORE_FAST               'r_canon'

 L.  88       292  LOAD_FAST                'add_lemma'
              294  LOAD_FAST                'l_stem'
              296  LOAD_FAST                'r_canon'
              298  CALL_FUNCTION_2       2  '2 positional arguments'
              300  POP_TOP          

 L.  89       302  LOAD_FAST                'debug'
          304_306  POP_JUMP_IF_FALSE   320  'to 320'

 L.  90       308  LOAD_GLOBAL              debug_message
              310  LOAD_STR                 '르 불규칙 활용'
              312  LOAD_FAST                'l_stem'
              314  LOAD_FAST                'r_canon'
              316  CALL_FUNCTION_3       3  '3 positional arguments'
              318  POP_TOP          
            320_0  COME_FROM           304  '304'
            320_1  COME_FROM           236  '236'
            320_2  COME_FROM           218  '218'

 L.  93       320  LOAD_FAST                'l_last'
              322  LOAD_CONST               2
              324  BINARY_SUBSCR    
              326  LOAD_STR                 ' '
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   516  'to 516'

 L.  94       334  LOAD_FAST                'l_front'
              336  LOAD_GLOBAL              compose
              338  LOAD_FAST                'l_last'
              340  LOAD_CONST               0
              342  BINARY_SUBSCR    
              344  LOAD_FAST                'l_last'
              346  LOAD_CONST               1
              348  BINARY_SUBSCR    
              350  LOAD_STR                 'ㅂ'
              352  CALL_FUNCTION_3       3  '3 positional arguments'
              354  BINARY_ADD       
              356  STORE_FAST               'l_stem'

 L.  95       358  LOAD_FAST                'r_first_'
              360  LOAD_STR                 '워'
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_TRUE    378  'to 378'
              368  LOAD_FAST                'r_first_'
              370  LOAD_STR                 '와'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   428  'to 428'
            378_0  COME_FROM           364  '364'

 L.  96       378  LOAD_GLOBAL              compose
              380  LOAD_STR                 'ㅇ'
              382  LOAD_FAST                'r_first_'
              384  LOAD_STR                 '와'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   396  'to 396'
              392  LOAD_STR                 'ㅏ'
              394  JUMP_FORWARD        398  'to 398'
            396_0  COME_FROM           388  '388'
              396  LOAD_STR                 'ㅓ'
            398_0  COME_FROM           394  '394'
              398  LOAD_FAST                'r_first'
              400  LOAD_CONST               2
              402  BINARY_SUBSCR    
          404_406  POP_JUMP_IF_FALSE   416  'to 416'
              408  LOAD_FAST                'r_first'
              410  LOAD_CONST               2
              412  BINARY_SUBSCR    
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           404  '404'
              416  LOAD_STR                 ' '
            418_0  COME_FROM           414  '414'
              418  CALL_FUNCTION_3       3  '3 positional arguments'
              420  LOAD_FAST                'r_end'
              422  BINARY_ADD       
              424  STORE_FAST               'r_canon'
              426  JUMP_FORWARD        488  'to 488'
            428_0  COME_FROM           374  '374'

 L.  97       428  LOAD_FAST                'r_end'
          430_432  POP_JUMP_IF_FALSE   484  'to 484'
              434  LOAD_FAST                'r_end'
              436  LOAD_CONST               0
              438  BINARY_SUBSCR    
              440  LOAD_STR                 '려'
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_FALSE   484  'to 484'

 L.  98       448  LOAD_GLOBAL              compose
              450  LOAD_STR                 'ㅇ'
              452  LOAD_STR                 'ㅜ'
              454  LOAD_FAST                'r_first'
              456  LOAD_CONST               2
              458  BINARY_SUBSCR    
          460_462  POP_JUMP_IF_FALSE   472  'to 472'
              464  LOAD_FAST                'r_first'
              466  LOAD_CONST               2
              468  BINARY_SUBSCR    
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           460  '460'
              472  LOAD_STR                 ' '
            474_0  COME_FROM           470  '470'
              474  CALL_FUNCTION_3       3  '3 positional arguments'
              476  LOAD_FAST                'r_end'
              478  BINARY_ADD       
              480  STORE_FAST               'r_canon'
              482  JUMP_FORWARD        488  'to 488'
            484_0  COME_FROM           444  '444'
            484_1  COME_FROM           430  '430'

 L. 100       484  LOAD_FAST                'r'
              486  STORE_FAST               'r_canon'
            488_0  COME_FROM           482  '482'
            488_1  COME_FROM           426  '426'

 L. 101       488  LOAD_FAST                'add_lemma'
              490  LOAD_FAST                'l_stem'
              492  LOAD_FAST                'r_canon'
              494  CALL_FUNCTION_2       2  '2 positional arguments'
              496  POP_TOP          

 L. 102       498  LOAD_FAST                'debug'
          500_502  POP_JUMP_IF_FALSE   516  'to 516'

 L. 103       504  LOAD_GLOBAL              debug_message
              506  LOAD_STR                 'ㅂ 불규칙 활용'
              508  LOAD_FAST                'l_stem'
              510  LOAD_FAST                'r_canon'
              512  CALL_FUNCTION_3       3  '3 positional arguments'
              514  POP_TOP          
            516_0  COME_FROM           500  '500'
            516_1  COME_FROM           330  '330'

 L. 107       516  LOAD_FAST                'l_last'
              518  LOAD_CONST               2
              520  BINARY_SUBSCR    
              522  LOAD_STR                 'ㄴ'
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_TRUE    586  'to 586'
              530  LOAD_FAST                'l_last'
              532  LOAD_CONST               2
              534  BINARY_SUBSCR    
              536  LOAD_STR                 'ㄹ'
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_TRUE    586  'to 586'
              544  LOAD_FAST                'l_last'
              546  LOAD_CONST               2
              548  BINARY_SUBSCR    
              550  LOAD_STR                 'ㅁ'
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_TRUE    586  'to 586'
              558  LOAD_FAST                'l_last'
              560  LOAD_CONST               2
              562  BINARY_SUBSCR    
              564  LOAD_STR                 'ㅂ'
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_TRUE    586  'to 586'
              572  LOAD_FAST                'l_last'
              574  LOAD_CONST               2
              576  BINARY_SUBSCR    
              578  LOAD_STR                 'ㅆ'
              580  COMPARE_OP               ==
          582_584  POP_JUMP_IF_FALSE   688  'to 688'
            586_0  COME_FROM           568  '568'
            586_1  COME_FROM           554  '554'
            586_2  COME_FROM           540  '540'
            586_3  COME_FROM           526  '526'

 L. 108       586  SETUP_LOOP          688  'to 688'
              588  LOAD_STR                 ' ㄹㅂㅎ'
              590  GET_ITER         
            592_0  COME_FROM           662  '662'
              592  FOR_ITER            686  'to 686'
              594  STORE_FAST               'jongsung'

 L. 109       596  LOAD_FAST                'l_last'
              598  LOAD_CONST               2
              600  BINARY_SUBSCR    
              602  LOAD_FAST                'jongsung'
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE   614  'to 614'

 L. 110   610_612  CONTINUE            592  'to 592'
            614_0  COME_FROM           606  '606'

 L. 111       614  LOAD_FAST                'l_front'
              616  LOAD_GLOBAL              compose
              618  LOAD_FAST                'l_last'
              620  LOAD_CONST               0
              622  BINARY_SUBSCR    
              624  LOAD_FAST                'l_last'
              626  LOAD_CONST               1
              628  BINARY_SUBSCR    
              630  LOAD_FAST                'jongsung'
              632  CALL_FUNCTION_3       3  '3 positional arguments'
              634  BINARY_ADD       
              636  STORE_FAST               'l_stem'

 L. 112       638  LOAD_FAST                'l_last'
              640  LOAD_CONST               2
              642  BINARY_SUBSCR    
              644  LOAD_FAST                'r'
              646  BINARY_ADD       
              648  STORE_FAST               'r_canon'

 L. 113       650  LOAD_FAST                'add_lemma'
              652  LOAD_FAST                'l_stem'
              654  LOAD_FAST                'r_canon'
              656  CALL_FUNCTION_2       2  '2 positional arguments'
              658  POP_TOP          

 L. 114       660  LOAD_FAST                'debug'
          662_664  POP_JUMP_IF_FALSE   592  'to 592'

 L. 115       666  LOAD_GLOBAL              debug_message
              668  LOAD_STR                 '어미의 첫글자가 종성일 경우 (%s)'
              670  LOAD_FAST                'jongsung'
              672  BINARY_MODULO    
              674  LOAD_FAST                'l_stem'
              676  LOAD_FAST                'r_canon'
              678  CALL_FUNCTION_3       3  '3 positional arguments'
              680  POP_TOP          
          682_684  JUMP_BACK           592  'to 592'
              686  POP_BLOCK        
            688_0  COME_FROM_LOOP      586  '586'
            688_1  COME_FROM           582  '582'

 L. 119       688  LOAD_FAST                'l_last'
              690  LOAD_CONST               2
              692  BINARY_SUBSCR    
              694  LOAD_STR                 ' '
              696  COMPARE_OP               ==
          698_700  POP_JUMP_IF_FALSE   782  'to 782'
              702  LOAD_FAST                'l'
              704  LOAD_CONST               -1
              706  BINARY_SUBSCR    
              708  LOAD_STR                 '벗'
              710  COMPARE_OP               !=
          712_714  POP_JUMP_IF_FALSE   782  'to 782'
              716  LOAD_FAST                'r_first'
              718  LOAD_CONST               0
              720  BINARY_SUBSCR    
              722  LOAD_STR                 'ㅇ'
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_FALSE   782  'to 782'

 L. 120       730  LOAD_FAST                'l_front'
              732  LOAD_GLOBAL              compose
              734  LOAD_FAST                'l_last'
              736  LOAD_CONST               0
              738  BINARY_SUBSCR    
              740  LOAD_FAST                'l_last'
              742  LOAD_CONST               1
              744  BINARY_SUBSCR    
              746  LOAD_STR                 'ㅅ'
              748  CALL_FUNCTION_3       3  '3 positional arguments'
              750  BINARY_ADD       
              752  STORE_FAST               'l_stem'

 L. 121       754  LOAD_FAST                'add_lemma'
              756  LOAD_FAST                'l_stem'
              758  LOAD_FAST                'r'
              760  CALL_FUNCTION_2       2  '2 positional arguments'
              762  POP_TOP          

 L. 122       764  LOAD_FAST                'debug'
          766_768  POP_JUMP_IF_FALSE   782  'to 782'

 L. 123       770  LOAD_GLOBAL              debug_message
              772  LOAD_STR                 'ㅅ 불규칙 활용'
              774  LOAD_FAST                'l_stem'
              776  LOAD_FAST                'r'
              778  CALL_FUNCTION_3       3  '3 positional arguments'
              780  POP_TOP          
            782_0  COME_FROM           766  '766'
            782_1  COME_FROM           726  '726'
            782_2  COME_FROM           712  '712'
            782_3  COME_FROM           698  '698'

 L. 126       782  LOAD_FAST                'l_last_'
              784  LOAD_STR                 '퍼'
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   852  'to 852'

 L. 127       792  LOAD_FAST                'l_front'
              794  LOAD_STR                 '푸'
              796  BINARY_ADD       
              798  STORE_FAST               'l_stem'

 L. 128       800  LOAD_GLOBAL              compose
              802  LOAD_STR                 'ㅇ'
              804  LOAD_FAST                'l_last'
              806  LOAD_CONST               1
              808  BINARY_SUBSCR    
              810  LOAD_FAST                'l_last'
              812  LOAD_CONST               2
              814  BINARY_SUBSCR    
              816  CALL_FUNCTION_3       3  '3 positional arguments'
              818  LOAD_FAST                'r'
              820  BINARY_ADD       
              822  STORE_FAST               'r_canon'

 L. 129       824  LOAD_FAST                'add_lemma'
              826  LOAD_FAST                'l_stem'
              828  LOAD_FAST                'r_canon'
              830  CALL_FUNCTION_2       2  '2 positional arguments'
              832  POP_TOP          

 L. 130       834  LOAD_FAST                'debug'
          836_838  POP_JUMP_IF_FALSE   852  'to 852'

 L. 131       840  LOAD_GLOBAL              debug_message
              842  LOAD_STR                 '우 불규칙 활용 (퍼)'
              844  LOAD_FAST                'l_stem'
              846  LOAD_FAST                'r_canon'
              848  CALL_FUNCTION_3       3  '3 positional arguments'
              850  POP_TOP          
            852_0  COME_FROM           836  '836'
            852_1  COME_FROM           788  '788'

 L. 134       852  LOAD_FAST                'l_last'
              854  LOAD_CONST               1
              856  BINARY_SUBSCR    
              858  LOAD_STR                 'ㅝ'
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE   934  'to 934'

 L. 135       866  LOAD_FAST                'l_front'
              868  LOAD_GLOBAL              compose
              870  LOAD_FAST                'l_last'
              872  LOAD_CONST               0
              874  BINARY_SUBSCR    
              876  LOAD_STR                 'ㅜ'
              878  LOAD_STR                 ' '
              880  CALL_FUNCTION_3       3  '3 positional arguments'
              882  BINARY_ADD       
              884  STORE_FAST               'l_stem'

 L. 136       886  LOAD_GLOBAL              compose
              888  LOAD_STR                 'ㅇ'
              890  LOAD_STR                 'ㅓ'
              892  LOAD_FAST                'l_last'
              894  LOAD_CONST               2
              896  BINARY_SUBSCR    
              898  CALL_FUNCTION_3       3  '3 positional arguments'
              900  LOAD_FAST                'r'
              902  BINARY_ADD       
              904  STORE_FAST               'r_canon'

 L. 137       906  LOAD_FAST                'add_lemma'
              908  LOAD_FAST                'l_stem'
              910  LOAD_FAST                'r_canon'
              912  CALL_FUNCTION_2       2  '2 positional arguments'
              914  POP_TOP          

 L. 138       916  LOAD_FAST                'debug'
          918_920  POP_JUMP_IF_FALSE   934  'to 934'

 L. 139       922  LOAD_GLOBAL              debug_message
              924  LOAD_STR                 '우 불규칙 활용'
              926  LOAD_FAST                'l_stem'
              928  LOAD_FAST                'r_canon'
              930  CALL_FUNCTION_3       3  '3 positional arguments'
              932  POP_TOP          
            934_0  COME_FROM           918  '918'
            934_1  COME_FROM           862  '862'

 L. 142       934  LOAD_FAST                'l_last'
              936  LOAD_CONST               1
              938  BINARY_SUBSCR    
              940  LOAD_STR                 'ㅘ'
              942  COMPARE_OP               ==
          944_946  POP_JUMP_IF_FALSE  1016  'to 1016'

 L. 143       948  LOAD_FAST                'l_front'
              950  LOAD_GLOBAL              compose
              952  LOAD_FAST                'l_last'
              954  LOAD_CONST               0
              956  BINARY_SUBSCR    
              958  LOAD_STR                 'ㅗ'
              960  LOAD_STR                 ' '
              962  CALL_FUNCTION_3       3  '3 positional arguments'
              964  BINARY_ADD       
              966  STORE_FAST               'l_stem'

 L. 144       968  LOAD_GLOBAL              compose
              970  LOAD_STR                 'ㅇ'
              972  LOAD_STR                 'ㅏ'
              974  LOAD_FAST                'l_last'
              976  LOAD_CONST               2
              978  BINARY_SUBSCR    
              980  CALL_FUNCTION_3       3  '3 positional arguments'
              982  LOAD_FAST                'r'
              984  BINARY_ADD       
              986  STORE_FAST               'r_canon'

 L. 145       988  LOAD_FAST                'add_lemma'
              990  LOAD_FAST                'l_stem'
              992  LOAD_FAST                'r_canon'
              994  CALL_FUNCTION_2       2  '2 positional arguments'
              996  POP_TOP          

 L. 146       998  LOAD_FAST                'debug'
         1000_1002  POP_JUMP_IF_FALSE  1016  'to 1016'

 L. 147      1004  LOAD_GLOBAL              debug_message
             1006  LOAD_STR                 '오 불규칙 활용'
             1008  LOAD_FAST                'l_stem'
             1010  LOAD_FAST                'r_canon'
             1012  CALL_FUNCTION_3       3  '3 positional arguments'
             1014  POP_TOP          
           1016_0  COME_FROM          1000  '1000'
           1016_1  COME_FROM           944  '944'

 L. 150      1016  LOAD_FAST                'l_last'
             1018  LOAD_CONST               1
             1020  BINARY_SUBSCR    
             1022  LOAD_STR                 'ㅓ'
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_TRUE   1044  'to 1044'
             1030  LOAD_FAST                'l_last'
             1032  LOAD_CONST               1
             1034  BINARY_SUBSCR    
             1036  LOAD_STR                 'ㅏ'
             1038  COMPARE_OP               ==
         1040_1042  POP_JUMP_IF_FALSE  1116  'to 1116'
           1044_0  COME_FROM          1026  '1026'

 L. 151      1044  LOAD_FAST                'l_front'
             1046  LOAD_GLOBAL              compose
             1048  LOAD_FAST                'l_last'
             1050  LOAD_CONST               0
             1052  BINARY_SUBSCR    
             1054  LOAD_STR                 'ㅡ'
             1056  LOAD_STR                 ' '
             1058  CALL_FUNCTION_3       3  '3 positional arguments'
             1060  BINARY_ADD       
             1062  STORE_FAST               'l_stem'

 L. 152      1064  LOAD_GLOBAL              compose
             1066  LOAD_STR                 'ㅇ'
             1068  LOAD_FAST                'l_last'
             1070  LOAD_CONST               1
             1072  BINARY_SUBSCR    
             1074  LOAD_FAST                'l_last'
             1076  LOAD_CONST               2
             1078  BINARY_SUBSCR    
             1080  CALL_FUNCTION_3       3  '3 positional arguments'
             1082  LOAD_FAST                'r'
             1084  BINARY_ADD       
             1086  STORE_FAST               'r_canon'

 L. 153      1088  LOAD_FAST                'add_lemma'
             1090  LOAD_FAST                'l_stem'
             1092  LOAD_FAST                'r_canon'
             1094  CALL_FUNCTION_2       2  '2 positional arguments'
             1096  POP_TOP          

 L. 154      1098  LOAD_FAST                'debug'
         1100_1102  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 155      1104  LOAD_GLOBAL              debug_message
             1106  LOAD_STR                 'ㅡ 탈락 불규칙 활용 (꺼)'
             1108  LOAD_FAST                'l_stem'
             1110  LOAD_FAST                'r_canon'
             1112  CALL_FUNCTION_3       3  '3 positional arguments'
             1114  POP_TOP          
           1116_0  COME_FROM          1100  '1100'
           1116_1  COME_FROM          1040  '1040'

 L. 158      1116  LOAD_FAST                'l_last'
             1118  LOAD_CONST               2
             1120  BINARY_SUBSCR    
             1122  LOAD_STR                 ' '
             1124  COMPARE_OP               ==
         1126_1128  POP_JUMP_IF_FALSE  1212  'to 1212'
             1130  LOAD_FAST                'r_first'
             1132  LOAD_CONST               0
             1134  BINARY_SUBSCR    
             1136  LOAD_STR                 'ㅇ'
             1138  COMPARE_OP               ==
         1140_1142  POP_JUMP_IF_FALSE  1212  'to 1212'
             1144  LOAD_FAST                'r_first'
             1146  LOAD_CONST               1
             1148  BINARY_SUBSCR    
             1150  LOAD_STR                 'ㅏ'
             1152  COMPARE_OP               ==
         1154_1156  POP_JUMP_IF_TRUE   1172  'to 1172'
             1158  LOAD_FAST                'r_first'
             1160  LOAD_CONST               1
             1162  BINARY_SUBSCR    
             1164  LOAD_STR                 'ㅓ'
             1166  COMPARE_OP               ==
         1168_1170  POP_JUMP_IF_FALSE  1212  'to 1212'
           1172_0  COME_FROM          1154  '1154'

 L. 159      1172  LOAD_FAST                'l'
             1174  LOAD_STR                 '으'
             1176  BINARY_ADD       
             1178  STORE_FAST               'l_stem'

 L. 160      1180  LOAD_FAST                'r'
             1182  STORE_FAST               'r_canon'

 L. 161      1184  LOAD_FAST                'add_lemma'
             1186  LOAD_FAST                'l_stem'
             1188  LOAD_FAST                'r_canon'
             1190  CALL_FUNCTION_2       2  '2 positional arguments'
             1192  POP_TOP          

 L. 162      1194  LOAD_FAST                'debug'
         1196_1198  POP_JUMP_IF_FALSE  1212  'to 1212'

 L. 163      1200  LOAD_GLOBAL              debug_message
             1202  LOAD_STR                 'ㅡ 탈락 불규칙 활용 (모으)'
             1204  LOAD_FAST                'l_stem'
             1206  LOAD_FAST                'r_canon'
             1208  CALL_FUNCTION_3       3  '3 positional arguments'
             1210  POP_TOP          
           1212_0  COME_FROM          1196  '1196'
           1212_1  COME_FROM          1168  '1168'
           1212_2  COME_FROM          1140  '1140'
           1212_3  COME_FROM          1126  '1126'

 L. 180      1212  LOAD_FAST                'l_last'
             1214  LOAD_CONST               0
             1216  BINARY_SUBSCR    
             1218  LOAD_STR                 'ㅎ'
             1220  COMPARE_OP               ==
         1222_1224  POP_JUMP_IF_FALSE  1296  'to 1296'
             1226  LOAD_FAST                'l_last'
             1228  LOAD_CONST               1
             1230  BINARY_SUBSCR    
             1232  LOAD_STR                 'ㅐ'
             1234  COMPARE_OP               ==
         1236_1238  POP_JUMP_IF_FALSE  1296  'to 1296'

 L. 181      1240  LOAD_FAST                'l_front'
             1242  LOAD_STR                 '하'
             1244  BINARY_ADD       
             1246  STORE_FAST               'l_stem'

 L. 182      1248  LOAD_GLOBAL              compose
             1250  LOAD_STR                 'ㅇ'
             1252  LOAD_STR                 'ㅏ'
             1254  LOAD_FAST                'l_last'
             1256  LOAD_CONST               2
             1258  BINARY_SUBSCR    
             1260  CALL_FUNCTION_3       3  '3 positional arguments'
             1262  LOAD_FAST                'r'
             1264  BINARY_ADD       
             1266  STORE_FAST               'r_canon'

 L. 183      1268  LOAD_FAST                'add_lemma'
             1270  LOAD_FAST                'l_stem'
             1272  LOAD_FAST                'r_canon'
             1274  CALL_FUNCTION_2       2  '2 positional arguments'
             1276  POP_TOP          

 L. 184      1278  LOAD_FAST                'debug'
         1280_1282  POP_JUMP_IF_FALSE  1296  'to 1296'

 L. 185      1284  LOAD_GLOBAL              debug_message
             1286  LOAD_STR                 '여 불규칙 활용'
             1288  LOAD_FAST                'l_stem'
             1290  LOAD_FAST                'r_canon'
             1292  CALL_FUNCTION_3       3  '3 positional arguments'
             1294  POP_TOP          
           1296_0  COME_FROM          1280  '1280'
           1296_1  COME_FROM          1236  '1236'
           1296_2  COME_FROM          1222  '1222'

 L. 188      1296  LOAD_FAST                'l_last'
             1298  LOAD_CONST               2
             1300  BINARY_SUBSCR    
             1302  LOAD_STR                 ' '
             1304  COMPARE_OP               ==
         1306_1308  POP_JUMP_IF_TRUE   1366  'to 1366'
             1310  LOAD_FAST                'l_last'
             1312  LOAD_CONST               2
             1314  BINARY_SUBSCR    
             1316  LOAD_STR                 'ㄴ'
             1318  COMPARE_OP               ==
         1320_1322  POP_JUMP_IF_TRUE   1366  'to 1366'
             1324  LOAD_FAST                'l_last'
             1326  LOAD_CONST               2
             1328  BINARY_SUBSCR    
             1330  LOAD_STR                 'ㄹ'
             1332  COMPARE_OP               ==
         1334_1336  POP_JUMP_IF_TRUE   1366  'to 1366'
             1338  LOAD_FAST                'l_last'
             1340  LOAD_CONST               2
             1342  BINARY_SUBSCR    
             1344  LOAD_STR                 'ㅂ'
             1346  COMPARE_OP               ==
         1348_1350  POP_JUMP_IF_TRUE   1366  'to 1366'
             1352  LOAD_FAST                'l_last'
             1354  LOAD_CONST               2
             1356  BINARY_SUBSCR    
             1358  LOAD_STR                 'ㅆ'
             1360  COMPARE_OP               ==
         1362_1364  POP_JUMP_IF_FALSE  1660  'to 1660'
           1366_0  COME_FROM          1348  '1348'
           1366_1  COME_FROM          1334  '1334'
           1366_2  COME_FROM          1320  '1320'
           1366_3  COME_FROM          1306  '1306'

 L. 190      1366  LOAD_FAST                'l_last'
             1368  LOAD_CONST               1
             1370  BINARY_SUBSCR    
             1372  LOAD_STR                 'ㅏ'
             1374  COMPARE_OP               ==
         1376_1378  POP_JUMP_IF_TRUE   1394  'to 1394'
             1380  LOAD_FAST                'l_last'
             1382  LOAD_CONST               1
             1384  BINARY_SUBSCR    
             1386  LOAD_STR                 'ㅓ'
             1388  COMPARE_OP               ==
         1390_1392  POP_JUMP_IF_FALSE  1476  'to 1476'
           1394_0  COME_FROM          1376  '1376'

 L. 191      1394  LOAD_FAST                'l_front'
             1396  LOAD_GLOBAL              compose
             1398  LOAD_FAST                'l_last'
             1400  LOAD_CONST               0
             1402  BINARY_SUBSCR    
             1404  LOAD_FAST                'l_last'
             1406  LOAD_CONST               1
             1408  BINARY_SUBSCR    
             1410  LOAD_STR                 'ㅎ'
             1412  CALL_FUNCTION_3       3  '3 positional arguments'
             1414  BINARY_ADD       
             1416  STORE_FAST               'l_stem'

 L. 192      1418  LOAD_FAST                'l_last'
             1420  LOAD_CONST               2
             1422  BINARY_SUBSCR    
             1424  LOAD_STR                 ' '
             1426  COMPARE_OP               ==
         1428_1430  POP_JUMP_IF_FALSE  1436  'to 1436'
             1432  LOAD_FAST                'r'
             1434  JUMP_FORWARD       1446  'to 1446'
           1436_0  COME_FROM          1428  '1428'
             1436  LOAD_FAST                'l_last'
             1438  LOAD_CONST               2
             1440  BINARY_SUBSCR    
             1442  LOAD_FAST                'r'
             1444  BINARY_ADD       
           1446_0  COME_FROM          1434  '1434'
             1446  STORE_FAST               'r_canon'

 L. 193      1448  LOAD_FAST                'add_lemma'
             1450  LOAD_FAST                'l_stem'
             1452  LOAD_FAST                'r_canon'
             1454  CALL_FUNCTION_2       2  '2 positional arguments'
             1456  POP_TOP          

 L. 194      1458  LOAD_FAST                'debug'
         1460_1462  POP_JUMP_IF_FALSE  1476  'to 1476'

 L. 195      1464  LOAD_GLOBAL              debug_message
             1466  LOAD_STR                 'ㅎ 탈락 불규칙 활용'
             1468  LOAD_FAST                'l_stem'
             1470  LOAD_FAST                'r_canon'
             1472  CALL_FUNCTION_3       3  '3 positional arguments'
             1474  POP_TOP          
           1476_0  COME_FROM          1460  '1460'
           1476_1  COME_FROM          1390  '1390'

 L. 198      1476  LOAD_FAST                'l_last'
             1478  LOAD_CONST               1
             1480  BINARY_SUBSCR    
             1482  LOAD_STR                 'ㅐ'
             1484  COMPARE_OP               ==
         1486_1488  POP_JUMP_IF_TRUE   1504  'to 1504'
             1490  LOAD_FAST                'l_last'
             1492  LOAD_CONST               1
             1494  BINARY_SUBSCR    
             1496  LOAD_STR                 'ㅔ'
             1498  COMPARE_OP               ==
         1500_1502  POP_JUMP_IF_FALSE  1660  'to 1660'
           1504_0  COME_FROM          1486  '1486'

 L. 200      1504  LOAD_GLOBAL              len
             1506  LOAD_FAST                'l'
             1508  CALL_FUNCTION_1       1  '1 positional argument'
             1510  LOAD_CONST               2
             1512  COMPARE_OP               >=
         1514_1516  POP_JUMP_IF_FALSE  1556  'to 1556'
             1518  LOAD_FAST                'l'
             1520  LOAD_CONST               -2
             1522  BINARY_SUBSCR    
             1524  LOAD_STR                 '그'
             1526  COMPARE_OP               ==
         1528_1530  POP_JUMP_IF_FALSE  1556  'to 1556'
             1532  LOAD_FAST                'l_last'
             1534  LOAD_CONST               0
             1536  BINARY_SUBSCR    
             1538  LOAD_STR                 'ㄹ'
             1540  COMPARE_OP               ==
         1542_1544  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 201      1546  LOAD_FAST                'l_front'
             1548  LOAD_STR                 '렇'
             1550  BINARY_ADD       
             1552  STORE_FAST               'l_stem'
             1554  JUMP_FORWARD       1594  'to 1594'
           1556_0  COME_FROM          1542  '1542'
           1556_1  COME_FROM          1528  '1528'
           1556_2  COME_FROM          1514  '1514'

 L. 203      1556  LOAD_FAST                'l_front'
             1558  LOAD_GLOBAL              compose
             1560  LOAD_FAST                'l_last'
             1562  LOAD_CONST               0
             1564  BINARY_SUBSCR    
             1566  LOAD_FAST                'l_last'
             1568  LOAD_CONST               1
             1570  BINARY_SUBSCR    
             1572  LOAD_STR                 'ㅔ'
             1574  COMPARE_OP               ==
         1576_1578  POP_JUMP_IF_FALSE  1584  'to 1584'
             1580  LOAD_STR                 'ㅓ'
             1582  JUMP_FORWARD       1586  'to 1586'
           1584_0  COME_FROM          1576  '1576'
             1584  LOAD_STR                 'ㅏ'
           1586_0  COME_FROM          1582  '1582'
             1586  LOAD_STR                 'ㅎ'
             1588  CALL_FUNCTION_3       3  '3 positional arguments'
             1590  BINARY_ADD       
             1592  STORE_FAST               'l_stem'
           1594_0  COME_FROM          1554  '1554'

 L. 204      1594  LOAD_GLOBAL              compose
             1596  LOAD_STR                 'ㅇ'
             1598  LOAD_FAST                'l_last'
             1600  LOAD_CONST               1
             1602  BINARY_SUBSCR    
             1604  LOAD_STR                 'ㅔ'
             1606  COMPARE_OP               ==
         1608_1610  POP_JUMP_IF_FALSE  1616  'to 1616'
             1612  LOAD_STR                 'ㅓ'
             1614  JUMP_FORWARD       1618  'to 1618'
           1616_0  COME_FROM          1608  '1608'
             1616  LOAD_STR                 'ㅏ'
           1618_0  COME_FROM          1614  '1614'
             1618  LOAD_FAST                'l_last'
             1620  LOAD_CONST               2
             1622  BINARY_SUBSCR    
             1624  CALL_FUNCTION_3       3  '3 positional arguments'
             1626  LOAD_FAST                'r'
             1628  BINARY_ADD       
             1630  STORE_FAST               'r_canon'

 L. 205      1632  LOAD_FAST                'add_lemma'
             1634  LOAD_FAST                'l_stem'
             1636  LOAD_FAST                'r_canon'
             1638  CALL_FUNCTION_2       2  '2 positional arguments'
             1640  POP_TOP          

 L. 206      1642  LOAD_FAST                'debug'
         1644_1646  POP_JUMP_IF_FALSE  1660  'to 1660'

 L. 207      1648  LOAD_GLOBAL              debug_message
             1650  LOAD_STR                 'ㅎ 축약 불규칙 활용'
             1652  LOAD_FAST                'l_stem'
             1654  LOAD_FAST                'r_canon'
             1656  CALL_FUNCTION_3       3  '3 positional arguments'
             1658  POP_TOP          
           1660_0  COME_FROM          1644  '1644'
           1660_1  COME_FROM          1500  '1500'
           1660_2  COME_FROM          1362  '1362'

 L. 213      1660  LOAD_FAST                'l_last'
             1662  LOAD_CONST               2
             1664  BINARY_SUBSCR    
             1666  LOAD_STR                 'ㅆ'
             1668  COMPARE_OP               ==
         1670_1672  POP_JUMP_IF_TRUE   1702  'to 1702'
             1674  LOAD_FAST                'l_last'
             1676  LOAD_CONST               2
             1678  BINARY_SUBSCR    
             1680  LOAD_STR                 'ㅅ'
             1682  COMPARE_OP               ==
         1684_1686  POP_JUMP_IF_TRUE   1702  'to 1702'
             1688  LOAD_FAST                'l_last'
             1690  LOAD_CONST               2
             1692  BINARY_SUBSCR    
             1694  LOAD_STR                 ' '
             1696  COMPARE_OP               ==
         1698_1700  POP_JUMP_IF_FALSE  1826  'to 1826'
           1702_0  COME_FROM          1684  '1684'
           1702_1  COME_FROM          1670  '1670'

 L. 214      1702  LOAD_FAST                'l_last'
             1704  LOAD_CONST               1
             1706  BINARY_SUBSCR    
             1708  LOAD_STR                 'ㅕ'
             1710  COMPARE_OP               ==
         1712_1714  POP_JUMP_IF_FALSE  1826  'to 1826'

 L. 217      1716  LOAD_FAST                'l_last'
             1718  LOAD_CONST               0
             1720  BINARY_SUBSCR    
             1722  LOAD_STR                 'ㅇ'
             1724  COMPARE_OP               ==
         1726_1728  POP_JUMP_IF_FALSE  1744  'to 1744'
             1730  LOAD_FAST                'l_last'
             1732  LOAD_CONST               1
             1734  BINARY_SUBSCR    
             1736  LOAD_STR                 'ㅕ'
             1738  COMPARE_OP               ==
         1740_1742  POP_JUMP_IF_TRUE   1758  'to 1758'
           1744_0  COME_FROM          1726  '1726'
             1744  LOAD_FAST                'l_last'
             1746  LOAD_CONST               0
             1748  BINARY_SUBSCR    
             1750  LOAD_STR                 'ㅇ'
             1752  COMPARE_OP               ==
         1754_1756  POP_JUMP_IF_TRUE   1826  'to 1826'
           1758_0  COME_FROM          1740  '1740'

 L. 218      1758  LOAD_FAST                'l_front'
             1760  LOAD_GLOBAL              compose
             1762  LOAD_FAST                'l_last'
             1764  LOAD_CONST               0
             1766  BINARY_SUBSCR    
             1768  LOAD_STR                 'ㅣ'
             1770  LOAD_STR                 ' '
             1772  CALL_FUNCTION_3       3  '3 positional arguments'
             1774  BINARY_ADD       
             1776  STORE_FAST               'l_stem'

 L. 219      1778  LOAD_GLOBAL              compose
             1780  LOAD_STR                 'ㅇ'
             1782  LOAD_STR                 'ㅓ'
             1784  LOAD_FAST                'l_last'
             1786  LOAD_CONST               2
             1788  BINARY_SUBSCR    
             1790  CALL_FUNCTION_3       3  '3 positional arguments'
             1792  LOAD_FAST                'r'
             1794  BINARY_ADD       
             1796  STORE_FAST               'r_canon'

 L. 220      1798  LOAD_FAST                'add_lemma'
             1800  LOAD_FAST                'l_stem'
             1802  LOAD_FAST                'r_canon'
             1804  CALL_FUNCTION_2       2  '2 positional arguments'
             1806  POP_TOP          

 L. 221      1808  LOAD_FAST                'debug'
         1810_1812  POP_JUMP_IF_FALSE  1826  'to 1826'

 L. 222      1814  LOAD_GLOBAL              debug_message
             1816  LOAD_STR                 '이었 -> 였 규칙 활용'
             1818  LOAD_FAST                'l_stem'
             1820  LOAD_FAST                'r_canon'
             1822  CALL_FUNCTION_3       3  '3 positional arguments'
             1824  POP_TOP          
           1826_0  COME_FROM          1810  '1810'
           1826_1  COME_FROM          1754  '1754'
           1826_2  COME_FROM          1712  '1712'
           1826_3  COME_FROM          1698  '1698'

 L. 225      1826  LOAD_FAST                'predefined'
         1828_1830  POP_JUMP_IF_FALSE  1898  'to 1898'
             1832  LOAD_FAST                'l'
             1834  LOAD_FAST                'r'
             1836  BUILD_TUPLE_2         2 
             1838  LOAD_FAST                'predefined'
             1840  COMPARE_OP               in
         1842_1844  POP_JUMP_IF_FALSE  1898  'to 1898'

 L. 226      1846  SETUP_LOOP         1898  'to 1898'
             1848  LOAD_FAST                'predefined'
             1850  LOAD_FAST                'l'
             1852  LOAD_FAST                'r'
             1854  BUILD_TUPLE_2         2 
             1856  BINARY_SUBSCR    
             1858  GET_ITER         
           1860_0  COME_FROM          1876  '1876'
             1860  FOR_ITER           1896  'to 1896'
             1862  STORE_FAST               'stem'

 L. 227      1864  LOAD_DEREF               'candidates'
             1866  LOAD_METHOD              add
             1868  LOAD_FAST                'stem'
             1870  CALL_METHOD_1         1  '1 positional argument'
             1872  POP_TOP          

 L. 228      1874  LOAD_FAST                'debug'
         1876_1878  POP_JUMP_IF_FALSE  1860  'to 1860'

 L. 229      1880  LOAD_GLOBAL              debug_message
             1882  LOAD_STR                 'Predefined'
             1884  LOAD_FAST                'l_stem'
             1886  LOAD_FAST                'r_canon'
             1888  CALL_FUNCTION_3       3  '3 positional arguments'
             1890  POP_TOP          
         1892_1894  JUMP_BACK          1860  'to 1860'
             1896  POP_BLOCK        
           1898_0  COME_FROM_LOOP     1846  '1846'
           1898_1  COME_FROM          1842  '1842'
           1898_2  COME_FROM          1828  '1828'

 L. 232      1898  LOAD_GLOBAL              set
             1900  CALL_FUNCTION_0       0  '0 positional arguments'
             1902  STORE_FAST               'candidates_'

 L. 233      1904  SETUP_LOOP         1994  'to 1994'
             1906  LOAD_DEREF               'candidates'
             1908  GET_ITER         
           1910_0  COME_FROM          1970  '1970'
             1910  FOR_ITER           1992  'to 1992'
             1912  UNPACK_SEQUENCE_2     2 
             1914  STORE_FAST               'stem'
             1916  STORE_FAST               'eomi'

 L. 234      1918  LOAD_FAST                'eomi'
         1920_1922  POP_JUMP_IF_TRUE   1928  'to 1928'

 L. 235  1924_1926  CONTINUE           1910  'to 1910'
           1928_0  COME_FROM          1920  '1920'

 L. 237      1928  LOAD_GLOBAL              decompose
             1930  LOAD_FAST                'eomi'
             1932  LOAD_CONST               0
             1934  BINARY_SUBSCR    
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  LOAD_CONST               2
             1940  BINARY_SUBSCR    
             1942  LOAD_STR                 'ㅎ'
             1944  COMPARE_OP               ==
         1946_1948  POP_JUMP_IF_FALSE  1954  'to 1954'

 L. 238  1950_1952  CONTINUE           1910  'to 1910'
           1954_0  COME_FROM          1946  '1946'

 L. 239      1954  LOAD_GLOBAL              conjugate
             1956  LOAD_FAST                'stem'
             1958  LOAD_FAST                'eomi'
             1960  CALL_FUNCTION_2       2  '2 positional arguments'
             1962  STORE_FAST               'surfaces'

 L. 240      1964  LOAD_FAST                'word'
             1966  LOAD_FAST                'surfaces'
             1968  COMPARE_OP               in
         1970_1972  POP_JUMP_IF_FALSE  1910  'to 1910'

 L. 241      1974  LOAD_FAST                'candidates_'
             1976  LOAD_METHOD              add
             1978  LOAD_FAST                'stem'
             1980  LOAD_FAST                'eomi'
             1982  BUILD_TUPLE_2         2 
             1984  CALL_METHOD_1         1  '1 positional argument'
             1986  POP_TOP          
         1988_1990  JUMP_BACK          1910  'to 1910'
             1992  POP_BLOCK        
           1994_0  COME_FROM_LOOP     1904  '1904'

 L. 242      1994  LOAD_FAST                'candidates_'
             1996  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 688