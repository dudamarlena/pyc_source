# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/utils.py
# Compiled at: 2020-01-10 09:07:13
import string

def reduce_text(text, limit):
    if len(text) <= limit:
        return text
    else:
        new_text = text[:limit]
        new_text_split = new_text.split(' ')
        slice_size = -1 if len(new_text_split) > 1 else 1
        clean_text = (' ').join(new_text_split[:slice_size])
        if clean_text[(-1)] in string.punctuation:
            clean_text = clean_text[:-1]
        if isinstance(clean_text, unicode):
            return ('{0}...').format(clean_text)
        return ('{0}...').format(clean_text.decode('utf-8'))


def format_date(date, fmt='%d %b %Y, %H:%M CET'):
    return date.strftime(fmt)