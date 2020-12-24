# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tools/console_tools.py
# Compiled at: 2016-02-25 04:17:16
try:
    import readline, rlcompleter
except ImportError:
    print 'auto complete failed to install'
else:
    readline.parse_and_bind('tab: complete')
    print 'auto complete installed'