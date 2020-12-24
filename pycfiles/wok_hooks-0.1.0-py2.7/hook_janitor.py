# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wok_hooks/hook_janitor.py
# Compiled at: 2014-10-05 10:58:25
import os, logging

def clean_temp_files(options):
    for root, dirnames, filenames in os.walk('./', topdown=True):
        for filename in filenames:
            if filename[(-1)] == '~':
                logging.info('remove %s/%s', root, filename)
                os.remove(root + '/' + filename)