# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/conf/pyage_conf.py
# Compiled at: 2015-12-21 16:57:03
import os, socket
from pyage.core.agent import Agent
workspace_name = 'workspace.' + socket.gethostname() + '.' + str(os.getpid())
agents = [
 Agent('makz')]