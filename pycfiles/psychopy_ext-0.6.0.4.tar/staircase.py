# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/demos/scripts/staircase.py
# Compiled at: 2015-12-11 19:53:07
"""
An basic staircase example. Compare it to the _Test class in `twotasks.py`
to see the differences from the "regular" (non-adaptive) approach.

This demo is part of psychopy_ext library.
"""
import sys, cPickle as pickle
from psychopy import core, visual, data, event
import numpy as np
try:
    import pandas
except:
    pass

from psychopy_ext import exp, ui, stats, plot
try:
    from collections import OrderedDict
except:
    from exp import OrderedDict

import computer
PATHS = exp.set_paths('staircase', computer)

class Staircase(exp.Experiment):
    """
    A perceptual learning experiment
    ================================

    Your task
    ---------

    **Fixate** on the central fixation spot. Two stimuli will briefly flash.
    If they appear to be the same, **hit 'f'**.
    If they appear to be different, **hit 'j'**.
    Please remember to fixate throughout the experiment!

    **Press spacebar to begin.**

    *(Use 'Left Shift + Esc' to exit.)*
    """

    def __init__(self, name='exp', info=('subjid', 'staircase_'), actions='run', **kwargs):
        super(Staircase, self).__init__(name=name, info=info, actions=actions, paths=PATHS, computer=computer, method='random', **kwargs)
        self.oris = {'attended': 60, 'unattended': 150}
        self.stim_size = 3.0
        self.stim_dist = 4.0
        self.ntrials = 30
        self.convergeto = {'attended': 4, 'unattended': 7}
        self.computer.valid_responses = {'f': 'left', 'j': 'right'}

    def create_stimuli(self):
        self.create_fixation()
        stim1 = visual.GratingStim(self.win, name='stim1', mask='circle', sf=2, size=self.stim_size)
        stim2 = visual.GratingStim(self.win, name='stim2', mask='circle', sf=2, size=self.stim_size)
        self.s = {'fix': self.fixation, 'stim1': stim1, 'stim2': stim2}

    def create_trial(self):
        """Create trial structure
        """
        self.trial = [
         exp.Event(self, dur=0.2, display=self.s['fix'], func=self.idle_event),
         exp.Event(self, dur=0.3, display=[
          self.s['fix'], self.s['stim1']], func=self.show_stim),
         exp.Event(self, dur=0.6, display=self.s['fix'], func=self.idle_event),
         exp.Event(self, dur=0.3, display=[
          self.s['fix'], self.s['stim2']], func=self.show_stim),
         exp.Event(self, dur=0, display=self.s['fix'], func=self.wait_until_response)]

    def create_exp_plan(self):
        self.exp_plan = []

    def get_blocks(self):
        blocks = []
        for name in self.oris.keys():
            blocks.append(data.QuestHandler(15, 3, pThreshold=0.63, nTrials=self.ntrials, minVal=0, maxVal=25, name=name))

        self.blocks = blocks

    def __iter__(self):
        """We need this for loop_trials
        """
        return self

    def next(self):
        """Define each trial's parameters
        """
        this_intensity = self.staircase.next()
        self.thisTrialN = self.staircase.thisTrialN
        if np.random.rand() < 0.5:
            corr_resp = 'left'
            ori_dir = -1
        else:
            corr_resp = 'right'
            ori_dir = 1
        this_trial = [
         (
          'trialno', self.thisTrialN),
         (
          'pos', self.staircase.name),
         (
          'dir', ori_dir),
         (
          'oridiff', this_intensity),
         ('onset', ''),
         ('dur', ''),
         (
          'corr_resp', corr_resp),
         ('subj_resp', ''),
         ('accuracy', ''),
         ('rt', '')]
        if self.rp['autorun'] > 0:
            auto = self.get_autorun_vals(self.staircase.name, this_intensity, corr_resp)
            this_trial.extend(auto)
        self.this_trial = OrderedDict(this_trial)
        self.exp_plan.append(self.this_trial)
        return self.this_trial

    def show_stim(self):
        if self.this_trial['pos'] == 'attended':
            pos = (
             -self.stim_dist, 0)
        else:
            pos = (
             self.stim_dist, 0)
        for stim in self.this_event.display:
            if stim.name == 'stim1':
                stim.setPos(pos)
                stim.setOri(self.oris[self.this_trial['pos']])
            if stim.name == 'stim2':
                stim.setPos(pos)
                stim.setOri(self.oris[self.this_trial['pos']] + self.this_trial['dir'] * self.this_trial['oridiff'])
            stim.draw()

        self.win.flip()
        self.idle_event(draw_stim=False)

    def get_autorun_vals(self, pos, this_intensity, corr_resp):
        """If autorun, simulate user responses
        """

        def rt(mean):
            add = np.random.normal(mean, scale=0.2) / self.rp['autorun']
            return trial_dur + add

        invert_resp = exp.invert_dict(self.computer.valid_responses)
        trial_dur = sum([ ev.dur for ev in self.trial ])
        thres = np.random.normal(self.convergeto[pos], scale=1)
        thres = max(0, thres)
        invert = {'right': 'left', 'left': 'right'}
        if this_intensity < thres:
            fake_resp = invert[corr_resp]
        else:
            fake_resp = corr_resp
        auto = [('autoresp', invert_resp[fake_resp]),
         (
          'autort', rt(0.5))]
        return auto

    def post_trial(self):
        this_resp = self.all_keys.pop()
        self.this_trial['subj_resp'] = self.computer.valid_responses[this_resp[0]]
        acc = exp.signal_det(self.this_trial['corr_resp'], self.this_trial['subj_resp'])
        self.this_trial['accuracy'] = acc
        self.this_trial['rt'] = this_resp[1]
        if acc == 'correct':
            acc_int = 1
        else:
            acc_int = 0
        self.staircase.addData(acc_int)
        return self.this_trial

    def run_task(self):
        self.setup_task()
        self.before_task()
        if not self.rp['no_output']:
            print 'Data will be saved in %s' % self.datafile.filename
        self.datafile.open()
        for blockno, block in enumerate(self.blocks):
            self.staircase = block
            self.this_blockn = blockno
            self.set_TrialHandler(self.exp_plan)
            self.run_block()

        self.datafile.close()
        self.after_task()


class Analysis(object):

    def __init__(self, name='analysis', info={'subjid': 'staircase_'}, rp={'all': False}):
        self.name = name
        self.info = info
        self.rp = rp
        self.paths = PATHS
        if self.rp['all']:
            self._set_all_subj()

    def _set_all_subj(self):
        self.info['subjid'] = [ 'staircase_%02d' % i for i in range(1, 11) ]

    def _get_staircase(self):
        pattern = self.paths['data'] + '%s.csv'
        df = exp.get_behav_df(subjid=self.info['subjid'], pattern=pattern)
        df_thres_all = []
        df['thres'] = 0.0
        for subj in np.unique(df.subjid):
            subjdf = df[(df.subjid == subj)]
            for pos in subjdf.pos.unique():
                posdf = subjdf[(subjdf.pos == pos)]
                st_mod = Staircase()
                st_mod.get_blocks()
                exps = dict((st.name, st) for st in st_mod.blocks)
                exps[pos].importData(posdf.oridiff.astype(float), np.array(posdf.corr_resp == posdf.subj_resp))
                posdf.thres = exps[pos].mean()
                df_thres_all.append(posdf)

        df_thres = pandas.concat(df_thres_all)
        return df_thres

    def thresholds(self):
        df = self._get_staircase()
        agg_thres = stats.aggregate(df, values='thres', cols='pos', yerr='subjid')
        plt = plot.Plot()
        plt.plot(agg_thres, kind='bar', title='orientation thresholds', ylabel='orientation threshold, deg')
        print agg_thres.mean()
        plt.show()
        return agg_thres

    def run(self):
        df = self._get_staircase()
        agg_thres = stats.aggregate(df, values='thres', rows='pos', unstack=True)
        agg = stats.aggregate(df, values='oridiff', rows='trialno', cols='pos')
        plt = plot.Plot()
        ax = plt.plot(agg, kind='line', ylabel='step')
        num_trials = len(agg.columns.levels[1])
        thres = agg_thres.mean(1).values[0]
        ax.axhline(y=thres, color='.2', ls='--', lw=2, marker='None')
        print agg_thres
        ax.text(num_trials - num_trials / 3.0, thres + 0.5, 'average threshold = %.2f' % thres, fontsize=8)
        plt.show()
        return agg_thres