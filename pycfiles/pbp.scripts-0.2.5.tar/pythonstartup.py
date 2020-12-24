# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacDev/perso/atomisator.ziade.org/packages/pbp.scripts/pbp/scripts/pythonstartup.py
# Compiled at: 2008-08-29 18:35:54
import readline, rlcompleter, atexit, os
readline.parse_and_bind('tab: complete')
histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
try:
    readline.read_history_file(histfile)
except IOError:
    pass

atexit.register(readline.write_history_file, histfile)
del os
del histfile
del readline
del rlcompleter