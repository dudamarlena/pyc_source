# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_data.py
# Compiled at: 2011-10-24 11:58:53
from droopy.lang.english import English
from droopy.lang.polish import Polish
TEXTS = [
 {'lang': English, 
    'id': 'Simple', 
    'text': 'Just a simple test.', 
    'nof_characters': 15, 
    'nof_words': 4, 
    'nof_sentences': 1, 
    'flesch_grade_level': 0.72, 
    'automated_readability_index': -1.77, 
    'smog': 3.13, 
    'flesch_reading_ease': 97.03, 
    'coleman_liau': -1.15},
 {'lang': Polish, 
    'id': 'Simple', 
    'text': 'Tylko prosty test.', 
    'nof_characters': 15, 
    'nof_words': 3, 
    'nof_sentences': 1, 
    'flesch_grade_level': 5.25, 
    'automated_readability_index': 3.62, 
    'smog': 3.13, 
    'flesch_reading_ease': 62.79, 
    'coleman_liau': 3.73}]