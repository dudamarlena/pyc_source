# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/diffractionData.py
# Compiled at: 2009-05-29 13:49:17


class DiffractionData:
    """ data class which represents diffraction planes and diffraction angles
    """

    def __init__(self, name, eta, chi, angle):
        self.name = name
        self.chi = chi
        self.eta = eta
        self.angle = angle
        self.flagOn = False

    def turnOnFlag(self):
        self.flagOn = True

    def turnOffFlag(self):
        self.flagOn = False