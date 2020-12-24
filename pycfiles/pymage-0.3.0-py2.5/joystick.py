# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pymage/joystick.py
# Compiled at: 2007-08-10 19:47:49
"""Manage joysticks"""
import pygame
from pygame.locals import *
__author__ = 'Ross Light'
__date__ = 'July 20, 2006'
__all__ = ['Axis']
__docformat__ = 'reStructuredText'

class Axis(object):
    """
    Represents a joystick axis.
    
    :CVariables:
        perfectRange : tuple
            The three magic values for calculating perfect mode.
    :IVariables:
        joy : ``pygame.joystick.Joystick``
            Joystick
        num : int
            Axis number
        invert : bool
            Invert axis (always calculated)
        perfect : bool
            Whether perfect mode is active.  When ``True``, a few extra
            calculations are performed to ensure that the axis is always within
            the -1.0 to 1.0 range.
    """
    perfectRange = (-1.0, 0.0, 1.0)
    perfect = False

    def __init__(self, joy, num, invert=False, perfect=None):
        """
        Initializes the axis.
        
        :Parameters:
            joy : ``pygame.joystick.Joystick``
                Joystick
            num : int
                Axis number
            invert : bool
                Invert axis
            perfect : bool
                Whether perfect mode is active.
        """
        self.joy, self.num = joy, num
        self.invert = invert
        if perfect is not None:
            self.perfect = perfect
        if self.perfect:
            (self.min, self.max) = (0.0, 0.0)
            (self.offset, self.scale) = (0.0, 1.0)
        return

    def addEntry(self, value):
        """
        If the axis is in perfect mode, calibrate the axis from the information
        given.
        
        .. Tip:: You shouldn't need to use this, instead, use `sample`.
        
        :Parameters:
            value : float
                Raw joystick value
        """
        if self.perfect:
            (perfectMin, perfectMid, perfectMax) = self.perfectRange
            if value > self.max:
                self.max = value
            elif value < self.min:
                self.min = value
            else:
                return
            mid = (self.max + self.min) / 2
            self.offset = perfectMid - mid
            self.scale = (perfectMax - perfectMin) / (self.max - self.min)

    def sample(self):
        """
        Samples calibration information for the axis.
        
        This method only needs to be called in perfect mode.  It is not
        neccessary in normal mode, but shouldn't take a performance hit, so you
        should probably stick it in your code anyway.
        """
        joy = pygame.joystick.Joystick(self.joy)
        self.addEntry(joy.get_axis(self.num))

    def convert(self, raw_value):
        """
        Converts a raw value from the joystick.
        
        .. Tip:: You shouldn't need to use this, instead, use `get`.
        
        :Parameters:
            raw_value : float
                Raw joystick value
        :Returns: Converted value
        :ReturnType: float
        """
        if self.perfect:
            value = (raw_value + self.offset) * self.scale
        else:
            value = raw_value
        if self.invert:
            value = -value
        return value

    def get(self):
        """
        Retrieves the current value of the axis.
        
        If the axis is in perfect mode, this performs calculations based on
        previous calibration information to ensure it is perfect.  If in normal
        mode, this retreives the raw value (inverted, if necessary).
        
        :Returns: Axis value
        :ReturnType: float
        """
        joy = pygame.joystick.Joystick(self.joy)
        return self.convert(joy.get_axis(self.num))