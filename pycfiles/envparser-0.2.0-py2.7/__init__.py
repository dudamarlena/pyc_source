# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envparser/__init__.py
# Compiled at: 2011-11-06 15:00:37
import ConfigParser, os

class Parser(object):

    def __init__(self, basefile, environment='DEFAULT'):
        self.__parser = ConfigParser.SafeConfigParser()
        if environment == 'DEFAULT':
            self.__parser.read(basefile)
        else:
            self.__parser.read([basefile, self.__environment_file_from(basefile, environment)])
        self.environment = environment

    def __environment_file_from(self, basefile, environment):
        extension = os.path.splitext(basefile)[1]
        directory = os.path.dirname(basefile)
        return os.path.join(directory, environment + extension)

    def __get_with_method(self, method, option):
        try:
            return method(self.environment, option)
        except ConfigParser.NoSectionError:
            return method('DEFAULT', option)

    def get(self, option):
        return self.__get_with_method(self.__parser.get, option)

    def getint(self, option):
        return self.__get_with_method(self.__parser.getint, option)

    def getfloat(self, option):
        return self.__get_with_method(self.__parser.getfloat, option)

    def getboolean(self, option):
        return self.__get_with_method(self.__parser.getboolean, option)