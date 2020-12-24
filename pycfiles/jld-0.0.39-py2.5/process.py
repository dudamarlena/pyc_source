# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\process.py
# Compiled at: 2008-12-04 08:40:48
"""
    Process tools
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: process.py 708 2008-12-04 13:40:35Z JeanLou.Dupont $'
import enumprocess

def findPid(name):
    """ Finds the pid list for process(es) with 'name'.
        Returns the first off the list.
    """
    liste = enumprocess.getPidNames()
    fliste = filter(lambda X: X[1] == name, liste.iteritems())
    first = fliste[0] if len(fliste) else None
    return first