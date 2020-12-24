# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/export.py
# Compiled at: 2014-12-25 06:48:18
import logging

def resultsToCSV(res):
    """ 
                Method to generate the text to be appended to a CSV file.

                :param res:     a dictionary with the information of the profiles
                
                :return:        csvText as the string to be written in a CSV file.                              
        """
    logger = logging.getLogger('i3visiotools')
    logger.info('Generating .csv...')
    csvText = 'User\tPlatform\tURL\n'
    logger.debug('Going through all the keys in the dictionary...')
    for r in res.keys():
        for p in res[r].keys():
            csvText += str(r) + '\t' + str(p) + '\t' + res[r][p] + '\n'

    logger.debug('Loading the dictionary onto a csv-style text...')
    return csvText