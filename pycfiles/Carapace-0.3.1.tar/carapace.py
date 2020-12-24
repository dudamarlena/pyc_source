# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oubiwann/lab/tx/carapace/twisted/plugins/carapace.py
# Compiled at: 2013-04-13 03:39:25
from twisted.application.service import ServiceMaker
CarapaceSSHService = ServiceMaker('Carapace SSH Server', 'carapace.app.service', 'A highly flexible pure-Python, Twisted-based SSH Server with custom account shells', 'carapace')