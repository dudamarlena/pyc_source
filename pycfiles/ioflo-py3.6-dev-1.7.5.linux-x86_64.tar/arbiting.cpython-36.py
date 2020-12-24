# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/arbiting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 13995 bytes
"""arbiting.py arbiter deed module

"""
import time, struct
from collections import deque
import inspect
from ..aid.sixing import *
from ..aid.odicting import odict
from . import doing
from ..aid.consoling import getConsole
console = getConsole()

class Arbiter(doing.Doer):
    __doc__ = 'Arbiter Doer Class\n       Generic Arbiter Class for Arbiters should be subclassed\n\n    '

    def __init__(self, output, group, inputs, **kw):
        (super(Arbiter, self).__init__)(**kw)
        self.output = self.store.create(output).create(value=0.0)
        self.output.value = 0.0
        self.output.truth = 0.0
        self.group = group
        self.default = self.store.create(group + '.default').create(value=0.0)
        if not self.GoodTruth(self.default.truth):
            self.default.truth = self.FixTruth(self.default.truth)
        self.insels = self.store.create(group + '.insels')
        self.inimps = self.store.create(group + '.inimps')
        self.inputs = odict()
        for tag, stuff in inputs.items():
            input, sel, imp = stuff
            if tag:
                input = self.store.create(input)
                self.inputs[tag] = input
                (self.insels.create)(**{tag: sel})
                (self.inimps.create)(**{tag: imp})

    def _expose(self):
        """prints out arbiter parameters

        """
        msg = 'Arbiter %s\n' % self.name
        msg += '   group = %s  outval = %s outcnf = %s defval = %s defcnf = %s\n' % (
         self.group, self.output.value, self.output.truth, self.default.value, self.default.truth)
        msg += '   inputs = \n'
        for tag, input in self.inputs.items():
            msg += '      tag = %s, input = %s, sel = %s, imp = %s,\n' % (
             tag, input.name, self.insels.fetch(tag), self.inimps.fetch(tag))
            msg += '      input value = %s input truth = %s\n' % (input.value, input.truth)

        console.terse(msg)

    def update(self):
        """update should be overridden by subclass

        """
        pass

    def action(self, **kw):
        """action is to update arbiter

        """
        console.profuse('Updating arbiter {0}\n'.format(self.name))
        self.update()

    @staticmethod
    def GoodTruth(truth):
        """Check if truth float in range [0.0, 1.0]
           this so only FixTruth when needed for initing default confidence
        """
        if isinstance(truth, float):
            if truth >= 0.0:
                if truth <= 1.0:
                    return True
        return False

    @staticmethod
    def FixTruth(truth):
        """make truth to be float in range [0.0, 1.0]
           if truth is None or Boolean True then make 1.0
           If truth is Boolean False then make 0.0
           otherwise Truth assumed to be number so hard limit to interval [0.0, 1.0]
        """
        if truth is None or truth is True:
            truth = 1.0
        else:
            if truth is False:
                truth = 0.0
            else:
                truth = float(min(1.0, max(0.0, truth)))
        return truth


class ArbiterSwitch(Arbiter):
    __doc__ = 'ArbiterSwitch Arbiter Deed Class\n\n\n    '

    def update(self, stamp=None):
        """update switch arbiter algorithm
           simply switch selected input to output
           ignore importances
           ignore threshold on confidence

           find first input whose:
              selection is logically True
              if found then output's value/truth is found input's value/truth

           otherwise output's value/truth is default's value/truth

        """
        for tag, input in self.inputs.items():
            if self.insels.fetch(tag):
                self.output.value = input.value
                self.output.truth = input.truth
                self.output.stamp = stamp
                return

        self.output.value = self.default.value
        self.output.truth = self.default.truth
        self.output.stamp = stamp


class ArbiterPriority(Arbiter):
    __doc__ = 'ArbiterPriority Arbiter Deed Class\n\n\n    '

    def update(self, stamp=None):
        """update priority arbiter algorithm

           an input is selected if its selection is logically true
           an input is sufficient if its confidence is > default truth
           confidence constrained to range [0.0, 1.0]
           if an input's truth is True or None then use truth = 1.0
           an input is most important if it has maximum importance of all selected sufficient inputs

           find first and most important input

           if found then output's value/truth is found input's value/truth
           else output's value/truth is default's value/truth

        """
        inputmax = None
        impmax = 0.0
        truthmax = 0.0
        for tag, input in self.inputs.items():
            truth = self.FixTruth(input.truth)
            imp = self.inimps.fetch(tag)
            if self.insels.fetch(tag) and truth > self.default.truth and imp > impmax:
                inputmax = input
                impmax = imp
                truthmax = truth

        if inputmax:
            self.output.value = inputmax.value
            self.output.truth = truthmax
            self.output.stamp = stamp
        else:
            self.output.value = self.default.value
            self.output.truth = self.default.truth
            self.output.stamp = stamp


class ArbiterTrusted(Arbiter):
    __doc__ = 'ArbiterTrusted Arbiter Deed Class\n\n\n    '

    def update(self, stamp=None):
        """update trusted arbiter algorithm

           an input is selected if its selection is logically true
           an input is sufficient if its confidence is > default truth
           input's truth confidence constrained to range [0.0, 1.0]
           if an input's truth is True or None then use truth = 1.0
           an input has the highest confidence if its confidence is maximum amoung all
              selected sufficient inputs
           an input is most important if it has maximum importance of all highest confidence inputs

           find first most important input

           if found then output's value/truth is found input's value/truth
           else output's value/truth is default's value/truth

        """
        inputmax = None
        impmax = 0.0
        truthmax = 0.0
        for tag, input in self.inputs.items():
            sel = self.insels.fetch(tag)
            truth = self.FixTruth(input.truth)
            imp = self.inimps.fetch(tag)
            if sel and truth > self.default.truth:
                if truth > truthmax:
                    truthmax = truth
                    impmax = imp
                    inputmax = input
                elif truth == truthmax and imp > imputmax:
                    truthmax = truth
                    impmax = imp
                    inputmax = input

        if inputmax:
            self.output.value = inputmax.value
            self.output.truth = truthmax
            self.output.stamp = stamp
        else:
            self.output.value = self.default.value
            self.output.truth = self.default.truth
            self.output.stamp = stamp


class ArbiterWeighted(Arbiter):
    __doc__ = 'ArbiterWeighted Arbiter Deed Class\n\n\n    '

    def update(self, stamp=None):
        """update weighted arbiter algorithm

           an input is selected if its selection is logically true
           compute normalized weighted average of all selected inputs where average is given by
           weighted conf = Sum(imp * cnf)/Sum(imp)
           weighted value = Sum(imp * cnf * value)/Sum(imp * cnf)

           input truth values are fixed up to be float in range [0.0, 1.0]

           if weighted conf > default truth then
              output's value/truth is found input's value/fixed truth
           else
              output's value/truth is default's value/truth

        """
        wgtval = 0.0
        wgtcnf = 0.0
        wgtimp = 0.0
        try:
            for tag, input in self.inputs.items():
                if self.insels.fetch(tag):
                    truth = self.FixTruth(input.truth)
                    imp = self.inimps.fetch(tag)
                    wgtimp += imp
                    wgtcnf += imp * truth
                    wgtval += imp * truth * input.value

            wgtval = wgtval / float(wgtcnf)
            wgtcnf = wgtcnf / float(wgtimp)
        except TypeError:
            console.terse('     Warning, bad input value for Arbiter {0}\n'.format(self.name))
            self.output.value = self.default.value
            self.output.truth = self.default.truth
            self.output.stamp = stamp
            return
        except ZeroDivisionError:
            self.output.value = self.default.value
            self.output.truth = self.default.truth
            self.output.stamp = stamp
            return
        else:
            if wgtcnf > self.default.truth:
                self.output.value = wgtval
                self.output.truth = wgtcnf
                self.output.stamp = stamp
            else:
                self.output.value = self.default.value
                self.output.truth = self.default.truth
                self.output.stamp = stamp