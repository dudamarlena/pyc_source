# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/frisi/instances/ritualnetz/src/collective.portlet.localevents/src/collective/portlet/localevents/setuphandlers.py
# Compiled at: 2015-06-19 09:09:34


def isNotCurrentProfile(context):
    return context.readDataFile('collectiveportletlocalevents_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return