# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pwserver/config.py
# Compiled at: 2010-06-18 06:48:40
import ConfigParser, StringIO
default_cfg = StringIO.StringIO('\n[main]\nlisteners = tcp\ndebug = false\n\n[tcp]\ntype = tcp\nport = 8099\ninterface = localhost\n')
config = ConfigParser.SafeConfigParser()
config.readfp(default_cfg)