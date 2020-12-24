# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nina/Documents/Sites/sitecomber-article-tests/sitecomber_article_tests/unit_tests/placeholder.py
# Compiled at: 2019-07-25 02:06:11
# Size of source mod 2**32: 698 bytes
from utils.article import get_placeholder_words

def test():
    print('Test placeholder flagging...')
    placeholder_words = ['lorem', 'ipsum', 'tk', 'todo']
    input_text = 'This is an example sentance with lorem Notsum Lorem and TODO and now klorem bipsum batkite'
    expected_placeholder_words = ['lorem', 'Lorem', 'TODO']
    actual_placeholder_words = get_placeholder_words(input_text, placeholder_words)
    if expected_placeholder_words != actual_placeholder_words:
        raise Exception("Placeholder word finder got unexpected output. \nExpected '%s' \nReceieved '%s' " % (expected_placeholder_words, actual_placeholder_words))
    print('Done testing placeholder functions!')