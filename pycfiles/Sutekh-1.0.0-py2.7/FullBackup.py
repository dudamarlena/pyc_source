# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/FullBackup.py
# Compiled at: 2019-12-11 16:37:54
"""Plugin to wrap zipfile backup and restore methods"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.plugins.BaseBackup import BaseBackup
from sutekh.io.ZipFileWrapper import ZipFileWrapper

class FullBackup(SutekhPlugin, BaseBackup):
    """Provide access to ZipFileWrapper's backup and restore methods."""
    cZipWrapper = ZipFileWrapper


plugin = FullBackup