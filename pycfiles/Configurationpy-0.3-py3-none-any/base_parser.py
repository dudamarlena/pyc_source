# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bogdan/projects/personal/configuration.py/configuration_py/parsers/base_parser.py
# Compiled at: 2017-03-28 11:26:23


class BaseConfigParser(object):

    @property
    def extensions(self):
        raise NotImplementedError

    def parse(self, file_content, context={}):
        raise NotImplementedError