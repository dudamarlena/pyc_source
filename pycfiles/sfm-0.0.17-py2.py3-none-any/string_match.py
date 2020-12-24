# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/single_file_module-project/sfm/string_match.py
# Compiled at: 2019-04-21 22:13:05
from fuzzywuzzy import process

def choose_best(text, choice, criterion=None):
    result, confidence_level = process.extractOne(text, choice)
    if criterion is None:
        return result
    else:
        if confidence_level >= criterion:
            return result
        else:
            return

        return