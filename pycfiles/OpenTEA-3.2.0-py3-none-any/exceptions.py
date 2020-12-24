# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/exceptions.py
# Compiled at: 2019-07-17 05:02:15
"""Exeptions.py

TODO

Created Nov 2016 by COOP team
"""
__all__ = [
 'XDRException',
 'XDRnoNodeException',
 'XDRtooManyNodesException',
 'XDRnoFileException',
 'XDRillFormed',
 'XDRUnknownValue',
 'XDRInterrupt',
 'OTException',
 'OTNoNodeException',
 'OTTooManyNodesException',
 'OTNoFileException',
 'OTIllFormed',
 'OTUnknownValue',
 'OTInterrupt']

class OTException(Exception):
    """Base exception for all OpenTEA library exceptions"""
    pass


class OTNoNodeException(OTException):
    """"No node found"""

    def __init__(self, msg='No node with this address found'):
        OTException.__init__(self, msg)


class OTTooManyNodesException(OTException):
    """Too many nodes have been found"""
    pass


class OTNoFileException(OTException):
    """No file found"""
    pass


class OTIllFormed(OTException):
    """Ill formed XML address"""
    pass


class OTUnknownValue(OTException):
    """Ill formed XML address"""

    def __init__(self, label, got_value, expected_values):
        OTException.__init__(self, ("XML tree at label {0} contains '{1}' but expected one of : {2}").format(label, got_value, expected_values))


class OTInterrupt(OTException):
    """Interruption of the OpenTEA process"""
    pass


XDRException = OTException
XDRnoNodeException = OTNoNodeException
XDRtooManyNodesException = OTTooManyNodesException
XDRnoFileException = OTNoFileException
XDRillFormed = OTIllFormed
XDRUnknownValue = OTUnknownValue
XDRInterrupt = OTInterrupt