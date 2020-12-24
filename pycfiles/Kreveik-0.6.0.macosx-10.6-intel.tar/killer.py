# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/family/killer.py
# Compiled at: 2012-09-09 23:45:49
"""
family.killer module
====================
Houses functions that kill a portion of a population.

Functions
---------
    random_killer: Kills randomly from an ensemble
    qualified_killer: TODO
    underachiever_killer: TODO
    
"""

def random_killer(ensemble, times):
    import numpy as num, logging
    logging.info('Killing ' + str(times) + ' individuals')
    for i in range(times):
        randomnum = num.random.randint(0, len(ensemble))
        logging.info('(' + str(i) + '/' + str(times) + ') Killing ' + str(ensemble[randomnum]))
        ensemble.remove(randomnum)


def qualified_killer(ensemble, **kwargs):
    pass


def underachiever_killer(ensemble, **kwargs):
    pass


__all__ = [
 random_killer, qualified_killer, underachiever_killer]