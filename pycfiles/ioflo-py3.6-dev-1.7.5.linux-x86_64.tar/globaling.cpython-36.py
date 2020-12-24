# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/globaling.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 5661 bytes
"""globaling.py module with global constants

"""
import sys, math, re
from collections import namedtuple
from ..aid.sixing import *
INDENT_ADD = '      '
INDENT_CREATE = '     '
STOP = 0
START = 1
RUN = 2
ABORT = 3
READY = 4
ControlNames = {STOP: 'Stop', START: 'Start', RUN: 'Run', ABORT: 'Abort', READY: 'Ready'}
STOPPED = STOP
STARTED = START
RUNNING = RUN
ABORTED = ABORT
READIED = READY
StatusNames = {STOPPED: 'Stopped', STARTED: 'Started', RUNNING: 'Running', ABORTED: 'Aborted', READIED: 'Readied'}
StatusValues = {'Stopped':STOPPED,  'Started':STARTED,  'Running':RUNNING,  'Aborted':ABORTED,  'Readied':READIED}
NEVER = 0
ONCE = 1
ALWAYS = 2
UPDATE = 3
CHANGE = 4
STREAK = 5
DECK = 6
LogRuleNames = {NEVER: 'Never', ONCE: 'Once', ALWAYS: 'Always', 
 UPDATE: 'Update', CHANGE: 'Change', STREAK: 'Streak', DECK: 'Deck'}
LogRuleValues = {'Never':NEVER,  'Once':ONCE,  'Always':ALWAYS,  'Update':UPDATE, 
 'Change':CHANGE,  'Streak':STREAK,  'Deck':DECK}
INACTIVE = 0
ACTIVE = 1
AUX = 2
SLAVE = 3
MOOT = 4
ScheduleNames = {INACTIVE: 'inactive', 
 ACTIVE: 'active', 
 AUX: 'aux', 
 SLAVE: 'slave', 
 MOOT: 'moot'}
ScheduleValues = {'inactive':INACTIVE,  'active':ACTIVE, 
 'aux':AUX, 
 'slave':SLAVE, 
 'moot':MOOT}
MID = 0
FRONT = 1
BACK = 2
OrderNames = {MID: 'mid', FRONT: 'front', BACK: 'back'}
OrderValues = {'mid':MID,  'front':FRONT,  'back':BACK}
NATIVE = 0
ENTER = 1
RECUR = 2
PRECUR = 3
EXIT = 4
RENTER = 5
REXIT = 6
BENTER = 7
TRANSIT = 8
ActionContextValues = {'native':NATIVE, 
 'enter':ENTER,  'recur':RECUR,  'precur':PRECUR, 
 'exit':EXIT,  'renter':RENTER,  'rexit':REXIT, 
 'benter':BENTER}
ActionContextNames = {NATIVE: 'native', ENTER: 'enter', RECUR: 'recur', 
 PRECUR: 'precur', EXIT: 'exit', RENTER: 'renter', 
 REXIT: 'rexit', BENTER: 'benter'}
ActionSubContextValues = {'transit': TRANSIT}
ActionSubContextNames = {TRANSIT: 'transit'}
REO_Identifier = re.compile('^[a-zA-Z_]\\w*$')
REO_IdentPub = re.compile('^[a-zA-Z]\\w*$')
REO_RelPath = re.compile('^([a-zA-Z_]\\w*)+([.][a-zA-Z_]\\w*)*$')
REO_DotPath = re.compile('^([.][a-zA-Z_]\\w*)+$')
REO_Path = re.compile('^([a-zA-Z_]\\w*)+([.][a-zA-Z_]\\w*)*$|^([.][a-zA-Z_]\\w*)+$')
REO_PathDotPath = re.compile('^([a-zA-Z_]\\w*)+([.][a-zA-Z_]\\w*)+$|^([.][a-zA-Z_]\\w*)+$')
REO_RelPathNode = re.compile('^([a-zA-Z_]\\w*)+(([.][a-zA-Z_]\\w*)*$|([.][a-zA-Z_]\\w*)*[.]$)')
REO_DotPathNode = re.compile('^([.][a-zA-Z_]\\w*)+$|^([.][a-zA-Z_]\\w*)+[.]$')
REO_PathNode = re.compile('^([a-zA-Z_]\\w*)+(([.][a-zA-Z_]\\w*)*$|([.][a-zA-Z_]\\w*)*[.]$)|^([.][a-zA-Z_]\\w*)+$|^([.][a-zA-Z_]\\w*)+[.]$')
REO_Chunks = re.compile('#.*|[^ "\']+|"[^"]*"|\'[^\']*\'')
REO_Quoted = re.compile('^"[^"]*"$')
REO_QuotedSingle = re.compile("^'[^']*'$")
REO_Comment = re.compile('^#.*$')
REO_Plain = re.compile('^[^ "]+$')
REO_LatLonNE = re.compile('^(\\d+)[N,E,n,e](\\d+\\.\\d+)$')
REO_LatLonSW = re.compile('^(\\d+)[S,W,s,w](\\d+\\.\\d+)$')
Pxy = namedtuple('Pxy', 'x y')
Pxyz = namedtuple('Pxyz', 'x y z')
Pne = namedtuple('Pne', 'n e')
Pned = namedtuple('Pned', 'n e d')
Pfs = namedtuple('Pfs', 'f s')
Pfsb = namedtuple('Pfsb', 'f s b')
REO_PointXY = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)?[X,x]([-+]?\\d+\\.\\d*|[-+]?\\d+)[Y,y]$')
REO_PointXYZ = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)[X,x]([-+]?\\d+\\.\\d*|[-+]?\\d+)[Y,y]([-+]?\\d+\\.\\d*|[-+]?\\d+)[Z,z]$')
REO_PointNE = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)[N,n]([-+]?\\d+\\.\\d*|[-+]?\\d+)[E,e]$')
REO_PointNED = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)[N,n]([-+]?\\d+\\.\\d*|[-+]?\\d+)[E,e]([-+]?\\d+\\.\\d*|[-+]?\\d+)[D,d]$')
REO_PointFS = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)[F,f]([-+]?\\d+\\.\\d*|[-+]?\\d+)[S,s]$')
REO_PointFSB = re.compile('^([-+]?\\d+\\.\\d*|[-+]?\\d+)[F,f]([-+]?\\d+\\.\\d*|[-+]?\\d+)[S,s]([-+]?\\d+\\.\\d*|[-+]?\\d+)[B,b]$')