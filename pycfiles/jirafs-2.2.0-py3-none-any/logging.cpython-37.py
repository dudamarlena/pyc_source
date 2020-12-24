# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/logging.py
# Compiled at: 2019-10-22 21:37:07
# Size of source mod 2**32: 424 bytes
import logging

class JirafsTicketFolderLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        return (
         '{{{issue_id}}} {msg}'.format(issue_id=(self.extra['issue_id']),
           msg=msg),
         kwargs)


def get_logger(name, ticket_number):
    logger = logging.getLogger(name)
    return JirafsTicketFolderLoggerAdapter(logger, {'issue_id': ticket_number})