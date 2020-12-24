# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/demos/scripts/trivial.py
# Compiled at: 2015-12-11 19:53:07
try:
    import pandas
except:
    pass

from psychopy import visual
from psychopy_ext import exp
try:
    from collections import OrderedDict
except:
    from exp import OrderedDict

import computer
PATHS = exp.set_paths('trivial', computer)

class Exp1(exp.Experiment):
    """
    Instructions (in reST format)
    =============================

    **Hit 'j'** to advance to the next trial, *Left-Shift + Esc* to exit.
    """

    def __init__(self, name='exp', info=OrderedDict([('subjid', 'quick_'),
 ('session', 1)]), rp=None, actions='run'):
        super(Exp1, self).__init__(name=name, info=info, rp=rp, actions=actions, paths=PATHS, computer=computer)
        self.ntrials = 8
        self.stimsize = 2

    def create_stimuli(self):
        """Define your stimuli here, store them in self.s
        """
        self.create_fixation()
        self.s = {}
        self.s['fix'] = self.fixation
        self.s['stim'] = visual.GratingStim(self.win, mask='gauss', size=self.stimsize)

    def create_trial(self):
        """Define trial composition
        """
        self.trial = [
         exp.Event(self, dur=0.2, display=[
          self.s['stim'], self.s['fix']], func=self.idle_event),
         exp.Event(self, dur=0, display=self.s['fix'], func=self.wait_until_response)]

    def create_exp_plan(self):
        """Put together trials
        """
        exp_plan = []
        for trialno in range(self.ntrials):
            exp_plan.append(OrderedDict([
             (
              'trialno', trialno),
             ('onset', ''),
             ('dur', ''),
             ('corr_resp', 1),
             ('subj_resp', ''),
             ('accuracy', ''),
             ('rt', '')]))

        self.exp_plan = exp_plan