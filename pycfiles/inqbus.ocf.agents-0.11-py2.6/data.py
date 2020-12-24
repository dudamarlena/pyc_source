# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/data.py
# Compiled at: 2011-11-21 17:36:12
from __future__ import print_function
from inqbus.ocf.generic import exits
import sys

def log(output):
    sys.stderr.write('\n' + '!' * len(output))
    sys.stderr.write('\n' + output)
    sys.stderr.write('\n' + '! ' * (len(output) / 2) + '\n')


GOOD_ACTIONS = [
 'start', 'stop', 'monitor', 'meta-data', 'validate-all']
BASE_ACTIONS = ['meta-data', 'validate-all']
BAD_ARGUMENTS = [['XX'], ['a', 2, 3], ['1', '2', '3'], 123]
BAD_ACTIONS = ['XX', 'a', 2, '1']
OCFTESTER_ACTIONS_RETCODES = [('meta-data', None),
 ('validate-all', None),
 (
  'monitor', exits.OCF_NOT_RUNNING),
 ('start', None),
 ('monitor', None),
 ('start', None),
 ('stop', None),
 (
  'monitor', exits.OCF_NOT_RUNNING),
 ('start', None),
 ('monitor', None),
 ('start', None),
 ('monitor', None),
 ('stop', None),
 (
  'monitor', exits.OCF_NOT_RUNNING),
 ('stop', None),
 (
  'monitor', exits.OCF_NOT_RUNNING)]
SCENARIO_OCFTESTER_ACTIONS_RETCODES = [ (action, {'action': action, 'error': error}) for (action, error) in OCFTESTER_ACTIONS_RETCODES ]

def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [ x[0] for x in items ]
        argvalues.append([ x[1] for x in items ])

    metafunc.parametrize(argnames, argvalues, ids=idlist)