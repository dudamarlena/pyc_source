# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/tests/test_stats.py
# Compiled at: 2016-03-14 08:48:09
import numpy as np, pandas
from .. import stats, plot
import unittest
N = 8
NSAMPL = 10

class TestAgg(unittest.TestCase):

    def get_df(self, n=N, nsampl=NSAMPL):
        k = n * nsampl
        df = stats.df_fromdict([
         (
          'subplots', ['session1', 'session2']),
         (
          'cond', [1, 2]),
         (
          'name', ['one', 'two', 'three']),
         (
          'levels', ['small', 'medium', 'large']),
         (
          'subjID', [ 'subj%d' % (i + 1) for i in range(8) ])], repeat=10)
        df['rt'] = range(k) * 36
        df['accuracy'] = ['correct', 'correct', 'incorrect', 'incorrect'] * k * 9
        return df

    def test_df_fromdict(self):
        n = 8
        nsampl = 10
        df = self.get_df(n=n, nsampl=nsampl)
        k = n * nsampl
        data = {'subplots': [
                      'session1'] * k * 18 + ['session2'] * k * 18, 
           'cond': [
                  1] * k * 9 + [2] * k * 9 + [1] * k * 9 + [2] * k * 9, 
           'name': ([
                  'one', 'one', 'one'] * k + ['two', 'two', 'two'] * k + [
                  'three', 'three', 'three'] * k) * 4, 
           'levels': ([
                    'small'] * k + ['medium'] * k + ['large'] * k) * 12, 
           'subjID': [ 'subj%d' % (i + 1) for i in np.repeat(range(n), nsampl) ] * 36, 'rt': range(k) * 36, 
           'accuracy': [
                      'correct', 'correct', 'incorrect', 'incorrect'] * k * 9}
        df_manual = pandas.DataFrame(data, columns=['subplots', 'cond', 'name',
         'levels', 'subjID', 'rt', 'accuracy'])
        self.assertEqual(df.to_string(), df_manual.to_string())


if __name__ == '__main__':
    unittest.main()