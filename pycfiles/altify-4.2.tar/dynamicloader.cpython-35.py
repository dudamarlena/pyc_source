# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/nn31/Dropbox/40-githubRrepos/althea/althea/dynamicloader/dynamicloader.py
# Compiled at: 2017-01-18 12:10:45
# Size of source mod 2**32: 188 bytes
__doc__ = '\nCreated on Fri Sep 23 10:08:30 2016\n\n@author: nn31\n'
import imp

def dynamic_score(path):
    utils = imp.load_source('scores', path)
    return utils.score