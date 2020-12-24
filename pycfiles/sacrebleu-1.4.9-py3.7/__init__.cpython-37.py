# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/sacrebleu/__init__.py
# Compiled at: 2020-04-30 19:35:56
# Size of source mod 2**32: 1229 bytes
__version__ = '1.4.9'
__description__ = 'Hassle-free computation of shareable, comparable, and reproducible BLEU scores'
from .sacrebleu import smart_open, corpus_bleu, corpus_chrf, sentence_bleu, sentence_chrf, compute_bleu, raw_corpus_bleu, get_source_file, get_reference_files, get_available_testsets, get_langpairs_for_testset, BLEU, CHRF, DATASETS, TOKENIZERS, SACREBLEU_DIR
from .sacrebleu import ref_stats, bleu_signature, extract_ngrams, extract_char_ngrams, get_corpus_statistics, display_metric, get_sentence_statistics, download_test_set