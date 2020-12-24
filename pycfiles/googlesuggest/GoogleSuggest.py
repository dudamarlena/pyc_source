# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Damjan\Desktop\GoogleSuggest\GoogleSuggest.py
# Compiled at: 2010-11-06 23:14:07
"""
GoogleSuggest
This module will help you to grab the Google suggestion for some expression

Usage:
    # Create instance without given value
    GoogleSuggest()
    # Create instance with given value
    GoogleSuggest( expression )
    # Grab the suggestion
    GoogleSuggest( expression ).read()
    GoogleSuggest().read( expression )
    Instance.read()
    Instance.suggest
    Instance.read( expression )

    # The method read( expression = None )
    # sets the list with the suggestion(s) and
    # returns the list with the suggestion(s)
"""
__all__ = [
 'url', 'tag', 'attribute', 'q', 'suggest', 'read']
__version__ = '1.0.0'
from urllib2 import urlopen
from xml.dom.minidom import parseString

class GoogleSuggestException(Exception):
    """ Handling GoogleSuggest exception(s) """
    pass


class GoogleSuggest(object):
    """ Class GoogleSuggest - Google suggestion grabber """

    def __init__(self, word=None, tag='suggestion', attr='data'):
        self.url = 'http://google.com/complete/search?output=toolbar&q='
        self.tag = tag
        self.attribute = attr
        self.q = word
        self.suggest = []

    def __del__(self):
        """ Destroy (Liberate) the used memory """
        self.suggest = None
        return

    def __fill(self, data=None):
        """ Fill the suggestion(s) """
        if not data:
            return
        try:
            self.suggest = []
            doc = parseString(data)
            nodes = doc.getElementsByTagName(self.tag)
            for node in nodes:
                tmp = node.getAttribute(self.attribute)
                self.suggest.append(tmp)

        except Exception as ex:
            raise GoogleSuggestException(ex)

    def __filter(self, text):
        """ Filtering the bad character(s) from the query string """
        return text

    def read(self, word=None):
        """ Read the suggestion(s) """
        query = None
        if word:
            query = word
        else:
            query = self.q
        if not query:
            return
        else:
            try:
                data = urlopen(self.url + self.__filter(query.replace(' ', '+'))).read()
                self.__fill(data)
                return self.suggest
            except Exception as ex:
                raise GoogleSuggestException(ex)

            return