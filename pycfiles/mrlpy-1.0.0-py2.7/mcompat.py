# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mcompat.py
# Compiled at: 2017-08-11 20:26:07
from mrlpy.mservice import MService
from org.myrobotlab.service import *

class MCompatibilityService(MService):

    def __init__(self, name=''):
        super(MCompatibilityService, self).__init__(name)

    def runScript(self, scriptFile):
        """
                Runs a script inside this compat service, allowing full usage of Jython syntax
                
                scriptFile represents the location of the script.
                """
        Runtime.setCompat(True)
        Runtime.setCompatServiceObject(self)
        execfile(str(scriptFile))

    def subscribe(self):
        """
                Implements python.subscribe()
                """
        pass