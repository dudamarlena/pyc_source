# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_other_pred_part.py
# Compiled at: 2020-03-20 10:12:11
# Size of source mod 2**32: 1071 bytes


def get_argparser_other_pred_part(parser):
    parser.add_argument('--auc', dest='AUC',
      help='Compute sample assignation using normal dist.',
      action='store_true')
    parser.add_argument('--normal', dest='NORMAL',
      help='Compute sample assignation using normal dist.',
      action='store_true')
    parser.add_argument('--ttest', dest='TTEST',
      help='Compute a p-value using ttest_ind from scipy.stats.',
      action='store_true')
    parser.add_argument('--utest', dest='UTEST',
      help='Compute a p-value using Mann-Whitney from scipy.stats. (NEED --auc)',
      action='store_true')
    parser.set_defaults(AUC=False)
    parser.set_defaults(NORMAL=False)
    parser.set_defaults(UTEST=False)
    parser.set_defaults(TTEST=False)