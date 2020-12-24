# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/setuphandlers.py
# Compiled at: 2015-10-13 13:57:55


def isNotCurrentProfile(context):
    return context.readDataFile('collectiveawstatshitcounter_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return