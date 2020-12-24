# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Palin/Code/courts-db/courts_db/text_utils.py
# Compiled at: 2020-02-18 11:20:15
import re
from string import punctuation
reg_punc = re.compile('[%s]' % re.escape(punctuation))
combined_whitespace = re.compile('\\s+')

def strip_punc(court_str):
    clean_court_str = reg_punc.sub(' ', court_str)
    clean_court_str = combined_whitespace.sub(' ', clean_court_str).strip()
    ccs = '%s' % clean_court_str.title()
    return ccs