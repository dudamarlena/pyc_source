# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/note/util.py
# Compiled at: 2015-01-22 23:06:08
import subprocess as SP, os
itemTypes = [
 'note', 'todo', 'contact', 'place']
colors = dict()
colors['reset'] = '\x1b[0m'
colors['hicolor'] = '\x1b[1m'
colors['underline'] = '\x1b[4m'
colors['invert'] = '\x1b[7m'
colors['foreground black'] = '\x1b[30m'
colors['foreground red'] = '\x1b[31m'
colors['foreground green'] = '\x1b[32m'
colors['foreground yellow'] = '\x1b[33m'
colors['foreground blue'] = '\x1b[34m'
colors['foreground magenta'] = '\x1b[35m'
colors['foreground cyan'] = '\x1b[36m'
colors['foreground white'] = '\x1b[37m'
colors['background black'] = '\x1b[40m'
colors['background red'] = '\x1b[41m'
colors['background green'] = '\x1b[42m'
colors['background yellow'] = '\x1b[43m'
colors['background blue'] = '\x1b[44m'
colors['background magenta'] = '\x1b[45m'
colors['background cyan'] = '\x1b[46m'
colors['background white'] = '\x1b[47m'

def scrubID(ID):
    """
        :param ID: An ID that can be of various types, this is very kludgy
        :returns: An integer ID
    """
    try:
        if type(ID) == list:
            return int(ID[0])
        if type(ID) == str:
            return int(ID)
        if type(ID) == int:
            return ID
        if type(ID) == unicode:
            return int(ID)
    except ValueError:
        return

    return


def which(bin_name):
    """
        :param bin_name: the name of the binary to test for (e.g. vim)
        :returns: True or False depending on wether the binary exists
    """
    with open(os.devnull) as (devnull):
        rc = SP.call(['which', bin_name])
    return rc