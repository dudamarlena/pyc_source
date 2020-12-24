# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/functions.py
# Compiled at: 2011-04-22 06:35:42
""" Contains some helper functions """
import os

def loadProperties(propertiesFile, ambiguous=False, enc='ISO-8859-15'):
    """ Loads data from a file into a dict

        The data in the file should have the format
        key=valu. If the file doesn't exist, it
        will be created. If no filename is given
        an empty dict is returned.

        @param propertiesFile: The file to deal with
        @type propertiesFile: string
        @rtype: dict
    """
    properties = {}
    if propertiesFile == '':
        return {}
    if os.path.exists(propertiesFile):
        propFile = open(propertiesFile, 'r')
        content = unicode(propFile.read(), enc, errors='replace')
        propFile.close()
        for line in content.split('\n'):
            if len(line) > 1 and line[0] != '#':
                pair = line.split('=', 1)
                if len(pair) == 2:
                    if pair[1][0] == '=':
                        continue
                    if ambiguous:
                        if pair[0] not in properties:
                            properties[pair[0]] = []
                        properties[pair[0]].append(pair[1])
                    else:
                        properties[pair[0]] = pair[1]

    else:
        if not os.path.isdir(os.path.dirname(propertiesFile)):
            os.makedirs(os.path.dirname(propertiesFile))
        propFile = open(propertiesFile, 'w')
        propFile.close()
    return properties


def loadList(listFile):
    """ loads data from a file into a list

        This function loads simply each line of the file into a list.
        If the filename is empty, a empty list is returned. If the file given
        doesn't exist, it will be created.
        @param listFile: the file to deal with
        @type listFile: string
        @rtype: list
    """
    if listFile == '':
        return []
    list = []
    if os.path.exists(listFile):
        file = open(listFile, 'r')
        content = file.read()
        file.close()
        for word in content.split('\n'):
            if word != '' and word[0] != '#':
                list.append(word)

    else:
        if not os.path.isdir(os.path.dirname(listFile)):
            os.makedirs(os.path.dirname(listFile))
        file = open(listFile, 'w')
        file.close()
    return list