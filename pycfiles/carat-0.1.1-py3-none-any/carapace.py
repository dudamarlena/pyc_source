# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/oubiwann/lab/tx/carapace/twisted/plugins/carapace.py
# Compiled at: 2013-04-13 03:39:25
from twisted.application.service import ServiceMaker
CarapaceSSHService = ServiceMaker('Carapace SSH Server', 'carapace.app.service', 'A highly flexible pure-Python, Twisted-based SSH Server with custom account shells', 'carapace')