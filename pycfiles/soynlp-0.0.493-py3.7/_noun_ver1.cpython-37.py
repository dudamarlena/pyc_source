# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/noun/_noun_ver1.py
# Compiled at: 2018-11-07 06:47:19
# Size of source mod 2**32: 10518 bytes
from collections import defaultdict, namedtuple
import math, sys
from soynlp.normalizer import normalize_sent_for_lrgraph
from soynlp.word import WordExtractor
from soynlp.utils import LRGraph
NounScore_v1 = namedtuple('NounScore_v1', 'frequency score known_r_ratio')

class LRNounExtractor:

    def __init__(self, max_left_length=10, max_right_length=7, predictor_fnames=None, verbose=True, min_num_of_features=1, ensure_normalized=False):
        self.coefficient = {}
        self.verbose = verbose
        self.max_left_length = max_left_length
        self.max_right_length = max_right_length
        self.lrgraph = None
        self.words = None
        self._substring_counter = {}
        self.min_num_of_features = min_num_of_features
        self.ensure_normalized = ensure_normalized
        if not predictor_fnames:
            import os
            directory = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
            predictor_fnames = ['%s/trained_models/noun_predictor_sejong' % directory]
            if verbose:
                print('[Noun Extractor] used default noun predictor; Sejong corpus predictor')
        for fname in predictor_fnames:
            if verbose:
                print('[Noun Extractor] used %s' % fname.split('/')[(-1)])
            self._load_predictor(fname)

        if verbose:
            print('[Noun Extractor] All %d r features was loaded' % len(self.coefficient))

    def _load_predictor(self, fname):
        try:
            if sys.version_info.major == 2:
                f = open(fname)
            else:
                f = open(fname, encoding='utf-8')
            try:
                try:
                    for num_line, line in enumerate(f):
                        r, score = line.strip().split('\t')
                        score = float(score)
                        if r in self.coefficient:
                            self.coefficient[r] = max(self.coefficient[r], score)
                        else:
                            self.coefficient[r] = score

                except Exception as e:
                    try:
                        print('[Noun Extractor] predictor parsing error line {} = {}'.format(num_line + 1, line))
                    finally:
                        e = None
                        del e

            finally:
                f.close()

        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def train_extract(self, sents, min_noun_score=0.5, min_noun_frequency=5, noun_candidates=None):
        self.train(sents, min_noun_frequency)
        return self.extract(min_noun_score, min_noun_frequency, noun_candidates)

    def train(self, sents, min_noun_frequency=5):
        wordset_l, wordset_r = self._scan_vocabulary(sents, min_noun_frequency)
        lrgraph = self._build_lrgraph(sents, wordset_l, wordset_r)
        self.lrgraph = LRGraph(lrgraph)
        self.words = wordset_l

    def _scan_vocabulary--- This code section failed: ---

 L.  85         0  LOAD_GLOBAL              defaultdict
                2  LOAD_LAMBDA              '<code_object <lambda>>'
                4  LOAD_STR                 'LRNounExtractor._scan_vocabulary.<locals>.<lambda>'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'wordset_l'

 L.  86        12  LOAD_GLOBAL              defaultdict
               14  LOAD_LAMBDA              '<code_object <lambda>>'
               16  LOAD_STR                 'LRNounExtractor._scan_vocabulary.<locals>.<lambda>'
               18  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  STORE_FAST               'wordset_r'

 L.  88        24  SETUP_LOOP          260  'to 260'
               26  LOAD_GLOBAL              enumerate
               28  LOAD_FAST                'sents'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  GET_ITER         
             34_0  COME_FROM           216  '216'
             34_1  COME_FROM           204  '204'
               34  FOR_ITER            258  'to 258'
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'i'
               40  STORE_FAST               'sent'

 L.  89        42  LOAD_FAST                'self'
               44  LOAD_ATTR                ensure_normalized
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L.  90        48  LOAD_GLOBAL              normalize_sent_for_lrgraph
               50  LOAD_FAST                'sent'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  STORE_FAST               'sent'
             56_0  COME_FROM            46  '46'

 L.  91        56  SETUP_LOOP          200  'to 200'
               58  LOAD_FAST                'sent'
               60  LOAD_METHOD              split
               62  LOAD_STR                 ' '
               64  CALL_METHOD_1         1  '1 positional argument'
               66  GET_ITER         
               68  FOR_ITER            198  'to 198'
               70  STORE_FAST               'token'

 L.  92        72  LOAD_FAST                'token'
               74  POP_JUMP_IF_TRUE     78  'to 78'

 L.  93        76  CONTINUE             68  'to 68'
             78_0  COME_FROM            74  '74'

 L.  94        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'token'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  STORE_FAST               'token_len'

 L.  95        86  SETUP_LOOP          142  'to 142'
               88  LOAD_GLOBAL              range
               90  LOAD_CONST               1
               92  LOAD_GLOBAL              min
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                max_left_length
               98  LOAD_FAST                'token_len'
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  LOAD_CONST               1
              104  BINARY_ADD       
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  GET_ITER         
              110  FOR_ITER            140  'to 140'
              112  STORE_FAST               'i'

 L.  96       114  LOAD_FAST                'wordset_l'
              116  LOAD_FAST                'token'
              118  LOAD_CONST               None
              120  LOAD_FAST                'i'
              122  BUILD_SLICE_2         2 
              124  BINARY_SUBSCR    
              126  DUP_TOP_TWO      
              128  BINARY_SUBSCR    
              130  LOAD_CONST               1
              132  INPLACE_ADD      
              134  ROT_THREE        
              136  STORE_SUBSCR     
              138  JUMP_BACK           110  'to 110'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP       86  '86'

 L.  97       142  SETUP_LOOP          196  'to 196'
              144  LOAD_GLOBAL              range
              146  LOAD_CONST               1
              148  LOAD_GLOBAL              min
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                max_right_length
              154  LOAD_FAST                'token_len'
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  CALL_FUNCTION_2       2  '2 positional arguments'
              160  GET_ITER         
              162  FOR_ITER            194  'to 194'
              164  STORE_FAST               'i'

 L.  98       166  LOAD_FAST                'wordset_r'
              168  LOAD_FAST                'token'
              170  LOAD_FAST                'i'
              172  UNARY_NEGATIVE   
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  DUP_TOP_TWO      
              182  BINARY_SUBSCR    
              184  LOAD_CONST               1
              186  INPLACE_ADD      
              188  ROT_THREE        
              190  STORE_SUBSCR     
              192  JUMP_BACK           162  'to 162'
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP      142  '142'
              196  JUMP_BACK            68  'to 68'
              198  POP_BLOCK        
            200_0  COME_FROM_LOOP       56  '56'

 L.  99       200  LOAD_FAST                'self'
              202  LOAD_ATTR                verbose
              204  POP_JUMP_IF_FALSE    34  'to 34'
              206  LOAD_FAST                'i'
              208  LOAD_CONST               1000
              210  BINARY_MODULO    
              212  LOAD_CONST               999
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE    34  'to 34'

 L. 100       218  LOAD_STR                 'scanning {} / {} sents'
              220  LOAD_METHOD              format
              222  LOAD_FAST                'i'
              224  LOAD_CONST               1
              226  BINARY_ADD       
              228  LOAD_GLOBAL              len
              230  LOAD_FAST                'sents'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  CALL_METHOD_2         2  '2 positional arguments'
              236  STORE_FAST               'message'

 L. 101       238  LOAD_GLOBAL              print
              240  LOAD_STR                 '\r[Noun Extractor] {}'
              242  LOAD_METHOD              format
              244  LOAD_FAST                'message'
              246  CALL_METHOD_1         1  '1 positional argument'
              248  LOAD_STR                 ''
              250  LOAD_CONST               ('end',)
              252  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              254  POP_TOP          
              256  JUMP_BACK            34  'to 34'
              258  POP_BLOCK        
            260_0  COME_FROM_LOOP       24  '24'

 L. 103       260  LOAD_CLOSURE             'min_frequency'
              262  BUILD_TUPLE_1         1 
              264  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              266  LOAD_STR                 'LRNounExtractor._scan_vocabulary.<locals>.<dictcomp>'
              268  MAKE_FUNCTION_8          'closure'
              270  LOAD_FAST                'wordset_l'
              272  LOAD_METHOD              items
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  GET_ITER         
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  LOAD_FAST                'self'
              282  STORE_ATTR               _substring_counter

 L. 104       284  LOAD_GLOBAL              set
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                _substring_counter
              290  LOAD_METHOD              keys
              292  CALL_METHOD_0         0  '0 positional arguments'
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  STORE_FAST               'wordset_l'

 L. 105       298  LOAD_CLOSURE             'min_frequency'
              300  BUILD_TUPLE_1         1 
              302  LOAD_SETCOMP             '<code_object <setcomp>>'
              304  LOAD_STR                 'LRNounExtractor._scan_vocabulary.<locals>.<setcomp>'
              306  MAKE_FUNCTION_8          'closure'
              308  LOAD_FAST                'wordset_r'
              310  LOAD_METHOD              items
              312  CALL_METHOD_0         0  '0 positional arguments'
              314  GET_ITER         
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  STORE_FAST               'wordset_r'

 L. 107       320  LOAD_FAST                'self'
              322  LOAD_ATTR                verbose
          324_326  POP_JUMP_IF_FALSE   362  'to 362'

 L. 108       328  LOAD_STR                 '(L,R) has (%d, %d) tokens'
              330  LOAD_GLOBAL              len
              332  LOAD_FAST                'wordset_l'
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  LOAD_GLOBAL              len
              338  LOAD_FAST                'wordset_r'
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  BUILD_TUPLE_2         2 
              344  BINARY_MODULO    
              346  STORE_FAST               'message'

 L. 109       348  LOAD_GLOBAL              print
              350  LOAD_STR                 '\r[Noun Extractor] scanning was done {}'
              352  LOAD_METHOD              format
              354  LOAD_FAST                'message'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  POP_TOP          
            362_0  COME_FROM           324  '324'

 L. 111       362  LOAD_FAST                'wordset_l'
              364  LOAD_FAST                'wordset_r'
              366  BUILD_TUPLE_2         2 
              368  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 302

    def _build_lrgraph(self, sents, wordset_l, wordset_r):
        lrgraph = defaultdict(lambda : defaultdict(lambda : 0))
        for i, sent in enumerate(sents):
            if not self.ensure_normalized:
                sent = normalize_sent_for_lrgraph(sent)
            for token in sent.split():
                if not token:
                    continue
                n = len(token)
                for i in range(1, min(self.max_left_length, n) + 1):
                    l = token[:i]
                    r = token[i:]
                    if l not in wordset_l:
                        continue
                    if len(r) > 0:
                        if r not in wordset_r:
                            continue
                    lrgraph[l][r] += 1

            if self.verbose and i % 1000 == 999:
                message = 'building L-R graph from {} / {} sents'.format(i + 1, len(sents))
                print(('\r[Noun Extractor] {}'.format(message)), end='')

        if self.verbose:
            print('\r[Noun Extractor] building L-R graph was done'.format('                    '))
        lrgraph = {l:{r:f for r, f in rdict.items()} for l, rdict in lrgraph.items()}
        return lrgraph

    def extract(self, min_noun_score=0.5, min_noun_frequency=5, noun_candidates=None):
        if not noun_candidates:
            noun_candidates = self.words
        nouns = {}
        for word in sorted(noun_candidates, key=(lambda w: len(w))):
            if len(word) <= 1:
                continue
            score = self.predict(word, nouns)
            if score[0] < min_noun_score:
                continue
            nouns[word] = score

        nouns = self._postprocess(nouns, min_noun_score, min_noun_frequency)
        nouns_ = self._to_NounScore(nouns)
        if self.verbose:
            print('[Noun Extractor] {} nouns are extracted'.format(len(nouns_)))
        return nouns_

    def _get_r_features(self, word):
        features = self.lrgraph.get_r(word, -1)
        features = [feature for feature in features if feature[0]]
        return features

    def _get_subword_score(self, word, min_noun_score, nouns):
        subword_scores = {}
        for e in range(1, len(word)):
            subword = word[:e]
            suffix = word[e:]
            if subword in nouns:
                if suffix in nouns:
                    score1 = nouns[subword]
                    score2 = nouns[suffix]
                    subword_scores[subword] = max(score1, score2)
            if subword in nouns and self.coefficient.get(suffix, 0.0) > min_noun_score:
                subword_scores[subword] = (
                 self.coefficient.get(suffix, 0.0), 0)

        if not subword_scores:
            return (0.0, 0)
        return sorted((subword_scores.items()), key=(lambda x: -x[1][0]))[0][1]

    def is_noun(self, word, min_noun_score=0.5):
        return self.predict(word)[0] >= min_noun_score

    def predict(self, word, min_noun_score=0.5, nouns=None):
        """Returns (noun_score, known_r_ratio)
        """
        features = self._get_r_features(word)
        if len(features) > self.min_num_of_features:
            score = self._predict(features, word)
        else:
            if nouns is None:
                nouns = {}
            score = self._get_subword_score(word, min_noun_score, nouns)
        return score

    def _predict(self, features, word):

        def exist_longer_r_feature(word, r):
            for e in range(len(word) - 1, -1, -1):
                suffix = word[e:] + r
                if suffix in self.coefficient:
                    return True

            return False

        score = 0
        norm = 0
        unknown = 0
        for r, freq in features:
            if r in self.coefficient:
                if not exist_longer_r_feature(word, r):
                    score += freq * self.coefficient[r]
                    norm += freq
            else:
                unknown += freq

        return (
         0 if norm == 0 else score / norm,
         0 if norm + unknown == 0 else norm / (norm + unknown))

    def _postprocess(self, nouns, min_noun_score, min_noun_frequency):

        def is_Noun_Josa(l, r):
            return l in nouns and self.coefficient.get(r, 0.0) > min_noun_score

        def cohesion(word):
            base = self._substring_counter.get(word[0], 0)
            n = len(word)
            if not base or n <= 1:
                return 0
            return math.pow(self._substring_counter.get(word, 0) / base, 1 / (n - 1))

        def longer_has_larger_cohesion(word):
            return cohesion(word) >= cohesion(word[:-1])

        removals = set()
        for word in nouns:
            if not word[(-1)] == '.':
                if word[(-1)] == ',':
                    removals.add(word)
                    continue
                n = len(word)
                if n <= 2 or longer_has_larger_cohesion(word):
                    continue
                for e in range(2, len(word)):
                    l = word[:e]
                    r = word[e:]
                    if is_Noun_Josa(l, r):
                        removals.add(word)
                        break

        nouns_ = {word:score for word, score in nouns.items() if (word in removals) == False}
        return nouns_

    def _to_NounScore(self, nouns):
        noun_frequencies = {}
        for word in sorted(nouns, key=(lambda x: -len(x))):
            r_count = self.lrgraph.get_r(word, -1)
            noun_frequencies[word] = sum((c for w, c in r_count))
            for r, count in r_count:
                self.lrgraph.remove_eojeol(word + r, count)

        self.lrgraph.reset_lrgraph()
        nouns_ = {}
        for word, score in nouns.items():
            nouns_[word] = NounScore_v1(noun_frequencies[word], score[0], score[1])

        return nouns_