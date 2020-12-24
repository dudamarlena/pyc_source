# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/Debug.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 247 bytes


def log(message):
    """
    Writes a message out in a log file.
    Use this to do printing while debugging, as you can't print while ncurses takes over the screen.
    """
    with open('vai.log', 'a') as (f):
        f.write(str(message) + '\n')