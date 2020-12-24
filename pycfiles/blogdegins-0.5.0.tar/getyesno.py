# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins/blogdegins/getyesno.py
# Compiled at: 2012-07-23 04:07:09


def getyesno(message, default='y'):
    """ Utility for ask yes or no
    """
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input('%s (%s) ' % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    if choice.strip().lower() in values:
        return True
    return False