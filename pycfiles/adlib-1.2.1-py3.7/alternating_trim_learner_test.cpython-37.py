# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/alternating_trim_learner_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 982 bytes
from adlib.tests.learners.dp_learner_test import TestDataPoisoningLearner
from adlib.utils.common import report
from data_reader.dataset import EmailDataset
import sys

def test_alternating_trim_learner():
    if len(sys.argv) == 2 and sys.argv[1] in ('label-flipping', 'k-insertion', 'data-modification',
                                              'dummy'):
        attacker_name = sys.argv[1]
    else:
        attacker_name = 'dummy'
    dataset = EmailDataset(path='./data_reader/data/raw/trec05p-1/test-400', binary=False,
      raw=True)
    tester = TestDataPoisoningLearner('atrim', attacker_name, dataset)
    result = tester.test()
    report(result)


if __name__ == '__main__':
    test_alternating_trim_learner()