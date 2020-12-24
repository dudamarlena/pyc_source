# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/options.py
# Compiled at: 2009-10-07 18:08:46
"""
Options class for reporters

Reporters receive this module instance when created. Contains useful defaults
and any change made here applies to all of them.
"""
descriptions = 1
verbosity = 1
immediate = False
coverage = (None, None)
silent = False
bgcolor = None