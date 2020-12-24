# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ac/filters.py
# Compiled at: 2013-07-14 15:43:54


def remove_empty(entry):
    """
        Filters all empty strings and 'None' entries from a list
    """
    return len(entry) >= 1


def nonalpha_filter(element):
    """
        Removes non-alpha characters from a filtered string.
    """
    return element in string.ascii_letters


def alphaonly(string):
    """
        Given a string, filters out all non-alpha characters
    """
    string = list(string)
    string = filter(nonalpha_filter, string)
    string = ('').join(string)
    return string