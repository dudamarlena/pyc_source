# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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