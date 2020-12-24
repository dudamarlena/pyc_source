# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sshm/__init__.py
# Compiled at: 2015-03-11 16:45:03
"""
This module can be used to ssh into multiple servers at once.

Example:
    from sshm.lib import sshm

    for result in sshm('example[5,8].com', 'ps aux | wc -l'):
            print(result)

    {
        'traceback': '',
        'stdout': u'195
',
        'uri': 'example5.com',
        'cmd': ['ssh', 'example5.com','ps aux | wc -l'],
        'return_code': 0,
        'stderr': u'',
        }
    {
        'traceback': '',
        'stdout': u'120
',
        'uri': 'example8.com',
        'cmd': ['ssh', 'example8.com', 'ps aux | wc -l'],
        'return_code': 0,
        'stderr': u'',
        }
"""