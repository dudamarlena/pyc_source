# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.jvzoo/src/niteoweb/ipn/jvzoo/upgrades/upgrades.py
# Compiled at: 2013-12-19 07:23:47
"""Upgrade steps for addon niteoweb.ipn.jvzoo."""

def upgrade_1_to_2(context):
    """Upgrade steps for version 1.5"""
    context.runImportStepFromProfile('profile-niteoweb.ipn.jvzoo:default', 'memberdata-properties')