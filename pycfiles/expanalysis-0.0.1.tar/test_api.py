# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/expfactory/expfactory-analysis/expanalysis/tests/test_api.py
# Compiled at: 2016-04-27 20:31:25
"""
Test analysis functions
"""
from expanalysis.maths import check_numeric
from expanalysis.utils import get_installdir
from expanalysis.results import Result
import pandas, tempfile, unittest, numpy, shutil, json, os, re

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.tmpdir = tempfile.mkdtemp()
        self.jsonfile = os.path.abspath('%s/tests/data/results/results.json' % self.pwd)
        self.result = Result()
        self.result.load_results(self.jsonfile)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_check_numeric(self):
        not_numeric = [
         'hello', 'goodbye']
        numeric_float = [1.1, 2.2, 3.3]
        numeric_int = [1, 2, 3]
        not_numeric_mixed = ['hello', 2, 3.0]
        self.assertTrue(check_numeric(numeric_float))
        self.assertTrue(check_numeric(numeric_int))
        self.assertTrue(check_numeric(not_numeric) == False)
        self.assertTrue(check_numeric(not_numeric_mixed) == False)

    def test_filter(self):
        filtered = self.result.filter(field='experiment_exp_id', value='bucket_game')
        self.assertTrue(filtered.shape[0] == 17)
        self.assertTrue(len(numpy.unique(filtered['experiment_exp_id'])) == 1)

    def test_load(self):
        print 'TESTING: load data'
        result = Result()
        data = result.load_results(self.jsonfile)
        self.assertTrue(isinstance(data, pandas.DataFrame))
        self.assertTrue(data.shape[0] == 864)
        self.assertTrue(data.shape[1] == 13)

    def test_experiment_extract(self):
        print 'TESTING: experiment extraction'
        experiment = self.result.extract_experiment(exp_id='stroop')
        experiment_columns = ['block_duration', 'condition', 'correct', 'correct_response',
         'current_trial', 'dateTime', 'feedback_duration',
         'internal_node_id', 'key_press', 'possible_responses', 'responses',
         'rt', 'stim_color', 'stim_duration', 'stim_word', 'stimulus',
         'time_elapsed', 'timing_post_trial', 'trial_id', 'trial_index',
         'trial_type', 'trialdata', 'uniqueid', 'view_history']
        self.assertTrue(isinstance(experiment, pandas.DataFrame))
        self.assertTrue(experiment.shape[0] == 747)
        [ self.assertTrue(x) in experiment.columns for x in experiment_columns ]

    def test_survey_extract(self):
        print 'TESTING: survey extraction'
        survey = self.result.extract_experiment(exp_id='bis11_survey')
        self.assertTrue(isinstance(survey, pandas.DataFrame))

    def test_game_extract(self):
        print 'TESTING: game extraction'
        game = self.result.extract_experiment(exp_id='bridge_game')
        game_columns = ['current_trial', 'uniqueid', 'dateTime', 'ACC', 'RT', 'solution',
         'problem_id', 'trial', 'finished', 'points', 'answer', 'n1',
         'n2', 'problem']
        self.assertTrue(isinstance(game, pandas.DataFrame))
        self.assertTrue(game.shape[0] == 301)
        [ self.assertTrue(x) in game.columns for x in game_columns ]


if __name__ == '__main__':
    unittest.main()