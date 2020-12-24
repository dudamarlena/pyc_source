# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/core/signal.py
# Compiled at: 2018-09-06 06:26:23
from flask import request_started, request_finished, got_request_exception, request
from flask_login import user_logged_in, user_logged_out
from application.model import DBSession

def log_request(sender, **extra):
    sender.logger.info('Request start')


def log_response(sender, response, **extra):
    sender.logger.info(('Response {}').format(response.response))


def log_exception(sender, exception, **extra):
    sender.logger.error(('Exception {}').format(exception))


def signal(app):
    request_started.connect(log_request, app)
    request_finished.connect(log_response, app)
    got_request_exception.connect(log_exception, app)