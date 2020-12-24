# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/util.py
# Compiled at: 2018-01-23 13:38:57
# Size of source mod 2**32: 682 bytes


def extract_number_from_string(text):
    """Take number like string out of text.
    """
    numberstr_list = list()
    chunks = list()
    for char in text:
        if char.isdigit() or char == '.':
            chunks.append(char)
        elif len(chunks):
            numberstr_list.append(''.join(chunks))
            chunks = list()

    if len(chunks):
        numberstr_list.append(''.join(chunks))
    new_numberstr_list = list()
    for s in numberstr_list:
        try:
            float(s)
            new_numberstr_list.append(s)
        except:
            pass

    return new_numberstr_list