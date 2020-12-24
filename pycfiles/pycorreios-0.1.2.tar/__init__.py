# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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