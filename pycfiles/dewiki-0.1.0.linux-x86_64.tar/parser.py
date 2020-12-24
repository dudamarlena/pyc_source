# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dewiki/parser.py
# Compiled at: 2013-02-13 16:13:17
"""
Created on Jan 12, 2013

@author: dirk dierickx
"""
import re

class Parser(object):
    """
    Parser to remove all kinds of wiki markup tags from an object
    """

    def __init__(self):
        """
        Constructor
        """
        self.string = ''
        self.wiki_re = re.compile("\\[{2}(File|Category):[\\s\\S]+\\]{2}|\n                                        [\\s\\w#()]+\\||\n                                        (\\[{2}|\\]{2})|\n                                        \\'{2,5}|\n                                        (<s>|<!--)[\\s\\S]+(</s>|-->)|\n                                        {{[\\s\\S]+}}|\n                                        ^={1,6}|={1,6}$", re.X)

    def __list(self, listmatch):
        return ' ' * (len(listmatch.group()) - 1) + '*'

    def __parse(self, string=''):
        """
        Parse a string to remove and replace all wiki markup tags
        """
        self.string = string
        self.string = self.wiki_re.sub('', self.string)
        self.listmatch = re.search('^(\\*+)', self.string)
        if self.listmatch:
            self.string = self.__list(self.listmatch) + re.sub('^(\\*+)', '', self.string)
        return self.string

    def parse_string(self, string=''):
        """
        Parse a string object to de-wikified text
        """
        self.strings = string.splitlines(1)
        self.strings = [ self.__parse(line) for line in self.strings ]
        return ('').join(self.strings)

    def parse_byte(self, byte=None):
        """
        Parse a byte object to de-wikified text
        """
        pass

    def parse_file(self, file=None):
        """
        Parse the content of a file to de-wikified text
        """
        pass