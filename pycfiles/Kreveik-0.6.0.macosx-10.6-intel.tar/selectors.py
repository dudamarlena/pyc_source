# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/kreveik/network/selectors.py
# Compiled at: 2012-09-09 23:45:49
"""
selectors module
===============

In this module, the selectors for the GA elements, networks are defined. A selector returns True
or False due to whether a particular element is eligible for mutation or not. 

Functions
---------
    hard_threshold:
    hard_threshold_with_probability:
    logistic:
 
"""

def hard_threshold(network, **kwargs):
    import numpy as num, logging
    if 'threshold' not in kwargs:
        logging.error('The hard_threshold Selector needs a threshold parameter to work.')
        return
    else:
        if network.score < kwargs['threshold']:
            logging.info('score = ' + str(network.score) + ' < ' + str(kwargs['threshold']) + ' = threshold.')
            return True
        if network.score == kwargs['threshold']:
            logging.info('score = ' + str(network.score) + ' = ' + str(kwargs['threshold']) + ' = threshold.')
            if num.random.randint(0, 2) == 1:
                return True
            return False
        else:
            return False
        return


def hard_threshold_with_probability(network, **kwargs):
    import numpy as num, logging
    if 'threshold' not in kwargs:
        logging.error('The hard_threshold Selector needs a threshold parameter to work.')
        return
    else:
        if 'prob' not in kwargs:
            logging.error('The hard_threshold Selector needs a prob parameter to work.')
            return
        if network.score < kwargs['threshold']:
            logging.debug('score = ' + str(network.score) + ' < ' + str(kwargs['threshold']) + ' = threshold.')
            if num.random.random() < kwargs['prob']:
                return True
            return False
        elif network.score == kwargs['threshold']:
            logging.debug('score = ' + str(network.score) + ' = ' + str(kwargs['threshold']) + ' = threshold.')
            if num.random.randint(0, 2) == 1:
                return True
            return False
        else:
            return False
        return


def logistic(network, **kwargs):
    import numpy as num, logging, math
    if 'angle' not in kwargs or 'midpoint' not in kwargs:
        logging.error('The logistic Selector needs angle and midpoint parameters to work.')
        return
    else:
        angle = kwargs['angle']
        midpoint = kwargs['midpoint']
        prob = 1 - 1 / (1 + math.exp(-angle * (network.score - midpoint)))
        if prob < num.random.random():
            return True
        return False
        return


__all__ = [
 hard_threshold, hard_threshold_with_probability, logistic]