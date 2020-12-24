# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/darkfy/lib/processing.py
# Compiled at: 2014-12-25 06:48:18
import os, time, i3visiotools.darkfy.lib.config_darkfy as config, i3visiotools.general as general, i3visiotools.logger, logging

def searchTerms(words=[], output=None):
    """ 
                Method that looks for the words in the Deep Web.

                :param words:   List of words to be searched.
                :param output:  File where the results will be stored.

                :return:        A dict containing the results.
        """
    logger = logging.getLogger('darkfy')
    platforms = config.getAllDarkEngines()
    allResults = {}
    for word in words:
        allResults[word] = {}
        for plat in platforms:
            allResults[word][str(plat)] = []
            allResults[word][str(plat)] = plat.getResults(word)

    logger.info('Writing results to json file')
    jsonData = general.dictToJson(allResults)
    if output != None:
        with open(os.path.join(output), 'w') as (oF):
            oF.write(jsonData + '\n')
    logger.info(jsonData)
    return allResults


def darkfy_main(args):
    """ 
                Main function. This function is created in this way so as to let other applications make use of the full configuration capabilities of the application. 
        """
    logger = logging.getLogger('darkfy')
    logger = logging.getLogger('darkfy')
    logger.info('darkfy.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions.\nFor details, run:\n\tpython darkfy.py --license')
    logger.info('Starting darkfy-launcher.py...')
    if args.license:
        logger.info('Looking for the license...')
        try:
            with open('COPYING', 'r') as (iF):
                contenido = iF.read().splitlines()
                for linea in contenido:
                    print linea

                return contenido
        except Exception:
            logger.error('ERROR: there has been an error when opening the COPYING file.\n\tThe file contains the terms of the GPLv3 under which this software is distributed.\n\tIn case of doubts, verify the integrity of the files or contact contacto@i3visio.com.')

    else:
        words = []
        logger.debug('Recovering nicknames to be processed...')
        if args.words:
            words = args.words
        else:
            try:
                words = args.list.read().splitlines()
            except:
                logger.error('ERROR: there has been an error when opening the file that stores the nicks.\tPlease, check the existence of this file.')

        return searchTerms(words=words, output=args.output)