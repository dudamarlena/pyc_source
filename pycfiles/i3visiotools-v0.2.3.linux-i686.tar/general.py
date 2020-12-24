# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/general.py
# Compiled at: 2014-12-25 06:48:18
import hashlib, json, datetime
from i3visiotools.maltego import MaltegoEntity, MaltegoTransform
import logging

def dictToJson(d):
    """
                Workaround to convert any dictionary to json text.
                
                :param d:       Dictionary to convert to json.

                :return:        jsonText (string).
        """
    jsonText = json.dumps(d, indent=2)
    return jsonText


def listToMaltego(profiles):
    """ 
                Method to generate the text to be appended to a Maltego file.

                :param profiles:        a list of dictionaries with the information of the profiles: {"a_nick": [<list_of_results>]}
                
                :return:        maltegoText as the string to be written for a Maltego file.                             
        """
    logger = logging.getLogger('i3visiotools')
    logger.info('Generating Maltego File...')
    maltegoText = ''
    logger.debug('Going through all the keys in the dictionary...')
    me = MaltegoTransform()
    for profile in profiles:
        valueEnt = profile['value']
        typeEnt = profile['type']
        attributesEnt = profile['attributes']
        newEnt = me.addEntity(str(typeEnt), str(valueEnt))
        newEnt.addAdditionalFields('attributes', 'attributes', True, dictToJson(attributesEnt))
        newEnt.setDisplayInformation('<h3>' + valueEnt + '</h3><pre>' + dictToJson(attributesEnt) + '</pre>')
        for att in attributesEnt:
            if att['type'] == 'i3visio.platform':
                newEnt.addAdditionalFields(str(att['type']), str(att['type']), True, str(att['value']))

    me.addUIMessage('completed!')
    me.returnOutput()
    return me.getOutput()


def fileToMD5(filename, block_size=32768, binary=False):
    """
                :param filename:        Path to the file.
                :param block_size:      Chunks of suitable size. Block size directly depends on the block size of your filesystem to avoid performances issues. Blocks of 4096 octets (Default NTFS).
                :return:        md5 hash.
        """
    md5 = hashlib.md5()
    with open(filename, 'rb') as (f):
        for chunk in iter(lambda : f.read(block_size), ''):
            md5.update(chunk)

    if not binary:
        return md5.hexdigest()
    return md5.digest()


def getCurrentStrDatetime():
    """
                Generating the current Datetime with a given format.

                :return:        strTime
        """
    i = datetime.datetime.now()
    strTime = '%s-%s-%s_%sh%sm' % (i.year, i.month, i.day, i.hour, i.minute)
    return strTime


def getFilesFromAFolder(path):
    """
                Getting all the files in a folder.
                
                :param path:    path in which looking for files.
                
                :return:        list of filenames.
        """
    from os import listdir
    from os.path import isfile, join
    onlyFiles = []
    for f in listdir(path):
        if isfile(join(path, f)):
            onlyFiles.append(f)

    return onlyFiles