# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sqldisco/splitter.py
# Compiled at: 2013-03-18 17:15:00
"""
File: splitter.py
Author: Jon Eisen
Description: Calculate parameters to split SQL data before transfer.
"""
import logging
from split import SqlSplit

def calculate_splits(config):
    """reads config to find out what type of split to perform"""
    if config.get('split', False):
        logging.error('Input splits are not implemented!')
    logging.info('Non-Split mode calculation entering.')
    return calculate_single_split(config)


def calculate_single_split(config):
    """Returns parameters for a single split"""
    split = SqlSplit(sqltype=config.get('sqltype'), connargs=config.get('connargs'), query=config.get('query'))
    logging.debug('Calculated split: %s' % split)
    return [
     split.uri()]