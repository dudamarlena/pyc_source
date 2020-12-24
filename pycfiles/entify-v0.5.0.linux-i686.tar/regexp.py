# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/patterns/regexp.py
# Compiled at: 2015-01-05 13:39:33
import os, re, copy, logging

class RegexpObject:
    """ 
        <RegexpObject> class.
    """

    def __init__(self):
        """ 
            Constructor without parameters...
            Most of the times, this will be the ONLY method needed to be overwritten.
        """
        self.name = '<empty>'
        self.reg_exp = []

    def __init__(self, name, reg_exp):
        """ 
            Constructor with parameters. This method permits the developer to instantiate dinamically <RegexpObject> objects.

            :param name:    string containing the name of the regular expression.
            :param reg_exp:    list of strings containing the regular expresion.
        """
        self.name = name
        self.reg_exp = [
         reg_exp]

    def __str__(self):
        """ 
            Function to obtain the text that represents this object.
            
            :return:    str(self.getJson())
        """
        return str(self.getResults())

    def getAttributes(self, foundExp):
        """
            Method to extract additional attributes from a given expression (i. e.: domains and ports from URL and so on). This method may be overwritten in certain child classes.
            :param found exp:   expression to be processed.
            :return:    The output format will be like:
                [{"type" : "i3visio.email", "value": "foo@bar.com", "attributes": [] }, {"type" : "i3visio.email", "value": "bar@foo.com", "attributes": [] }]
        """
        return []

    def getResults(self, parFound=None):
        """ 
            Function to obtain the Dictionarythat represents this object.
            
            :param parFound:    values to return.

            :return:    The output format will be like:
                [{"type" : "i3visio.email", "value": "foo@bar.com", "attributes": [] }, {"type" : "i3visio.email", "value": "bar@foo.com", "attributes": [] }]
        """
        results = []
        if len(parFound) > 0:
            for found in parFound:
                aux = {}
                aux['type'] = self.name
                aux['value'] = found
                aux['attributes'] = self.getAttributes(found)
                results.append(aux)

        return results

    def isValidExp(self, exp):
        """    
            Method to verify if a given expression is correct just in case the used regular expression needs additional processing to verify it.
            This method will be overwritten when necessary.

            :param exp:    Expression to verify.

            :return:    True | False
        """
        return True

    def findExp(self, data):
        """ 
            Method to look for the current regular expression in the provided string.

            :param data:    string containing the text where the expressions will be looked for.

            :return:    a list of verified regular expressions.
        """
        temp = []
        for r in self.reg_exp:
            try:
                temp += re.findall(r, data)
            except:
                print self.name
                print r
                print 'CABOOOOM!'

        verifiedExp = []
        for t in temp:
            if self.isValidExp(t):
                if t not in verifiedExp:
                    verifiedExp.append(t)

        return self.getResults(verifiedExp)