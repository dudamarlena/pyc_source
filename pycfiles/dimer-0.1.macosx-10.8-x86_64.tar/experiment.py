# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/experiment.py
# Compiled at: 2013-08-06 22:00:04
"""
Created on Jul 11, 2013

@author: odenas
"""
import datetime, os

def this_train_name(cfg_file, seed='noseed'):
    """train subdir inside archive"""
    cfg_name = os.path.splitext(os.path.basename(cfg_file))[0]
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    seed = str(seed)
    return 'tr_%s_%s_%s' % (cfg_name, timestamp, seed)