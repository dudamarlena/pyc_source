# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/Dropbox/studies/newpainmachine/software/FAB/fab_controller/settings.py
# Compiled at: 2015-01-06 09:36:37
import os
from collections import namedtuple
import random, pkg_resources
FAB_VERSION = pkg_resources.require('fab_controller')[0].version
HANDS = [
 'left', 'right']
Pair = namedtuple('Pair', HANDS)
Block = namedtuple('Block', ['duration', 'grams'])
LOG_INTERVAL = 0.5
LOGFILE_DIR = os.path.expanduser('~/Documents/fab/logs/')
REST_N_FROM_TOP = 500
STEP_DELAY = 0.0003
TIGHT_LOOP_INTERVAL = 0.001
ALLOWABLE_DISCREPANCY = 20
TWO_KG = Pair(0.4457, 0.4692)
DASHBOARD_UPDATE_INTERVAL = 0.2
SERVER_PORT = 8000
STEP_PIN = Pair(2, 3)
DIRECTION_PIN = Pair(6, 7)
HIGH_LIMIT_PIN = Pair(17, 18)
LOW_LIMIT_PIN = Pair(15, 16)
SENSOR_PIN = Pair(4, 5)
UP = 0
DOWN = 1
MOVEMENT_LABELS = {UP: 'up', DOWN: 'down'}
MOVEMENT = {v:k for k, v in list(MOVEMENT_LABELS.items())}
STEPS_PER_FULL_STEP = 8
FULL_STEPS_PER_REV = 200
STEPS_PER_REV = FULL_STEPS_PER_REV * STEPS_PER_FULL_STEP
MM_PER_REV = 5
MM_MAX_TRAVEL = 15
MAX_REVS = MM_MAX_TRAVEL / MM_PER_REV
MAX_STEPS = MAX_REVS * STEPS_PER_REV
SWITCH_CHECKING_WINDOW_LENGTH = 5
SENSOR_MEASUREMENTS_WINDOW_LENGTH = 5