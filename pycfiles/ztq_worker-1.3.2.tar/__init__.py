# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/panjy/git/ztq/ztq_worker/ztq_worker/system_info/__init__.py
# Compiled at: 2014-01-15 20:42:34
import sys
if sys.platform.startswith('win'):
    from win import get_cpu_style, get_cpu_usage, get_mem_usage, get_ip
else:
    from linux import get_cpu_style, get_cpu_usage, get_mem_usage, get_ip