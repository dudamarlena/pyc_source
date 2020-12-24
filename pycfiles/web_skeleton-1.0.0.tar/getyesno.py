# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yuneta-dev/yuneta/^yuneta-v2/webyunotemplate/webyunotemplate/getyesno.py
# Compiled at: 2015-12-25 13:24:48


def getyesno(message, default='y'):
    """ Utility for ask yes or no
    """
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input('%s (%s) ' % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    if choice.strip().lower() in values:
        return True
    return False


def getstring(message, default=''):
    """ Utility for ask a string
    """
    value = raw_input('%s ' % (message,))
    if not value:
        value = default
    return value