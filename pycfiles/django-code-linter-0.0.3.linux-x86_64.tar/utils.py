# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/djinter/utils.py
# Compiled at: 2014-05-07 07:37:54


def grep(filepath, match_pattern, dont_match_pattern):
    """
    finds patt in file - patt is a compiled regex
    returns all lines that match patt

    http://grantmcwilliams.com/tech/programming/python/item/581-grep-a-file-in-python

    """
    matchlines = []
    f = open(filepath)
    for line in f.readlines():
        match = match_pattern.search(line)
        if match and not dont_match_pattern.search(line):
            matchlines.append(line)

    results = ('\n ').join(matchlines)
    if results:
        return results
    else:
        return
        return