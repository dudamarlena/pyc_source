# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/plone/learning.playgroup.com.tw/zeocluster/src/collective.api4tal/src/collective/api4tal/setuphandlers.py
# Compiled at: 2015-08-18 22:06:56


def post_install(context):
    """Post install script"""
    if context.readDataFile('collectiveapi4tal_default.txt') is None:
        return
    else:
        return


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('collectiveapi4tal_uninstall.txt') is None:
        return
    else:
        return