# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/vectorizer/_word_context.py
# Compiled at: 2018-10-01 03:38:35
# Size of source mod 2**32: 3706 bytes
from soynlp.utils import get_process_memory
from collections import defaultdict
from scipy.sparse import csr_matrix

def sent_to_word_contexts_matrix(sents, windows=3, min_tf=10, tokenizer=lambda x: x.split(), dynamic_weight=False, verbose=True):
    """
    :param dynamic_weight : Use dynamic weight if True.
        co-occurrence weight = [1, (w-1)/w, (w-2)/w, ... 1/w]
    """
    if verbose:
        print('Create (word, contexts) matrix')
    vocab2idx, idx2vocab = _scanning_vocabulary(sents, min_tf, tokenizer, verbose)
    word2contexts = _word_context(sents, windows, tokenizer, dynamic_weight, verbose, vocab2idx)
    x = _encode_as_matrix(word2contexts, vocab2idx, verbose)
    if verbose:
        print('  - done')
    return (
     x, idx2vocab)


def _scanning_vocabulary--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              defaultdict
                2  LOAD_GLOBAL              int
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_DEREF              'word_counter'

 L.  33         8  SETUP_LOOP           94  'to 94'
               10  LOAD_GLOBAL              enumerate
               12  LOAD_FAST                'sents'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  GET_ITER         
               18  FOR_ITER             92  'to 92'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'i_sent'
               24  STORE_FAST               'sent'

 L.  35        26  LOAD_FAST                'verbose'
               28  POP_JUMP_IF_FALSE    52  'to 52'
               30  LOAD_FAST                'i_sent'
               32  LOAD_CONST               1000
               34  BINARY_MODULO    
               36  LOAD_CONST               0
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L.  36        42  LOAD_GLOBAL              _print_status
               44  LOAD_STR                 '  - counting word frequency'
               46  LOAD_FAST                'i_sent'
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  POP_TOP          
             52_0  COME_FROM            40  '40'
             52_1  COME_FROM            28  '28'

 L.  38        52  LOAD_FAST                'tokenizer'
               54  LOAD_FAST                'sent'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  STORE_FAST               'words'

 L.  39        60  SETUP_LOOP           90  'to 90'
               62  LOAD_FAST                'words'
               64  GET_ITER         
               66  FOR_ITER             88  'to 88'
               68  STORE_FAST               'word'

 L.  40        70  LOAD_DEREF               'word_counter'
               72  LOAD_FAST                'word'
               74  DUP_TOP_TWO      
               76  BINARY_SUBSCR    
               78  LOAD_CONST               1
               80  INPLACE_ADD      
               82  ROT_THREE        
               84  STORE_SUBSCR     
               86  JUMP_BACK            66  'to 66'
               88  POP_BLOCK        
             90_0  COME_FROM_LOOP       60  '60'
               90  JUMP_BACK            18  'to 18'
               92  POP_BLOCK        
             94_0  COME_FROM_LOOP        8  '8'

 L.  42        94  LOAD_FAST                'verbose'
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L.  43        98  LOAD_GLOBAL              _print_status
              100  LOAD_STR                 '  - counting word frequency'
              102  LOAD_FAST                'i_sent'
              104  LOAD_CONST               True
              106  LOAD_CONST               ('new_line',)
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  POP_TOP          
            112_0  COME_FROM            96  '96'

 L.  46       112  LOAD_CLOSURE             'min_tf'
              114  BUILD_TUPLE_1         1 
              116  LOAD_SETCOMP             '<code_object <setcomp>>'
              118  LOAD_STR                 '_scanning_vocabulary.<locals>.<setcomp>'
              120  MAKE_FUNCTION_8          'closure'
              122  LOAD_DEREF               'word_counter'
              124  LOAD_METHOD              items
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  GET_ITER         
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  STORE_FAST               'vocab2idx'

 L.  47       134  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              136  LOAD_STR                 '_scanning_vocabulary.<locals>.<dictcomp>'
              138  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              140  LOAD_GLOBAL              enumerate

 L.  48       142  LOAD_GLOBAL              sorted
              144  LOAD_FAST                'vocab2idx'
              146  LOAD_CLOSURE             'word_counter'
              148  BUILD_TUPLE_1         1 
              150  LOAD_LAMBDA              '<code_object <lambda>>'
              152  LOAD_STR                 '_scanning_vocabulary.<locals>.<lambda>'
              154  MAKE_FUNCTION_8          'closure'
              156  LOAD_CONST               ('key',)
              158  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  GET_ITER         
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  STORE_FAST               'vocab2idx'

 L.  49       168  LOAD_LISTCOMP            '<code_object <listcomp>>'
              170  LOAD_STR                 '_scanning_vocabulary.<locals>.<listcomp>'
              172  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              174  LOAD_GLOBAL              sorted
              176  LOAD_FAST                'vocab2idx'
              178  LOAD_METHOD              items
              180  CALL_METHOD_0         0  '0 positional arguments'
              182  LOAD_LAMBDA              '<code_object <lambda>>'
              184  LOAD_STR                 '_scanning_vocabulary.<locals>.<lambda>'
              186  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              188  LOAD_CONST               ('key',)
              190  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              192  GET_ITER         
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  STORE_FAST               'idx2vocab'

 L.  50       198  DELETE_DEREF             'word_counter'

 L.  52       200  LOAD_FAST                'vocab2idx'
              202  LOAD_FAST                'idx2vocab'
              204  BUILD_TUPLE_2         2 
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 116


def _print_status(message, i_sent, new_line=False):
    print(('\r{} from {} sents, mem={} Gb'.format(message, i_sent, '%.3f' % get_process_memory())),
      flush=True,
      end=('\n' if new_line else ''))


def _word_context(sents, windows, tokenizer, dynamic_weight, verbose, vocab2idx):
    word2contexts = defaultdict(lambda : defaultdict(int))
    if dynamic_weight:
        weight = [(windows - i) / windows for i in range(windows)]
    else:
        weight = [
         1] * windows
    for i_sent, sent in enumerate(sents):
        if verbose:
            if i_sent % 1000 == 0:
                _print_status'  - scanning (word, context) pairs'i_sent
        words = tokenizer(sent)
        if not words:
            continue
        n = len(words)
        for i, word in enumerate(words):
            if word not in vocab2idx:
                continue
            for w in range(windows):
                j = i - (w + 1)
                if not j < 0:
                    if words[j] not in vocab2idx:
                        continue
                    word2contexts[word][words[j]] += weight[w]

            for w in range(windows):
                j = i + w + 1
                if not j >= n:
                    if words[j] not in vocab2idx:
                        continue
                    word2contexts[word][words[j]] += weight[w]

    if verbose:
        _print_status('  - scanning (word, context) pairs', i_sent, new_line=True)
    return word2contexts


def _encode_as_matrix(word2contexts, vocab2idx, verbose):
    rows = []
    cols = []
    data = []
    for word, contexts in word2contexts.items():
        word_idx = vocab2idx[word]
        for context, cooccurrence in contexts.items():
            context_idx = vocab2idx[context]
            rows.append(word_idx)
            cols.append(context_idx)
            data.append(cooccurrence)

    x = csr_matrix((data, (rows, cols)))
    if verbose:
        print('  - (word, context) matrix was constructed. shape = {}{}'.format(x.shape, '                    '))
    return x