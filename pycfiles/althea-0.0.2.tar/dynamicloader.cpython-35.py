# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nn31/Dropbox/40-githubRrepos/althea/althea/dynamicloader/dynamicloader.py
# Compiled at: 2017-01-18 12:10:45
# Size of source mod 2**32: 188 bytes
"""
Created on Fri Sep 23 10:08:30 2016

@author: nn31
"""
import imp

def dynamic_score(path):
    utils = imp.load_source('scores', path)
    return utils.score