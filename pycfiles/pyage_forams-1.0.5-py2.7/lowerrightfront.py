# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/conf/distributed3d/lowerrightfront.py
# Compiled at: 2014-11-03 18:14:25
from functools import partial
from pyage_forams.solutions.agent.remote_aggegate import create_remote_agent
from pyage_forams.conf.distributed3d.common import *
agents = partial(create_remote_agent, 'lowerrightfront')
neighbours = lambda : {'left': 'lowerleftfront', 'upper': 'upperrightfront', 'back': 'lowerrightback'}