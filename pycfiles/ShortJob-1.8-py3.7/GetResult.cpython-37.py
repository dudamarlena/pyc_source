# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ShortJob/GetResult.py
# Compiled at: 2020-04-28 04:53:42
# Size of source mod 2**32: 3556 bytes
from ROOT import TTree, TFile
from array import array

class GetResult:
    __doc__ = '\n    Reqiure ROOT\n    How:\n        The program tries to find any pattern "name value" in the log file\n        For example:\n            alpha 0.321\n        In this case, the "alpha" is assigned to be 0.021.\n            beta 0.01 0.321 +/- 0.001\n        In this case, the "beta" is assigned to be 0.321 +/- 0.001, while\n        0.001 is the uncertainty\n        * Warrn: the new value will overwrite the old one.\n    Example:\n        info = GetResult.("fit.log")\n        fcn = info.FCN()\n        tmpArgValue = info.GetVal("alpha")\n    '

    def __init__(self, log='log0000'):
        self._log = log

    def SetLog(self, log):
        """Set the log file
        Args:
        log(str): the name of log file
        Returns:
          void
        """
        self._log = log

    def FCN(self):
        """obtain the FCN of likelihood fit, FCN = -log(L)
        Args:
          none
        Returns:
          FCN(double): the minimum -log(L)
        """
        for line in open(self._log):
            if 'RooFitResult:' not in line:
                continue
            ll = line.split()
            ii = ll.index('value:')
            return float(ll[(ii + 1)].split(',')[0])

    def GetVal(self, var='sigma'):
        """ get the value of "var" from the log file
        Args:
           var(str): the name of variable
        Returns:
           value(double): the value of `var`
        """
        ll = []
        ll2 = []
        for line in open(self._log):
            if len(line.split()) == 0:
                continue
            if line.split()[0] == var:
                if '+/-' in line:
                    ll = line.split()
            if line.split()[0] == var and len(line.split()) == 2:
                ll2 = line.split()

        if len(ll) != 0:
            ii = ll.index('+/-')
            return float(ll[(ii - 1)])
        if len(ll2) != 0:
            return float(ll2[(-1)])
        return self.FF(var)

    def GetError(self, var='sigma'):
        """ get the value of uncertainty of "var" from the log file
        Args:
           var(str): the name of variable
        Returns:
           value(double): the uncertainty of `var`
        """
        ll = []
        ll2 = []
        for line in open(self._log):
            if len(line.split()) == 0:
                continue
            if line.split()[0] == var:
                if '+/-' in line:
                    ll = line.split()
            if line.split()[0] == var and len(line.split()) == 2:
                ll2 = line.split()

        if len(ll) != 0:
            ii = ll.index('+/-')
            return float(ll[(ii + 1)])
        if len(ll2) != 0:
            return float(ll2[(-1)])
        return self.FF(var)

    def WriteToFile(self, inputval=[], output='out.root'):
        """write a list to root file, the tree name is default as "sig",
         the branch is default as "val"
        Args:
            inputval(list): the input list, all element will convert into
              double
            output(str): the name of root file, the default value is "out.root"
        Returns:
            void
        """
        fout = TFile(output, 'recreate')
        tout = TTree('sig', '')
        val = array('d', [0.0])
        tout.Branch('val', val, 'val/D')
        for i in inputval:
            val[0] = i
            tout.Fill()

        tout.Write()
        fout.Close()