# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/issackelly/Projects/python/servee/servee/utils.py
# Compiled at: 2012-09-09 14:37:07


def space_out_camel_case(camel):
    """
    Converts a "CamelCasedName" to "Camel Case Name".
    """
    chars = []
    for char in camel:
        if len(chars) >= 2 and chars[(-1)] != ' ':
            if char.isupper() and chars[(-1)].islower():
                chars.append(' ')
            elif char.islower() and chars[(-1)].isupper() and chars[(-2)].isupper():
                chars.insert(len(chars) - 1, ' ')
        chars.append(char)

    return ('').join(chars)