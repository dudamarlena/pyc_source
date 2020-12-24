# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/serviceExceptions.py
# Compiled at: 2009-09-24 03:11:06
import traceback

class SOAPException(Exception):
    """
    A generic wrapper for SOAP exceptions
    """

    def __init__(self):
        try:
            self.message = [ line for line in traceback.format_exc().splitlines() if line.find('WebFault') != -1 ][(-1)]
        except:
            self.message = 'SOAP Fault.'

    def __str__(self):
        return self.message