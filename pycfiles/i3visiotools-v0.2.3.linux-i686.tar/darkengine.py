# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/lib/wrappers/darkengine.py
# Compiled at: 2014-12-25 06:48:18
import os, re, copy, logging, i3visiotools.browser as usufybrowser

class DarkEngine:
    """ 
                <DarkEngine> class.
        """

    def __init__(self):
        """ 
                        Constructor without parameters...
                        Most of the times, this will be the ONLY method needed to be overwritten.
                """
        self.name = '<empty>'
        self.url = 'http://example.com/?q=' + '<THE_WORD>'
        self.delimiters = {}
        self.delimiters['start'] = '<start_text>'
        self.delimiters['end'] = '<end_text>'
        self.fields = {}

    def __str__(self):
        """ 
                        Function to obtain the text that represents this object.
                        
                        :return:        str(self.getJson())
                """
        return str(self.name)

    def getResults(self, word=None):
        r""" 
                        Function to recover the.
                        
                        :param word:    word to be searched.

                        :return:        The output format will be like:
                                {"email" : {"reg_exp" : "[a-zA-Z0-9\.\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]+" , "found_exp" : ["foo@bar.com", "bar@foo.com"] } }
                """
        logger = logging.getLogger('darkfy')
        searchURL = self.url.replace('<THE_WORD>', word)
        logger.debug('Recovering the targetted url (authenticated)...')
        uBrowser = usufybrowser.Browser()
        html = uBrowser.recoverURL(searchURL)
        start = self.delimiters['start']
        end = self.delimiters['end']
        values = re.findall(start + '(.*?)' + end, html, re.DOTALL)
        parsedResults = []
        for val in values:
            newResource = {}
            for field in self.fields.keys():
                foundElems = re.findall(self.fields[field]['start'] + '(.*?)' + self.fields[field]['end'], val, re.DOTALL)
                newResource[field] = self.cleanSpecialChars(foundElems)

            parsedResults.append(newResource)

        return parsedResults

    def cleanSpecialChars(self, auxList):
        """
                        Method that cleans any text deleting certain special characters and avoiding the text between '<' and '>'.
        
                        :param auxList: Any list of strings.
                        :return:        A cleaned list of strings.
                """
        final = []
        cleaningChars = [
         '\n', '\t', '\r']
        for elem in auxList:
            for c in cleaningChars:
                elem = elem.replace(c, '')

            elem = re.sub('<.+?>', ' ', elem)
            final.append(elem)

        return final