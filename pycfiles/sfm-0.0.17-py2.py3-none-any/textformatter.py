# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/single_file_module-project/sfm/textformatter.py
# Compiled at: 2019-04-21 23:25:37
"""
本模块提供了一些迷你的文本处理函数。

- 所有函数名都以 ``format_xxx`` 开头, 这样是为了防止在使用 
  ``from textformatter import *`` 时会污染命名空间。
"""
import string
FILENAME_FORBIDDEN_CHAR = "\\/:*?|<'>"
FUNCTION_WORD = set([
 'a', 'an', 'the',
 'and', 'or', 'not',
 'in', 'on', 'at',
 'am', 'is', 'are',
 'was', 'were',
 'with', 'within', 'as', 'of',
 'to', 'from', 'by',
 'than'])
ALPHA_DIGITS = set(string.ascii_letters + string.digits)

def format_single_space_only(text):
    u"""Revise consecutive empty space to single space.

    Example::

        " I   feel    so  GOOD!" => "This is so GOOD!"

    **中文文档**

    确保文本中不会出现多余连续1次的空格。
    """
    return (' ').join([ word for word in text.strip().split(' ') if len(word) >= 1 ])


def format_title(text):
    u"""Capitalize first letter for each words except function words.

    Example::

        title = "Beautiful is Better than Ugly"

    **中文文档**

    将文本 "标题化", 即除了虚词, 每一个英文单词的第一个字母大写。
    """
    text = text.strip()
    if len(text) == 0:
        return text
    else:
        text = text.lower()
        words = [ word for word in text.strip().split(' ') if len(word) >= 1 ]
        words_new = list()
        for word in words:
            if word not in FUNCTION_WORD:
                word = word[0].upper() + word[1:]
            words_new.append(word)

        words_new[0] = words_new[0][0].upper() + words_new[0][1:]
        return (' ').join(words_new)


def format_person_name(text):
    u"""Capitalize first letter for each part of the name.

    Example::

        person_name = "James Bond"

    **中文文档**

    将文本修改为人名格式。每个单词的第一个字母大写。
    """
    text = text.strip()
    if len(text) == 0:
        return text
    else:
        text = text.lower()
        words = [ word for word in text.strip().split(' ') if len(word) >= 1 ]
        words = [ word[0].upper() + word[1:] for word in words ]
        return (' ').join(words)


def format_filename(text):
    u"""Remove file-system forbidden character from file name.

    **中文文档**

    从文件名中移除文件系统中不允许的字符。 
    """
    for char in FILENAME_FORBIDDEN_CHAR:
        text = text.replace(char, '')

    return text


def format_camel_case(text):
    u"""
    Example::

        ThisIsVeryGood

    **中文文档**

    将文本格式化为各单词首字母大写, 拼接而成的长变量名。
    """
    text = text.strip()
    if len(text) == 0:
        raise ValueError('can not be empty string!')
    else:
        text = text.lower()
        words = list()
        word = list()
        for char in text:
            if char in ALPHA_DIGITS:
                word.append(char)
            elif len(word):
                words.append(('').join(word))
                word = list()

        if len(word):
            words.append(('').join(word))
        words = [ word[0].upper() + word[1:] for word in words ]
        return ('').join(words)


def format_small_camel_case(text):
    """
    Example::

        thisIsVeryGood
    """
    text = format_camel_case(text)
    return text[0].lower() + text[1:]


def format_unix_var(text):
    """
    Example::

        this_is_very_good
    """
    text = text.strip()
    if len(text) == 0:
        raise ValueError('can not be empty string!')
    else:
        if text[0] in string.digits:
            raise ValueError('variable can not start with digits!')
        text = text.lower()
        words = list()
        word = list()
        for char in text:
            if char in ALPHA_DIGITS:
                word.append(char)
            elif len(word):
                words.append(('').join(word))
                word = list()

        if len(word):
            words.append(('').join(word))
        return ('_').join(words)