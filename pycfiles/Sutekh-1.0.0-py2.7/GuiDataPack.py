# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/GuiDataPack.py
# Compiled at: 2019-12-11 16:37:48
"""Wrap various functions from base.io.UrlOps with timeout handling"""
import urllib2, socket
from ..io.UrlOps import fetch_data
from .SutekhDialog import do_exception_complaint
from .ProgressDialog import ProgressDialog, SutekhCountLogHandler

def gui_error_handler(oExp):
    """Default error handler for url fetching operations."""
    if isinstance(oExp, socket.timeout):
        do_exception_complaint('Connection Timeout')
    elif isinstance(oExp, urllib2.URLError) and isinstance(oExp.reason, socket.timeout):
        do_exception_complaint('Connection Timeout')
    else:
        do_exception_complaint('Connection Error')


def progress_fetch_data(oFile, oOutFile=None, sHash=None, sDesc=None):
    """Wrap a Progress Dialog around fetch_data"""
    oProgress = ProgressDialog()
    if sDesc:
        oProgress.set_description(sDesc)
    else:
        oProgress.set_description('Download progress')
    oLogHandler = SutekhCountLogHandler()
    oLogHandler.set_dialog(oProgress)
    try:
        return fetch_data(oFile, oOutFile, sHash, oLogHandler, gui_error_handler)
    finally:
        oProgress.destroy()

    return