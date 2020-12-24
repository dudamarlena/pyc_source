# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtcore/util/tauruslog.py
# Compiled at: 2019-08-19 15:09:29
"""This module sets the taurus.core.util.log.Logger to be the Qt message handler"""
__all__ = [
 'getQtLogger', 'initTaurusQtLogger']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus import Logger
qtLogger = None
QT_LEVEL_MATCHER = {Qt.QtDebugMsg: Logger.debug, 
   Qt.QtWarningMsg: Logger.warning, 
   Qt.QtCriticalMsg: Logger.error, 
   Qt.QtFatalMsg: Logger.error, 
   Qt.QtSystemMsg: Logger.info}

def getQtLogger():
    global qtLogger
    if qtLogger is None:
        qtLogger = Logger('QtLogger')
    return qtLogger


def qtTaurusMessageHandler(msg_type, log_ctx, msg):
    if qtLogger is not None:
        caller = QT_LEVEL_MATCHER.get(msg_type)
        return caller('Qt%s %s.%s[%s]: %a', log_ctx.category, log_ctx.file, log_ctx.function, log_ctx.line, msg)
    else:
        return


def qtTaurusMsgHandler(msg_type, msg):
    if qtLogger is not None:
        caller = QT_LEVEL_MATCHER.get(msg_type)
        caller(qtLogger, msg)
    return


def initTaurusQtLogger():
    if not qtLogger:
        if hasattr(Qt, 'qInstallMessageHandler'):
            Qt.qInstallMessageHandler(qtTaurusMessageHandler)
        elif hasattr(Qt, 'qInstallMsgHandler'):
            Qt.qInstallMsgHandler(qtTaurusMsgHandler)