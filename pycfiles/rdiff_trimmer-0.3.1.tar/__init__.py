# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bystrousak/Plocha/Syncthing/c0d3z/python/tools/rdiff_trimmer/docs/__init__.py
# Compiled at: 2017-02-04 19:36:22


def get_version(data):

    def all_same(s):
        return all(x == s[0] for x in s)

    def has_digit(s):
        return any(x.isdigit() for x in s)

    data = data.splitlines()
    return list(line for line, underline in zip(data, data[1:]) if len(line) == len(underline) and all_same(underline) and has_digit(line) and '.' in line)[0]