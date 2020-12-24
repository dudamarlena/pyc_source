# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notify/consts.py
# Compiled at: 2018-03-14 02:02:46
SERVICE_URL = 'https://notify.soft=way.biz'
NOTIFY_STATUS_HOLD = 'hold'
NOTIFY_STATUS_PROCESSING = 'send'
NOTIFY_STATUS_SUCCESS = 'delivered'
NOTIFY_STATUS_FAILURE = 'failure'
NOTIFY_STATUS_NO_ANSWER = 'no-answer'
NOTIFY_STATUS_BUSY = 'busy'
NOTIFY_STATUS_IN_PROGRESS = 'in-progress'
NOTIFY_STATUS_CANCELED = 'canceled'
NOTIFY_STATUSES = [
 NOTIFY_STATUS_HOLD, NOTIFY_STATUS_PROCESSING, NOTIFY_STATUS_SUCCESS, NOTIFY_STATUS_FAILURE, NOTIFY_STATUS_NO_ANSWER,
 NOTIFY_STATUS_BUSY, NOTIFY_STATUS_IN_PROGRESS, NOTIFY_STATUS_CANCELED]
CALL_TYPE = 'call'
MESSAGE_TYPE = 'message'
NOTIFY_TYPES = [
 CALL_TYPE, MESSAGE_TYPE]
CONNECTION_ERROR_MESSAGE = 'The notification service does not respond'
JSON_ERROR_MESSAGE = 'Unable to recognize the response from the notifications service'
ERRORS = [
 CONNECTION_ERROR_MESSAGE, JSON_ERROR_MESSAGE]