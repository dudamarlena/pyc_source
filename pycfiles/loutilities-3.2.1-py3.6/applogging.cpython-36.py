# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\applogging.py
# Compiled at: 2020-03-06 11:27:35
# Size of source mod 2**32: 3297 bytes
"""
applogging - define logging for the application
================================================
"""
import logging
from logging.handlers import SMTPHandler
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from flask import current_app

def setlogging():
    current_app.logger.setLevel(logging.DEBUG)
    ADMINS = [
     'lou.king@steeplechasers.org']
    if not current_app.debug:
        mail_handler = SMTPHandler('localhost', 'noreply@steeplechasers.org', ADMINS, 'members exception encountered')
        if 'LOGGING_LEVEL_MAIL' in current_app.config:
            mailloglevel = current_app.config['LOGGING_LEVEL_MAIL']
        else:
            mailloglevel = logging.ERROR
        mail_handler.setLevel(mailloglevel)
        mail_handler.setFormatter(Formatter('\n        Message type:       %(levelname)s\n        Location:           %(pathname)s:%(lineno)d\n        Module:             %(module)s\n        Function:           %(funcName)s\n        Time:               %(asctime)s\n\n        Message:\n\n        %(message)s\n        '))
        current_app.logger.addHandler(mail_handler)
        current_app.config['LOGGING_MAIL_HANDLER'] = mail_handler
        logpath = None
        if 'LOGGING_PATH' in current_app.config:
            logpath = current_app.config['LOGGING_PATH']
        if logpath:
            file_handler = TimedRotatingFileHandler(logpath, when='W0', delay=True)
            if 'LOGGING_LEVEL_FILE' in current_app.config:
                fileloglevel = current_app.config['LOGGING_LEVEL_FILE']
            else:
                fileloglevel = logging.WARNING
            file_handler.setLevel(fileloglevel)
            current_app.logger.addHandler(file_handler)
            current_app.config['LOGGING_FILE_HANDLER'] = file_handler
            file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))