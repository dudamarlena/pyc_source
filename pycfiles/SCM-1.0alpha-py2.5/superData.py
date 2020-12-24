# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/superData.py
# Compiled at: 2009-05-29 13:49:17


class SuperData:
    """ parent class for all the data class in EPSC
    It has default functions to process data.
    """

    def __init__(self):
        self.data = {}
        self.flags = {}

    def setData(self, target, data):
        """ Set value to the dictionary
        """
        self.data[target] = data

    def getData(self, target):
        """ Get value from the dictionary
        """
        return self.data[target]

    def turnOnFlag(self, target):
        """ Turn the flag on
        """
        self.flags[target] = True

    def turnOffFlag(self, target):
        """ Turn the flag off
        """
        self.flags[target] = False

    def checkFlagOn(self, target):
        """ Check if the flag is on or not
        """
        return self.flags[target]