# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pycorrector/__init__.py
# Compiled at: 2019-12-02 04:33:46
from .corrector import Corrector
from .utils.logger import set_log_level
from .utils.text_utils import get_homophones_by_char, get_homophones_by_pinyin
from .utils.text_utils import traditional2simplified, simplified2traditional
corrector = Corrector()
get_same_pinyin = corrector.get_same_pinyin
get_same_stroke = corrector.get_same_stroke
set_custom_confusion_dict = corrector.set_custom_confusion_dict
set_custom_word = corrector.set_custom_word
set_language_model_path = corrector.set_language_model_path
correct = corrector.correct
ngram_score = corrector.ngram_score
ppl_score = corrector.ppl_score
word_frequency = corrector.word_frequency
detect = corrector.detect
enable_char_error = corrector.enable_char_error
enable_word_error = corrector.enable_word_error
set_log_level = set_log_level