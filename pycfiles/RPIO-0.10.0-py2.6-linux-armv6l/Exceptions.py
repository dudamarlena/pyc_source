# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/RPIO/Exceptions.py
# Compiled at: 2013-03-14 10:44:22
"""
This module contains all the exceptions used by the C GPIO wrapper.
"""
import RPIO._GPIO as _GPIO
WrongDirectionException = _GPIO.WrongDirectionException
InvalidModeException = _GPIO.InvalidModeException
InvalidDirectionException = _GPIO.InvalidDirectionException
InvalidChannelException = _GPIO.InvalidChannelException
InvalidPullException = _GPIO.InvalidPullException
ModeNotSetException = _GPIO.ModeNotSetException