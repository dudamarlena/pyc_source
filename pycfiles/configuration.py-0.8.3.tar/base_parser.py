# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bogdan/projects/personal/configuration.py/configuration_py/parsers/base_parser.py
# Compiled at: 2017-03-28 11:26:23


class BaseConfigParser(object):

    @property
    def extensions(self):
        raise NotImplementedError

    def parse(self, file_content, context={}):
        raise NotImplementedError