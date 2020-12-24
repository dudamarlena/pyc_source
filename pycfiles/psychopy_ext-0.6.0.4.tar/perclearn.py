# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/demos/scripts/perclearn.py
# Compiled at: 2015-12-11 19:53:07
"""
A perceptual learning experiment
================================

This demo combined twotasks.py and staircase.py into a single quite
complex experiment.

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
PATHS = exp.set_paths('perclearn', computer)

class PercLearn(exp.Experiment):
    """
    A perceptual learning experiment
    ================================

    This experiment is composed of **four parts**. Each part consists of
    **training** for 1 min (for presentation purposes only) and
    **testing** for 5 min.

    **Press spacebar to continue.**

    *(Use 'Left Shift + Esc' to exit.)*
    """

    def __init__(self, name='exp', info=('subjid', 'perclearn_'), rp=OrderedDict([
 (
  'phase', ('both', 'train', 'test')),
 (
  'kind', ('2AFC', 'QUEST')),
 (
  'practice', False)])):
        super(PercLearn, self).__init__(name=name, info=info, rp=rp, actions='run', paths=PATHS, computer=computer)
        if self.rp['practice']:
            self.rp['no_output'] = True
        self.nsessions = 3
        if self.rp['kind'] == '2AFC':
            self.tasks = [
             _Train, _Test2AFC]
        else:
            self.tasks = [
             _Train, _TestQuest]
        self.oris = {'attended': 60, 'unattended': 150}
        self.stim_size = 3.0
        self.stim_dist = 4.0

    def run(self):
        self.setup()
        self.before_exp()
        for expno in range(self.nsessions):
            self.show_text('Session %d' % (expno + 1), auto=1)
            if self.rp['phase'] in ('train', 'both'):
                self.tasks[0](self, session=expno + 1).run_task()
            if self.rp['phase'] in ('test', 'both'):
                self.tasks[1](self, session=expno + 1).run_task()
            pause_instr = 'End of session %d.\nWhen ready, press spacebar to continue.' % (expno + 1)
            if expno != self.nsessions - 1:
                self.show_text(pause_instr)

        self.after_exp()
        self.repo_action()
        self.quit()


class _Train(exp.Task):
    """
    Training
    ========

    Your task
    ---------

    **Fixate** on the central fixation spot.
    Attend to stimulus on the **left**.
    When you notice a decrease in its contrast, **press 'j'**.
    Please remember to fixate throughout the experiment.

    **Press spacebar to begin.**

    *(Use 'Left Shift + Esc' to exit.)*
    """

    def __init__(self, parent, session=1):
        data_fname = parent.paths['data'] + parent.info['subjid'] + '_train.csv'
        super(_Train, self).__init__(parent, method='random', data_fname=data_fname)
        self.session = session
        self.computer.valid_responses = {'j': 1}
        self.oris = parent.oris
        self.stim_size = parent.stim_size
        self.stim_dist = parent.stim_dist
        self.ntrials = 75
        self.nblocks = 2
        self.task_rate = 0.1
        self.low_contrast = 0.5
        self.anl = Analysis(info=self.parent.info)

    def create_stimuli(self):
        self.create_fixation()
        self.s = {'fix': self.fixation}
        self.s['attended'] = visual.GratingStim(self.win, name='attended', mask='circle', sf=2, size=self.stim_size, pos=(
         -self.stim_dist, 0), ori=self.oris['attended'])
        self.s['unattended'] = visual.GratingStim(self.win, name='unattended', mask='circle', sf=2, size=self.stim_size, pos=(
         self.stim_dist, 0), ori=self.oris['unattended'])

    def create_trial(self):
        """Create trial structure
        """
        allstim = [
         self.s['fix'], self.s['attended'], self.s['unattended']]
        self.trial = [
         exp.Event(self, dur=0.2, display=allstim, func=self.show_stim),
         exp.Event(self, dur=0.2, display=self.s['fix'], func=self.idle_event)]

    def create_exp_plan(self):
        """Define each trial's parameters
        """
        exp_plan = []
        for block in range(self.nblocks):
            for trial in range(self.ntrials):
                if trial < self.ntrials * self.task_rate:
                    cond = 'low'
                    corr_resp = 1
                else:
                    cond = 'high'
                    corr_resp = ''
                exp_plan.append(OrderedDict([
                 (
                  'session', self.session),
                 (
                  'block', block),
                 (
                  'cond', cond),
                 ('onset', ''),
                 ('dur', ''),
                 (
                  'corr_resp', corr_resp),
                 ('subj_resp', ''),
                 ('rt', '')]))

        self.exp_plan = exp_plan

    def set_autorun(self, exp_plan):

        def rt(mean):
            add = np.random.normal(mean, scale=0.2) / self.rp['autorun']
            return self.trial[0].dur + add

        for trial in exp_plan:
            trial['autort'] = ''
            trial['autoresp'] = ''
            if trial['corr_resp'] == 1:
                acc = [
                 0.1, 0.9]
                resp_ind = exp.weighted_choice(weights=acc)
                if resp_ind == 1:
                    trial['autort'] = rt(0.8)
                    trial['autoresp'] = 1

        return exp_plan

    def get_auto_resp(self, trial):
        """
        In case of autorun, simulates user responses.

        This is very complicated but the idea is to simulate responses
        around the time the stimulus was presented.
        """
        resp_win = 5
        start = max(0, self.thisTrialN - resp_win + 1)
        end = self.thisTrialN + 1
        resp = ''
        rt = ''
        for i, idx in enumerate(self.sequenceIndices[start:end]):
            tr = self.trialList[idx[0]]
            if tr['autort'] != '':
                trial_dur = sum([ ev.dur for ev in self.trial ])
                if i != end - start - 1:
                    trial_dur *= self.rp['autorun']
                offset = int(np.floor(tr['autort'] / trial_dur)) + 1
                if offset == end - start - i:
                    rt = tr['autort'] % trial_dur
                    if i != end - start - 1:
                        rt /= self.rp['autorun']
                    try:
                        resp += 1
                    except:
                        resp = 1

        return (
         resp, rt)

    def show_stim(self):
        if self.this_trial['cond'] == 'low':
            contrast = self.low_contrast
        else:
            contrast = 1
        for stim in self.this_event.display:
            if stim.name == 'attended':
                stim.setContrast(contrast)
            stim.draw()

        self.win.flip()
        event_keys = self.idle_event(draw_stim=False)
        return event_keys

    def post_trial(self):
        """ What to do after a trial is over.
        """
        if self.rp['autorun'] > 0:
            all_keys = [
             self.get_auto_resp(self.this_trial)]
        else:
            all_keys = self.all_keys
        if len(all_keys) > 0:
            if all_keys[0][0] != '':
                self.this_trial['subj_resp'] = len(all_keys)
            else:
                self.this_trial['subj_resp'] = ''
            self.this_trial['rt'] = all_keys[(-1)][1]
        else:
            self.this_trial['subj_resp'] = ''
            self.this_trial['rt'] = ''
        return self.this_trial

    def before_task(self):
        """We slightly redefine the default function so that full
        instructions are shown the first time round.
        """
        if self.session == 1:
            super(_Train, self).before_task()
        else:
            text = "\n            Training, session %d\n            --------------------\n\n            (decrease in its contrast: **press 'j'**)\n            "
            super(_Train, self).before_task(text=text % self.session)

    def after_task(self):
        acc = self.anl.train_feedback(self.session)
        pause_instr = 'Your accuracy is %d%%.' % (100 * acc)
        super(_Train, self).after_task(text=pause_instr)


class _BaseTest(exp.Task):
    """
    Testing
    =======

    Your task
    ---------

    **Fixate** on the central fixation spot. Two stimuli will briefly flash.
    If they appear to be the **same, hit 'f'**.
    If they appear to be **different, hit 'j'**.
    Please remember to fixate throughout the experiment!

    **Press spacebar to begin.**

    *(Use 'Left Shift + Esc' to exit.)*
    """

    def __init__(self, parent, session=1):
        data_fname = parent.paths['data'] + parent.info['subjid'] + '_test.csv'
        super(_BaseTest, self).__init__(parent, method='random', data_fname=data_fname)
        self.session = session
        self.oris = parent.oris
        self.stim_size = parent.stim_size
        self.stim_dist = parent.stim_dist
        self.computer.valid_responses = {'f': 'same', 'j': 'diff'}

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
        if self.rp['practice']:
            self.trial.append(exp.Event(self, dur=0.2, display=self.s['fix'], func=self.feedback))

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

    def before_task(self):
        """We slightly redefine the default function so that full
        instructions are shown the first time round.
        """
        if self.session == 1:
            super(_BaseTest, self).before_task(text=_BaseTest.__doc__)
        else:
            text = "\n            Testing, session %d\n            -------------------\n\n            (same stimuli: **hit 'f'**, different stimuli: **hit 'j'**)\n            "
            super(_BaseTest, self).before_task(text=text % self.session)


class _TestQuest(_BaseTest):

    def __init__(self, *args, **kwargs):
        """
        Runs a QUEST procedure.
        """
        super(_TestQuest, self).__init__(*args, **kwargs)
        self.ntrials_diff = 30
        self.ntrials_same = 5
        self.convergeto = {'attended': 4, 'unattended': 7}

    def __iter__(self):
        """We need this for loop_trials
        """
        return self

    def next(self):
        """Define each trial's parameters
        """
        if np.random.rand() < 0.5:
            ori_dir = -1
        else:
            ori_dir = 1
        prop = self.ntrials_same / float(self.ntrials_diff + self.ntrials_same)
        if np.random.rand() < prop and self.count_same < self.ntrials_same:
            this_intensity = 0
            corr_resp = 'same'
            self.count_same += 1
            trialno = self.count_same
        else:
            self.staircase._checkFinished()
            if self.staircase.finished == False:
                this_intensity = self.staircase.next()
                self.thisTrialN += 1
                corr_resp = 'diff'
                self.count_diff += 1
                trialno = self.count_diff
            elif self.count_same < self.ntrials_same:
                this_intensity = 0
                corr_resp = 'same'
                self.count_same += 1
                trialno = self.count_same
            else:
                self.staircase._terminate()
        this_trial = [
         (
          'session', self.session),
         (
          'trialno', trialno),
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

    def get_autorun_vals(self, posno, this_intensity, corr_resp):
        """If autorun, simulate user responses
        """

        def rt(mean):
            add = np.random.normal(mean, scale=0.2) / self.rp['autorun']
            return trial_dur + add

        invert_resp = exp.invert_dict(self.computer.valid_responses)
        trial_dur = sum([ ev.dur for ev in self.trial ])
        if corr_resp == 'same':
            fake_resp = 'same'
        else:
            thres = np.random.normal(self.convergeto[posno], scale=1)
            thres = max(0, thres)
            if this_intensity < thres:
                fake_resp = 'same'
            else:
                fake_resp = 'diff'
        auto = [
         (
          'autoresp', invert_resp[fake_resp]),
         (
          'autort', rt(0.5))]
        return auto

    def create_exp_plan(self):
        self.exp_plan = []

    def get_blocks(self):
        blocks = []
        for name in self.oris.keys():
            blocks.append(data.QuestHandler(15, 3, pThreshold=0.63, nTrials=self.ntrials_diff, minVal=0, maxVal=25, name=name))

        self.blocks = blocks

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
        if self.this_trial['corr_resp'] == 'diff':
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
            self.count_diff = 0
            self.count_same = 0
            self.set_TrialHandler(self.exp_plan)
            self.run_block()

        self.datafile.close()
        self.after_task()


class _Test2AFC(_BaseTest):

    def __init__(self, *args, **kwargs):
        super(_Test2AFC, self).__init__(*args, **kwargs)
        self.blockcol = 'pos'
        self.ntrials = 32
        self.oridiff = 13
        self.anl = Analysis(info=self.parent.info)

    def create_exp_plan(self):
        exp_plan = []
        for name in self.oris.keys():
            for ori_dir in [-1, 1]:
                for trial in range(self.ntrials / 2):
                    if trial < self.ntrials / 4:
                        corr_resp = 'same'
                        oridiff = 0
                    else:
                        corr_resp = 'diff'
                        oridiff = self.oridiff
                    exp_plan.append(OrderedDict([
                     (
                      'session', self.session),
                     (
                      'pos', name),
                     (
                      'dir', ori_dir),
                     (
                      'oridiff', oridiff),
                     ('onset', ''),
                     ('dur', ''),
                     (
                      'corr_resp', corr_resp),
                     ('subj_resp', ''),
                     ('accuracy', ''),
                     ('rt', '')]))

        self.exp_plan = exp_plan

    def set_autorun(self, exp_plan):

        def rt(mean):
            add = np.random.normal(mean, scale=0.2) / self.rp['autorun']
            return trial_dur + add

        invert_resp = exp.invert_dict(self.computer.valid_responses)
        trial_dur = sum([ ev.dur for ev in self.trial ])
        for trial in exp_plan:
            if trial['pos'] == 'attended':
                acc = 0.9
            elif trial['pos'] == 'unattended':
                acc = 0.6
            if trial['corr_resp'] == 'same':
                resp_ind = exp.weighted_choice(choices=invert_resp.keys(), weights=[
                 1 - acc, acc])
            else:
                resp_ind = exp.weighted_choice(choices=invert_resp.keys(), weights=[
                 acc, 1 - acc])
            trial['autoresp'] = invert_resp[resp_ind]
            trial['autort'] = rt(0.8)

        return exp_plan

    def after_task(self):
        acc = self.anl.test_feedback(self.exp_plan)
        pause_instr = 'Your accuracy is %d%%.' % acc
        super(_Test2AFC, self).after_task(text=pause_instr)


class Analysis(object):

    def __init__(self, name='analysis', info={'subjid': 'perclearn_'}, rp=OrderedDict([('no_output', False),
 (
  'plot', True),
 (
  'saveplot', False),
 (
  'all', False)])):
        self.name = name
        self.info = info
        self.rp = rp
        self.paths = PATHS
        if self.rp['all']:
            self._set_all_subj()

    def _set_all_subj(self):
        self.info['subjid'] = [ 'perclearn_%02d' % i for i in range(1, 11) ]

    def plot(self, agg):
        plt = plot.Plot()
        plt.plot(agg)
        if self.rp['plot']:
            plt.show()
        else:
            print agg

    def _train_acc(self, df):
        resp_win = 5
        resp = df.subj_resp.copy()
        resp[resp.isnull()] = 0
        resp = np.array(resp)
        resp[resp == ''] = 0
        count = 0
        for i in range(resp_win):
            roll = np.roll(resp, -i)
            roll[(len(roll) - i):] = 0
            count += roll

        df['count'] = count
        df['accuracy'] = ''
        for idx, row in df.iterrows():
            if row['count'] >= 1:
                subj_resp = 1
            else:
                subj_resp = ''
            if row['corr_resp'] == '' or pandas.isnull(row['corr_resp']):
                corr_resp = ''
            else:
                corr_resp = row['corr_resp']
            acc = exp.signal_det(corr_resp, subj_resp)
            if acc == 'false alarm':
                acc = ''
            df.loc[(idx, 'accuracy')] = acc

        return df

    def train(self):
        pattern = self.paths['data'] + '%s_train.csv'
        df = exp.get_behav_df(self.info['subjid'], pattern=pattern)
        dfs = []
        for session in df.session.unique():
            sdf = df[(df.session == session)]
            dfs.append(self._train_acc(sdf))

        df = pandas.concat(dfs)
        agg_acc = stats.accuracy(df, cols='session', values='accuracy', yerr='subjid', incorrect='miss')
        self.plot(agg_acc)

    def train_feedback(self, session):
        pattern = self.paths['data'] + '%s_train.csv'
        try:
            df = exp.get_behav_df(self.info['subjid'], pattern=pattern)
        except:
            return 0

        df = df[(df.session == session)]
        df = self._train_acc(df)
        cor = np.sum(df.accuracy == 'correct')
        acc = float(cor) / (np.sum(df.accuracy == 'miss') + cor)
        return acc

    def test_feedback(self, trial_list):
        """Provides feedback during the test phase (2AFC task)
        """
        df = pandas.DataFrame(trial_list)
        acc = float(np.sum(df.accuracy == 'correct'))
        acc /= np.sum(df.accuracy == 'correct') + np.sum(df.accuracy == 'incorrect')
        return acc * 100

    def test(self):
        """Analysis of the test phase data (for 2AFC task)
        """
        pattern = self.paths['data'] + '%s_test.csv'
        df = exp.get_behav_df(self.info['subjid'], pattern=pattern)
        agg_acc = stats.accuracy(df, rows='session', cols='pos', values='accuracy', yerr='subjid')
        plt = plot.Plot()
        plt.plot(agg_acc)
        plt.show()

    def _get_staircase(self):
        pattern = self.paths['data'] + '%s_test.csv'
        df = exp.get_behav_df(subjid=self.info['subjid'], pattern=pattern)
        df = df[(df.corr_resp == 'diff')]
        df_thres_all = []
        df['thres'] = 0.0
        gr = PercLearn(info=self.info)
        for subj in np.unique(df.subjid):
            subjdf = df[(df.subjid == subj)]
            for sid in subjdf.session.unique():
                sdf = subjdf[(subjdf.session == sid)]
                for pos in sdf.pos.unique():
                    posdf = sdf[(sdf.pos == pos)]
                    st_mod = _TestQuest(gr)
                    st_mod.get_blocks()
                    exps = dict((st.name, st) for st in st_mod.blocks)
                    exps[pos].importData(posdf.oridiff.astype(float), np.array(posdf.corr_resp == posdf.subj_resp))
                    posdf.thres = exps[pos].mean()
                    df_thres_all.append(posdf)

        df_thres = pandas.concat(df_thres_all)
        return df_thres

    def thresholds(self):
        df = self._get_staircase()
        agg_thres = stats.aggregate(df, values='thres', cols='pos', rows='session', yerr='subjid')
        plt = plot.Plot()
        plt.plot(agg_thres, kind='bar', title='orientation thresholds', ylabel='orientation threshold, deg')
        print agg_thres.mean()
        if self.rp['plot']:
            plt.show()
        return agg_thres

    def staircase(self):
        df = self._get_staircase()
        agg_thres = stats.aggregate(df, values='thres', rows='session', unstack=True)
        agg = stats.aggregate(df, values='oridiff', subplots='session', rows='trialno', cols='pos')
        if self.rp['plot'] or self.rp['saveplot']:
            plt = plot.Plot(nrows=2, ncols=2, sharex=True, sharey=True)
            ax = plt.plot(agg, kind='line', ylabel='step')
            num_trials = len(agg.columns.levels[1])
            for pno, (sno, thres) in enumerate(agg_thres.mean().iteritems()):
                ax = plt.get_ax(pno)
                ax.set_title('session %d' % sno)
                ax.axhline(y=thres, color='.2', ls='--', lw=2, marker='None')
                print thres
                ax.text(num_trials - 15, thres + 0.5, 'average threshold = %.2f' % thres, fontsize=8)

            print agg_thres
            plt.hide_plots(3)
            if self.rp['plot']:
                plt.show()
            if self.rp['saveplot']:
                plt.savefig(PATHS['analysis'] + '%s.svg' % self.info['subjid'])
        return agg_thres