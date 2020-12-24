# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngsphy/ngsphyexceptions.py
# Compiled at: 2017-12-14 13:13:35


class NGSphyException(Exception):
    """
    Exception raised for errors of the NGSphy program.
    ----------------------------------------------------------------------------
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message, time):
        self.expression = expression
        self.message = message
        self.time = time


class NGSphyExitException(Exception):
    """
    Exception raised for ending of the NGSphy process.
    ----------------------------------------------------------------------------
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message, time):
        self.expression = expression
        self.message = message
        self.time = time