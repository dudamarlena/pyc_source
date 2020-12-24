# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/noun/_josa.py
# Compiled at: 2018-07-02 01:15:52
# Size of source mod 2**32: 3960 bytes
import math

def extract_domain_pos_features--- This code section failed: ---

 L.  10         0  LOAD_CLOSURE             'min_noun_frequency'
                2  LOAD_CLOSURE             'min_noun_score'
                4  BUILD_TUPLE_2         2 
                6  LOAD_SETCOMP             '<code_object <setcomp>>'
                8  LOAD_STR                 'extract_domain_pos_features.<locals>.<setcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_FAST                'prediction_scores'
               14  LOAD_METHOD              items
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  GET_ITER         
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  STORE_DEREF              'nouns'

 L.  14        24  LOAD_FAST                'ignore_features'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  15        32  BUILD_MAP_0           0 
               34  STORE_FAST               'ignore_features'
             36_0  COME_FROM            30  '30'

 L.  17        36  BUILD_MAP_0           0 
               38  STORE_FAST               'pos_candidates'

 L.  18        40  SETUP_LOOP          118  'to 118'
               42  LOAD_DEREF               'nouns'
               44  GET_ITER         
               46  FOR_ITER            116  'to 116'
               48  STORE_FAST               'noun'

 L.  19        50  SETUP_LOOP          114  'to 114'
               52  LOAD_FAST                'lrgraph'
               54  LOAD_METHOD              get_r
               56  LOAD_FAST                'noun'
               58  LOAD_CONST               -1
               60  CALL_METHOD_2         2  '2 positional arguments'
               62  GET_ITER         
             64_0  COME_FROM            78  '78'
               64  FOR_ITER            112  'to 112'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'r'
               70  STORE_FAST               'count'

 L.  20        72  LOAD_FAST                'r'
               74  LOAD_DEREF               'known_pos_features'
               76  COMPARE_OP               in
               78  POP_JUMP_IF_TRUE     64  'to 64'
               80  LOAD_FAST                'r'
               82  LOAD_FAST                'ignore_features'
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE    90  'to 90'

 L.  21        88  CONTINUE             64  'to 64'
             90_0  COME_FROM            86  '86'

 L.  22        90  LOAD_FAST                'pos_candidates'
               92  LOAD_METHOD              get
               94  LOAD_FAST                'r'
               96  LOAD_CONST               0
               98  CALL_METHOD_2         2  '2 positional arguments'
              100  LOAD_FAST                'count'
              102  BINARY_ADD       
              104  LOAD_FAST                'pos_candidates'
              106  LOAD_FAST                'r'
              108  STORE_SUBSCR     
              110  JUMP_BACK            64  'to 64'
              112  POP_BLOCK        
            114_0  COME_FROM_LOOP       50  '50'
              114  JUMP_BACK            46  'to 46'
              116  POP_BLOCK        
            118_0  COME_FROM_LOOP       40  '40'

 L.  25       118  LOAD_CLOSURE             'min_pos_feature_frequency'
              120  BUILD_TUPLE_1         1 
              122  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              124  LOAD_STR                 'extract_domain_pos_features.<locals>.<dictcomp>'
              126  MAKE_FUNCTION_8          'closure'
              128  LOAD_FAST                'pos_candidates'
              130  LOAD_METHOD              items
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  GET_ITER         
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  STORE_FAST               'pos_candidates'

 L.  29       140  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              142  LOAD_STR                 'extract_domain_pos_features.<locals>.<dictcomp>'
              144  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              146  LOAD_DEREF               'known_pos_features'
              148  GET_ITER         
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  STORE_FAST               'domain_pos_features'

 L.  32       154  SETUP_LOOP          330  'to 330'
              156  LOAD_GLOBAL              sorted
              158  LOAD_FAST                'pos_candidates'
              160  LOAD_LAMBDA              '<code_object <lambda>>'
              162  LOAD_STR                 'extract_domain_pos_features.<locals>.<lambda>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_CONST               ('key',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  GET_ITER         
            172_0  COME_FROM           312  '312'
            172_1  COME_FROM           304  '304'
            172_2  COME_FROM           296  '296'
            172_3  COME_FROM           182  '182'
              172  FOR_ITER            328  'to 328'
              174  STORE_FAST               'r'

 L.  34       176  LOAD_FAST                'r'
              178  LOAD_DEREF               'known_pos_features'
              180  COMPARE_OP               in
              182  POP_JUMP_IF_TRUE    172  'to 172'
              184  LOAD_FAST                'r'
              186  LOAD_DEREF               'nouns'
              188  COMPARE_OP               in
              190  POP_JUMP_IF_FALSE   194  'to 194'

 L.  35       192  CONTINUE            172  'to 172'
            194_0  COME_FROM           190  '190'

 L.  37       194  LOAD_GLOBAL              _get_noun_feature
              196  LOAD_FAST                'r'
              198  LOAD_FAST                'lrgraph'
              200  CALL_FUNCTION_2       2  '2 positional arguments'
              202  STORE_FAST               'features'

 L.  38       204  LOAD_GLOBAL              predict
              206  LOAD_FAST                'r'
              208  LOAD_FAST                'features'
              210  LOAD_DEREF               'nouns'
              212  LOAD_FAST                'domain_pos_features'

 L.  39       214  LOAD_FAST                'min_pos_score'
              216  LOAD_DEREF               'min_pos_feature_frequency'

 L.  40       218  LOAD_FAST                'min_num_of_unique_lastchar'
              220  LOAD_FAST                'min_entropy_of_lastchar'
              222  CALL_FUNCTION_8       8  '8 positional arguments'
              224  UNPACK_SEQUENCE_2     2 
              226  STORE_FAST               'score'
              228  STORE_FAST               'freq'

 L.  43       230  LOAD_GLOBAL              sum
              232  LOAD_CLOSURE             'nouns'
              234  BUILD_TUPLE_1         1 
              236  LOAD_GENEXPR             '<code_object <genexpr>>'
              238  LOAD_STR                 'extract_domain_pos_features.<locals>.<genexpr>'
              240  MAKE_FUNCTION_8          'closure'
              242  LOAD_FAST                'features'
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  STORE_DEREF              'noun_sum'

 L.  44       252  LOAD_CLOSURE             'noun_sum'
              254  LOAD_CLOSURE             'nouns'
              256  BUILD_TUPLE_2         2 
              258  LOAD_LISTCOMP            '<code_object <listcomp>>'
              260  LOAD_STR                 'extract_domain_pos_features.<locals>.<listcomp>'
              262  MAKE_FUNCTION_8          'closure'
              264  LOAD_FAST                'features'
              266  GET_ITER         
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  STORE_FAST               'noun_entropy'

 L.  45       272  LOAD_GLOBAL              sum
              274  LOAD_LISTCOMP            '<code_object <listcomp>>'
              276  LOAD_STR                 'extract_domain_pos_features.<locals>.<listcomp>'
              278  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              280  LOAD_FAST                'noun_entropy'
              282  GET_ITER         
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  STORE_FAST               'noun_entropy'

 L.  47       290  LOAD_FAST                'score'
              292  LOAD_FAST                'min_pos_score'
              294  COMPARE_OP               >=
              296  POP_JUMP_IF_FALSE   172  'to 172'

 L.  48       298  LOAD_FAST                'freq'
              300  LOAD_DEREF               'min_pos_feature_frequency'
              302  COMPARE_OP               >=
              304  POP_JUMP_IF_FALSE   172  'to 172'

 L.  49       306  LOAD_FAST                'noun_entropy'
              308  LOAD_FAST                'min_noun_entropy'
              310  COMPARE_OP               >=
              312  POP_JUMP_IF_FALSE   172  'to 172'

 L.  50       314  LOAD_FAST                'score'
              316  LOAD_FAST                'freq'
              318  BUILD_TUPLE_2         2 
              320  LOAD_FAST                'domain_pos_features'
              322  LOAD_FAST                'r'
              324  STORE_SUBSCR     
              326  JUMP_BACK           172  'to 172'
              328  POP_BLOCK        
            330_0  COME_FROM_LOOP      154  '154'

 L.  53       330  LOAD_CLOSURE             'known_pos_features'
              332  BUILD_TUPLE_1         1 
              334  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              336  LOAD_STR                 'extract_domain_pos_features.<locals>.<dictcomp>'
              338  MAKE_FUNCTION_8          'closure'
              340  LOAD_FAST                'domain_pos_features'
              342  LOAD_METHOD              items
              344  CALL_METHOD_0         0  '0 positional arguments'
              346  GET_ITER         
              348  CALL_FUNCTION_1       1  '1 positional argument'
              350  STORE_FAST               'domain_pos_features'

 L.  56       352  LOAD_FAST                'domain_pos_features'
              354  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_noun_feature(r, lrgraph):
    return [(l, c) for l, c in lrgraph.get_lr(-1) if len(l) > 1]


def predict(r, features, nouns, pos_r, min_pos_score=0.3, min_pos_feature_frequency=30, min_num_of_unique_lastchar=4, min_entropy_of_lastchar=0.5):
    n_unique, n_sum, entropy = _last_character_criterions(features)
    if n_unique < min_num_of_unique_lastchar or entropy < min_entropy_of_lastchar:
        return (0, 0)
    pos, neg, unk = _predict(r, features, nouns, pos_r)
    score = (pos - neg) / (pos + neg) if pos + neg > 0 else 0
    freq = pos if score >= min_pos_score else neg + unk
    if freq < min_pos_feature_frequency:
        return (
         0, freq)
    return (score, freq)


def _predict(r, features, nouns, pos_r):
    pos, neg, unk = (0, 0, 0)
    for l, freq in features:
        if len(l) <= 1:
            continue
        if _is_NJ(r, nouns, pos_r):
            neg += freq
        elif _exist_longer_noun(l, r, nouns):
            neg += freq
        elif l in nouns:
            pos += freq
        else:
            unk += freq

    return (
     pos, neg, unk)


def _exist_longer_noun(l, r, nouns):
    for i in range1(len(r) + 1):
        if l + r[:i] in nouns:
            return True

    return False


def _is_NJ(r, nouns, pos_r):
    n = len(r)
    for i in range1n:
        if r[:i] in nouns:
            for j in rangein:
                return r[j:] in pos_r

    return False


def _last_character_criterions(lcount):
    counter = {}
    for l, count in lcount:
        last = l[(-1)]
        counter[last] = counter.getlast0 + count

    n_unique = len(counter)
    n_sum = sum(counter.values)
    entropy = [freq / n_sum for freq in counter.values]
    entropy = -1 * sum((p * math.log(p) for p in entropy))
    return (
     n_unique, n_sum, entropy)