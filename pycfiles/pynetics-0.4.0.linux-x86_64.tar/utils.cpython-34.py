# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/utils.py
# Compiled at: 2016-03-12 06:09:25
# Size of source mod 2**32: 763 bytes
import random

def take_chances(probability=0.5):
    """ Given a probability, the method generates a random value to see if is
        lower or not than that probability.

    :param probability: The value of the probability to beat. Default is 0.5.
    :return: A value of True if the value geneated is bellow the probability
        specified, and false otherwise.
    """
    return random.random() < probability


def clone_empty(obj):
    """ Used by classes which need to be cloned avoiding the call to __init__.

    :param obj: The object to be cloned.
    :return: A newly empty object of the class obj.
    """

    class Empty(obj.__class__):

        def __init__(self):
            pass

    empty = Empty()
    empty.__class__ = obj.__class__
    return empty