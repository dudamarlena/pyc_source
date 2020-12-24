# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Dropbox\experiments\psychopy_ext\psychopy_ext\demos\scripts\mouse_resp.py
# Compiled at: 2014-01-21 05:00:32
__doc__ = '\nThe configural superiority effect experiment\n\nA full implementation with many option exposed. For a minimal implementation,\nsee minimal.py.\n\nThis demo is part of psychopy_ext library.\n'
import numpy as np
try:
    import pandas
except:
    pass

from psychopy import visual
from psychopy_ext import exp, stats, plot
try:
    from collections import OrderedDict
except:
    from exp import OrderedDict

import computer
PATHS = exp.set_paths(exp_root='mouse_resp', computer=computer)

class Confsup(exp.Experiment):
    """
    The configural superiority effect experiment
    ============================================

    Task
    ----

    Indicate which shape is different by clicking on it!

    Please remember to fixate on the central dot.

    **Please press spacebar to begin.**

    *(Use Left Shift + Esc to exit.)*
    """

    def __init__(self, name='exp', info=OrderedDict([
 ('subjid', 'confsup_')]), rp=OrderedDict([
 (
  'no_output', False),
 (
  'debug', False),
 ('autorun', 0),
 (
  'register', False),
 (
  'push', False)]), actions='run'):
        super(Confsup, self).__init__(name=name, info=info, rp=rp, actions=actions, method='random', computer=computer, paths=PATHS, blockcol='rep')
        self.computer.trigger = 'left-click'
        self.computer.default_keys['trigger'] = self.computer.trigger
        self.computer.valid_responses = {'left-click': 1}
        self.stim_size = 3.0
        self.stim_width = 0.3
        self.stim_dist = 4.0
        self.stim_color = 'black'
        self.nreps = 5
        self.paratable = OrderedDict([
         (
          1, ['parts', 'top left']),
         (
          2, ['parts', 'top right']),
         (
          3, ['parts', 'bottom left']),
         (
          4, ['parts', 'bottom right']),
         (
          5, ['whole', 'top left']),
         (
          6, ['whole', 'top right']),
         (
          7, ['whole', 'bottom left']),
         (
          8, ['whole', 'bottom right'])])
        sh = self.stim_dist
        self.pos = [(-sh, sh),
         (
          sh, sh),
         (
          -sh, -sh),
         (
          sh, -sh)]

    def create_stimuli(self):
        """Define stimuli
        """
        self.create_fixation()
        sh = self.stim_size / 2
        diag45 = exp.ThickShapeStim(self.win, lineColor=self.stim_color, lineWidth=self.stim_width, fillColor=self.stim_color, closeShape=False, vertices=[
         [
          -sh, -sh], [sh, sh]])
        diag135 = exp.ThickShapeStim(self.win, lineColor=self.stim_color, lineWidth=self.stim_width, fillColor=self.stim_color, closeShape=False, vertices=[
         [
          -sh, sh], [sh, -sh]])
        corner = exp.ThickShapeStim(self.win, lineColor=self.stim_color, lineWidth=self.stim_width, fillColor=None, closeShape=False, vertices=[
         [
          -sh, sh], [-sh, -sh], [sh, -sh]])
        self.s = {'fix': self.fixation, 
           'parts': exp.GroupStim(stimuli=diag45, name='parts'), 
           'parts_odd': exp.GroupStim(stimuli=diag135, name='parts_odd'), 
           'whole': exp.GroupStim(stimuli=[corner, diag45], name='whole'), 
           'whole_odd': exp.GroupStim(stimuli=[corner, diag135], name='whole_odd')}
        self.create_respmap()
        return

    def create_respmap(self):
        self.respmap = []
        qbs = (self.stim_dist + self.stim_width / 2) * 1.5
        qverts = [[[-qbs, qbs], [0, qbs], [0, 0], [-qbs, 0]],
         [
          [
           qbs, qbs], [0, qbs], [0, 0], [qbs, 0]],
         [
          [
           -qbs, -qbs], [0, -qbs], [0, 0], [-qbs, 0]],
         [
          [
           qbs, -qbs], [0, -qbs], [0, 0], [qbs, 0]]]
        for qvertno, qvert in enumerate(qverts):
            box = visual.ShapeStim(self.win, name=qvertno, lineColor=None, fillColor=None, vertices=qvert)
            self.respmap.append(box)

        return

    def create_trial(self):
        """Create trial structure
        """
        self.trial = [
         exp.Event(self, dur=0.3, display=self.s['fix'], func=self.idle_event),
         exp.Event(self, dur=0, display=None, func=self.show_stim),
         exp.Event(self, dur=0.3, display=self.s['fix'], func=self.feedback)]
        return

    def create_exp_plan(self):
        """Define each trial's parameters
        """
        exp_plan = []
        for rep in range(self.nreps):
            for cond, (context, posname) in self.paratable.items():
                pos = (cond - 1) % 4
                exp_plan.append(OrderedDict([
                 (
                  'rep', rep),
                 (
                  'cond', cond),
                 (
                  'context', context),
                 (
                  'posname', posname),
                 (
                  'pos', pos),
                 ('onset', ''),
                 ('dur', ''),
                 (
                  'corr_resp', pos),
                 ('subj_resp', ''),
                 ('accuracy', ''),
                 ('rt', '')]))

        self.exp_plan = exp_plan

    def set_autorun(self, exp_plan):

        def rt(mean, trialno):
            add = np.random.normal(mean, scale=0.2) / self.rp['autorun']
            return self.trial[0].dur + add

        invert_resp = exp.invert_dict(self.computer.valid_responses)
        for trialno, trial in enumerate(exp_plan):
            if trial['context'] == 'parts':
                acc = [
                 0.1, 0.1, 0.1, 0.1]
                acc[trial['pos']] = 0.7
                resp = exp.weighted_choice(choices=invert_resp, weights=acc)
                trial['autoresp'] = resp
                trial['autort'] = rt(1.0, trialno)
            elif trial['context'] == 'whole':
                acc = [
                 0.05, 0.05, 0.05, 0.05]
                acc[trial['pos']] = 0.85
                resp = exp.weighted_choice(choices=invert_resp, weights=acc)
                trial['autoresp'] = resp
                trial['autort'] = rt(0.8, trialno)

        return exp_plan

    def show_stim(self):
        """
        Fully prepare the display but don't flip yet:
            - Determine which context is shown (parts or whole)
            - Set positions of all stimuli.
        This will be invoked at the beginning of each trial for the stimulus
        presentation events (called by :func:`during_trial`).
        #"""
        odd_pos = self.this_trial['pos']
        stim = self.s[self.this_trial['context']]
        for pos in range(4):
            if pos != odd_pos:
                stim.setPos(self.pos[pos])
                stim.draw()

        stim = self.s[(self.this_trial['context'] + '_odd')]
        stim.setPos(self.pos[odd_pos])
        stim.draw()
        self.s['fix'].draw()
        self.win.flip()
        event_keys = self.wait_until_response(draw_stim=False)
        return event_keys


class Analysis(object):

    def __init__(self, name='analysis', info=OrderedDict([('subjid', 'confsup_')]), rp=OrderedDict([('no_output', False),
 (
  'all', False)])):
        self.name = name
        self.info = info
        self.rp = rp
        if self.rp['all']:
            self._set_all_subj()
        self.exp = exp.Experiment(info=self.info, rp=self.rp)

    def _set_all_subj(self):
        self.info['subjid'] = [ 'subj_%02d' % i for i in range(1, 9) ]

    def run(self):
        pattern = PATHS['data'] + '%s.csv'
        df = self.exp.get_behav_df(pattern=pattern)
        agg_acc = stats.accuracy(df, cols='context', values='accuracy', yerr='subjid', order='sorted')
        agg_rt = stats.aggregate(df[(df.accuracy == 'correct')], cols='context', values='rt', yerr='subjid', order='sorted')
        plt = plot.Plot(ncols=2)
        if len(df.subjid.unique()) == 1:
            kind = 'bar'
        else:
            kind = 'bean'
        plt.plot(agg_acc, kind=kind, title='accuracy', ylabel='% correct')
        plt.plot(agg_rt, kind=kind, title='response time', ylabel='seconds')
        print agg_acc
        print agg_rt
        plt.show()