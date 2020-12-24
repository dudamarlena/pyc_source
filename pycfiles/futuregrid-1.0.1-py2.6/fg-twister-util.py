# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/twister/fg-twister-util.py
# Compiled at: 2012-09-06 11:03:15
import os
instance_id = 'emi-F3E41594'

def get_nodes():
    text = os.popen('euca-describe-instances').read()
    lines = text.split('\n')
    remove_lines = []
    for line in lines:
        if line.find(instance_id) == -1:
            remove_lines.append(line)

    for line in remove_lines:
        lines.remove(line)

    return lines