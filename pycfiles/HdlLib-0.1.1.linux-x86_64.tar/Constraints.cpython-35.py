# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/Constraints.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 2877 bytes
import os, sys, logging

class Constraints:

    def __init__(self, Throughput, HwModel, AddCommunication=False):
        """
                Setup parameters Throughput and HwModel.
                """
        self.Throughput = Throughput
        self.HwModel = HwModel
        self.AddCommunication = AddCommunication

    def GetCommunicationService(self, ServDict):
        """
                Return a communication service that is supported by the Hw model.
                """
        if self.AddCommunication is True:
            for SName, S in ServDict.items():
                if S.IsCommunication is True:
                    return S

            logging.error("Cannot find any communication module that satisfies these constraints '{0}'.".format(self))
            return
        else:
            ServName = 'SimuCom'
            for SName, S in ServDict.items():
                if SName == ServName:
                    return S

            logging.error("Cannot find the 'SimuCom' service in library.")
            return

    def SatisfiedFor(self, Module):
        """
                return True if Module satisfy Hw and throughput constraints.
                """
        if self.HwModel is None:
            logging.error('[pyInterCo.Constraints.Constraints.Satisfy] No HwModel specified for constraint checking.')
            return False
        else:
            FPGA = self.HwModel.GetFPGA(FullId=False)
            if FPGA not in Module.CompatibleFPGAs():
                if 'ALL' in Module.CompatibleFPGAs():
                    FPGA = 'ALL'
            else:
                return False
            if self.Throughput is None:
                return True
            print('MaxFreq of module:', Module.MaxFreq)
            F = Module.GetMaxFreq(FPGA=FPGA)
            DII = Module.GetDataIntroductionInterval()
            print('Freq is', F)
            print('DII is', DII)
            print('Throughput is', F * DII)
            input()
            if F * DII < self.Throughput:
                return False
            return True

    def Copy(self):
        """
                Return object with same attributes.
                """
        Copy = Constraints(Throughput=self.Throughput, HwModel=self.HwModel)
        return Copy

    def __repr__(self):
        """
                Return string representation.
                """
        return 'pyInterCo.Constraints(Throughput={Throughput}, HwModel={HwModel}, AddCommunication={AddCommunication})'.format(Throughput=repr(self.Throughput), HwModel=repr(self.HwModel), AddCommunication=repr(self.AddCommunication))

    def __str__(self):
        """
                Return string representation.
                """
        return str(self.HwModel)