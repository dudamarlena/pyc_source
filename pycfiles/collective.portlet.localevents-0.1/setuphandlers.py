# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/frisi/instances/ritualnetz/src/collective.portlet.localevents/src/collective/portlet/localevents/setuphandlers.py
# Compiled at: 2015-06-19 09:09:34


def isNotCurrentProfile(context):
    return context.readDataFile('collectiveportletlocalevents_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return