# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mindhive/dicarlolab/u/qbilius/libs/psychopy_ext/psychopy_ext/tests/test_exp.py
# Compiled at: 2015-12-11 19:53:10
import numpy as np
from psychopy import visual, monitors
from .. import exp
import unittest
try:
    from collections import OrderedDict
except:
    from exp import OrderedDict

exp.default_computer.recognized = True
PATHS = exp.set_paths('', exp.default_computer)

class TestExp(unittest.TestCase):

    def test_setpaths(self):
        exp.set_paths('', exp.default_computer)
        exp.set_paths()

    def test_exp(self):
        thisexp = MyExp(rp={'no_output': True, 'debug': True, 'unittest': True})
        with self.assertRaises(SystemExit):
            thisexp.run()

    def test_ThickShapeStim(self):
        monitor = monitors.Monitor('test', distance=57, width=37)
        monitor.setSizePix((1028, 768))
        win = visual.Window([128, 128], monitor=monitor)
        line = exp.ThickShapeStim(win)
        line.draw()
        line.setOri(10)
        line.setPos((10, 10))
        line.setVertices(value=[(-0.5, 0), (0, 0.5), (0.5, 0), (0.7, 0.9)])
        line.draw()
        win.close()

    def test_GroupStim(self):
        win = visual.Window([128, 128])
        line1 = visual.ShapeStim(win)
        line2 = visual.ShapeStim(win)
        group1 = exp.GroupStim(stimuli=line1, name='group1')
        group2 = exp.GroupStim(stimuli=[line1, line2])
        group1.draw()
        group1.setPos((10, 8))
        group2.setOri(10)
        group1.draw()
        group2.draw()
        win.close()

    def test_invert_dict(self):
        d = {1: 2, -3: 4, 0: 'a'}
        invd = exp.invert_dict(d)
        self.assertEqual(invd, OrderedDict([(2, 1), (4, -3), ('a', 0)]))

    def test_other(self):
        self.assertEqual(exp.signal_det('5', '5'), 'correct')
        exp.get_mon_sizes()


class MyExp(exp.Experiment):
    """
    Test experiment.
    """

    def __init__(self, name='exp', **kwargs):
        super(MyExp, self).__init__(name=name, paths=PATHS, computer=exp.default_computer, **kwargs)
        self.computer.valid_responses = {'1': 0, 'd': 1}

    def create_stimuli(self):
        """Define stimuli
        """
        self.create_fixation()
        stim1 = visual.ShapeStim(self.win)
        stim2 = visual.ShapeStim(self.win)
        self.s = {'fix': self.fixation, 
           'stim1': stim1, 
           'both': exp.GroupStim(stimuli=[stim1, stim2], name='both')}

    def create_trial(self):
        """Create trial structure
        """
        self.trial = [
         exp.Event(self, dur=0.3, display=self.s['fix'], func=self.idle_event),
         exp.Event(self, dur=0, display=[
          self.s['stim1'], self.s['both']], func=self.wait_until_response),
         exp.Event(self, dur=0.3, display=self.s['fix'], func=self.feedback)]

    def create_exp_plan(self):
        """Define each trial's parameters
        """
        exp_plan = []
        for cond in range(8):
            exp_plan.append(OrderedDict([
             (
              'cond', cond),
             ('onset', ''),
             ('dur', ''),
             ('corr_resp', 1),
             ('subj_resp', ''),
             ('accuracy', ''),
             ('rt', '')]))

        self.exp_plan = exp_plan


if __name__ == '__main__':
    unittest.main()