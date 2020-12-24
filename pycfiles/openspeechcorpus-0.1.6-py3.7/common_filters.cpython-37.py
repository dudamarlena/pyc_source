# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/common_filters.py
# Compiled at: 2020-01-11 08:44:43
# Size of source mod 2**32: 1487 bytes


def clean_accents(word):
    output = []
    for letter in word:
        if letter == 'á':
            modified_letter = 'a'
        else:
            if letter == 'é':
                modified_letter = 'e'
            else:
                if letter == 'í':
                    modified_letter = 'i'
                else:
                    if letter == 'ó':
                        modified_letter = 'o'
                    else:
                        if letter == 'ú':
                            modified_letter = 'u'
                        else:
                            if letter == 'ñ':
                                modified_letter = 'N'
                            else:
                                modified_letter = letter
        output.append(modified_letter)

    return ''.join(output)


def filter_special_characters(word):
    output = []
    for letter in word:
        if letter == '-':
            modified_letter = ''
        else:
            if letter == '\n':
                modified_letter = ''
            else:
                if letter == '\\.':
                    modified_letter = ''
                else:
                    if letter == '?':
                        modified_letter = ''
                    else:
                        modified_letter = letter
        output.append(modified_letter)

    return ''.join(output)


def allow_characters(word):
    alphabet = 'abcdefghijklmnNopqrstuvwxyz '
    output = []
    for letter in word:
        if letter in alphabet:
            output.append(letter)

    return ''.join(output)


def extract_phones_from_word(word):
    return ' '.join(apply_filters(word))


def apply_filters(word):
    return allow_characters(filter_special_characters(clean_accents(word)))


def remove_jump_characters(word):
    return word.replace('\n', '').replace('\r', '')