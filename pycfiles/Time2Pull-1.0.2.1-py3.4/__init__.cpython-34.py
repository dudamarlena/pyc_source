# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/time2pull/__init__.py
# Compiled at: 2014-06-16 16:07:16
# Size of source mod 2**32: 680 bytes
"""
Time2Pull is a small application that monitor git repositories and notify you
when the remote has changed and its time to pull.

How do we check repo status? We simply run the two following commands on each
repository and parse their output to detect the remote status::

    git remote update
    git status -uno

Icons source:
    - app icon : https://www.iconfinder.com/icons/126865/clock_loading_refresh_reload_slow_throbber_time_update_wait_waiting_icon#size=96
    - arrows: http://kyo-tux.deviantart.com/
    - database: http://www.icojoy.com
    - git: https://www.iconfinder.com/icons/83306/git_icon#size=32

"""
__version__ = '1.0.2.1'