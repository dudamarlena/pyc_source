# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/confdir.py
# Compiled at: 2018-12-30 10:46:50
import os, sys, tempfile
if sys.platform[:3] == 'win':
    variation = [
     os.path.join(os.environ['HOMEPATH'], 'SNMP Simulator', 'Variation'), os.path.join(os.environ['APPDATA'], 'SNMP Simulator', 'Variation'), os.path.join(os.environ['PROGRAMFILES'], 'SNMP Simulator', 'Variation'), os.path.join(os.path.split(__file__)[0], 'variation')]
    data = [
     os.path.join(os.environ['HOMEPATH'], 'SNMP Simulator', 'Data'), os.path.join(os.environ['APPDATA'], 'SNMP Simulator', 'Data'), os.path.join(os.environ['PROGRAMFILES'], 'SNMP Simulator', 'Data'), os.path.join(os.path.split(__file__)[0], 'data')]
elif sys.platform == 'darwin':
    variation = [
     os.path.join(os.environ['HOME'], '.snmpsim', 'variation'), os.path.join('/', 'usr', 'local', 'share', 'snmpsim', 'variation'), os.path.join(sys.prefix, 'snmpsim', 'variation'), os.path.join(sys.prefix, 'share', 'snmpsim', 'variation'), os.path.join(os.path.split(__file__)[0], 'variation')]
    data = [
     os.path.join(os.environ['HOME'], '.snmpsim', 'data'), os.path.join('/', 'usr', 'local', 'share', 'snmpsim', 'data'), os.path.join(sys.prefix, 'snmpsim', 'data'), os.path.join(sys.prefix, 'share', 'snmpsim', 'data'), os.path.join(os.path.split(__file__)[0], 'data')]
else:
    variation = [
     os.path.join(os.environ['HOME'], '.snmpsim', 'variation'), os.path.join(sys.prefix, 'snmpsim', 'variation'), os.path.join(sys.prefix, 'share', 'snmpsim', 'variation'), os.path.join(os.path.split(__file__)[0], 'variation')]
    data = [
     os.path.join(os.environ['HOME'], '.snmpsim', 'data'), os.path.join(sys.prefix, 'snmpsim', 'data'), os.path.join(sys.prefix, 'share', 'snmpsim', 'data'), os.path.join(os.path.split(__file__)[0], 'data')]
cache = os.path.join(tempfile.gettempdir(), 'snmpsim')