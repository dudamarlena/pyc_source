# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\aerodynamics.py
# Compiled at: 2020-04-18 12:09:58
# Size of source mod 2**32: 329 bytes
from aerosandbox.geometry import *
from aerosandbox.performance import *

class AeroProblem(AeroSandboxObject):

    def __init__(self, airplane, op_point):
        self.airplane = airplane
        self.op_point = op_point