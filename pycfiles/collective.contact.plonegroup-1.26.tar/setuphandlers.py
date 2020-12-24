# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/setuphandlers.py
# Compiled at: 2014-02-10 04:38:39


def isNotCurrentProfile(context):
    return context.readDataFile('collectivecontactmembrane_marker.txt') is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return
    portal = context.getSite()