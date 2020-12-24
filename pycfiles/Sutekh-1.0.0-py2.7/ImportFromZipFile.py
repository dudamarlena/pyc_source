# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ImportFromZipFile.py
# Compiled at: 2019-12-11 16:37:54
"""Plugin to import selected card sets from a zip file"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.io.ZipFileWrapper import ZipFileWrapper
from sutekh.base.gui.plugins.BaseZipImport import BaseZipImport

class ImportFromZipFile(SutekhPlugin, BaseZipImport):
    """Extract selected card sets from a zip file."""
    cZipWrapper = ZipFileWrapper


plugin = ImportFromZipFile