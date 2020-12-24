# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pycorrector/config.py
# Compiled at: 2019-11-25 03:20:36
import os
from pathlib import Path
USER_DIR = Path.expanduser(Path('~')).joinpath('.pycorrector')
if not USER_DIR.exists():
    USER_DIR.mkdir()
USER_DATA_DIR = USER_DIR.joinpath('datasets')
if not USER_DATA_DIR.exists():
    USER_DATA_DIR.mkdir()
language_model_path = os.path.join(USER_DATA_DIR, 'zh_giga.no_cna_cmn.prune01244.klm')
pwd_path = os.path.abspath(os.path.dirname(__file__))
word_freq_path = os.path.join(pwd_path, 'data/word_freq.txt')
common_char_path = os.path.join(pwd_path, 'data/common_char_set.txt')
same_pinyin_path = os.path.join(pwd_path, 'data/same_pinyin.txt')
same_stroke_path = os.path.join(pwd_path, 'data/same_stroke.txt')
custom_confusion_path = os.path.join(pwd_path, 'data/custom_confusion.txt')
custom_word_freq_path = os.path.join(pwd_path, 'data/custom_word_freq.txt')
person_name_path = os.path.join(pwd_path, 'data/person_name.txt')
place_name_path = os.path.join(pwd_path, 'data/place_name.txt')
stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')