# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\date.py
# Compiled at: 2008-12-12 20:05:33
"""Date related tools
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: date.py 728 2008-12-11 16:47:54Z jeanlou.dupont $'
import datetime

def convertDate(date):
    """ Converts a date in string format
        to a datastore compatible format
        
        Input format:   YYYY-MM-DD HH:MM:SS.ssssss
        Output format:  datetime
        
        throws: Exception
    """
    sdate = date.split('.')
    return datetime.datetime.strptime(sdate[0], '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print 'test!'