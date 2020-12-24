# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/analize.py
# Compiled at: 2014-10-05 16:25:50
# Size of source mod 2**32: 895 bytes
import os
from tkinter.messagebox import showerror
from equations import *
from mkreport import MkReport

class AnalizeSpec(Equations, MkReport):
    MashNodeError = 'Mashs or Nodes must be defined'

    def __init__(self):
        pass

    def analize(self):
        with open(self.FileName) as (specfile):
            lines = specfile.readlines()
            for line in lines:
                exec(line.upper(), {}, self.NetDict)

        try:
            if 'NODES' in self.NetDict:
                self.Nodes = self.NetDict['NODES']
                self.AnalType = 'Node'
            else:
                if 'MASHS' in self.NetDict:
                    self.Nodes = self.NetDict['MASHS']
                    self.AnalType = 'Mash'
                else:
                    raise MashNodeError
        except MashNodeError:
            showerror('Error', 'Mashs or Nodes must be defined')

        if self.Nodes < 2:
            showerror('Error', 'Enter Number of Mashs or Nodes.\nMust be 2 or higher.', 'Net Size', '2')