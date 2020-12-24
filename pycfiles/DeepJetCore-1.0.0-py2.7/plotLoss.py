# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/bin/plotLoss.py
# Compiled at: 2018-07-12 08:05:01
from DeepJetCore.evaluation import plotLoss
from argparse import ArgumentParser
parser = ArgumentParser('')
parser.add_argument('inputDir')
parser.add_argument('--file', help='specify loss file', metavar='FILE', default='losses.log')
parser.add_argument('--range', help='specify y axis range', nargs='+', type=float, metavar='OPT', default=[])
args = parser.parse_args()
infilename = args.inputDir + '/' + args.file
plotLoss(infilename, args.inputDir + '/losses.pdf', args.range)