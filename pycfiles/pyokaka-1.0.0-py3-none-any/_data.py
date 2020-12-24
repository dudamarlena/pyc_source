# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dojo\_data.py
# Compiled at: 2013-05-30 06:32:31
__doc__ = ' Data management utilities.  \n'
from _base import Dojo

class string(Dojo):
    """ Provides some simple string manipulation utilities.
    """
    require = [
     'dojo/string']


class date(Dojo):
    """ Provides date handling functions.
    """
    require = [
     'dojo/date']


class text(Dojo):
    """ AMD plugin that loads arbitrary string data from a file and returns it.
    """
    require = [
     'dojo/text!']


class json(Dojo):
    """ JSON parsing and serialization.
    """
    require = [
     'dojo/json']

    def parse(self):
        pass

    def stringfy(self):
        pass


class ioQuery(Dojo):
    """ Functions for converting between JavaScript objects and query strings 
    that are part of a URL.
    """
    require = [
     'dojo/io-query']

    def objectToQuery(self):
        pass

    def queryToObject(self):
        pass


class i18n(Dojo):
    """ A module that provides internationalization features.
    """
    require = [
     'dojo/i18n!']


class number(Dojo):
    """ Methods for user presentation of JavaScript Number objects: formatting, 
    parsing, and rounding.
    """
    require = [
     'dojo/number']


class currency(Dojo):
    """ Handling of virtually every type currency according to local customs.
    """
    require = [
     'dojo/currency']


class cldr(Dojo):
    """ Contains data from the Common Locale Data Repository (CLDR).
    """
    require = [
     'dojo/cldr']