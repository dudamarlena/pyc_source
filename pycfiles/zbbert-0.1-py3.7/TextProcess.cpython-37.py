# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zbbert\TextProcess.py
# Compiled at: 2019-05-22 06:29:59
# Size of source mod 2**32: 1216 bytes
import re

def pause(string_text, max_length=200):
    string_text = re.sub(' +', ' ', string_text)
    string_text = string_text.strip()
    list_text = string_text.split(' ')
    output_text = ''
    count_length = 0
    for word in list_text:
        if word == '':
            continue
        if len(word) > max_length:
            output_text = output_text + word + '。'
            count_length = 0
            continue
        if word[(-1)] == '。' or word[(-1)] == '！' or word[(-1)] == '？' or word[(-1)] == '.' or word[(-1)] == '!' or word[(-1)] == '?':
            output_text = output_text + word
            count_length = 0
        else:
            count_length += len(word)
            if count_length <= max_length:
                output_text = output_text + word + '，'
            else:
                output_text = output_text + '。' + word + '，'
                count_length = len(word)

    output_text = output_text + '。'
    output_text = re.sub('。+', '。', output_text)
    return output_text