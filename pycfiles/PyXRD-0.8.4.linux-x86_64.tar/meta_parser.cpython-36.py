# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/meta_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 458 bytes


class MetaParser(type):
    __doc__ = '\n        Metatype for the parser sub classes, allowing for auto file filter\n        creation.\n    '

    def __new__(meta, name, bases, attrs):
        res = super(MetaParser, meta).__new__(meta, name, bases, attrs)
        res.setup_file_filter()
        return res