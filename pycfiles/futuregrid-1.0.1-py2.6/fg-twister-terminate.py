# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/twister/fg-twister-terminate.py
# Compiled at: 2012-09-06 11:03:15
"""
This program is to terminate Twister on FutureGrid automatically
"""
import os
from fg_euca_twister_util import get_nodes
lines = get_nodes()
num_nodes = len(lines)
print 'Get', num_nodes, 'instances,', 'try to terminate them...'
for i in range(num_nodes):
    items = lines[i].split('\t')
    cmd = 'euca-terminate-instances ' + items[1].strip()
    print cmd
    os.system(cmd)